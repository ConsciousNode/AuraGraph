#!/usr/bin/env python3
"""AuraGraph timbre lane (Kehai Interim, 2026-10-21).

Follow one instrument by *how it sounds*, at whatever pitch it plays.

Idea: an instrument's timbre is mostly the shape of its overtone stack (how loud the
2nd, 3rd, 4th... harmonics are relative to the 1st). That shape stays roughly the same
when the note changes; the whole stack just slides up or down. So:
  1. learn a template: the harmonic-level profile of a clean moment of the instrument
     (e.g. the melodica entrance at 0:17), with the background just before it removed;
  2. for every frame and every candidate pitch f0, read the levels at f0, 2f0, ... 10f0;
  3. score how well that profile matches the template (correlation of the shapes),
     gated by whether the stack actually stands above the background;
  4. the lane = best score over pitch at each moment, plus which pitch won.
Prior art: harmonic templates / shift-invariant NMF on a log-frequency axis; spectral
envelope and MFCC-style timbre fingerprints. Nothing here needs a library a browser lacks.

usage: timbre.py AUDIO LEARN_START LEARN_END BG_START BG_END OUT_PREFIX WIN0-WIN1 [WIN0-WIN1 ...]
"""
import sys
import numpy as np
from scipy.signal import stft
from scipy.ndimage import uniform_filter1d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import proto as P

NFFT, HOP, NH = 2048, 256, 10
F0S = 220.0 * 2 ** (np.arange(0, 12 * 3 * 2.6) / 36)   # 220 Hz up ~2.6 octaves, 1/3-semitone steps


