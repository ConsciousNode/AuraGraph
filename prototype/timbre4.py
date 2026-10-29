#!/usr/bin/env python3
"""AuraGraph timbre judge v4 (Kehai Interim, 2026-10-21).

Same features as v3 (salience pitch, harmonics 2..8 relative to the 1st, optional pan mask),
now with Kham's full label set (labels_birdhouse.py) and an honest test:
**leave-one-span-out**. For every labelled span, train on all *other* spans, then judge it.
Two training regimes:
  in-song   : Birdhouse labels only
  in-song + : plus the clean references, re-mixed toward the live sound (see below)

"Re-mixing toward the live sound": v3 showed that clean solo recordings have steep overtone
fall-off while everything in the live mix is flatter. Here each clean frame's harmonic levels
are floored at the live mix's typical noise floor for that harmonic (what a crowded room
would add), so the judge can't tell the two worlds apart by fall-off alone.

usage: timbre4.py BIRDHOUSE REFDIR OUT_PREFIX
"""
import sys
import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import proto as P
from timbre3 import spec_lr, feats
import labels_birdhouse as LB

REFS = {"accordion": [("accordion_bach.wav", 5, 95)],
        "guitar": [("guitar_clean_soft_solo.wav", 0.5, 16), ("guitar_distorted_metal_riff.wav", 0.5, 18.5)],
        "voice": [("voice_exsultet_pl.ogg", 2, 120)]}


def spans():
    out = []
    for k, (a, b, v, w) in LB.VOICE.items(): out.append(("voice", k, a, b, None))
    for k, (a, b, s, w) in LB.GUITAR.items(): out.append(("guitar", k, a, b, s))
    for k, (a, b, s, w) in LB.ACCORDION.items(): out.append(("accordion", k, a, b, s))
    for k, (a, b, s, w) in LB.KEYBOARD.items(): out.append(("keyboard", k, a, b, s))
    return out


def fit(X):
    mu = np.median(X, 0); sd = 1.4826 * np.median(np.abs(X - mu), 0) + 1.5
    return mu, sd


def judge(X, model):
    names = list(model)
    ll = np.stack([(-0.5 * ((X - model[k][0]) / model[k][1]) ** 2 - np.log(model[k][1])).sum(1) for k in names], 1)
    v = ll.argmax(1)
    votes = {n: int((v == i).sum()) for i, n in enumerate(names)}
    return max(votes, key=votes.get), votes


def main():
    bird, refdir, prefix = sys.argv[1:4]
    B = spec_lr(bird)
    S = spans()
    data = {s[1]: feats(*B, s[2], s[3], s[4])[0] for s in S}
    floor = np.percentile(np.vstack(list(data.values())), 10, axis=0)   # live mix's low end per harmonic

    ref = {}
    for cls, items in REFS.items():
        Xs = []
        for fn, a, b in items:
            X = feats(*spec_lr(f"{refdir}/{fn}"), a, b)[0]
            Xs.append(np.maximum(X, floor))
        ref[cls] = np.vstack(Xs)

    lines = ["# timbre judge v4: leave-one-span-out on Kham's Birdhouse labels", ""]
    for regime in ("in-song", "in-song + refs"):
        right = 0; rows = []
        for cls, name, a, b, side in S:
            model = {}
            for c in sorted({s[0] for s in S}):
                parts = [data[s[1]] for s in S if s[0] == c and s[1] != name]
                if regime != "in-song" and c in ref: parts.append(ref[c])
                parts = [p for p in parts if len(p)]
                if parts: model[c] = fit(np.vstack(parts))
            X = data[name]
            if len(X) == 0:
                rows.append(f"- {cls}/{name}: no confident pitch"); continue
            if cls not in model:
                rows.append(f"- {cls}/{name}: only example of its class, can't be tested"); continue
            win, votes = judge(X, model)
            right += win == cls
            rows.append(f"- {cls}/{name} -> {'**' + win + '**' if win == cls else win + ' ✗'} {votes}")
        testable = sum(1 for s in S if sum(1 for t in S if t[0] == s[0]) > 1 and len(data[s[1]]))
        lines += [f"## {regime}: {right}/{testable} spans right", *rows, ""]
    txt = "\n".join(lines); open(prefix + ".md", "w").write(txt + "\n"); print(txt)


if __name__ == "__main__":
    main()
