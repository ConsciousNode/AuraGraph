#!/usr/bin/env python3
"""
plain.py: audio -> a plain AuraGraph tile (no axes, no panels) with its bounds inside.

The panelled tiles from proto.py are for reading. This one is the raw material:
one pixel column per STFT frame, 160 log-spaced rows from 30 Hz to 11 kHz, magma
brightness over 80 dB. AuraLoom and Paint-a-Tile can play it back, and clip.py
can cut pieces out of it that still know where they came from.

Two analyses:
  v1  the one LEGIBILITY-1 tested: one 2048-point FFT for every band, a fixed 80 dB range
  v2  (default) the AuraGraph app's: bands too narrow for a 2048-point bin (below ~290 Hz) are read
      from a 4096-point FFT centred on the same moment, so the bass rows mostly stop copying each
      other (8192 was tried: cleaner bass, but kick drums smeared into blobs); and the range follows the recording: from the loud end down to its 15th-percentile
      level (its noise floor), kept between 40 and 80 dB, so a room's hiss goes near-black instead of
      mid-gray. Silent-background audio still gets the full 80 dB, exactly as v1.

Usage:
  python3 plain.py song.ogg [out.png] [--start S] [--dur D] [--v1]
"""
import argparse, os
import numpy as np
from scipy.signal import stft
from proto import decode, spec, logbands, tobands, db, SR, HOP, NFFT, FMIN, FMAX, NBANDS
import tilemeta

DBR = 80.0
SIZES = (2048, 4096)                # v2: the FFT sizes a band can be read from. 8192 was tried and dropped:
                                    # it turned kick drums into blobs (0.37 s of smear); 4096 keeps their sweep
RANGE_PCT, RANGE_MIN, RANGE_MAX = 15, 40.0, 80.0


def band_plan():
    """v2: for each band, the smallest FFT whose bin fits inside it, and the bins it averages."""
    edges = np.geomspace(FMIN, FMAX, NBANDS + 1)
    plan = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        n = next((n for n in SIZES if hi - lo >= SR / n), SIZES[-1])
        k = np.arange(n // 2 + 1) * SR / n
        ks = np.where((k >= lo) & (k < hi))[0]
        if not len(ks):
            ks = np.array([int(round(np.sqrt(lo * hi) / (SR / n)))])
        plan.append((n, ks))
    return plan


def levels_v2(x):
    """Returns (levels 0..1, the dB range used). Frame c is centred on sample NFFT/2 + c*HOP for every FFT size."""
    F = (len(x) - NFFT) // HOP + 1
    mags = {}
    for n in SIZES:
        pad = (n - NFFT) // 2
        xp = np.concatenate([np.zeros(pad), x, np.zeros(pad)])
        _, _, Z = stft(xp, fs=SR, nperseg=n, noverlap=n - HOP, boundary=None, padded=False)   # 'spectrum' scaling: / sum(window)
        mags[n] = np.abs(Z)[:, :F]
    B = np.stack([mags[n][ks].mean(axis=0) for n, ks in band_plan()])
    ref = np.percentile(B, 99.7) or 1.0
    d = db(B, ref)
    rng = float(np.clip(-np.percentile(d, RANGE_PCT), RANGE_MIN, RANGE_MAX))
    return np.clip(1 + d / rng, 0, 1), rng


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
    ap.add_argument("--v1", action="store_true", help="the LEGIBILITY-1 analysis (one FFT size, fixed 80 dB)")
    a = ap.parse_args()
    L, R = decode(a.audio)
    x = (L + R) / 2
    s0 = int(a.start * SR)
    x = x[s0: s0 + int(a.dur * SR)] if a.dur else x[s0:]
    if a.v1:
        lev, rng, ana = tile_levels(x), DBR, "v1"
    else:
        (lev, rng), ana = levels_v2(x), "v2"
    dt = HOP / SR
    # column c is centred on (NFFT/2 + c*HOP)/SR, so it covers half a hop either side of that
    t0 = a.start + (NFFT / 2) / SR - dt / 2
    t1 = t0 + lev.shape[1] * dt
    out = a.out or os.path.splitext(os.path.basename(a.audio))[0] + "_plain" + tilemeta.name_bounds(t0, t1, FMIN, FMAX) + tilemeta.EXT
    meta = tilemeta.save(tilemeta.colorize(lev), out, {
        "t0": round(t0, 4), "t1": round(t1, 4), "f0": FMIN, "f1": FMAX, "axis": "log",
        "bands": NBANDS, "db": [-round(rng, 1), 0], "cmap": "magma8", "sr": SR, "hop": HOP, "analysis": ana,
        "src": "plain.py:" + os.path.basename(a.audio)})
    print(out, lev.shape[1], "columns x", NBANDS, "bands,", f"{meta['t0']}-{meta['t1']} s")


if __name__ == "__main__":
    main()
