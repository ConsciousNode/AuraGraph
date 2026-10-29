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
    notes   pinned notes (coming next)
"""
import json, re
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
