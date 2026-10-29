#!/usr/bin/env python3
"""AuraGraph selfsim: which seconds look like which other seconds (Kehai, 2026-10-17).
Builds a self-similarity matrix from chroma (harmony) and log-band timbre, 0.25 s frames.
Loops = bright diagonal stripes; sections = bright blocks. usage: selfsim.py AUDIO OUT.png"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import proto as P
L, R = P.decode(sys.argv[1]); x = (L + R) / 2
f, t, M = P.spec(x)
# features per STFT frame
bands = np.geomspace(60, 8000, 33)
tim = np.stack([M[(f >= a) & (f < b)].mean(0) for a, b in zip(bands[:-1], bands[1:])])
tim = np.log1p(tim * 50)
pc = np.zeros((12, M.shape[1])); ok = f > 50
midi = 69 + 12 * np.log2(f[ok] / 440.0); idx = np.round(midi).astype(int) % 12
for k in range(12): pc[k] = M[ok][idx == k].sum(0)
# pool to 0.25 s
hop = P.HOP / P.SR; n = max(1, int(round(0.25 / hop)))
def pool(A): T = A.shape[1] // n; return A[:, :T * n].reshape(A.shape[0], T, n).mean(2)
tim, pc = pool(tim), pool(pc)
def norm(A): A = A - A.mean(1, keepdims=True); return A / (np.linalg.norm(A, axis=0, keepdims=True) + 1e-9)
F = np.vstack([norm(pc) * 0.6, norm(tim) * 0.8])
F = F / (np.linalg.norm(F, axis=0, keepdims=True) + 1e-9)
S = F.T @ F
# smooth along diagonals (repeats become lines, noise fades)
D = 6; Sd = np.zeros_like(S)
for d in range(D): Sd[:len(S)-d, :len(S)-d] += S[d:, d:]
S = Sd / D
T = S.shape[0] * n * hop
# novelty (checkerboard kernel) -> section boundaries
k = 16; g = np.outer(np.r_[-np.ones(k), np.ones(k)], np.r_[-np.ones(k), np.ones(k)])
nov = np.array([ (S[i-k:i+k, i-k:i+k] * g).sum() if k <= i < len(S)-k else 0 for i in range(len(S))])
nov = np.clip(nov, 0, None); nov /= nov.max() + 1e-9
peaks = [i for i in range(1, len(nov)-1) if nov[i] > 0.35 and nov[i] >= nov[i-1] and nov[i] >= nov[i+1]]
fig, ax = plt.subplots(2, 1, figsize=(10, 11.5), gridspec_kw={'height_ratios': [10, 1.5]})
ax[0].imshow(S, origin='lower', cmap='magma', extent=[0, T, 0, T], vmin=np.percentile(S, 50), vmax=np.percentile(S, 99.5))
ax[0].set_title("AuraGraph selfsim | which seconds look like which other seconds | bright diagonal = repeat")
ax[0].set_xlabel("seconds"); ax[0].set_ylabel("seconds")
ts = np.arange(len(nov)) * n * hop
ax[1].plot(ts, nov, lw=1); [ax[1].axvline(ts[p], color='r', lw=.6) for p in peaks]
ax[1].set_xlim(0, T); ax[1].set_title("novelty (section-change strength); red = candidate boundaries")
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=90)
print("boundaries (s):", [round(ts[p], 1) for p in peaks])
