#!/usr/bin/env python3
"""AuraGraph v0.2 prototype (Kehai Interim, 2026-10-17; v0.2 2026-10-20).

v0.2: high-band transient lane (hi-hats / count-ins), tempo with an octave check and
beat grid lines, colour bars with units on the spectrogram and stereo-width panels,
units on every panel label.
v0.2.1: mid-zoom panel (~200 Hz-5 kHz, 4x finer frequency resolution) for lead lines.

Turn an audio file into numbered, timestamped tiles an LLM can read:
one PNG per time window + a markdown sidecar of numbers.
numpy/scipy/matplotlib only, so every step ports to the browser Web Audio API later.

usage: proto.py AUDIO OUTDIR [--tile SECONDS]
"""
import argparse, json, os, subprocess, sys
import numpy as np
from scipy.signal import stft, find_peaks
from scipy.ndimage import median_filter, uniform_filter1d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 22050
NFFT = 2048
HOP = 512
FMIN, FMAX, NBANDS = 30.0, 11000.0, 160
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
    return x[:, 0].astype(np.float64), x[:, 1].astype(np.float64)


def spec(sig):
    f, t, Z = stft(sig, fs=SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
    return f, t, np.abs(Z)


def logbands(f):
    edges = np.geomspace(FMIN, FMAX, NBANDS + 1)
    centers = np.sqrt(edges[:-1] * edges[1:])
    idx = [np.where((f >= lo) & (f < hi))[0] for lo, hi in zip(edges[:-1], edges[1:])]
    # bands narrower than one FFT bin borrow the nearest bin
    idx = [i if len(i) else np.array([np.argmin(np.abs(f - c))]) for i, c in zip(idx, centers)]
    return centers, idx


def tobands(M, idx):
    return np.stack([M[i].mean(axis=0) for i in idx])


def db(x, ref):
    return 20 * np.log10(np.maximum(x, 1e-10) / ref)


def chroma(M, f):
    C = np.zeros((12, M.shape[1]))
    ok = (f > 55) & (f < 4200)
    midi = 69 + 12 * np.log2(f[ok] / 440.0)
    pcs = np.round(midi).astype(int) % 12
    P = M[ok] ** 2
    for pc in range(12):
        C[pc] = P[pcs == pc].sum(axis=0)
    return C / np.maximum(C.max(axis=0, keepdims=True), 1e-12)


def chord_templates():
    T, names = [], []
    for root in range(12):
        for q, ivs in (("", (0, 4, 7)), ("m", (0, 3, 7))):
            v = np.zeros(12); v[[(root + i) % 12 for i in ivs]] = 1
            T.append(v / np.linalg.norm(v)); names.append(NOTE_NAMES[root] + q)
    return np.array(T), names


def note_label(freq):
    m = int(round(69 + 12 * np.log2(freq / 440.0)))
    return f"{NOTE_NAMES[m % 12]}{m // 12 - 1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("out")
    ap.add_argument("--tile", type=float, default=15.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    L, R = decode(a.audio)
    mid, side = (L + R) / 2, (L - R) / 2
    f, t, Mm = spec(mid)
    _, _, Ms = spec(side)
    centers, idx = logbands(f)
    Bm, Bs = tobands(Mm, idx), tobands(Ms, idx)
    ref = np.percentile(Bm, 99.5)
    Dm = np.clip(db(Bm, ref), -80, 0)
    # stereo width per band: side energy relative to mid (0 = mono, ~1 = very wide)
    width = np.clip(Bs / np.maximum(Bm, 1e-10), 0, 1.5)
    # readable width: 24 coarse bands, ~0.5 s smoothing
    coarse = np.array_split(np.arange(NBANDS), 24)
    Wc = np.stack([width[c].mean(0) for c in coarse])
    Wc = uniform_filter1d(Wc, size=int(0.5 * SR / HOP), axis=1)
    # harmonic/percussive split (median filtering, Fitzgerald 2010): sustained vs transient
    H = median_filter(Bm, size=(1, 17)); Pp = median_filter(Bm, size=(17, 1))
    mask_h = H ** 2 / (H ** 2 + Pp ** 2 + 1e-20)
    Dh = np.clip(db(Bm * mask_h, ref), -80, 0); Dp = np.clip(db(Bm * (1 - mask_h), ref), -80, 0)

    # loudness (RMS dB) and onset strength (positive spectral flux on log bands)
    rms = np.sqrt((Mm ** 2).mean(axis=0))
    rms_db = db(rms, rms.max())
    flux = np.maximum(np.diff(Dm, axis=1), 0).sum(axis=0)
    flux = np.concatenate([[0], flux])
    flux = flux / max(flux.max(), 1e-9)
    # high-band transient lane (v0.2): percussive layer above ~6 kHz only, where hi-hats,
    # shakers and count-in clicks live. The crowd/vocal wash can't hide them here.
    hf = centers >= 6000
    Dhf = Dp[hf]
    hflux = np.maximum(np.diff(Dhf, axis=1), 0).sum(0)
    hflux = np.concatenate([[0], hflux])
    # gate: only where there is real energy up there (else quiet pieces show noise as clicks)
    hflux[Dhf.max(0) < -55] = 0
    hflux = hflux / max(np.percentile(hflux, 99.5), 1e-9)

    # band energy split, brightness, noisiness
    P = Mm ** 2
    low = P[f < 250].sum(0); midb = P[(f >= 250) & (f < 2000)].sum(0); high = P[f >= 2000].sum(0)
    tot = low + midb + high + 1e-12
    centroid = (f[:, None] * P).sum(0) / (P.sum(0) + 1e-12)
    flat = np.exp(np.log(Mm[1:] + 1e-10).mean(0)) / (Mm[1:].mean(0) + 1e-10)

    # mid-zoom (v0.2.1): longer FFT window -> ~5.4 Hz bins, so close pitches, bends and
    # vibrato in the lead range separate instead of smearing. Same hop, so time lines up.
    fz, tz, Mz = stft(mid, fs=SR, nperseg=4096, noverlap=4096 - HOP, boundary=None, padded=False)
    Mz = np.abs(Mz)
    ze = np.geomspace(200, 5000, 241)
    zc = np.sqrt(ze[:-1] * ze[1:])
    zidx = [np.where((fz >= lo) & (fz < hi))[0] for lo, hi in zip(ze[:-1], ze[1:])]
    zidx = [i if len(i) else np.array([np.argmin(np.abs(fz - c))]) for i, c in zip(zidx, zc)]
    Bz = np.stack([Mz[i].mean(0) for i in zidx])
    Dz = db(Bz, 1.0)
    zyt = [i for i, c in enumerate(zc) if any(abs(np.log2(c / n)) < 0.01 for n in (220, 440, 880, 1760, 3520))]

    C = chroma(Mm, f)
    T, cnames = chord_templates()
    fps = SR / HOP

    def tempo(seg, tt):
        """Tempo with an octave check. Autocorrelation of the onset curve, weighted by a
        broad log-normal prior around 110 bpm (so a beat multiple doesn't win by default),
        then the beat phase that lands the most onset energy on the grid.
        Returns (bpm, {half, double strengths}, beat_times) or (None, {}, [])."""
        s = seg - seg.mean()
        if len(s) < fps * 3 or not np.any(s): return None, {}, []
        ac = np.correlate(s, s, "full")[len(s) - 1:]
        ac = ac / (ac[0] + 1e-12)
        lo, hi = int(fps * 60 / 220), int(fps * 60 / 45)
        if hi >= len(ac): return None, {}, []
        lags = np.arange(lo, hi)
        bpms = 60 * fps / lags
        prior = np.exp(-0.5 * (np.log2(bpms / 110.0) / 0.9) ** 2)
        lag = int(lags[np.argmax(ac[lo:hi] * prior)])
        # parabolic interpolation between lag bins (one bin is ~5 bpm at 120 bpm otherwise)
        y0, y1, y2 = ac[lag - 1], ac[lag], ac[lag + 1]
        den = y0 - 2 * y1 + y2
        flag = lag + (0.5 * (y0 - y2) / den if den < 0 else 0.0)
        bpm = 60 * fps / flag
        def strength(l):
            l = int(round(l)); return round(float(ac[l]), 2) if 0 < l < len(ac) else None
        alts = {"this": strength(lag), "half_tempo": strength(2 * lag), "double_tempo": strength(lag / 2)}
        if alts["this"] is not None and alts["this"] < 0.15:
            alts["note"] = "weak pulse: no steady beat, treat bpm as a guess"
        # beat phase on the fractional period, so the grid doesn't drift across the tile
        def grid(o): return np.round(o + np.arange(0, len(seg) - o, flag)).astype(int)
        def score(o):
            g = grid(o); g = g[g < len(seg)]
            return seg[g].sum()
        phase = int(np.argmax([score(o) for o in range(lag)]))
        g = grid(phase); beats = tt[g[g < len(tt)]]
        return bpm, alts, beats

    ntiles = int(np.ceil(t[-1] / a.tile))
    yt = [i for i, c in enumerate(centers) if any(abs(np.log2(c / n)) < 0.02 for n in (55, 110, 220, 440, 880, 1760, 3520, 7040))]
    summary = []
    for k in range(ntiles):
        t0, t1 = k * a.tile, min((k + 1) * a.tile, t[-1])
        sel = (t >= t0) & (t < t1)
        tt = t[sel]
        fig = plt.figure(figsize=(12, 9), dpi=100)
        gs = fig.add_gridspec(8, 1, height_ratios=[4, 3.0, 2.4, 2.4, 0.9, 1.0, 1.4, 1.1], hspace=0.14)
        fig.set_size_inches(12, 16.5)
        bpm, alts, beats = tempo(flux[sel], tt)
        ext = [t0, t1, 0, NBANDS]

        ax = fig.add_subplot(gs[0])
        im0 = ax.imshow(Dm[:, sel], origin="lower", aspect="auto", extent=ext, cmap="magma", vmin=-80, vmax=0)
        cb = fig.colorbar(im0, cax=ax.inset_axes([1.005, 0, 0.012, 1])); cb.ax.tick_params(labelsize=6)
        cb.set_label("dB below loudest", fontsize=6)
        for b in beats: ax.axvline(b, color="w", lw=0.4, alpha=0.25)
        ax.set_yticks([i + 0.5 for i in yt]); ax.set_yticklabels([f"{note_label(centers[i])} {centers[i]:.0f}Hz" for i in yt], fontsize=7)
        ax.set_title(f"AuraGraph v0.2.1 | tile {k + 1:02d}/{ntiles} | {int(t0//60)}:{int(t0%60):02d}-{int(t1//60)}:{int(t1%60):02d} | mid (L+R) log-frequency, brightness = loudness", fontsize=9)
        ax.set_xticks([])

        selz = (tz >= t0) & (tz < t1)
        axz = fig.add_subplot(gs[1])
        # whitened per tile: each row minus its own median, so a lead line that stands above
        # the bed shows bright even in a dense mix. Scale: 0..+24 dB above that row's median.
        Zt = Dz[:, selz]; Zt = np.clip(Zt - np.median(Zt, axis=1, keepdims=True), 0, 24)
        imz = axz.imshow(Zt, origin="lower", aspect="auto", extent=[t0, t1, 0, len(zc)], cmap="inferno", vmin=0, vmax=24)
        cbz = fig.colorbar(imz, cax=axz.inset_axes([1.005, 0, 0.012, 1]), ticks=[0, 12, 24]); cbz.ax.tick_params(labelsize=5)
        cbz.set_label("dB above row median", fontsize=5)
        axz.set_yticks([i + 0.5 for i in zyt]); axz.set_yticklabels([f"{note_label(zc[i])} {zc[i]:.0f}Hz" for i in zyt], fontsize=6)
        axz.set_xticks([]); axz.set_ylabel("mid-zoom 200 Hz-5 kHz\n(lead lines, whitened)", fontsize=6)

        for gi, (D_, lab) in ((2, (Dh, "sustained / tonal\n(harmonic layer, dB)")), (3, (Dp, "transient / percussive\n(layer, dB)"))):
            axh = fig.add_subplot(gs[gi])
            axh.imshow(D_[:, sel], origin="lower", aspect="auto", extent=ext, cmap="magma", vmin=-80, vmax=0)
            axh.set_yticks([i + 0.5 for i in yt[::2]]); axh.set_yticklabels([note_label(centers[i]) for i in yt[::2]], fontsize=6)
            axh.set_xticks([]); axh.set_ylabel(lab, fontsize=7)

        axl = fig.add_subplot(gs[4])
        axl.imshow(Dhf[:, sel], origin="lower", aspect="auto", extent=[t0, t1, 0, 1], cmap="magma", vmin=-80, vmax=0)
        axl.plot(tt, np.clip(hflux[sel], 0, 1), color="#6cf", lw=0.8)
        for b in beats: axl.axvline(b, color="w", lw=0.4, alpha=0.3)
        axl.set_xlim(t0, t1); axl.set_yticks([]); axl.set_xticks([])
        axl.set_ylabel(f"hi-hat lane\n>{centers[hf][0] / 1000:.0f} kHz\n(clicks)", fontsize=6)

        ax2 = fig.add_subplot(gs[5])
        im2 = ax2.imshow(Wc[:, sel], origin="lower", aspect="auto", extent=[t0, t1, 0, 24], cmap="viridis", vmin=0, vmax=0.8)
        ax2.set_yticks([1, 22]); ax2.set_yticklabels(["low", "high"], fontsize=6); ax2.set_ylabel("stereo\nwidth", fontsize=7); ax2.set_xticks([])
        cb2 = fig.colorbar(im2, cax=ax2.inset_axes([1.005, 0, 0.012, 1]), ticks=[0, 0.4, 0.8])
        cb2.ax.set_yticklabels(["0 mono", "0.4", "0.8+ wide"], fontsize=5)

        ax3 = fig.add_subplot(gs[6])
        ax3.imshow(C[:, sel], origin="lower", aspect="auto", extent=[t0, t1, 0, 12], cmap="Greys", vmin=0, vmax=1)
        ax3.set_yticks(np.arange(12) + 0.5); ax3.set_yticklabels(NOTE_NAMES, fontsize=6); ax3.set_xticks([])
        ax3.set_ylabel("chroma\n(pitch class)", fontsize=7)

        ax4 = fig.add_subplot(gs[7])
        ax4.fill_between(tt, flux[sel], color="#d62", lw=0, alpha=0.8, label="onsets")
        ax4.plot(tt, (rms_db[sel] + 60) / 60, color="#36c", lw=1, label="loudness")
        for b in beats: ax4.axvline(b, color="#888", lw=0.4, alpha=0.5)
        ax4.set_xlim(t0, t1); ax4.set_ylim(0, 1.05); ax4.set_yticks([]); ax4.set_ylabel("onsets /\nloudness\n(-60..0 dB)", fontsize=6)
        ax4.set_xticks(np.arange(np.ceil(t0), t1 + 0.01, 1)); ax4.tick_params(labelsize=6)
        ax4.set_xlabel("seconds", fontsize=7); ax4.legend(fontsize=6, loc="upper right")
        png = os.path.join(a.out, f"tile_{k + 1:02d}.png")
        fig.savefig(png, bbox_inches="tight"); plt.close(fig)

        # numbers
        hh = find_peaks(np.clip(hflux[sel], 0, None), height=0.35, distance=max(1, int(0.08 * fps)))[0]
        seg_chords = []
        step = int(fps * 2)  # one chord guess per ~2 s
        idxs = np.where(sel)[0]
        for s0 in range(idxs[0], idxs[-1] + 1, step):
            cv = C[:, s0:s0 + step].mean(1)
            cv = cv / (np.linalg.norm(cv) + 1e-12)
            seg_chords.append(cnames[int(np.argmax(T @ cv))])
        info = {
            "tile": k + 1, "start": round(t0, 2), "end": round(t1, 2),
            "tempo_bpm": round(bpm, 1) if bpm else None,
            "tempo_check": alts,
            "hihat_clicks": [round(float(tt[i]), 2) for i in hh][:40],
            "hihat_click_strength": [round(float(np.clip(hflux[sel][i], 0, 1)), 2) for i in hh][:40],
            "loudness_db_mean": round(float(rms_db[sel].mean()), 1),
            "energy_low_mid_high_pct": [round(100 * float(x[sel].sum() / tot[sel].sum()), 1) for x in (low, midb, high)],
            "brightness_hz": round(float(np.median(centroid[sel]))),
            "noisiness_0to1": round(float(np.median(flat[sel])), 3),
            "stereo_width": round(float(np.median(width[:, sel])), 3),
            "chords_every_2s": seg_chords,
        }
        summary.append(info)

    with open(os.path.join(a.out, "sidecar.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    with open(os.path.join(a.out, "sidecar.md"), "w") as fh:
        fh.write(f"# AuraGraph v0.2.1 sidecar: {os.path.basename(a.audio)}\n\n")
        for s in summary:
            fh.write(f"## tile {s['tile']:02d}  {s['start']:.0f}-{s['end']:.0f}s\n"
                     f"tempo≈{s['tempo_bpm']} bpm (autocorr this/half/double: {s['tempo_check']}) · loudness {s['loudness_db_mean']} dB · low/mid/high {s['energy_low_mid_high_pct']}% · "
                     f"brightness {s['brightness_hz']} Hz · noisiness {s['noisiness_0to1']} · width {s['stereo_width']}\n"
                     f"chords: {' '.join(s['chords_every_2s'])}\n"
                     f"hi-hat lane clicks ({len(s['hihat_clicks'])}, time:strength): {' '.join(f'{c}:{v}' for c, v in zip(s['hihat_clicks'][:16], s['hihat_click_strength'][:16]))}\n\n")
    print(f"{ntiles} tiles -> {a.out}")


if __name__ == "__main__":
    main()
