#!/usr/bin/env python3
"""AuraGraph timbre lane v2 (Kehai Interim, 2026-10-21).

v1 (timbre.py) taught two lessons:
  * every pitched sound has a strong fundamental and falling overtones, so "does this
    stack look like the melodica?" says yes to voices and guitars too;
  * taking the best match over ~90 candidate pitches every frame inflates the score
    (try enough pitches and something always fits): a multiple-comparisons trap.

v2 separates the two jobs:
  1. pitch first, by salience alone (no template): per frame, the f0 whose harmonics
     1-5 stand furthest above the song's usual level, fundamental required;
  2. then timbre at that one pitch: the overtone shape h2..h8 relative to h1 (kept
     below ~7 kHz, out of cymbal territory), plus how steady the pitch is over 60 ms;
  3. a nearest-centroid judge trained on labelled moments from Kham's ears
     (melodica vs. voice vs. guitar), tested on moments it never saw.

usage: timbre2.py AUDIO OUT_PREFIX
(labels are below, from Kham's calibration of Birdhouse (live), 2026-10-17/21)
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import proto as P
from timbre import spectrum, harmonic_levels, F0S

TRAIN = {"melodica": [(17.12, 17.70)],
         "voice":    [(77.0, 78.8)],             # John holding "soul"
         "guitar":   [(81.65, 82.6)]}            # guitar solo, back half of 1:21
TEST = {"melodica": [(80.43, 80.62), (80.74, 80.95), (81.04, 81.36)],   # the doots
        "voice":    [(79.0, 79.6)],                                      # end of "soul"
        "guitar":   [(82.7, 83.6)]}
NHF = 8


def features(f, D, W, sel):
    Hw = harmonic_levels(f, W[:, sel], F0S)
    sal = np.clip(Hw[:, :5], 0, 40).mean(1)            # (cands, frames)
    sal[np.clip(Hw[:, 0], 0, None) < 6] = 0            # fundamental must stand out
    c = sal.argmax(0)
    Hd = harmonic_levels(f, D[:, sel], F0S)
    fr = np.arange(len(c))
    stack = Hd[c, :NHF, fr]                            # (frames, NHF)
    rel = stack[:, 1:] - stack[:, :1]                  # h2..h8 relative to h1
    f0 = F0S[c]
    cents = 1200 * np.log2(f0)
    steady = np.array([np.std(cents[max(0, i - 3):i + 4]) for i in range(len(cents))])
    # envelope: does the stack hold (reed press, voice) or fade (pluck)? Level of the
    # chosen stack ~90 ms later at the *same* pitch, minus now, in dB. Lesson #4 (10-17).
    lvl = Hd[c, :3, fr].mean(1)
    later = np.array([Hd[c[i], :3, min(i + 8, len(c) - 1)].mean() for i in range(len(c))])
    decay = np.clip(later - lvl, -30, 10)
    feat = np.column_stack([rel, np.minimum(steady, 200) / 20.0, decay / 2.0])
    ok = sal.max(0) > 4
    return feat, f0, ok


def gather(f, t, D, W, spans):
    X = []
    for a, b in spans:
        sel = (t >= a) & (t < b)
        x, _, ok = features(f, D, W, sel)
        X.append(x[ok])
    return np.vstack(X)


def main():
    path, prefix = sys.argv[1], sys.argv[2]
    L, R = P.decode(path); mid = (L + R) / 2
    f, t, D = spectrum(mid)
    W = D - np.median(D, axis=1, keepdims=True)

    cent, spread = {}, {}
    for k, spans in TRAIN.items():
        X = gather(f, t, D, W, spans)
        cent[k] = np.median(X, 0); spread[k] = np.median(np.abs(X - cent[k]), 0) + 1.0
    scale = np.mean([spread[k] for k in cent], 0)          # shared per-feature scale
    names = list(cent)

    def judge(X):
        d = np.stack([np.sqrt((((X - cent[k]) / scale) ** 2).mean(1)) for k in names], 1)
        return d.argmin(1), d

    lines = ["# timbre lane v2: pitch by salience, timbre at that pitch, nearest-centroid judge",
             "centroids (h2..h8 rel. h1 in dB, pitch wobble/20 cents, level change over 90 ms /2 dB):"]
    for k in names:
        lines.append(f"- {k}: {np.round(cent[k], 1).tolist()}")
    lines.append("\n## held-out test (frames voted per span)")
    correct = total = 0
    for k, spans in TEST.items():
        for a, b in spans:
            sel = (t >= a) & (t < b)
            X, f0, ok = features(f, D, W, sel)
            if ok.sum() == 0:
                lines.append(f"- {a:.2f}-{b:.2f} truth {k}: no confident pitch"); continue
            lab, _ = judge(X[ok])
            votes = {n: int((lab == i).sum()) for i, n in enumerate(names)}
            win = max(votes, key=votes.get)
            correct += win == k; total += 1
            lines.append(f"- {a:.2f}-{b:.2f} s truth **{k}** -> {win} {votes}  pitch ~{P.note_label(np.median(f0[ok]))}")
    lines.append(f"\nspans right: {correct}/{total}")

    # lane picture over 76-83 s
    w0, w1 = 76.0, 83.0
    sel = (t >= w0) & (t < w1)
    X, f0, ok = features(f, D, W, sel)
    lab, d = judge(X)
    tt = t[sel]
    fig, ax = plt.subplots(len(names) + 1, 1, figsize=(13, 5), sharex=True)
    cols = {"melodica": "#3c9", "voice": "#e8a", "guitar": "#fb3"}
    for i, n in enumerate(names):
        conf = np.exp(-d[:, i]) / np.exp(-d).sum(1)
        conf[~ok] = 0
        ax[i].fill_between(tt, conf, color=cols.get(n, "#999"), lw=0)
        ax[i].set_ylim(0, 1); ax[i].set_yticks([]); ax[i].set_ylabel(n, fontsize=8)
    ax[-1].scatter(tt[ok], f0[ok], s=3, c=[cols[names[j]] for j in lab[ok]])
    ax[-1].set_yscale("log"); ax[-1].set_ylabel("pitch\n(colour = judge)", fontsize=7)
    ax[-1].set_xticks(np.arange(w0, w1 + 0.01, 0.5)); ax[-1].tick_params(labelsize=7)
    ax[0].set_title("timbre lane v2 | Birdhouse 76-83 s | lane height = how sure the judge is", fontsize=9)
    fig.tight_layout(); fig.savefig(prefix + ".png", dpi=100)
    txt = "\n".join(lines); open(prefix + ".md", "w").write(txt + "\n"); print(txt)


if __name__ == "__main__":
    main()
