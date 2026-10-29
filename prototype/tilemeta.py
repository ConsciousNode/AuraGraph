#!/usr/bin/env python3
"""
tilemeta.py: the AuraGraph tile container (v0.3).

A tile is an ordinary PNG, so any model, browser or person can open it. Inside it
is a small text chunk with the keyword "auragraph" holding JSON. The JSON says
what the pixels mean: which seconds the tile covers, which pitches, on what axis,
and how brightness maps to loudness. It carries the pinned notes later on.

That chunk is for the tools (AuraLoom uses it to put a clip back at the right
pitch and time). A model reading an uploaded tile only sees pixels, so anything
a model needs to know must also be drawn into the picture.

If a PNG has no chunk, the bounds can come from the filename instead:
    anything_t12.3-13.1_f200-800.aura.png  (seconds, Hz; "k" allowed: f1.2k-4k)

Tiles are named *.aura.png: still PNGs everywhere, easy to tell from other pictures.
Any picture can still be read; the extension is housekeeping, not a gate.

Fields (all optional except format and v):
    format  "auragraph-tile"
    v       "0.3"
    t0, t1  seconds covered, left edge of the first column to right edge of the last
    f0, f1  Hz at the bottom edge of the bottom row and the top edge of the top row
    axis    "log" (rows evenly spaced in log frequency); the only axis so far
    db      [lo, hi]: brightness 0 = lo dB, brightness 1 = hi dB (relative to the loud end)
    cmap    "magma8": the 8-stop magma AuraLoom and Paint-a-Tile draw with
    src     what made it; parent: the tile a clip was cut from; px: [x0, y0, x1, y1] of the cut
    notes   pinned notes (seed 10): see notes.py and the grid below

The grid (seed 10a): columns A-H run left to right across the tile's time, rows 1-8 run
bottom to top up its pitch (evenly in log frequency, like the rows). Each cell splits the
same way with lowercase letters, so "C6·d3" is cell C6, sub-cell d3. Add levels for finer
spots ("C6·d3·a8"). A reference always resolves to real seconds and Hz.
"""
import json, math, re
import numpy as np
from PIL import Image, PngImagePlugin

KEY = "auragraph"
EXT = ".aura.png"   # a tile is still a PNG; the double extension just makes tiles easy to spot
VERSION = "0.3"

# the same 8-stop magma as AuraLoom's LUT, so brightness round-trips exactly
_MAGMA8 = np.array([[0, 0, 4], [40, 11, 84], [101, 21, 110], [159, 42, 99], [212, 72, 66],
                    [245, 125, 21], [250, 193, 39], [252, 255, 164]], float)


def magma_lut():
    x = np.arange(256) / 255 * (len(_MAGMA8) - 1)
    k = np.minimum(np.floor(x).astype(int), len(_MAGMA8) - 2)
    t = (x - k)[:, None]
    return np.round(_MAGMA8[k] * (1 - t) + _MAGMA8[k + 1] * t).astype(np.uint8)


LUT = magma_lut()


def colorize(level):
    """level: 2-D array in 0..1, row 0 = lowest pitch. Returns an RGB image array, high pitch on top."""
    idx = np.clip(np.round(level * 255), 0, 255).astype(int)
    return LUT[idx][::-1]


def levels_of(rgb):
    """Inverse of colorize: RGB array (high pitch on top) -> 0..1 levels, row 0 = lowest pitch."""
    px = rgb[..., :3].reshape(-1, 3).astype(int)
    d = ((px[:, None, :] - LUT[None, :, :].astype(int)) ** 2).sum(-1)
    return (d.argmin(1) / 255).reshape(rgb.shape[:2])[::-1]


def bounds_from_name(name):
    m = {}
    t = re.search(r"_t(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)", name)
    f = re.search(r"_f(\d+(?:\.\d+)?)(k?)-(\d+(?:\.\d+)?)(k?)", name, re.I)
    if t:
        m["t0"], m["t1"] = float(t.group(1)), float(t.group(2))
    if f:
        m["f0"] = float(f.group(1)) * (1000 if f.group(2) else 1)
        m["f1"] = float(f.group(3)) * (1000 if f.group(4) else 1)
    return m


def read(path):
    """The tile's metadata: chunk first, filename as the fallback for anything missing."""
    meta = bounds_from_name(str(path))
    with Image.open(path) as im:
        raw = im.text.get(KEY) if hasattr(im, "text") else None
    if raw:
        meta.update(json.loads(raw))
    return meta


def save(rgb, path, meta):
    meta = {"format": "auragraph-tile", "v": VERSION, **meta}
    info = PngImagePlugin.PngInfo()
    info.add_text(KEY, json.dumps(meta, ensure_ascii=True, separators=(",", ":")))
    Image.fromarray(rgb).save(path, pnginfo=info)
    return meta


def name_bounds(t0, t1, f0, f1):
    """The filename suffix that carries the bounds, for when the chunk gets stripped."""
    return f"_t{t0:.2f}-{t1:.2f}_f{f0:.0f}-{f1:.0f}"


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(p, json.dumps(read(p), indent=1))


# ---- the grid: C6·d3 <-> seconds and Hz -------------------------------------------------
COLS = "abcdefgh"


def parse_ref(ref):
    """'C6·d3' -> [(2, 5), (3, 2)]: (column, row) per level, 0-based, row 0 at the bottom."""
    toks = re.findall(r"([A-Ha-h])\s*([1-8])", ref)
    if not toks or re.sub(r"[A-Ha-h]\s*[1-8]|[\s·.:/-]", "", ref):
        raise ValueError(f"not a grid reference: {ref!r} (like C6 or C6·d3)")
    return [(COLS.index(c.lower()), int(r) - 1) for c, r in toks]


def fmt_ref(levels):
    out = []
    for k, (c, r) in enumerate(levels):
        out.append((COLS[c].upper() if k == 0 else COLS[c]) + str(r + 1))
    return "·".join(out)


def ref_box(ref, m):
    """A grid reference -> (t0, t1, f0, f1) inside the tile whose bounds are in m."""
    lv = parse_ref(ref)
    n = 8 ** len(lv)
    ci = ri = 0
    for c, r in lv:
        ci, ri = ci * 8 + c, ri * 8 + r
    T0, T1, F0, F1 = m["t0"], m["t1"], m["f0"], m["f1"]
    t = lambda i: T0 + i / n * (T1 - T0)
    f = lambda j: F0 * (F1 / F0) ** (j / n)
    return t(ci), t(ci + 1), f(ri), f(ri + 1)


def point_ref(t, fz, m, levels=2):
    """seconds, Hz -> the grid reference of the cell holding that point."""
    n = 8 ** levels
    ci = min(n - 1, max(0, int((t - m["t0"]) / (m["t1"] - m["t0"]) * n)))
    ri = min(n - 1, max(0, int(math.log(fz / m["f0"]) / math.log(m["f1"] / m["f0"]) * n)))
    out = []
    for k in range(levels - 1, -1, -1):
        out.append(((ci // 8 ** k) % 8, (ri // 8 ** k) % 8))
    return fmt_ref(out)
