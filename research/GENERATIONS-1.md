# GENERATIONS-1: what a copy of a copy of a copy keeps

*Experiment by Kham, run by hand in AuraLoom, 2026-10-29 around 4 a.m. Numbers by Kehai.*

## What Kham did
1. Load a stretch of a real recording (`source-full-track.png` is its full tile).
2. Export it as an AuraGraph tile.
3. Load that tile back into AuraLoom and export it as a WAV. That WAV is the tile played back through Griffin-Lim, which has to guess the phase.
4. Import the WAV, export a tile, and repeat.

The result is 14 generations, `generations-1/gen01.png` to `gen14.png`. All are 398 × 160 and no two are identical (checked by hash). It's the photocopier game, or *I Am Sitting in a Room*, but for a picture codec.

## What the numbers say
Each tile is read as grayscale brightness, 0 to 1.

| gen | match to gen 1 (corr) | top third: high pitch, harmonics | middle | bottom third: bass, drums |
|---|---|---|---|---|
| 2 | 0.93 | 0.81 | 0.95 | 0.94 |
| 4 | 0.79 | 0.45 | 0.73 | 0.83 |
| 7 | 0.66 | 0.31 | 0.53 | 0.74 |
| 10 | 0.62 | 0.27 | 0.47 | 0.71 |
| 14 | 0.59 | 0.26 | 0.44 | 0.69 |

- **The top goes first.** High harmonics and the upper melody lines fade fastest: the top third falls to 0.26 match.
- **The bottom lasts longest.** Bass and the big drum hits still match at 0.69 after 14 rounds. Those are the vertical bright stripes that persist in every frame.
- **Detail across pitch collapses early.** The sharp edges between neighbouring pitch rows drop from 0.050 to 0.014 by gen 5, then stay there. That's the "clean lines" look turning into a wash.
- **Detail across time holds.** The edge sharpness along time stays roughly level (0.039 → 0.025, flat from gen 3 on). Onsets survive after pitch detail has gone.
- **The overall spectral balance is the most durable thing.** That's the average brightness of each pitch row, which matches at 0.87 after 14 generations. You can still tell it's "this kind of sound" long after you can't follow the tune.
- **It doesn't settle.** Each generation keeps about 93–98% of the one before, and that rate doesn't climb toward 100%. So there's no exact fixed point yet, only a slow drift. The match to gen 1 levels off around 0.59 at gens 12–14, but it's still moving sideways.

## Reading it with INVERSION-1
This agrees with `INVERSION-1.md`, which found that melody lives on the pitch axis and rhythm on the time axis. Repeated generations attack the pitch axis first: Griffin-Lim's phase guess smears energy across neighbouring rows, and quiet high rows sink into the noise floor. The time axis and the loud low energy hold. If you only kept the bottom third of gen 14, you'd still mostly have the groove.

## Kham's ears (the real test)
Kham listened to every generation. In his words: up to about generation 7 *"it just kept getting more muffled and noisy but still recognizable if you squinted with your ears"*. At **generation 8–9** (the two tiles he pointed to are exactly `gen08` and `gen09`) it became *"entirely unrecognizable… still sort of recognizable as music, but nothing resembling the original."*

Here's how that lines up with the middle third of the tile, where most of this song's melody sits:

| gen | middle third | top third | whole |
|---|---|---|---|
| 5 | 0.58 | 0.34 | 0.68 |
| 6 | 0.65 | 0.38 | 0.73 |
| 7 | 0.53 | 0.31 | 0.66 |
| **8** | **0.49** | **0.29** | **0.64** |
| **9** | **0.48** | **0.28** | **0.63** |
| 10 | 0.47 | 0.27 | 0.62 |
| 14 | 0.44 | 0.26 | 0.59 |

- **The song was lost where the middle band fell below half.** Gen 8 is the first generation where the middle third matches the original at less than 0.5. That's one listener and one song, so treat it as a hunch, not a law.
- **It's also where the curve flattens.** Before gen 8 each generation takes a big bite out of the original. After it, the tiles mostly drift around what the pipeline itself produces. Kham's "still music, but not *that* music" is a good description of that state: what's left is mostly the playback process's own texture, plus the loud low hits.
- **To test the hunch:** run the same loop on two or three very different songs, have Kham mark the generation where each one goes, and see whether the middle-band number lands near 0.5 every time.

## Open questions
- Is it the **tile step** (8-bit brightness, 160 bands) or the **Griffin-Lim step** (phase guess) that does most of the damage? Test it: run tile → tile with no audio in between, and separately WAV → WAV through Ghost mode.
- Would more Griffin-Lim iterations, or a saved phase, slow the drift?
- At what generation does a listener stop recognising the song? That needs Kham's ears, not correlations.

*Unit caveat: correlation of grayscale brightness is a crude stand-in for "sounds the same". It's a ruler, not a listener.*
