#!/usr/bin/env python3
"""
views.py: one sound, several ways of drawing it (seeds 11-14, for the legibility test).

Every view gets the same frame: the same size, margins, time ticks (seconds) and
pitch labels (each C, with Hz). Only the way loudness is drawn changes, plus the
grid lines in the grid view. That way a reading difference between views comes
from the drawing, not from one view having better labels.

  magma   brightness on the magma scale (the current AuraGraph default)
  gray    brightness only, black to white
  sharp   magma after edge sharpening: crisper onsets and harmonic lines
  slices  three loudness slices in three colour channels (seed 11):
          red = the loud top 20 dB, green = -20 to -45 dB, blue = -45 to -80 dB.
          Loud reads white, the body cyan, whispers and room blue.
  topo    contour bands of 10 dB each, in an ordered sequence of colours (seed 12),
          with a dark line where one band meets the next
  grid    magma with Kham's A-H x 1-8 grid burned in (seeds 10a, 14)

Usage: python3 views.py audio.wav out_prefix [--views magma,gray,...]
"""
import argparse, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
import tilemeta
from plain import tile_levels, DBR
from proto import decode, SR, HOP, NFFT, FMIN, FMAX, NBANDS

VIEWS = ["magma", "gray", "sharp", "slices", "topo", "grid"]
LEGEND = {
    "magma": "brightness = loudness (dark purple = quiet, yellow-white = loud)",
    "gray": "brightness = loudness (black = quiet, white = loud)",
    "sharp": "brightness = loudness (magma), edges sharpened",
    "slices": "colour = loudness range: deep blue = quiet (-80 to -45 dB), sky blue = middle (-45 to -20 dB), white = loud (top 20 dB)",
    "topo": "colour bands = 10 dB steps of loudness, in order: navy, blue, teal, green, olive, orange, red, white (loudest)",
    "grid": "brightness = loudness (magma); grid: columns A-H across time, rows 1-8 up pitch",
}
TOPO = np.array([[16, 18, 60], [33, 60, 140], [22, 120, 150], [40, 160, 90], [140, 170, 40],
                 [230, 150, 30], [220, 60, 40], [255, 255, 245]], np.uint8)


def font(n):
    try:
        return ImageFont.load_default(size=n)
    except TypeError:
        return ImageFont.load_default()


def paint(L, view):
    """L: levels 0..1 over DBR dB, row 0 = lowest pitch. Returns an RGB array, high pitch on top."""
    if view in ("magma", "grid"):
        return tilemeta.colorize(L)
    if view == "gray":
        g = np.clip(np.round(L * 255), 0, 255).astype(np.uint8)[::-1]
        return np.stack([g, g, g], -1)
    if view == "sharp":
        S = np.clip(L + 1.2 * (L - gaussian_filter(L, (1.0, 1.5))), 0, 1)
        return tilemeta.colorize(S)
    db = (L - 1) * DBR
    if view == "slices":
        r = np.clip((db + 20) / 20, 0, 1); g = np.clip((db + 45) / 25, 0, 1); b = np.clip((db + 80) / 35, 0, 1)
        return (np.stack([r, g, b], -1)[::-1] * 255).round().astype(np.uint8)
    if view == "topo":
        k = np.clip(((db + 80) // 10).astype(int), 0, 7)
        return TOPO[k][::-1]
    raise ValueError(view)


def frame(rgb, view, t0, t1, f0=FMIN, f1=FMAX, size=(900, 480), title=None):
    H, W = rgb.shape[:2]
    up = Image.fromarray(rgb).resize(size, Image.NEAREST)
    a = np.array(up)
    if view == "topo":                                    # dark contour lines where bands meet
        e = np.zeros(a.shape[:2], bool)
        same = lambda x, y: (x == y).all(-1)
        e[:, 1:] |= ~same(a[:, 1:], a[:, :-1]); e[1:, :] |= ~same(a[1:, :], a[:-1, :])
        a[e] = (a[e] * 0.35).astype(np.uint8)
        up = Image.fromarray(a)
    w, h = size
    Lm, Rm, Tm, Bm = 70, 24 if view != "grid" else 30, 26, 58
    c = Image.new("RGB", (w + Lm + Rm, h + Tm + Bm), (12, 12, 15))
    c.paste(up, (Lm, Tm))
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    F, S = font(13), font(11)
    X = lambda t: Lm + (t - t0) / (t1 - t0) * w
    Y = lambda f: Tm + h - math.log(f / f0) / math.log(f1 / f0) * h
    # time ticks: every 0.25 s small, every 1 s labelled
    t = math.ceil(t0 * 4) / 4
    while t <= t1 + 1e-9:
        major = abs(t - round(t)) < 1e-6
        d.line([(X(t), Tm + h), (X(t), Tm + h + (7 if major else 3))], fill=(210, 210, 210, 255))
        if major:
            d.text((X(t), Tm + h + 9), f"{t:.0f} s", fill=(220, 220, 220, 255), font=S, anchor="ma")
        t += 0.25
    # pitch labels at every C
    for octv in range(1, 10):
        fz = 440 * 2 ** ((12 * (octv + 1) - 69) / 12)
        if f0 <= fz <= f1:
            d.line([(Lm - 6, Y(fz)), (Lm, Y(fz))], fill=(210, 210, 210, 255))
            lab = f"C{octv} {fz:.0f}" if fz < 1000 else f"C{octv} {fz / 1000:.1f}k"
            d.text((Lm - 8, Y(fz)), lab, fill=(220, 220, 220, 255), font=S, anchor="rm")
    if view == "grid":
        for i in range(9):
            x = Lm + i / 8 * w; y = Tm + h - i / 8 * h
            d.line([(x, Tm), (x, Tm + h)], fill=(255, 255, 255, 120)); d.line([(Lm, y), (Lm + w, y)], fill=(255, 255, 255, 120))
        for k in range(8):
            d.text((Lm + (k + 0.5) / 8 * w, 6), "ABCDEFGH"[k], fill=(235, 235, 235, 255), font=F, anchor="ma")
            d.text((Lm + w + 15, Tm + h - (k + 0.5) / 8 * h), str(k + 1), fill=(235, 235, 235, 255), font=F, anchor="mm")
    if title:
        d.text((Lm, 6), title, fill=(235, 235, 235, 255), font=F) if view != "grid" else None
    d.text((Lm, Tm + h + 28), "time: left to right   pitch: bottom to top (log)   " + LEGEND[view], fill=(190, 190, 190, 255), font=S)
    return Image.alpha_composite(c.convert("RGBA"), ov).convert("RGB")


def render(audio, view, title=None):
    Lc, Rc = decode(audio)
    L = tile_levels((Lc + Rc) / 2)
    dt = HOP / SR; t0 = (NFFT / 2) / SR - dt / 2; t1 = t0 + L.shape[1] * dt
    return frame(paint(L, view), view, t0, t1, title=title)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("prefix")
    ap.add_argument("--views", default=",".join(VIEWS))
    a = ap.parse_args()
    for v in a.views.split(","):
        out = f"{a.prefix}_{v}.png"; render(a.audio, v).save(out); print(out)
