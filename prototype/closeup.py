#!/usr/bin/env python3
"""AuraGraph close-up tile (Kehai Interim, 2026-10-21).

For short stretches (1-4 s) where things happen faster than the main tile can show:
  1. timing view : short window (~23 ms), whitened, 250 Hz-5 kHz, many pixels per second
  2. pitch view  : constant-Q (v2): 36 bins per octave, window length shrinks as pitch rises
     (Q=34: ~half-semitone resolution everywhere; ~130 ms at 250 Hz, ~7 ms at 5 kHz).
     Pitch per note is refined between bins and reported in cents off the nearest note.
  3. spike raster: SpikeVox-style leaky integrate-and-fire neurons, one per log band.
     Each neuron integrates the *rise* in its band's energy, leaks, fires, then rests and
     adapts, so it answers note starts and stays quiet through sustain. Spikes have
     ~3 ms timing regardless of window size. (A re-implementation of the SpikeVox idea
     from Evangelion, not its code.)
  4. note events : spike bursts grouped across bands -> onset time, main pitch, length,
     printed to stdout and written as markdown next to the PNG, because text is never
     downscaled.

usage: closeup.py AUDIO START END OUT.png
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

FLO, FHI = 250.0, 5000.0


def banded(sig, nfft, hop, nb=200):
    f, t, M = stft(sig, fs=P.SR, nperseg=nfft, noverlap=nfft - hop, boundary=None, padded=False)
    M = np.abs(M)
    e = np.geomspace(FLO, FHI, nb + 1); c = np.sqrt(e[:-1] * e[1:])
    idx = [np.where((f >= lo) & (f < hi))[0] for lo, hi in zip(e[:-1], e[1:])]
    idx = [i if len(i) else np.array([np.argmin(abs(f - cc))]) for i, cc in zip(idx, c)]
    return c, t, np.stack([M[i].mean(0) for i in idx])


def whiten(D, ctx_cols):
    return np.clip(D - np.median(D[:, ctx_cols], axis=1, keepdims=True), 0, 24)


def lif(B, dt, tau=0.03, thresh=1.0, refractory=0.04, adapt=0.6, tau_a=0.25):
    """B: band energies in dB (bands x frames). Input current = positive rise in dB per frame."""
    rise = np.maximum(np.diff(B, axis=1, prepend=B[:, :1]), 0)
    rise = rise / (np.percentile(rise[rise > 0], 95) + 1e-9)
    nb, T = B.shape
    v = np.zeros(nb); a = np.zeros(nb); rest = np.zeros(nb)
    spikes = np.zeros((nb, T), bool)
    k = np.exp(-dt / tau); ka = np.exp(-dt / tau_a)
    for j in range(T):
        live = rest <= 0
        v = v * k + rise[:, j] * live
        fire = live & (v > thresh + a)
        spikes[fire, j] = True
        v[fire] = 0; rest[fire] = refractory; a[fire] += adapt
        rest -= dt; a *= ka
    return spikes


def note_label(fr):
    return P.note_label(fr)


def cqt(sig, hop, bpo=36, Q=34.0):
    """Constant-Q magnitudes on a fixed hop. Each bin: Hann-windowed complex sinusoid of
    length Q*SR/f, correlated with the signal by FFT convolution, sampled every `hop`."""
    from scipy.signal import fftconvolve
    nb = int(np.floor(bpo * np.log2(FHI / FLO))) + 1
    freqs = FLO * 2 ** (np.arange(nb) / bpo)
    out = np.empty((nb, len(sig) // hop))
    for k, fk in enumerate(freqs):
        N = int(round(Q * P.SR / fk)) | 1
        n = np.arange(N) - N // 2
        ker = np.hanning(N) * np.exp(-2j * np.pi * fk * n / P.SR)
        ker /= np.abs(ker).sum()
        y = fftconvolve(sig, ker[::-1].conj(), mode="same")
        out[k] = np.abs(y[::hop][:out.shape[1]])
    times = np.arange(out.shape[1]) * hop / P.SR
    return freqs, times, out


def refine(freqs, prof, k):
    """Parabolic peak between neighbouring CQT bins (log-frequency), returns Hz."""
    if 0 < k < len(prof) - 1:
        y0, y1, y2 = prof[k - 1], prof[k], prof[k + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if den < 0 else 0.0
        return freqs[k] * 2 ** (np.clip(d, -0.5, 0.5) * np.log2(freqs[1] / freqs[0]))
    return freqs[k]


def cents_label(fr):
    m = 69 + 12 * np.log2(fr / 440.0); r = int(round(m))
    return f"{P.NOTE_NAMES[r % 12]}{r // 12 - 1}{(m - r) * 100:+.0f}c"


def main():
    path, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    L, R = P.decode(path)
    pad = 3.0
    a0 = max(0, int((t0 - pad) * P.SR)); a1 = int((t1 + pad) * P.SR)
    mid = ((L + R) / 2)[a0:a1]; off = a0 / P.SR

    cS, tS, BS = banded(mid, 512, 64)      # timing: 23 ms window, 2.9 ms hop
    cL, tL, BL = cqt(mid, 64)              # pitch: constant-Q, same hop
    tS += off; tL += off
    DS, DL = P.db(BS, 1.0), P.db(BL, 1.0)
    selS = (tS >= t0) & (tS < t1); selL = (tL >= t0) & (tL < t1)
    WS, WL = whiten(DS, slice(None))[:, selS], whiten(DL, slice(None))[:, selL]

    # spikes on 48 coarse bands from the timing view
    groups = np.array_split(np.arange(len(cS)), 48)
    Bc = np.stack([DS[g].mean(0) for g in groups]); cc = np.array([np.sqrt(cS[g[0]] * cS[g[-1]]) for g in groups])
    dt = 64 / P.SR
    SP = lif(Bc, dt)[:, selS]
    ts = tS[selS]

    # note events: population spike count, smoothed; peaks = onsets; pitch from pitch view
    pop = uniform_filter1d(SP.sum(0).astype(float), size=max(1, int(0.012 / dt)))
    from scipy.signal import find_peaks
    pk, pr = find_peaks(pop, height=max(3, 0.25 * pop.max()), distance=int(0.06 / dt))
    events = []
    for n, i in enumerate(pk):
        nxt = pk[n + 1] if n + 1 < len(pk) else len(ts) - 1
        # pitch: strongest *held* row, 30-150 ms after onset (skips the broadband attack),
        # below 2.5 kHz so cymbal hiss can't win
        j0 = np.searchsorted(tL[selL], ts[i] + 0.03); j1 = np.searchsorted(tL[selL], ts[i] + 0.15)
        # unclipped whitening here: the display clips at +24 dB, and a loud note saturates
        # several neighbouring rows at once, so argmax on the clipped image picked the
        # lowest saturated row (a steady ~-60 cent bias, caught on synthetic notes)
        UL = (DL - np.median(DL, axis=1, keepdims=True))[:, selL]
        prof = np.median(UL[:, j0:max(j1, j0 + 1)], axis=1)
        prof[cL >= 2500] = -np.inf
        top = int(np.argmax(prof))
        fref = refine(cL, np.median(DL[:, selL][:, j0:max(j1, j0 + 1)], axis=1), top)
        # length: how long that row stays > half its onset level (pitch view)
        row = WL[top, j0:]; lvl = row[:max(1, j1 - j0)].mean()
        dur_cols = np.argmax(row < 0.5 * lvl) if np.any(row < 0.5 * lvl) else len(row)
        bands_hit = int(SP[:, max(0, i - 4):i + 5].any(1).sum())
        events.append((ts[i], fref, dur_cols * dt, bands_hit, pop[i]))

    fig, ax = plt.subplots(4, 1, figsize=(14, 11), sharex=True,
                           gridspec_kw={"height_ratios": [3, 3, 2, 1]})
    for a_, W, cf, lab in ((ax[0], WS, cS, "timing view\n23 ms window"), (ax[1], WL, cL, "pitch view\nconstant-Q, 36/oct")):
        yt = [int(np.argmin(abs(np.log2(cf / n)))) for n in (330, 440, 660, 880, 1320, 1760, 3520)]
        a_.imshow(W, origin="lower", aspect="auto", extent=[t0, t1, 0, len(cf)], cmap="inferno", vmin=0, vmax=24)
        a_.set_yticks([y + 0.5 for y in yt]); a_.set_yticklabels([f"{note_label(cf[i])} {cf[i]:.0f}Hz" for i in yt], fontsize=7)
        a_.set_ylabel(lab, fontsize=8)
    for e in events:
        for a_ in ax[:3]: a_.axvline(e[0], color="#6cf", lw=0.7, alpha=0.6)
    si, sj = np.nonzero(SP)
    ax[2].scatter(ts[sj], si, s=4, c="#fc6", marker="|")
    ax[2].set_ylim(-1, 48); ax[2].set_facecolor("#111")
    ax[2].set_yticks([0, 47]); ax[2].set_yticklabels([f"{cc[0]:.0f}Hz", f"{cc[-1]:.0f}Hz"], fontsize=7)
    ax[2].set_ylabel("LIF spikes\n(SpikeVox-style)", fontsize=8)
    ax[3].fill_between(ts, pop, color="#6cf", lw=0)
    ax[3].set_yticks([]); ax[3].set_ylabel("spikes\nper frame", fontsize=8)
    ax[3].set_xticks(np.arange(np.ceil(t0 * 10) / 10, t1 + 1e-6, 0.1)); ax[3].tick_params(labelsize=7)
    ax[3].set_xlabel("seconds", fontsize=8)
    ax[0].set_title(f"AuraGraph close-up | {t0:.2f}-{t1:.2f} s | blue lines = detected note starts", fontsize=9)
    fig.tight_layout(); fig.savefig(out, dpi=110)

    lines = [f"# close-up {t0:.2f}-{t1:.2f} s: note events (onset, main pitch, length, bands spiking, strength)"]
    for e in events:
        lines.append(f"- {e[0]:.3f} s | {cents_label(e[1])} ~{e[1]:.0f} Hz | ~{e[2] * 1000:.0f} ms | {e[3]} bands | {e[4]:.1f}")
    txt = "\n".join(lines)
    open(out.rsplit(".", 1)[0] + "_events.md", "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
