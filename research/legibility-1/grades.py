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

S = {"s1": "s1-melody", "s2": "s2-drums", "s3": "s3-chords", "s4": "s4-hidden", "s5": "s5-glides", "s6": "s6-timbre"}
def _f(rows):
    return {(p, S[k]): (a, t, c) for p, k, a, t, c in rows}
z = [0] * 8
GROK = _f([
 (1,"s3",[1,1,0,0,0,0,0,0],0,4), (1,"s5",[1,0,1,1,1,0,0,1],0,4), (1,"s2",z,1,3), (1,"s6",[0,0,0,1,1,0,0,0],0,4), (1,"s1",[1,0,0,0,0,1,1,0],0,4), (1,"s4",[1,1,0,0,0,0],1,5),
 (2,"s4",[1,1,0,0,0,0],1,4), (2,"s5",[1,0,1,1,1,0,0,1],.5,3), (2,"s3",[1,1,1,0,0,0,0,0],1,4), (2,"s6",[0,0,0,0,1,0,0,0],0,4), (2,"s2",z,1,3), (2,"s1",[1,0,0,0,0,1,1,0],0,3.5),
 (3,"s2",[1,0,0,0,0,0,0,0],1,4), (3,"s3",[1,1,1,0,0,0,0,0],1,4), (3,"s1",[1,0,0,0,0,1,1,0],0,4), (3,"s4",[1,1,0,0,0,0],1,5), (3,"s6",[0,0,0,1,1,0,0,0],0,4), (3,"s5",[0,0,1,0,0,0,0,0],.5,3),
 (4,"s6",[1,0,0,0,1,0,0,0],0,4), (4,"s2",z,1,3), (4,"s1",[1,0,0,0,1,1,1,0],0,3), (4,"s3",[1,0,1,0,0,0,0,0],1,3), (4,"s5",[0,0,0,1,0,1,0,0],0,3), (4,"s4",[1,1,0,0,0,0],.5,4),
 (5,"s3",[1,1,1,1,0,0,0,0],1,4), (5,"s6",[0,0,0,1,1,0,0,0],0,4), (5,"s5",z,0,3), (5,"s2",[0,0,0,.5,0,0,0,0],0,3), (5,"s1",[1,0,0,0,1,1,1,1],0,4), (5,"s4",[1,1,0,0,0,0],.5,5),
 (6,"s1",[1,0,0,0,1,1,1,0],0,3), (6,"s2",z,1,4), (6,"s3",[1,1,1,0,0,0,0,0],1,4), (6,"s5",[0,0,0,1,0,0,0,0],0,4), (6,"s6",[0,0,1,0,1,0,0,0],.5,4), (6,"s4",[1,1,0,0,0,0],.5,5)])
DEEPSEEK = _f([
 (1,"s3",z,0,2), (1,"s5",z,0,2), (1,"s2",z,0,3), (1,"s6",[0,0,0,0,1,0,0,0],0,3), (1,"s1",z,0,3), (1,"s4",[0]*6,0,3),
 (2,"s4",[1,0,0,0,0,0],1,2), (2,"s5",[1,0,1,1,1,0,0,0],0,4), (2,"s3",[1,1,1,1,0,0,0,0],1,4), (2,"s6",[0,0,0,1,1,0,0,0],0,4), (2,"s2",z,0,3), (2,"s1",[1,0,0,0,0,1,1,0],0,5),
 (3,"s2",z,0,3), (3,"s3",[0,0,1,0,0,1,0,0],0,4), (3,"s1",[0,0,0,0,0,1,1,0],0,3), (3,"s4",[1,1,0,0,0,0],1,3), (3,"s6",[0,0,0,1,1,0,0,0],0,4), (3,"s5",[0,0,0,1,1,0,0,0],0,4),
 (4,"s6",[0,0,0,1,1,0,0,0],0,3), (4,"s2",z,0,2), (4,"s1",[0,0,0,0,0,1,1,0],0,4), (4,"s3",[0,0,1,0,0,0,0,0],.5,2), (4,"s5",[0,0,0,1,0,0,0,0],0,2), (4,"s4",[1,1,0,0,0,0],1,4),
 (5,"s3",z,0,3), (5,"s6",[1,0,0,0,1,0,0,0],0,2), (5,"s5",[0,0,0,1,1,0,0,0],0,2), (5,"s2",z,0,3), (5,"s1",[0,0,0,0,0,1,1,0],0,2), (5,"s4",[1,1,0,0,0,0],.5,3),
 (6,"s1",[1,0,0,0,0,1,1,0],0,2), (6,"s2",z,0,2), (6,"s3",[1,0,0,0,0,0,0,0],0,2), (6,"s5",[0,0,0,1,0,0,0,0],.5,2), (6,"s6",[1,0,0,0,1,0,0,0],0,1), (6,"s4",[1,1,0,0,0,0],1,2)])
