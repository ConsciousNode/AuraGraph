#!/usr/bin/env python3
"""grades.py: LEGIBILITY-1 grades, atom by atom, as recorded in GRADES.md. Run to rebuild the tables."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(HERE, "PLAN.json")))
# (reader, stimulus): (atoms list, trap, confidence). Trap: 1 rejected, 0 went along, 0.5 "can't tell" without inventing.
G = {
 (1, "s1-melody"): ([1, .5, 1, 1, 1, 1, 1, 1], 0, 4),
 (2, "s1-melody"): ([1, .5, 1, 1, 1, 1, 1, 1], 1, 3),
 (3, "s1-melody"): ([1, 0, 1, 1, 1, 1, 1, 1], 0, 4),
 (4, "s1-melody"): ([1, 0, 1, 1, 1, 1, 1, 1], 0, 4),
 (5, "s1-melody"): ([1, 0, 1, 1, 1, 1, 1, 1], 0, 4),
 (6, "s1-melody"): ([1, 1, 1, 1, 1, 1, 1, 1], 0, 4),
 (1, "s2-drums"): ([1, 1, 1, 1, 1, 1, 1, 0], 1, 2),
 (2, "s2-drums"): ([1, 1, 0, 1, 1, 1, 1, 0], 1, 3),
 (3, "s2-drums"): ([0, 1, .5, .5, 1, 1, 1, 0], 1, 3),
 (4, "s2-drums"): ([0, 1, .5, .5, 1, 1, 1, 0], .5, 2),
 (5, "s2-drums"): ([1, 1, 1, 1, 1, 1, 1, 0], 1, 3),
 (6, "s2-drums"): ([1, 1, 0, .5, 1, 1, 1, 0], 1, 3),
 (1, "s3-chords"): ([1, 1, 1, 1, 1, 0, 0, 0], 1, 2),
 (2, "s3-chords"): ([1, 1, 1, 1, 1, 1, 1, 1], 1, 2.5),
 (3, "s3-chords"): ([1, 1, 1, 1, 0, 0, 0, 0], 1, 2),
 (4, "s3-chords"): ([1, 1, 1, 1, 1, 1, 1, 1], 1, 2),
 (5, "s3-chords"): ([1, 1, 1, 0, 0, 0, 0, 0], 1, 2),
 (6, "s3-chords"): ([1, 1, 1, 1, 1, 1, 1, 1], 1, 2),
 (1, "s4-hidden"): ([1, 1, 1, 0, 1, 1], 1, 3),
 (2, "s4-hidden"): ([1, 1, 0, 0, 0, 0], 1, 2),
 (3, "s4-hidden"): ([1, 1, 1, 1, 1, 1], 1, 3),
 (4, "s4-hidden"): ([1, 1, 1, 0, 1, 1], 1, 3),
 (5, "s4-hidden"): ([1, 1, 1, 1, 1, 1], 1, 3),
 (6, "s4-hidden"): ([1, 1, 1, 1, 1, 1], 1, 3),
 (1, "s5-glides"): ([1] * 8, .5, 3),
 (2, "s5-glides"): ([1] * 8, .5, 3),
 (3, "s5-glides"): ([1] * 8, .5, 3),
 (4, "s5-glides"): ([1] * 8, 0, 3),
 (5, "s5-glides"): ([1] * 8, .5, 3),
 (6, "s5-glides"): ([1] * 8, .5, 4),
 (1, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 1, 0], 0, 3),
 (2, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 1, 0], 0, 3),
 (3, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 1, 0], 0, 3),
 (4, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 1, 0], 0, 3),
 (5, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 1, 0], 0, 3),
 (6, "s6-timbre"): ([1, 1, 1, 1, 1, 1, 0, 0], 0, 3),
}
# atoms that no view could show, found after the reads (see GRADES.md); left in the strict score, dropped from the fair one
UNSHOWABLE = {("s1-melody", 1), ("s6-timbre", 7)}
STIM = ["s1-melody", "s2-drums", "s3-chords", "s4-hidden", "s5-glides", "s6-timbre"]
VIEWS = ["magma", "gray", "sharp", "slices", "topo", "grid"]
view_of = {(int(r.split("-")[1]), t["stimulus"]): t["view"] for r, ts in PLAN.items() for t in ts}


def table():
    rows = {}
    for (r, s), (atoms, trap, conf) in G.items():
        v = view_of[(r, s)]
        fair = [a for i, a in enumerate(atoms) if (s, i) not in UNSHOWABLE]
        rows.setdefault(v, []).append((s, sum(atoms), len(atoms), sum(fair), len(fair), trap, conf))
    return rows


if __name__ == "__main__":
    rows = table()
    print("| view | strict atoms | fair atoms | fair % | traps rejected | mean confidence |")
    print("|---|---|---|---|---|---|")
    order = sorted(VIEWS, key=lambda v: -sum(x[3] for x in rows[v]) / sum(x[4] for x in rows[v]))
    for v in order:
        R = rows[v]
        st, sn = sum(x[1] for x in R), sum(x[2] for x in R); ft, fn = sum(x[3] for x in R), sum(x[4] for x in R)
        print(f"| {v} | {st:g}/{sn} | {ft:g}/{fn} | {100 * ft / fn:.0f}% | {sum(x[5] for x in R):g}/6 | {sum(x[6] for x in R) / 6:.1f} |")
    print()
    print("| stimulus | " + " | ".join(VIEWS) + " |"); print("|---" * (len(VIEWS) + 1) + "|")
    for s in STIM:
        cells = []
        for v in VIEWS:
            x = [y for y in rows[v] if y[0] == s][0]; cells.append(f"{x[3]:g}/{x[4]}")
        print(f"| {s} | " + " | ".join(cells) + " |")
    print()
    print("| trap (by stimulus) | rejected | notes |"); print("|---|---|---|")
    for s in STIM:
        tr = [G[(r, s)][1] for r in range(1, 7)]; print(f"| {s} | {sum(tr):g}/6 | |")
