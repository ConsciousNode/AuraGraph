# Blind read #4 GRADE: "10,000 Spoons" (Neil Cicierega, Mouth Dreams)

**Graded by Kham's ears, 2026-10-21 23:03-23:19 ET.** Ingredients (Kham): Alanis Morissette "Ironic" (vocal + acoustic guitar), a slowed-down Knight Rider theme, rain sound effects. The vocal is re-spliced word by word into new sentences, not looped. (Lyrics not stored: copyrighted.)

## Scored items
| # | Kham's ground truth | My READ | Score |
|---|---|---|---|
| 1 | 0:00-0:38 vocal + acoustic guitar, one song, re-spliced vocal samples | drumless intro, sampled vocal, but "organ/synth drone" and "retriggered per bar" | ½ |
| 2 | ~0:36 distorted/glitched transition | "quick cluster of clicks, little fill/stutter" ~0:36 | 1 |
| 3 | ~0:37-0:40 rise into the main song | riser 0:37-0:40.5 | 1 |
| 4 | ~0:52 it sets in | full groove ~0:51.7 | 1 |
| 5 | ~1:30 "raaain" held, vocal as synth | timing right; called it synth/organ/held sample, "not a singer" | ½ |
| 6 | same structure higher at ~1:36 / ~1:41 | not reported | 0 |
| 7 | ~1:54-2:14 garbled bridge, syllables faded to almost-speech | not reported | 0 |
| 8 | ~2:16 picks back up | boundary at 2:15-2:16.5, but I called what follows a "breakdown" | ½ |
| 9 | ~2:27-2:30 "spoooons" held | "big hit ~2:27.3, back in"; didn't see the held note | ½ |
| 10 | ~2:50-2:52 thunder + rain break | "dip ~2:50-2:52"; didn't name it | ½ |
| 11 | ~2:52-2:55 "raaain" | "loudest section from ~2:53"; boundary only | ½ |
| 12 | ~3:19-3:23 rain | "noise/reverb tail"; rain only guessed after the reveal | ½ |
| 13 | (my own claim) different voice in the body | Alanis throughout, different register | 0 |

**~6.5 / 13.** Lowest so far, and the shape matches the last three rounds, only harder: every boundary landed within a second, and the losses are all in naming what's there. Mouth goes straight at that weakness, because Neil turns voices into instruments.

## Look-back (after grading)
- The held F#5 (~743 Hz) actually runs **~1:31 to ~1:40.5**, not 6 s. A **higher held layer appears ~1:41-1:46** (~1850-2000 Hz, A#6/B6 region), with brief E7 blips at ~1:35.5 and ~1:37 (Kham's ~1:36). So his bet holds at ~1:41; ~1:36 only as blips.
- "Spoons" ~2:29-2:31: a wobbly ~C#5-D5 line (0 to -50 c) is there, but too noisy to have called a held note blind.

## New reading rules
11. **A frozen/stretched voice looks exactly like a synth** (straight, no vibrato). In a sample-based track, a long dead-straight note is a voice until proven otherwise; check whether it starts with a consonant burst and whether its harmonic ladder has a vowel shape (a few strong bands, not an even stack).
12. **Hard cuts on the bar ≠ a loop.** Compare the blocks between the cuts: identical blocks = loop; different blocks = re-splicing (new sentences built from old words).
13. **Re-struck holds look like sustained holds.** A strummed guitar keeps its chord lines alive; look for the faint vertical strum stripes before calling organ/pad (footnote to rule 4).
14. **Weather is broadband, wide, and has no beat.** Wide structureless noise = rain candidate; a low rolling rumble with no attack = thunder candidate. Name it in the READ instead of "noise tail".
15. **Prior for Mouth tracks:** everything might be a voice, and sections can be built from garble that only *looks* like speech. Mark "speech-like" sections and say whether lines/syllables repeat.