def spectrum(sig):
    f, t, Z = stft(sig, fs=P.SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
    return f, t, 20 * np.log10(np.abs(Z) + 1e-9)


def harmonic_levels(f, D, f0s):
    """levels[c, h, t]: dB at h*f0 (peak within +-1/4 semitone), for each candidate f0."""
    df = f[1] - f[0]
    out = np.full((len(f0s), NH, D.shape[1]), -120.0)
    for h in range(1, NH + 1):
        fh = f0s * h
        ok = fh < f[-1] / 1.02
        lo = np.floor(fh[ok] * 2 ** (-1 / 48) / df).astype(int)
        hi = np.ceil(fh[ok] * 2 ** (1 / 48) / df).astype(int) + 1
        rows = np.where(ok)[0]
        for r, a, b in zip(rows, lo, hi):
            out[r, h - 1] = D[a:b].max(0)
    return out


def shape(levels):
    """Profile relative to its own mean (removes overall loudness), along the harmonic axis."""
    return levels - levels.mean(axis=-2, keepdims=True)


def main():
    path = sys.argv[1]
    ls, le, bs, be = map(float, sys.argv[2:6])
    prefix = sys.argv[6]
    wins = [tuple(map(float, w.split("-"))) for w in sys.argv[7:]]
    L, R = P.decode(path)
    mid = (L + R) / 2
    f, t, D = spectrum(mid)
    med = np.median(D, axis=1, keepdims=True)          # per-frequency background level
    W = D - med                                        # dB above usual

    # --- learn the template at the clean moment, background removed ---
    fl = (t >= ls) & (t < le); fb = (t >= bs) & (t < be)
    spec_l = D[:, fl].mean(1); spec_b = D[:, fb].mean(1)
    gain = np.maximum(spec_l - spec_b, 0)              # what the instrument added, in dB
    Hl = harmonic_levels(f, gain[:, None], F0S)[:, :, 0]
    # pick the f0 whose harmonic stack captures the most added energy
    # (the fundamental itself must carry added energy, or an octave-low f0 wins by
    #  treating the real 1st, 2nd, 3rd harmonics as its own 2nd, 4th, 6th)
    G = np.clip(Hl[:, :4], 0, None)
    c0 = int(np.argmax(G[:, 0] + 0.5 * G[:, 1:].mean(1)))
    f0_learn = F0S[c0]
    tmpl = Hl[c0] - Hl[c0].mean()
    print(f"template learned at f0 ~ {f0_learn:.0f} Hz ({P.note_label(f0_learn)}); "
          f"harmonic levels dB rel. mean: {np.round(tmpl, 1).tolist()}")

    # --- contrast: what does a *typical* harmonic sound in this song look like? ---
    # Every pitched sound has a strong fundamental and falling overtones, so raw shape
    # matching says "yes" to voices and guitars too. Subtract the song's typical stack
    # shape from both sides, and compare only harmonics 2-10 relative to the 1st:
    # what's left is how this instrument *differs* from the average sound.
    gsel = np.arange(0, D.shape[1], 8)                     # every 8th frame, whole song
    Hg = harmonic_levels(f, D[:, gsel], F0S); Hgw = harmonic_levels(f, W[:, gsel], F0S)
    wg = np.clip(Hgw[:, :3], 0, 30).mean(1)                 # weight by how much it stands out
    wg = wg * (wg >= np.percentile(wg, 90))
    rel_g = Hg[:, 1:, :] - Hg[:, :1, :]
    generic = (rel_g * wg[:, None, :]).sum((0, 2)) / (wg.sum() + 1e-9)
    rel_t = Hl[c0, 1:] - Hl[c0, 0]
    tmplc = rel_t - generic; tmplc = tmplc - tmplc.mean()
    print("contrast template (h2..h10 vs song-typical, dB):", np.round(tmplc, 1).tolist())

    # --- score every frame / candidate pitch in the windows of interest ---
    rows = []
    for (w0, w1) in wins:
        sel = (t >= w0) & (t < w1)
        Hw = harmonic_levels(f, W[:, sel], F0S)            # dB above usual at each harmonic
        Hd = harmonic_levels(f, D[:, sel], F0S)            # raw dB, for the shape
        sh = (Hd[:, 1:, :] - Hd[:, :1, :]) - generic[None, :, None]
        sh = sh - sh.mean(1, keepdims=True)
        num = (sh * tmplc[None, :, None]).sum(1)
        den = np.sqrt((sh ** 2).sum(1) * (tmplc ** 2).sum()) + 1e-9
        corr = num / den                                    # -1..1, shape match
        stand = np.clip(Hw[:, :3], 0, 30).mean(1) / 30      # does the stack stand out? 0..1
        score = np.clip(corr, 0, 1) * np.clip(stand * 2, 0, 1)
        best = score.argmax(0)
        lane = score.max(0)
        lane = uniform_filter1d(lane, 3)
        rows.append((w0, w1, t[sel], lane, F0S[best], score))

    fig, axes = plt.subplots(len(rows) * 2, 1, figsize=(13, 3.3 * len(rows)),
                             gridspec_kw={"height_ratios": [2, 1] * len(rows)})
    for k, (w0, w1, tt, lane, fbest, score) in enumerate(rows):
        a = axes[2 * k]
        a.imshow(score, origin="lower", aspect="auto", extent=[w0, w1, 0, len(F0S)], cmap="viridis", vmin=0, vmax=0.8)
        yt = [int(np.argmin(abs(np.log2(F0S / n)))) for n in (220, 440, 880, 1320)]
        a.set_yticks(yt); a.set_yticklabels([f"{P.note_label(F0S[i])}" for i in yt], fontsize=7)
        a.set_ylabel("match by\nwhich pitch", fontsize=7); a.set_xticks([])
        a.set_title(f"timbre lane: melodica template (learned {ls:.2f}-{le:.2f} s at {P.note_label(f0_learn)}) | {w0:.1f}-{w1:.1f} s", fontsize=9)
        b = axes[2 * k + 1]
        b.fill_between(tt, lane, color="#3c9", lw=0)
        b.set_xlim(w0, w1); b.set_ylim(0, 1); b.set_yticks([0, 0.5, 1]); b.tick_params(labelsize=7)
        b.set_xticks(np.arange(np.ceil(w0), w1 + 0.01, 0.5)); b.set_ylabel("lane", fontsize=7)
    fig.tight_layout(); fig.savefig(prefix + ".png", dpi=100)

    # text: where the lane is high, with the winning pitch
    out = [f"# timbre lane (template {P.note_label(f0_learn)} learned {ls}-{le} s, bg {bs}-{be} s)"]
    for (w0, w1, tt, lane, fbest, score) in rows:
        out.append(f"\n## {w0}-{w1} s  (mean lane {lane.mean():.2f})")
        on = lane > 0.45
        edges = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]])))
        for a_, b_ in zip(edges[::2], edges[1::2]):
            if tt[min(b_, len(tt) - 1)] - tt[a_] < 0.06: continue
            fmed = np.median(fbest[a_:b_])
            out.append(f"- {tt[a_]:.2f}-{tt[min(b_, len(tt) - 1)]:.2f} s  peak {lane[a_:b_].max():.2f}  pitch ~{P.note_label(fmed)} ({fmed:.0f} Hz)")
    txt = "\n".join(out); open(prefix + ".md", "w").write(txt + "\n"); print(txt)


if __name__ == "__main__":
    main()
