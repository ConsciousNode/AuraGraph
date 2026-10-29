#!/usr/bin/env python3
"""AuraGraph timbre judge v3 (Kehai Interim, 2026-10-21).

v2 had one half-second training example per instrument, all from one dense live mix.
v3 trains on clean solo recordings Kham found (CC BY-SA / PD, see samples/reference/SOURCES.md)
plus labelled Birdhouse moments, and uses stereo to pull sources apart:

  * a pan mask: keep only the spectrogram cells that lean right (or left, or centre),
    because Kham's ears say the accordion sits right and the guitar left in 1:31-1:36;
  * pitch by salience inside the masked spectrum (no template, so no best-of-N trap);
  * timbre features at that pitch: harmonics 2..8 relative to the 1st (kept below 7 kHz);
  * a per-class Gaussian judge (centroid + spread per feature), frames voted per span.

usage: timbre3.py BIRDHOUSE ACCORDION_REF MELODICA_REF OUT_PREFIX
"""
import sys
import numpy as np
from scipy.signal import stft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import proto as P
from timbre import harmonic_levels

NFFT, HOP, NH = 2048, 256, 8
F0S = 180.0 * 2 ** (np.arange(0, 36 * 2.3) / 36)      # ~180-870 Hz, so h8 stays < 7 kHz


def spec_lr(path):
    L, R = P.decode(path)
    f, t, ZL = stft(L, fs=P.SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
    _, _, ZR = stft(R, fs=P.SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
    AL, AR = np.abs(ZL), np.abs(ZR)
    pan = (AR - AL) / (AR + AL + 1e-9)
    D = 20 * np.log10((AL + AR) / 2 + 1e-9)
    return f, t, D, pan


def feats(f, t, D, pan, a, b, side=None):
    sel = (t >= a) & (t < b)
    Dm = D[:, sel].copy()
    if side == "right": Dm[pan[:, sel] < 0.15] = -120
    if side == "left": Dm[pan[:, sel] > -0.15] = -120
    base = np.median(D, axis=1, keepdims=True)
    W = Dm - base
    Hw = harmonic_levels(f, W, F0S)
    sal = np.clip(Hw[:, :5], 0, 40).mean(1)
    sal[np.clip(Hw[:, 0], 0, None) < 6] = 0
    c = sal.argmax(0); ok = sal.max(0) > 5
    Hd = harmonic_levels(f, Dm, F0S)
    fr = np.arange(len(c))
    st = Hd[c, :, fr]
    rel = st[:, 1:] - st[:, :1]
    ok &= (st[:, 1:] > -100).all(1)                    # masked-out harmonics: skip frame
    return rel[ok], F0S[c][ok]


def main():
    bird, acc, mel, prefix = sys.argv[1:5]
    B = spec_lr(bird); A = spec_lr(acc); M = spec_lr(mel)
    train = {
        "accordion": [feats(*A, 5, 95)[0]],                                   # Bach, solo accordion
        "melodica":  [feats(*M, 1, 44)[0]],                                   # Rakes of Kildare, solo
        "guitar":    [feats(*B, 91.4, 92.6, "left")[0], feats(*B, 81.65, 82.6)[0]],
        "voice":     [feats(*B, 77.0, 78.8)[0]],
    }
    stats = {}
    for k, xs in train.items():
        X = np.vstack(xs)
        mu = np.median(X, 0); sd = 1.4826 * np.median(np.abs(X - mu), 0) + 1.5
        stats[k] = (mu, sd, len(X))
    names = list(stats)

    def judge(X):
        ll = np.stack([(-0.5 * ((X - stats[k][0]) / stats[k][1]) ** 2 - np.log(stats[k][1])).sum(1) for k in names], 1)
        return ll.argmax(1)

    tests = [
        ("accordion", "doot 1", 80.43, 80.62, None), ("accordion", "doot 2", 80.74, 80.95, None),
        ("accordion", "doot 3", 81.04, 81.36, None), ("accordion", "entrance 0:17", 17.12, 17.70, None),
        ("accordion", "fast part 1:32.7-1:36, right side", 92.7, 96.0, "right"),
        ("guitar", "1:32.7-1:36, left side", 92.7, 96.0, "left"),
        ("guitar", "solo tail 1:22.7-1:23.6", 82.7, 83.6, None),
        ("voice", "end of 'soul' 1:19-1:19.6", 79.0, 79.6, None),
    ]
    out = ["# timbre judge v3: clean references + Birdhouse labels, pan masks", "",
           "training frames: " + ", ".join(f"{k} {stats[k][2]}" for k in names), "",
           "centroids (h2..h8 rel. h1, dB):"]
    for k in names:
        out.append(f"- {k}: {np.round(stats[k][0], 1).tolist()}")
    out += ["", "## held-out spans (frames voted)"]
    right = 0
    for truth, lab, a, b, side in tests:
        X, f0 = feats(*B, a, b, side)
        if len(X) == 0:
            out.append(f"- {lab}: no confident pitch"); continue
        v = judge(X); votes = {n: int((v == i).sum()) for i, n in enumerate(names)}
        win = max(votes, key=votes.get); right += win == truth
        out.append(f"- {lab} (truth {truth}) -> **{win}** {votes} pitch ~{P.note_label(float(np.median(f0)))}")
    out.append(f"\nspans right: {right}/{len(tests)}")
    txt = "\n".join(out); open(prefix + ".md", "w").write(txt + "\n"); print(txt)


if __name__ == "__main__":
    main()
