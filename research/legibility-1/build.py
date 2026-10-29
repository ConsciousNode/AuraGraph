#!/usr/bin/env python3
"""
build.py: assemble the LEGIBILITY-1 reader packets.

Six stimuli x six views, as a Latin square: reader r sees stimulus s in view
VIEWS[(r + s) % 6], so every reader sees every stimulus once and every view once,
and every stimulus is seen in every view by someone. Stimulus order is shuffled per
reader (fixed seed) and the files are named tile-1..tile-6, so nothing in a name gives
the content away.

Usage (from the AuraGraph repo root, with the stimuli rendered to WAV by AuraLoom's weave.py):
  python3 research/legibility-1/build.py /path/to/render_dir
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "prototype"))
import views

STIM = ["s1-melody", "s2-drums", "s3-chords", "s4-hidden", "s5-glides", "s6-timbre"]
VIEWS = views.VIEWS

# open questions: they ask what is there, never what something "is", and assume nothing
QUESTIONS = {
    "s1-melody": ["Is there a melody? If so, list its notes in order: note name (or approximate Hz) and start time for each.",
                  "Is anything sounding underneath or below it? If so, what, and when?"],
    "s2-drums": ["Are there pitched (tonal) sounds, unpitched sounds, or both?",
                 "List each kind of sound event you can tell apart, how many times each occurs, and when. Estimate the tempo if there is one."],
    "s3-chords": ["How many separate events are there, and when does each start?",
                  "For each event, which notes are sounding (note names or approximate Hz)? If any are chords, say whether each sounds major or minor."],
    "s4-hidden": ["List every sound you can find, including the quietest. For each, give its approximate frequency range and its start and end times."],
    "s5-glides": ["Describe how the pitch moves over time: where it slides smoothly, where it holds, where it moves in separate steps, and where nothing sounds. Give the notes (or Hz) and times at each change."],
    "s6-timbre": ["How many parts are there, and when does each start? Are they at the same pitch or different pitches? Give the note or Hz for each.",
                  "For each part, describe its pattern of overtones: how many lines above the lowest one, whether they are evenly spaced, and whether the pattern changes over time."],
}
# one false-premise question per stimulus: the right answer is that the thing isn't there.
# Worded so it gives nothing real away (no "the slides", no "the drone").
TRAPS = {
    "s1-melody": "What rhythm do the drums play?",
    "s2-drums": "What key is the melody in?",
    "s3-chords": "At what time does the singer come in?",
    "s4-hidden": "At what time does everything go silent in the middle, and for how long?",
    "s5-glides": "Which chord is playing underneath?",
    "s6-timbre": "When does the drum come in?",
}

GUIDE = """You'll be shown 6 images. Each is a picture of a short sound clip (an "AuraGraph tile").

How to read a tile:
- Time runs left to right (ticks in seconds along the bottom). Pitch runs bottom to top on a log scale (each C is labelled with its frequency in Hz on the left).
- The caption under each image says how loudness is drawn in that image. The drawing style differs from image to image; read each caption.
- Horizontal lines are sustained pitched sounds. Evenly spaced parallel lines above a lowest line are that sound's overtones (its timbre). Curved or slanted lines are pitch slides.
- Vertical stripes are hits (drums, clicks, strikes). Sounds that ring out fade toward the right.
- Low rows are bass; the top rows are very high (cymbals, hiss).

For each tile, answer the questions. Give numbers (times in seconds, notes or Hz) wherever you can. If you can't tell, or something isn't there, say so plainly: "not there" and "can't tell" are good answers when they're true. End each tile with a confidence from 1 (guess) to 5 (sure).
"""


def main(render_dir):
    out = os.path.join(HERE, "packets")
    os.makedirs(out, exist_ok=True)
    plan = {}
    for r in range(6):
        rng = random.Random(1000 + r)
        order = STIM[:]; rng.shuffle(order)
        d = os.path.join(out, f"reader-{r + 1}"); os.makedirs(d, exist_ok=True)
        lines = [f"# AuraGraph reading, packet {r + 1}\n", GUIDE]
        plan[f"reader-{r + 1}"] = []
        for k, s in enumerate(order):
            v = VIEWS[(r + STIM.index(s)) % 6]
            img = f"tile-{k + 1}.png"
            views.render(os.path.join(render_dir, s + ".wav"), v).save(os.path.join(d, img))
            qs = QUESTIONS[s][:]
            qs.insert(rng.randrange(len(qs) + 1), TRAPS[s])      # the trap sits somewhere among the real questions
            lines.append(f"\n## Tile {k + 1} (`{img}`)\n")
            lines += [f"{i + 1}. {q}" for i, q in enumerate(qs)]
            lines.append(f"{len(qs) + 1}. Confidence, 1-5.")
            plan[f"reader-{r + 1}"].append({"tile": img, "stimulus": s, "view": v, "trap_q": qs.index(TRAPS[s]) + 1})
        open(os.path.join(d, "PROMPT.md"), "w").write("\n".join(lines) + "\n")
    json.dump(plan, open(os.path.join(HERE, "PLAN.json"), "w"), indent=1)
    print("packets written; plan in PLAN.json (keep it away from readers)")


if __name__ == "__main__":
    main(sys.argv[1])
