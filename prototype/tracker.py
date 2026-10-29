#!/usr/bin/env python3
"""AuraGraph sample tracker (Kehai, 2026-10-17; Kham's lesson #6: same sample, different pitch).
Take a snippet [t0,t1]; slide its semitone-binned spectrogram over the whole track at every
time offset and every pitch shift (-12..+12 semitones); report where it recurs and how shifted.
usage: tracker.py AUDIO t0 t1 OUT.png [threshold]"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import proto as P
audio, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
thr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
L, R = P.decode(audio); x = (L + R) / 2
f, t, M = P.spec(x); hop = P.HOP / P.SR
# semitone bins, MIDI 36 (C2, 65 Hz) .. 108 (C8, 4.2 kHz)
lo, hi = 36, 108
midi = 69 + 12 * np.log2(np.maximum(f, 1) / 440.0)
S = np.zeros((hi - lo, M.shape[1]))
for m in range(lo, hi):
    sel = (midi >= m - .5) & (midi < m + .5)
    if sel.any(): S[m - lo] = M[sel].sum(0)
S = np.log1p(S * 30)
S -= S.mean(1, keepdims=True)                      # remove the constant bed per pitch
a, b = int(t0 / hop), int(t1 / hop); Tm = S[:, a:b]; w = b - a
best = np.full(S.shape[1] - w, -1.0); shift = np.zeros(S.shape[1] - w, int)
for sh in range(-12, 13):
    Ts = np.roll(Tm, sh, axis=0)
    if sh > 0: Ts[:sh] = 0
    if sh < 0: Ts[sh:] = 0
    tv = Ts.ravel() - Ts.mean(); tn = np.linalg.norm(tv) + 1e-9
    for i in range(0, S.shape[1] - w):
        W = S[:, i:i + w]; wv = W.ravel() - W.mean()
        c = float(tv @ wv) / (tn * (np.linalg.norm(wv) + 1e-9))
        if c > best[i]: best[i], shift[i] = c, sh
# peaks: local maxima above threshold, at least one snippet-length apart
hits = []
for i in np.argsort(-best):
    if best[i] < thr: break
    if all(abs(i - j) >= w * 0.8 for j, _, _ in hits): hits.append((i, best[i], shift[i]))
hits.sort()
ts = np.arange(len(best)) * hop
fig, ax = plt.subplots(2, 1, figsize=(12, 5.5), sharex=True)
ax[0].plot(ts, best, lw=.6); ax[0].axhline(thr, color='gray', ls=':')
for i, c, sh in hits: ax[0].plot(ts[i], c, 'o', ms=4, color='C3' if sh else 'C2')
ax[0].set_ylabel("match"); ax[0].set_title(f"sample tracker: snippet {t0}-{t1}s | green = same pitch, red = transposed")
ax[1].scatter([ts[i] for i,_,_ in hits], [sh for _,_,sh in hits], c=['C3' if sh else 'C2' for *_ ,sh in hits], s=18)
ax[1].set_ylabel("pitch shift (semitones)"); ax[1].set_xlabel("seconds"); ax[1].set_ylim(-13, 13); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(out, dpi=90)
print(f"{len(hits)} hits ≥ {thr}:")
for i, c, sh in hits: print(f"  {ts[i]:6.2f}s  match {c:.2f}  shift {sh:+d}")
