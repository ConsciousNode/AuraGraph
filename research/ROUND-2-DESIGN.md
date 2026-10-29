# AuraGraph outside test #2: design on paper
*Kehai Interim (lead), 2026-10-20 ~20:40 ET.*

> **Status: PARKED / optional (Kham, 20:38).** The outside-model tests were something to do cheaply while usage was near the cap. The format is primarily for the crew (and rich-image LLMs), so the main line is dev: tile improvements and the HTML port. Keep this only if a second outside check is ever useful. My slip: I read my own handoff's ordering as the project's priority.

Builds on `OUTSIDE-TEST-1.md` and the 2026-10-19 handoff. Round 1 was a pilot: n=1 per cell, an in-sample guide, and one invalid run (X9). Round 2 tries to answer the question round 1 could only hint at.

## The questions
1. **Does the reading guide help, on songs it was not written from?** (Round 1's guide effect was about +2.9 over the direct-vision models, but in-sample and noisy.)
2. **How much do models make up when there is nothing to read?** (Grok's no-image control confabulated full readings in round 1.)
3. **Do the tile fixes close the round-1 blind spots?** These were the hi-hat count-in nobody found, voice samples read as piano, and stereo width read both ways.

## Tile changes (do these before making the pack)
1. **High-band transient lane:** a thin strip showing only sharp onsets above ~6 kHz (hi-hats, shakers, count-ins).
2. **Labeled color bar on the stereo-width panel** (narrow to wide, with numbers).
3. **Legend on every panel:** units and range. Zoom tiles say which tile and which seconds they zoom.
4. **Mid-zoom panel option:** between the full tile and the 10 s zoom.
5. **Local tempo:** beat tracking per tile, not one global BPM. (Round 1's 112 vs ~88-90 BPM miss came from my tool.)

## Guide changes
1. The wobble/glide cue applies only to horizontal lines in the top three (pitch) panels, never to the loudness or onset traces.
2. Counter-cues:
   - a plain piano gets brighter all at once when struck harder, and a new instrument adds its own line;
   - a crowd shows up as arcs, not a synth;
   - a short voice sample can look like a struck note, so check for glide inside the note.
3. Calibration rule: say "High" only when two panels agree.
4. The guide is written **before** the round-2 songs are chosen, and frozen with a commit hash, so it is genuinely out-of-sample.

## Arms (one fresh chat each)
- **C, control:** the questions with no image attached. Measures confabulation.
- **A, blind:** the image pack plus the questions, no guide.
- **B, guide:** the image pack plus the questions plus the frozen guide.

Order across chats doesn't matter because every chat is fresh. Never put two arms in one chat.

## Logging (the round-1 lessons)
- Mark prompt boundaries in every saved file (`=== PROMPT A BEGIN ===`, etc.) so a stray paste is visible.
- Check the input box before sending (X9 lesson).
- Note per run: did the model see **pixels or a text description** (Lumo lesson), and did it use tools or code? Tool-using runs are reported separately, not mixed in.
- Canonical image order and on-tile headers; models' "Image N" labels are mapped by header.

## Songs (Kham picks; criteria from me)
About 4-6 clips, none used in round 1, none I've analyzed before. Aim for one of each:
- a solo instrument that is **not** piano (guitar, violin or voice), the new clean-ladder baseline;
- a clear **hi-hat or count-in** opening, to test the new transient lane;
- a **dense full-band mix**;
- a **tempo or feel change** inside the clip;
- something **electronic or synth-led**, to see whether the synth vs piano confusion flips;
- optionally one more mashup (Mouth album) for the hard end.
Where possible, use public-domain or CC recordings for anything that might go public. Audio itself never goes in a repo, only derived tiles.

## The key: ground truth comes from ears, not my tool
- Kham listens and gives what he hears in plain words: instruments, when things enter and leave, tempo by tapping, anything wet or dry. I add tool measurements and mark which items came from which source.
- Tempo and harmony items count only if Kham's ears and the tool agree. Otherwise they're left out of the score (round-1 lesson).
- The key and rubric are committed **before** any answers are pasted back.

## Scoring
Same rubric as round 1: +1 per key item, half credit for partial, -1 per confident wrong claim, wrong-but-hedged = 0. Plus:
- **Confabulation count** for arm C: the number of specific musical claims made with no image (ideal is 0, or saying "I can't tell without the image").
- **Calibration:** the share of High-confidence claims that were right.
- Grading stays blind: Kham relabels answers X1..Xn before pasting, and I unblind only after the grades are committed.

## Load on Kham (honest estimate)
Each subject model gets 3 chats (C, A, B). Four models means 12 chats, five means 15. Round 1 was 10 plus controls, and he did it all by hand. Options to keep it humane:
- start with 3-4 models (Gemini, Kimi, Grok, DeepSeek; Lumo as a separate description-only track);
- a second run per cell (n=2) only for the arm and model pairs that land close to each other.

## Build order
1. This design (Kham reacts).
2. Tile fixes in `proto.py` (cheap, mine).
3. Freeze the guide v2.
4. Kham picks songs and sends audio; I make the pack and Kham writes the ear notes; key committed.
5. Kham runs the chats; I grade blind; then unblind.
6. Then the AuraGraph HTML port (Xinu single file), carrying the fixed tiles.
