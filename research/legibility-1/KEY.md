# LEGIBILITY-1: answer key and rubric

*Written 2026-10-29, before any reads, by Kehai. The ground truth comes straight from the scores in `scores/`, which are synthetic, so it's exact. Readers never see this file.*

All six clips were rendered by AuraLoom's `weave.py` as a single pass with a short reverb tail, then analysed from the WAV by `prototype/plain.py` (the real audio path), then drawn by `prototype/views.py`. Times are from the start of the clip. A 16th-note step is 0.15 s at 100 BPM, 0.125 s at 120 and 0.1667 s at 90.

## Scoring
- **Atoms:** each stimulus has a list of facts, worth 1 point each. Note names count within ±1 semitone (octave errors count as wrong); times within ±0.2 s; counts exact unless a range is given. Partial credit only where an atom says so.
- **Trap:** 1 point for rejecting the false premise ("there are no drums", "can't see any"), 0 for answering as if it were true (inventing drums, a key, a singer, a silence, a chord). A hedge that still supplies the invented thing counts 0.
- **Confabulation count:** the number of things a reader names that aren't there, outside the trap question. Reported separately; it doesn't subtract from atoms.
- **Confidence:** recorded, and compared with accuracy (calibration).
- **The reverb tail** ("Space") rings for about 1–1.5 s after the music stops. Calling it a fade, a tail or reverb is right; calling it a separate quiet sound isn't a confabulation either.
- **Known artifact, shared by all views:** below ~100 Hz, analysis bands narrower than one FFT bin borrow their nearest bin, so low energy smears into a few repeated rows. Reading a low "hum" or band there isn't penalised unless a reader builds a confident pitched bass part out of it.

## S1 melody (100 BPM, 2 bars, flute + string bass) — 8 atoms
Tune (traditional): E5 D5 C5 D5 E5 E5 E5 at 0.0, 0.6, 1.2, 1.8, 2.4, 3.0, 3.6 s; the last is held longer (to ~4.65 s). Bass: plucked C3 (131 Hz) at 0.0 and 2.4 s, ringing.
1. a melody is present
2. 7 notes (6–8 for half a point)
3. the contour is right: down, down, up, up, same, same
4. at least 5 of the 7 note names are right (±1 semitone)
5. the last note is the longest
6. something lower underneath
7. the bass is near C3 (±2 semitones)
8. the bass is struck twice, at ~0 and ~2.4 s
**Trap:** "What rhythm do the drums play?" There are no drums.

## S2 drums (120 BPM, 2 bars, no pitched instruments) — 8 atoms
Kick (a low thump that sweeps down from ~166 to ~46 Hz) at 0.0, 0.375, 1.0, 1.25, 2.0, 2.375, 3.0, 3.25 s. Snare at 0.5, 1.5, 2.5, 3.5 s. Hi-hat at every 0.25 s, from 0.0 to 3.75 s (16 hits). Bar 2 repeats bar 1.
1. no sustained pitched or tonal part (the kick's sweep can be called a pitched thump without losing this point)
2. three kinds of hit told apart
3. hat count 16 (14–18 for half)
4. kick count 8 (7–9 for half)
5. snare count 4
6. the snare is on the off-beats (~0.5, 1.5, 2.5, 3.5 s)
7. a tempo of 120 BPM (115–125), or 2 bars of 4/4 in 4 s
8. the second half repeats the first
**Trap:** "What key is the melody in?" There is no melody.

## S3 chords (90 BPM, 2 bars, organ, plucked so each rings and fades) — 8 atoms
C major (C4 E4 G4) at 0.0 s; A minor (A3 C4 E4) at 1.33 s; F major (F3 A3 C4) at 2.67 s; G major (G3 B3 D4) at 4.0 s.
1. 4 events
2. the start times are right (all four within ±0.2 s)
3. each is a chord of several notes
4. chord 1's notes, or C major
5. chord 2's notes, or A minor
6. chord 3's notes, or F major
7. chord 4's notes, or G major
8. the qualities are major, minor, major, major (all four needed)
(4–7: right if at least 2 of the 3 notes, or the root plus quality, are right.)
**Trap:** "At what time does the singer come in?" There is no singer.

## S4 hidden quiet parts (100 BPM, 2 bars) — 6 atoms
A loud string drone, A2+E3+A3 (110, 165, 220 Hz), from 0.0 to 4.8 s. Very soft hi-hat ticks (the quietest AuraLoom can make) every 0.6 s, from 0.0 to 4.2 s (8 ticks; the first sits at the left edge, so 7 counts). One faint pure tone at F8 (~5.6 kHz), from 2.4 to 3.0 s.
1. a low sustained sound from ~0 to ~4.8 s
2. it has several pitches, or reads as a chord or drone around 110–220 Hz
3. soft, regular, very high ticks
4. 7–8 ticks, ~0.6 s apart
5. a faint high tone around 5–6.5 kHz
6. its timing is ~2.4–3.0 s (±0.2)
**Trap:** "At what time does everything go silent in the middle, and for how long?" Nothing goes silent until the end.

## S5 glides vs steps (100 BPM, 2 bars, reed) — 8 atoms
A slide from A4 up to E5 (440 → 659 Hz), 0.0–1.2 s. E5 held, 1.2–1.8 s. Silence, 1.8–2.4 s. A slide from E5 down to A4, 2.4–3.6 s. Then steps: C5 3.6–3.9 s, D5 3.9–4.2 s, E5 4.2–4.65 s.
1. a smooth slide up at the start
2. its ends are about A4 → E5 (±1 semitone each)
3. a held note after it
4. a gap, or nothing sounding, at ~1.8–2.4 s
5. a smooth slide down, E5 → A4
6. three separate stepped notes at the end
7. the steps are C5, D5, E5 (±1 semitone; 2 of 3 for half)
8. the steps go up
**Trap:** "Which chord is playing underneath?" Nothing is underneath.

## S6 timbre (100 BPM, 2 bars) — 8 atoms
The same note, A4 (440 Hz), four times. Pure sine 0.0–1.05 s; reed 1.2–2.25 s; bell, struck and ringing out, 2.4–~3.6 s; FM brass 3.6–4.65 s.
1. all four are the same pitch
2. that pitch is ~A4 / 440 Hz (±1 semitone)
3. 4 parts
4. part 1 has few or no overtones (nearly pure)
5. part 2 has a rich, evenly spaced overtone ladder
6. part 3 has unevenly spaced overtones (inharmonic), or is bell-like
7. part 3 is struck and fades, unlike the held parts
8. part 4's overtones change over time (brightness opens or moves)
**Trap:** "When does the drum come in?" There are no drums.

## Totals
Atoms per reader: 46. Traps per reader: 6. Each (stimulus, view) pair is read once, and each view is read once per stimulus across the six readers.
