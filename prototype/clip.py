#!/usr/bin/env python3
"""
clip.py: cut a piece out of a plain tile, and the piece remembers where it was.

Seed 9: when part of a tile is hard to parse, the reader cuts just that part and
hands it to a human, who plays it in AuraLoom. A clip has to carry its own bounds,
or AuraLoom would stretch it over the full 30 Hz - 11 kHz and every note would land
on the wrong pitch. So the cut snaps to whole pixels, and the clip records the exact
seconds and Hz of the pixels it really holds: in its chunk and in its filename.
A clip of a clip works the same way.

Usage:
  python3 clip.py tile.png --t 12.3 13.1 [--f 200 800] [-o out.png]
  (the source's bounds come from its chunk or filename; --src-t / --src-f override)
"""
import argparse, math, os, re
import numpy as np
from PIL import Image
import tilemeta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tile")
    ap.add_argument("--t", nargs=2, type=float, required=True, metavar=("T0", "T1"))
    ap.add_argument("--f", nargs=2, type=float, metavar=("F0", "F1"))
    ap.add_argument("--src-t", nargs=2, type=float)
    ap.add_argument("--src-f", nargs=2, type=float)
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    m = tilemeta.read(a.tile)
    if a.src_t: m["t0"], m["t1"] = a.src_t
    if a.src_f: m["f0"], m["f1"] = a.src_f
    if "t0" not in m or "f0" not in m:
        raise SystemExit("the source tile doesn't say its bounds (no chunk, no _t/_f in the name); pass --src-t and --src-f")
    T0, T1, F0, F1 = m["t0"], m["t1"], m["f0"], m["f1"]
    rgb = np.array(Image.open(a.tile).convert("RGB"))
    H, W = rgb.shape[:2]

    t0, t1 = max(a.t[0], T0), min(a.t[1], T1)
    f0, f1 = a.f if a.f else (F0, F1)
    f0, f1 = max(f0, F0), min(f1, F1)
    if not (t1 > t0 and f1 > f0):
        raise SystemExit("that range is outside the tile")
    # snap outward to whole pixels, then report the bounds of those pixels exactly
    x0 = math.floor((t0 - T0) / (T1 - T0) * W); x1 = math.ceil((t1 - T0) / (T1 - T0) * W)
    lg = lambda f: math.log(f / F0) / math.log(F1 / F0) * H          # rows up from the bottom
    b0 = max(0, math.floor(lg(f0) + 1e-9)); b1 = min(H, math.ceil(lg(f1) - 1e-9))
    ct0 = T0 + x0 / W * (T1 - T0); ct1 = T0 + x1 / W * (T1 - T0)
    cf0 = F0 * (F1 / F0) ** (b0 / H); cf1 = F0 * (F1 / F0) ** (b1 / H)
    piece = rgb[H - b1: H - b0, x0:x1]

    stem = os.path.basename(a.tile)
    stem = stem[:-len(tilemeta.EXT)] if stem.endswith(tilemeta.EXT) else os.path.splitext(stem)[0]
    stem = re.sub(r"_t\d+(?:\.\d+)?-\d.*$", "", stem)   # drop the old bounds suffix
    out = a.out or f"{stem}_clip{tilemeta.name_bounds(ct0, ct1, cf0, cf1)}{tilemeta.EXT}"
    keep = {k: m[k] for k in ("axis", "db", "cmap", "sr", "hop") if k in m}
    meta = tilemeta.save(np.ascontiguousarray(piece), out, {
        **keep, "t0": round(ct0, 4), "t1": round(ct1, 4), "f0": round(cf0, 3), "f1": round(cf1, 3),
        "bands": b1 - b0, "src": "clip.py", "parent": os.path.basename(a.tile), "px": [x0, H - b1, x1, H - b0]})
    print(out, f"{x1 - x0}x{b1 - b0} px,", f"{meta['t0']}-{meta['t1']} s,", f"{meta['f0']}-{meta['f1']} Hz")


if __name__ == "__main__":
    main()
