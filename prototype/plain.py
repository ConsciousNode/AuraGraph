#!/usr/bin/env python3
"""
plain.py: audio -> a plain AuraGraph tile (no axes, no panels) with its bounds inside.

The panelled tiles from proto.py are for reading. This one is the raw material:
one pixel column per STFT frame, 160 log-spaced rows from 30 Hz to 11 kHz, magma
brightness over 80 dB. AuraLoom and Paint-a-Tile can play it back, and clip.py
can cut pieces out of it that still know where they came from.

Usage:
  python3 plain.py song.ogg [out.png] [--start S] [--dur D]
"""
import argparse, os
import numpy as np
from proto import decode, spec, logbands, tobands, db, SR, HOP, NFFT, FMIN, FMAX, NBANDS
import tilemeta

DBR = 80.0


def tile_levels(x):
    f, _, M = spec(x)
    _, idx = logbands(f)
    B = tobands(M, idx)
    ref = np.percentile(B, 99.7) or 1.0
    return np.clip(1 + db(B, ref) / DBR, 0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--dur", type=float, default=None)
    a = ap.parse_args()
    L, R = decode(a.audio)
    x = (L + R) / 2
    s0 = int(a.start * SR)
    x = x[s0: s0 + int(a.dur * SR)] if a.dur else x[s0:]
    lev = tile_levels(x)
    dt = HOP / SR
    # column c is centred on (NFFT/2 + c*HOP)/SR, so it covers half a hop either side of that
    t0 = a.start + (NFFT / 2) / SR - dt / 2
    t1 = t0 + lev.shape[1] * dt
    out = a.out or os.path.splitext(os.path.basename(a.audio))[0] + "_plain" + tilemeta.name_bounds(t0, t1, FMIN, FMAX) + tilemeta.EXT
    meta = tilemeta.save(tilemeta.colorize(lev), out, {
        "t0": round(t0, 4), "t1": round(t1, 4), "f0": FMIN, "f1": FMAX, "axis": "log",
        "bands": NBANDS, "db": [-DBR, 0], "cmap": "magma8", "sr": SR, "hop": HOP,
        "src": "plain.py:" + os.path.basename(a.audio)})
    print(out, lev.shape[1], "columns x", NBANDS, "bands,", f"{meta['t0']}-{meta['t1']} s")


if __name__ == "__main__":
    main()
