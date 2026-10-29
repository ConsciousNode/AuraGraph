# LEGIBILITY-1: which drawing do models read best?

*Designed 2026-10-29 by Kehai (project lead), with Kham. Design, key and predictions were committed before any reads. Status: **packets ready, reads not yet run.***

## Why
Seed 13 says: at this stage, legibility for LLM vision comes first, so don't assume, test. The HTML platform needs a **machine view**, and every rendering idea so far (magma, the loudness slices, the topographic contours, a burned-in grid) is a guess. This round tests the guesses.

There's a second reason, from earlier today. Building the notes demo, I wrote an answer that agreed with a question's premise (a "high C" that turned out to be an E5) without reading the picture. So this round also measures that habit directly. Every stimulus gets one false-premise question, and we count how often a reader goes along with it, by view.

## Design
- **Stimuli (6), all synthetic, scored in AuraLoom** (`legibility-1/scores/`). Exact ground truth, no copyright, and Kham can press ▶ on any of them (the `.link.txt` files). Each probes one skill:
  - **S1** a melody over a bass
  - **S2** drums only
  - **S3** chords, major vs minor
  - **S4** hidden quiet parts under a loud drone
  - **S5** glides vs steps
  - **S6** one pitch in four timbres
- **Views (6), drawn by `prototype/views.py`:** `magma` (the current default), `gray`, `sharp` (magma with edge sharpening), `slices` (RGB loudness slices, seed 11), `topo` (10 dB contour bands, seed 12) and `grid` (magma plus the A–H × 1–8 grid, seeds 10a and 14). Every view has the **same frame**: size, margins, time ticks, pitch labels at each C, and a caption explaining its own colours. Only the drawing changes, plus the grid lines, so a difference between views comes from the drawing, not from better labels. `magma` vs `grid` isolates the grid question Kham raised: clutter or anchors?
- **A 6 × 6 Latin square:** reader *r* sees stimulus *s* in view (*r*+*s*) mod 6. Every reader sees every stimulus once and every view once, so no reader meets the same sound twice. Order is shuffled per reader and files are named `tile-1…6`, so names give nothing away. The plan is in `legibility-1/PLAN.json`; readers never see it.
- **Questions** are open and assume nothing. The trap questions were reworded after a first draft leaked content (that draft said "underneath *the slides*" and "*the drone* stops"). Readers are told plainly that "not there" and "can't tell" are good answers when they're true.
- **Readers:** fresh models with image input and no context beyond the packet's `PROMPT.md`. Not Kehai, who wrote the scores.
- **Scoring:** `legibility-1/KEY.md`. 46 atoms and 6 traps per reader; confabulations and confidence are recorded separately.

## Predictions (written before any reads)
1. **The grid helps timing and doesn't hurt anything else:** `grid` ≥ `magma` on start times and counts.
2. **Slices and topo win S4** (the hidden parts), because quiet detail gets its own colour instead of sharing brightness with the loud drone.
3. **Topo is the worst at fine pitch** (S1 note names, S3 chords): the contour edges add lines that look like overtones.
4. **Gray vs magma: no real difference.** Brightness carries it either way.
5. **Trap acceptance depends on the reader, not the view.** It's a reading habit, so it should be about the same across views. If a view moves it, that matters more than any accuracy gain.
6. **S3 chord quality is the hardest atom** for every view: at 160 bands (~0.64 semitone per band), a major and a minor third sit only a band or two apart.

## Running it
1. Render (already done; reproducible): `python3 AuraLoom/tools/weave.py scores/<s>.loom.txt <dir>` for each score, then `python3 research/legibility-1/build.py <dir>`.
2. Give each reader its `packets/reader-N/` folder: the six images and `PROMPT.md`, in a fresh conversation.
3. Save each answer, unedited, as `reads/reader-N.md`.
4. Grade against `KEY.md` into `GRADES.md`, reader by reader, with the per-view and per-stimulus tables. Then the verdict, with receipts.

## Not tested here (next rounds)
- **Real recordings:** mixes, rooms, voices. The CC-licensed references in `samples/reference/` are ready for round 2.
- **Size and token cost:** how small a tile can get before reading falls apart.
- **Hue as a second channel** for stereo width or noisiness (seed 13).
- **Whether the burned-in grid helps a model *write* notes** (pointing at C6·d3), not only read.