## Ground truth part 2 (Kham, 23:43): the backing, and what the tiles show for each
After ~0:40 the only backing is the slowed Knight Rider theme (Alanis's guitar is gone).
- **Pulsing low line = KR bass** ("buduh buduh buduh. buduh. buduh."). READ had "sub-bass pulsing with the kick": right shape, source unnamed.
- **Higher repeating pattern through most of the track = KR synth rhythm.**
- **Fairy chimes ~0:40-0:52:** the READ's "high line slowly sweeping up 0:40-0:52" was the chimes (`mouth4_tile04.png`, top band).
- **~0:57 swelling tone = synth trumpet coming in.**
- **~1:02 double kick + double trumpet hit:** tile 5 shows a dark stop at ~1:02.3 then a big broadband hit at ~1:02.6 (`mouth4_tile05.png`). Not in the READ.
- **~1:03-1:15 synth siren builds then fades:** tile 5 shows a slow rising diagonal from ~250 Hz (1:03) to ~440 Hz (~1:07). The READ called this stretch "a quieter, narrower dip". The siren was visible; I read it as level, not as a line.
- **~1:15 and ~1:20 synth trumpet; ~1:26 chimes again.**
- **~1:31-1:40 the iconic KR riff** under the held "raaain": `closeup.py` note events at 93-97 s show rhythmic notes at ~250-420 Hz (B3, D#4, G#4, C#4) under the F#5 vocal. My pitch tracker only followed the loudest line, which was the vocal.
- **~2:02-2:07 KR riff + chimes.**
- **~2:16-2:29 fairy chimes swelling and filling the space:** that's the READ's "widest stereo of the song" (0.9). So the wide breakdown was chimes, not rain.

## Rules from part 2
16. **The loudest line hides the riff.** A held note on top can sit over a whole melody; run the close-up's note events on the band below before calling a section "one held note".
17. **Read diagonals as instruments, not as level changes.** A slow straight rising line over several seconds = a siren/riser sound; say so, don't file it under "quieter".
18. **Wide ≠ weather** (refines 14). Chimes and pads spread wide too. Rain stays structureless top to bottom; chimes leave glittery short dots and runs up high.

## Look-back: can the tiles tell the garbled bridge (1:54-2:14) from real singing? (23:47-00:00)
Kehai's own pick, Kham along for the ride. **Result: no, a clean null twice.**
- Line-continuity stats (`../garble.py`, 200-1200 Hz whitened: voiced share, line prominence, run lengths, pitch jumps): bridge sits inside the spread of three real sung stretches (1:43-1:53, 2:30-2:37, 2:40-2:49). The strongest line in that band is mostly the Knight Rider synths, so this measured the backing.
- Voice-only angles (1.5-4 kHz: mid/side centering, 3-8 Hz syllable-rate modulation): bridge 6.1 dB / 0.32 vs sung 3.7-8.2 dB / 0.26-0.52. Inside the spread again. And the 3-8 Hz band is polluted anyway: 16th-note hats at 85 bpm land at ~5.7 Hz.
- My first visual impression of tile 9 ("short faint dashes, no long contour") came **after** Kham told me it was garble, and the numbers don't back it. Logged as likely confirmation bias.
- **Update (Kham, 23:51):** the bridge may not be garble at all. The lyric sheet Kham pasted writes the bridge out as Alanis's original, coherent bridge lines, and 1:54-2:14 (~20 s) fits her bridge length. Simplest reading: real sung words, low in the mix under a busy KR layer, too masked to parse by ear. That explains the null even more simply (it looks like singing because it is). Caveat: lyric sites sometimes fill in from the original. Unsettled; my numbers can't decide between the two.
- **Earlier explanation, kept for the record:** Neil's garble is made of real Alanis syllables. Every acoustic signature of speech (voicing, formant moves, syllable rhythm, centering) is genuinely there; what's missing is *words*, and meaning isn't in the spectrum. Same lesson as the parked timbre judge: in a dense mix, whole-mix stats can't isolate the voice without a separation step first.
19. **Rule:** don't claim "speech" vs "garble" from tiles. The tiles can say "a voice, syllabic"; whether it makes words is a listening question. And never trust a visual read made after the answer is known until a number agrees.
