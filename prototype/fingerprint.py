#!/usr/bin/env python3
"""AuraGraph harmonic fingerprint (Kehai, 2026-10-17).

For each labeled window: find the fundamental (harmonic product spectrum), then measure the strength of
overtones 1x..12x. Draws one spectrum slice + one overtone bar chart per window, side by side, so timbres
can be compared. usage: fingerprint.py AUDIO OUT.png "label:start-end[:fmin-fmax]" ...
"""
import sys
import numpy as np
from scipy.signal import stft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import proto as P

NH = 12


def fingerprint(mid, t0, t1, fmin=80, fmax=4000):
    seg = mid[int(t0 * P.SR):int(t1 * P.SR)]
    f, _, Z = stft(seg, fs=P.SR, nperseg=8192, noverlap=6144)
    S = np.abs(Z).mean(axis=1)
    df = f[1] - f[0]
    # harmonic product spectrum over 3 harmonics -> fundamental
    hps = S.copy()
    for h in (2, 3):
        dec = S[::h]
        hps[:len(dec)] *= dec
        hps[len(dec):] = 0
    band = (f >= fmin) & (f <= fmax)
    f0 = f[band][np.argmax(hps[band])]
    amps = []
    for k in range(1, NH + 1):
        fk = k * f0
        if fk > f[-1]: amps.append(0.0); continue
        w = max(2, int(0.02 * fk / df))
        i = int(round(fk / df))
        amps.append(float(S[max(0, i - w):i + w + 1].max()))
    amps = np.array(amps)
    rel_db = 20 * np.log10(np.maximum(amps, 1e-12) / max(amps.max(), 1e-12))
    return f, S, f0, rel_db


def main():
    audio, out, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    L, R = P.decode(audio)
    mid = (L + R) / 2
    fig, axes = plt.subplots(len(specs), 2, figsize=(12, 3.2 * len(specs)), squeeze=False)
    lines = []
    for row, sp in enumerate(specs):
        parts = sp.split(":")
        label, (t0, t1) = parts[0], map(float, parts[1].split("-"))
        lo, hi = map(float, parts[2].split("-")) if len(parts) > 2 else (80, 4000)
        f, S, f0, rel = fingerprint(mid, t0, t1, lo, hi)
        a, b = axes[row]
        a.semilogx(f[1:], 20 * np.log10(S[1:] / S.max() + 1e-12), lw=0.6, color="#444")
        for k in range(1, NH + 1):
            a.axvline(k * f0, color="#d62", lw=0.5, alpha=0.6)
        a.set_xlim(50, 11000); a.set_ylim(-90, 2)
        a.set_title(f"{label}  {t0:.1f}-{t1:.1f}s  spectrum slice, f0 = {f0:.0f} Hz ({P.note_label(f0)}), red = overtones", fontsize=8)
        a.set_ylabel("dB", fontsize=7); a.tick_params(labelsize=6)
        b.bar(np.arange(1, NH + 1), rel + 60, bottom=-60, color="#36c")
        b.set_ylim(-60, 2); b.set_xticks(range(1, NH + 1)); b.set_xlabel("overtone (x f0)", fontsize=7)
        b.set_title(f"{label}: harmonic fingerprint (dB relative to strongest)", fontsize=8); b.tick_params(labelsize=6)
        lines.append(f"{label} ({t0}-{t1}s): f0 {f0:.0f} Hz {P.note_label(f0)} | overtones dB: " + " ".join(f"{x:.0f}" for x in rel))
    fig.tight_layout(); fig.savefig(out, dpi=100)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