o = [1] * 8; o6 = [1] * 6
GEMINI = _f([
 (1,"s3",[1,1,0,0,1,1,0,0],1,4), (1,"s5",[1,0,1,1,1,1,1,1],1,5), (1,"s2",[1,1,1,1,1,1,1,0],1,5), (1,"s6",[1,1,1,1,1,1,1,0],1,4), (1,"s1",[1,0,1,0,1,1,1,1],1,5), (1,"s4",o6,1,5),
 (2,"s4",[1,1,0,0,0,0],1,5), (2,"s5",o,1,5), (2,"s3",[1,1,0,0,0,0,0,0],1,5), (2,"s6",[1,1,1,1,1,1,1,0],1,5), (2,"s2",[1,1,0,1,1,1,1,0],1,5), (2,"s1",[1,0,1,0,1,1,0,1],1,5),
 (3,"s2",[1,1,1,0,1,1,1,1],1,5), (3,"s3",[1,1,1,1,0,0,0,0],1,5), (3,"s1",[1,0,1,1,1,1,1,1],1,5), (3,"s4",o6,1,5), (3,"s6",[1,1,1,1,1,1,1,0],1,5), (3,"s5",[1,0,1,1,1,1,.5,1],1,5),
 (4,"s6",[1,1,1,1,1,1,1,0],1,5), (4,"s2",o,1,5), (4,"s1",[1,0,1,1,1,1,1,1],1,5), (4,"s3",[1,1,1,1,0,0,0,0],1,5), (4,"s5",o,1,5), (4,"s4",o6,1,5),
 (5,"s3",[1,1,1,1,0,0,0,0],1,4), (5,"s6",[1,1,1,1,1,0,1,0],1,5), (5,"s5",[1,0,1,1,1,1,.5,1],1,5), (5,"s2",[1,1,1,.5,1,1,0,0],1,5), (5,"s1",[1,0,1,0,1,1,1,1],1,5), (5,"s4",o6,1,5),
 (6,"s1",[1,0,1,1,1,1,1,1],1,5), (6,"s2",o,1,5), (6,"s3",o,1,5), (6,"s5",[1,0,1,1,1,1,.5,1],1,5), (6,"s6",[1,1,1,1,1,0,1,0],1,5), (6,"s4",o6,1,5)])
FAMILIES = {"claude": G, "gemini": GEMINI, "grok": GROK, "deepseek": DEEPSEEK}

# atoms that no view could show, found after the reads (see GRADES.md); left in the strict score, dropped from the fair one
UNSHOWABLE = {("s1-melody", 1), ("s6-timbre", 7)}
STIM = ["s1-melody", "s2-drums", "s3-chords", "s4-hidden", "s5-glides", "s6-timbre"]
VIEWS = ["magma", "gray", "sharp", "slices", "topo", "grid"]
view_of = {(int(r.split("-")[1]), t["stimulus"]): t["view"] for r, ts in PLAN.items() for t in ts}


def table(g):
    rows = {}
    for (r, s), (atoms, trap, conf) in g.items():
        v = view_of[(r, s)]
        fair = [a for i, a in enumerate(atoms) if (s, i) not in UNSHOWABLE]
        rows.setdefault(v, []).append((s, sum(atoms), len(atoms), sum(fair), len(fair), trap, conf))
    return rows


def pct(R):
    return 100 * sum(x[3] for x in R) / sum(x[4] for x in R)


if __name__ == "__main__":
    allrows = {f: table(g) for f, g in FAMILIES.items()}
    print("## Fair score by view and family\n")
    print("| view | " + " | ".join(FAMILIES) + " | all 24 readers |"); print("|---" * (len(FAMILIES) + 2) + "|")
    tot = {v: sum((allrows[f][v] for f in FAMILIES), []) for v in VIEWS}
    for v in sorted(VIEWS, key=lambda v: -pct(tot[v])):
        print(f"| {v} | " + " | ".join(f"{pct(allrows[f][v]):.0f}%" for f in FAMILIES) + f" | **{pct(tot[v]):.0f}%** |")
    print("| *family overall* | " + " | ".join(f"{pct(sum(allrows[f].values(), [])):.0f}%" for f in FAMILIES) + " | |")
    print("\n## Fair score by stimulus and family\n")
    print("| stimulus | " + " | ".join(FAMILIES) + " |"); print("|---" * (len(FAMILIES) + 1) + "|")
    for s in STIM:
        print(f"| {s} | " + " | ".join(f"{pct([x for v in VIEWS for x in allrows[f][v] if x[0] == s]):.0f}%" for f in FAMILIES) + " |")
    print("\n## Traps rejected, by stimulus and family (of 6)\n")
    print("| stimulus | " + " | ".join(FAMILIES) + " |"); print("|---" * (len(FAMILIES) + 1) + "|")
    for s in STIM:
        print(f"| {s} | " + " | ".join(f"{sum(g[(r, s)][1] for r in range(1, 7)):g}" for g in FAMILIES.values()) + " |")
    print("| *total of 36* | " + " | ".join(f"{sum(x[1] for x in g.values()):g}" for g in FAMILIES.values()) + " |")
    print("\n## Traps rejected by view (all families, of 24)\n")
    print("| " + " | ".join(VIEWS) + " |"); print("|---" * len(VIEWS) + "|")
    print("| " + " | ".join(f"{sum(x[5] for x in tot[v]):g}" for v in VIEWS) + " |")
    print("\n## Confidence vs accuracy, by family\n")
    print("| family | mean confidence | fair % | confidence when the tile scored under 50% |"); print("|---|---|---|---|")
    for f, g in FAMILIES.items():
        R = sum(allrows[f].values(), []); low = [x[6] for x in R if x[3] / x[4] < 0.5]
        print(f"| {f} | {sum(x[6] for x in R) / len(R):.1f} | {pct(R):.0f}% | {sum(low) / len(low):.1f} (n={len(low)}) |" if low else f"| {f} | {sum(x[6] for x in R) / len(R):.1f} | {pct(R):.0f}% | none under 50% |")
