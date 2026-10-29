# LEGIBILITY-1: grades, round A (Claude readers)

*Graded 2026-10-29 by Kehai against `KEY.md` (committed before the reads). The reads are in `reads/`, saved unedited. Six fresh Claude (Opus 5.5) readers, one packet each, who saw nothing but their packet. Atom-by-atom scores are in `grades.py`; run it to rebuild these tables. Round B, the outside models run by Kham, is still to come.*

**Read this first: n = 1 per cell.** Each (stimulus, view) pair was read by one reader. The Latin square spreads reader differences evenly across views, but any single cell can still be one reader's good or bad minute. Treat view differences of a few points as suggestive, not settled.

## By view
*Fair score* drops the two atoms that turned out to be unshowable in every view (see "Stimulus flaws" below). Strict scores are shown too.

| view | strict atoms | fair atoms | fair % | traps rejected | mean confidence |
|---|---|---|---|---|---|
| gray | 43.5/46 | 43/44 | 98% | 4/6 | 2.7 |
| grid | 44/46 | 43/44 | 98% | 3.5/6 | 3.0 |
| slices | 40/46 | 40/44 | 91% | 3.5/6 | 3.2 |
| sharp | 39/46 | 39/44 | 89% | 3.5/6 | 3.0 |
| magma | 36/46 | 35.5/44 | 81% | 3.5/6 | 3.0 |
| topo | 32/46 | 32/44 | 73% | 3/6 | 2.7 |

## By stimulus and view (fair atoms)
| stimulus | magma | gray | sharp | slices | topo | grid |
|---|---|---|---|---|---|---|
| s1-melody | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| s2-drums | 5.5/8 | 7/8 | 6/8 | 5/8 | 5/8 | 7/8 |
| s3-chords | 3/8 | 8/8 | 5/8 | 8/8 | 4/8 | 8/8 |
| s4-hidden | 5/6 | 6/6 | 6/6 | 5/6 | 2/6 | 6/6 |
| s5-glides | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| s6-timbre | 7/7 | 7/7 | 7/7 | 7/7 | 6/7 | 7/7 |

Melody, glides and timbre are read almost perfectly in every view. **The views separate on chords (S3), the hidden quiet parts (S4) and drum counting (S2).**

