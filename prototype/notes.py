#!/usr/bin/env python3
"""
notes.py: pinned notes on a tile (seed 10), both directions.

Human -> model: "cowbell here", "she breathes", "the bass drops out".
Model -> human: "voice or synth?", "what's this smear at 3 kHz?"

Each note is pinned to a grid spot (C6·d3: cell C6, sub-cell d3) and always carries
the real seconds and Hz of that spot, so "C6·d3" and "12.3 s around A4" always agree.
Notes live in the tile's auragraph chunk, travel with it into AuraLoom and back, and
can be printed as a markdown sidecar for when the chunk can't travel (chat uploads).

Usage:
  notes.py TILE                              list the notes
  notes.py TILE add C6·d3 "text" [--by Kehai] [--kind note|question|answer] [--re N]
  notes.py TILE add --at 12.3 440 "text"     pin at seconds + Hz instead of a reference
  notes.py TILE rm N
  notes.py TILE md                           a markdown sidecar
  notes.py TILE grid [out.png]               a copy with the grid, bounds and pins drawn in,
                                             for models, who only see pixels
"""
import argparse, datetime, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tilemeta


def hz(f):
    return f"{f / 1000:.2f} kHz" if f >= 1000 else f"{f:.0f} Hz"


def note_name(f):
    m = 69 + 12 * math.log2(f / 440)
    r = round(m)
    return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][r % 12] + str(r // 12 - 1)


def where(n):
    cell = f"{n['t0']:.2f}–{n['t1']:.2f} s, {hz(n['f0'])}–{hz(n['f1'])}"
    if n.get("pt"):                                    # the exact spot, when it was pinned by clicking
        return cell + f" · at {n['pt'][0]:.2f} s, {hz(n['pt'][1])} ({note_name(n['pt'][1])})"
    return cell + f" (~{note_name(math.sqrt(n['f0'] * n['f1']))})"


def load(path):
    m = tilemeta.read(path)
    if not all(k in m for k in ("t0", "t1", "f0", "f1")):
        raise SystemExit("this tile doesn't know its bounds, so its grid can't be resolved")
    return m


def save(path, m):
    im = Image.open(path)
    arr = np.array(im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"))
    keep = {k: v for k, v in m.items() if k not in ("format", "v")}
    tilemeta.save(arr, path, keep)


def line(n):
    re_ = f" (re #{n['re']})" if n.get("re") else ""
    return f"#{n['n']} {n['ref']} [{n.get('kind', 'note')}{re_}, {n.get('by', '?')}]: {n['text']}\n      {where(n)}"


def grid_copy(path, m, out):
    rgb = np.array(Image.open(path).convert("RGB"))
    H, W = rgb.shape[:2]
    sx = max(1, math.ceil(900 / W)); sy = max(2, math.ceil(480 / H))
    big = Image.fromarray(rgb).resize((W * sx, H * sy), Image.NEAREST)
    w, h = big.size
    L, R, T, B = 34, 34, 24, 46
    canvas = Image.new("RGB", (w + L + R, h + T + B), (12, 12, 15))
    canvas.paste(big, (L, T))
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    try:
        font = ImageFont.load_default(size=13); small = ImageFont.load_default(size=10)
    except TypeError:
        font = small = ImageFont.load_default()
    for i in range(65):
        x = L + i / 64 * w; y = T + h - i / 64 * h
        major = i % 8 == 0
        if major or (w / 64 >= 10):
            d.line([(x, T), (x, T + h)], fill=(255, 255, 255, 110 if major else 28), width=1)
        if major or (h / 64 >= 10):
            d.line([(L, y), (L + w, y)], fill=(255, 255, 255, 110 if major else 28), width=1)
        d.line([(x, T - (6 if major else 3)), (x, T)], fill=(200, 200, 200, 255))
        d.line([(L - (6 if major else 3), y), (L, y)], fill=(200, 200, 200, 255))
    for k in range(8):
        cx = L + (k + 0.5) / 8 * w; cy = T + h - (k + 0.5) / 8 * h
        for yy in (2, T + h + 3):
            d.text((cx, yy), "ABCDEFGH"[k], fill=(230, 230, 230, 255), font=font, anchor="ma")
        d.text((L / 2, cy), str(k + 1), fill=(230, 230, 230, 255), font=font, anchor="mm")
        d.text((L + w + R / 2, cy), str(k + 1), fill=(230, 230, 230, 255), font=font, anchor="mm")
    spots = {}
    for n in m.get("notes", []):                       # notes on the same spot share one box and label
        spots.setdefault((n["t0"], n["t1"], n["f0"], n["f1"]), []).append(n)
    for (t0, t1, f0, f1), group in spots.items():
        x0 = L + (t0 - m["t0"]) / (m["t1"] - m["t0"]) * w; x1 = L + (t1 - m["t0"]) / (m["t1"] - m["t0"]) * w
        lg = lambda f: T + h - math.log(f / m["f0"]) / math.log(m["f1"] / m["f0"]) * h
        y0, y1 = lg(f1), lg(f0)
        q = any(n.get("kind") == "question" for n in group) and not any(n.get("kind") == "answer" for n in group)
        col = (250, 193, 39, 255) if q else (103, 232, 249, 255)
        d.rectangle([x0, y0, max(x1, x0 + 3), max(y1, y0 + 3)], outline=col, width=2)
        d.text((x0 + 2, y0 - 2), "#" + ",".join(str(n["n"]) for n in group), fill=col, font=font, anchor="lb")
    cap = (f"t {m['t0']:.2f}-{m['t1']:.2f} s (A-H, 8 cols; a-h inside)   f {hz(m['f0'])}-{hz(m['f1'])} log (1-8 up; 1-8 inside)"
           f"   bright = loud")
    d.text((L, T + h + 22), cap, fill=(190, 190, 190, 255), font=small)
    Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB").save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tile")
    ap.add_argument("cmd", nargs="?", default="list", choices=["list", "add", "rm", "md", "grid"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--at", nargs=2, type=float, metavar=("SECONDS", "HZ"))
    ap.add_argument("--by", default="Kehai")
    ap.add_argument("--kind", default="note", choices=["note", "question", "answer"])
    ap.add_argument("--re", type=int)
    ap.add_argument("--levels", type=int, default=2)
    a = ap.parse_args()
    m = load(a.tile)
    notes = m.setdefault("notes", [])

    if a.cmd == "list":
        print(f"{os.path.basename(a.tile)}: {m['t0']:.2f}–{m['t1']:.2f} s, {hz(m['f0'])}–{hz(m['f1'])}, {len(notes)} note(s)")
        for n in notes:
            print(line(n))
    elif a.cmd == "add":
        if a.at:
            ref, text = tilemeta.point_ref(a.at[0], a.at[1], m, a.levels), " ".join(a.args)
        else:
            if len(a.args) < 2:
                raise SystemExit('add needs a reference and text: add C6·d3 "text"')
            ref, text = tilemeta.fmt_ref(tilemeta.parse_ref(a.args[0])), " ".join(a.args[1:])
        t0, t1, f0, f1 = tilemeta.ref_box(ref, m)
        n = {"n": max([x["n"] for x in notes], default=0) + 1, "ref": ref, "t0": round(t0, 4), "t1": round(t1, 4),
             "f0": round(f0, 2), "f1": round(f1, 2), "by": a.by, "kind": a.kind, "text": text,
             "when": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}
        if a.re:
            n["re"] = a.re
        if a.at:
            n["pt"] = [round(a.at[0], 3), round(a.at[1], 1)]
        notes.append(n)
        save(a.tile, m)
        print("pinned", line(n))
    elif a.cmd == "rm":
        k = int(a.args[0])
        m["notes"] = [x for x in notes if x["n"] != k]
        save(a.tile, m)
        print("removed #%d" % k)
    elif a.cmd == "md":
        print(f"# Notes on {os.path.basename(a.tile)}\n")
        print(f"Tile: {m['t0']:.2f}–{m['t1']:.2f} s, {hz(m['f0'])}–{hz(m['f1'])}. Grid: A–H left to right, 1–8 bottom to top; sub-cells a–h, 1–8.\n")
        for n in notes:
            re_ = f", re #{n['re']}" if n.get("re") else ""
            print(f"- **#{n['n']} {n['ref']}** ({n.get('kind', 'note')}, {n.get('by', '?')}{re_}) — {where(n)}: {n['text']}")
    elif a.cmd == "grid":
        out = a.args[0] if a.args else os.path.basename(a.tile).replace(tilemeta.EXT, "").replace(".png", "") + "_grid.png"
        print(grid_copy(a.tile, m, out))


if __name__ == "__main__":
    main()