## Traps (false premises), by stimulus
| stimulus | trap | rejected | what was in the picture |
|---|---|---|---|
| S3 chords | "when does the singer come in?" | **6/6** | nothing voice-like |
| S4 hidden | "when does everything go silent in the middle?" | **6/6** | no gap |
| S2 drums | "what key is the melody in?" | **5.5/6** | no tonal line |
| S5 glides | "which chord is underneath?" | 2.5/6 | real low energy in the bottom rows; five readers said "can't tell" (0.5) and one named a chord (0) |
| S1 melody | "what rhythm do the drums play?" | **1/6** | full-height onset stripes at every pitch change (AuraLoom's note edges were too sharp; see below) |
| S6 timbre | "when does the drum come in?" | **0/6** | low-band blocks under the reed and brass (real, about −50 dB) and a low thump on the bell's strike |

**This is the clearest result of the round.** Readers almost never invented something from an empty picture. Where the picture held a real mark that *could* fit the premise (a stripe, a low smear), they bent that mark to fit the question nearly every time. Trap rejection hardly moves between views (3 to 4 out of 6 each), but it swings from 0/6 to 6/6 between stimuli. It isn't a property of the drawing. It's how a question pulls on a reader when the picture holds an ambiguous mark. That's the same thing I did with the C5 earlier today, only there the mark was real and the C was invented.

## Predictions, scored
1. **The grid helps and doesn't hurt: supported.** Grid 98% vs magma 81%. The grid view is exactly magma plus lines, so the lines cost nothing and may help. Caveat: the gap is mostly one cell (S3: magma 3/8 vs grid 8/8, two different readers).
2. **Slices and topo win S4: wrong.** On S4, topo was the worst (2/6: its 10 dB bands swallowed the faint tone and the ticks) and slices 5/6. Gray, sharp and grid were perfect.
3. **Topo is the worst at fine pitch: half right.** Topo was the worst overall (73%) and on chords and the hidden parts, but melody and glides read fine in topo.
4. **Gray vs magma, no difference: not supported this round.** Gray 98% vs magma 81%, but that's the same single S3 cell again (n = 1). Needs round B and a replication before I believe it.
5. **Trap acceptance depends on the reader, not the view: right about the view, wrong about why.** It barely depends on the view. It depends on the *stimulus*: whether there's a real mark to bend (table above).
6. **S3 chord quality is the hardest atom: right.** 3 of 6 readers got all four qualities. The other three said "can't tell" rather than guess, which is the honest miss.

## Stimulus flaws (found in the reads, checked against the audio)
- **AuraLoom's note edges were too sharp.** *(Corrected after checking: it isn't a click in the audio.)* There are no sample-level discontinuities, and the onsets aren't louder in any band. The stripes come from analysis: any onset much shorter than the 93 ms analysis window leaks a faint vertical line across every frequency, and at the tile's 80 dB depth it shows. Real instruments do this too; it's how a spectrogram draws an attack. AuraLoom's Clean renderer started and stopped notes with 12 ms straight-line corners, which made the lines strong and full-height. That's behind the S1 trap result. **Fixed in AuraLoom v0.6.1:** each tone row's envelope is smoothed at the sample rate (~23 ms), and the stripes at pitch changes nearly vanish, while kick and snare peaks are unchanged (measured). **For the guide:** an onset stripe means a sound started, not that a drum hit. **The round's packets were left unchanged,** so the outside models read the same pictures.
- **Same-pitch notes merge, sometimes.** AuraLoom ends each scored tone one column early so repeats re-articulate, but the rounding of 12.92 columns per 16th made that gap appear at some joins and not others. Here the E5 at 3.0 s merged and the one at 3.6 s didn't, so the picture shows E D C D E, a long E. "7 notes" (S1 atom 2) can't be read from any view, so it's dropped from the fair score. Every reader read the picture right. **Fixed in v0.6.1:** every scored tone now ends exactly one column before the next step, so all seven notes show.
- **The FM brass "opens" too briefly to see.** It goes from 7 to 10 overtone lines in its first ~0.15 s and then holds. "Steady" is a fair read, so S6 atom 8 is dropped from the fair score.
- **The reed and brass voices put energy into the bottom rows** (about −50 to −55 dB, measured). It's real, not the low-band artifact. It made the S6 trap a fair-looking trap rather than a clean one.

## Judgment calls (recorded so they can be argued with)
- **A third trap outcome.** "Can't tell" while describing a real mark, without inventing the premised thing, scored 0.5. The key only had 1 and 0, and this case needed its own value. It's applied the same way everywhere: S5 (five readers) and S2 reader 4 ("can't pick out the notes of a melody with 10 dB bands", which implies a melody might exist).
- **S1 contour and names:** credited when the reader got D-D-U-U and ended on a held E, since the picture can't show the repeats.
- **S2 atom 1 (no sustained pitched part):** withheld from the two readers who reported a sustained "tonal band". That band is the snare noise's lower edge, smeared by reverb.
- **S4 atom 4 (7–8 ticks):** six ticks scored 0, since the key asked for 7–8.

## Calibration
Confidence barely tracks accuracy. S3 readers who got all four chords right still said 2/5, and the S1 readers who called the clicks drums said 4/5. Readers were humble where they were right and sure where a premise had misled them.

## What this means for the machine view (provisional, pending round B)
- **Drop topo.** It's the worst overall, and it loses quiet detail into its bands.
- **Keep the burned-in grid.** It's free at worst, and it's what pinned notes point at.
- **Gray or magma under the grid:** undecided. Round B, and a replication with more readers per cell, should settle it. "Gray + grid" becomes a candidate for round 2.
- **Slices are not a win** for quiet detail at these levels. Shelve them for now; they may return as a second channel (seed 13), not the main one.
- **Not a view question, but the biggest lever for honest reading:** the guide should teach readers that a mark which *could* fit a question's premise isn't evidence for the premise. This round gives the worked examples.

## Next
1. **Round B:** Kham's outside models, the same packets, graded the same way.
2. ~~Fix the AuraLoom note edges~~ (done, v0.6.1). Re-render S1 for round 2, not for this round.
3. **A replication** for the cells that decide things (S3 and S4 across all views) with 2–3 readers per cell, including "gray + grid".
