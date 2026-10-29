# AuraGraph — first-listen findings
*Kehai Interim, 2026-10-17 ~03:00 ET. Song: "Birdhouse in Your Soul," They Might Be Giants, live at Music Hall of Williamsburg (Kham's file). Prototype: `proto.py` v0.1.*

## What I could actually perceive

**Crowd vs band.** Tile 01 (0:00–0:02.4) and tile 14 (3:21 onward) are full of *arcs*: curved lines bending up and down through 200–1800 Hz, overlapping, no low end. Those are human voices cheering and whooping. Pitch that glides instead of stepping. At 3:24–3:25 one voice does a long descending swoop from ~440 Hz down to ~110 Hz. Somebody's big "whoooo." I didn't need a label to know it was people.

**The band arriving.** At 0:02.4 the bottom of the picture lights up all at once: heavy blocks in the 55–110 Hz range, pulsing in a pattern with gaps. Bass and kick coming in together, staccato. The blocks have a rhythm I can count.

**Sustained tone with a rich comb.** Tile 01, 0:12.3 onward: the low end drops away and a dense ladder of evenly spaced horizontal lines appears up high. One sustained sound with many strong overtones. That ladder spacing is the harmonic signature Kham's hypothesis is about. This is where timbre lives.

**The final chord.** Tile 14, 3:15–3:19: long flat horizontal lines, chroma solid on **A** (D faint). The band holding the last chord. Then it decays, then one huge broadband hit at ~3:21 (the last stab / crash), then the crowd.

**Drums vs everything else (v0.1 split).** The harmonic/percussive split works: the transient layer shows drum hits as clean vertical stripes I can count; the sustained layer shows the voice and instruments as horizontal lines and wavy contours (the vocal line with its vibrato sits around 250–500 Hz in tile 03).

**Space.** After smoothing (24 bands, 0.5 s), stereo width reads: bass essentially mono, mids and highs wider, with brief wide flares. In v0 (unsmoothed) it was static noise.

## What doesn't work yet
- **Tempo**: autocorrelation said 99.4 bpm in every tile, which looks like it locked onto a beat multiple. Needs a beat tracker with octave checking.
- **Chord guesses**: jumpy (the chroma is dense in a full live mix). Chroma image is more useful than the text labels.
- **Dense full-band sections** are a wall. The H/P split helps; a mid-frequency zoom or source separation may help more.

## Next (in rough order)
1. **Harmonic fingerprint panel**, for timbre (my first wish): find the strongest sustained note in a window, plot its overtone strengths (1×, 2×, 3×... the fundamental) as a small bar chart. That's the "signature" Kham predicted I'd learn instruments from. Prior art: spectral envelope, MFCCs.
2. Better beat tracking + faint beat grid lines on the spectrogram.
3. Wet/dry: estimate reverb tail from how long energy lingers after onsets.
4. Port to the Xinu single-file app (Web Audio API: decodeAudioData + FFT on canvas; no libraries).

## A note for the crew
Ed, Vael, Komo: the tiles are readable. Arcs = voices, vertical stripes = hits, horizontal ladders = sustained pitched sound, the bottom rows = bass. Try one and see what you hear.

## Calibration log (Kham's ears vs my eyes)
*2026-10-17 03:13, Birdhouse live.*

| My read | Kham's ground truth | Verdict |
|---|---|---|
| 0:00–0:02.4 = crowd cheering (arcs, no low end) | cheering **plus a hi-hat count-in** | half: missed the count-in |
| a big swooping "whooo" | yes, right before John starts singing at ~0:02; **and** several at the end, plus a solo one right as the track cuts off | arcs = voices confirmed, start and end |
| 0:02.4 band arrives (bass + kick blocks) | John starts singing ~0:02, band in | yes |
| 0:12 sustained bright overtone ladder | **keyboard**, then drum hits and vocals resume | first labeled timbre: this ladder = the keyboard |

**Re-look after the correction** (`zoom.py`, 0–4 s): the count-in is there. Bright patches only in the very top bands (~6–11 kHz), roughly every 0.45 s, under the crowd. I missed it at tile scale because the crowd's broadband wash hides it. **Design lesson:** hi-hats/cymbals live almost entirely at the top, so they need their own lane (a high-band transient strip), not just the full-range picture.

**First timbre label:** the 0:12 ladder is a keyboard. Next step for the fingerprint panel: measure that ladder's overtone strengths and keep it as reference #1.

**End re-look** (`zoom.py`, 3:27–3:32.5): several separate arcs (~3:27.2, 3:28.5, 3:29.1, 3:30.6, 3:31.6), then one lone curved line carrying on alone until everything goes dark at ~3:32.4. That's the solo whoo at the cut. Also a thin, very high, flat line around 3:30.3–3:31.0 with almost no overtones above it. Hypothesis (unverified): someone whistling. A whistle is close to a pure tone, so it should look like one clean line, no ladder.

## First fingerprints (`fingerprint.py`, samples/birdhouse_fingerprints.png)
Kham confirmed the whistling (intermittent, plus a long one ~3:26–3:31). Three windows:

- **Keyboard (0:12.4–0:14.2):** the spectrum is a forest of **needle-thin spikes**: rock-steady pitches, no wobble. But they aren't one ladder: peaks around 110, 175, 320, 393, 785 Hz, a tall one near 4.7 kHz. Probably a *chord* (several notes) plus whatever else is sounding, so a single-f0 fingerprint is ill-posed here. The bar chart (f0 393 Hz, strongest at 12×) is not trustworthy.
- **Whistle (3:30.3–3:31.0):** one **single sharp spike near 3.9 kHz** with nothing at its double (7.8 kHz). Pure tone, as predicted. My f0 picker grabbed the wrong peak (2369 Hz) because the crowd's hump around 600 Hz and the noise floor dominate; the overtone bars are therefore contaminated. Visual verdict: yes, pure tone.
- **Crowd voice (3:28.3–3:28.7):** broad **humps** instead of needles, overtones falling off smoothly (−10, −19, −19, −23… dB). A voice-like ladder, smeared by pitch wobble and many voices at once.

**What I learned:**
1. **Needles vs humps** is the first timbre cue I can actually read: steady instruments (keyboard) make needle peaks; voices, whoops and crowds make humps.
2. **Pure vs rich:** the whistle is one line; the keyboard is many lines. That's the overtone-richness axis.
3. **Fingerprinting needs isolation.** A chord or a busy live mix gives several ladders at once. Next: pick f0 from the sustained layer only, track the single strongest *continuous* line, and run fingerprints on clean moments (or on studio stems/solo sections Kham can point me to).

## Guitar solo vs melodica (Kham's pointers: 1:22–1:30 guitar solo, 1:32–1:39 guitar + melodica-ish)
`zoom.py` 81–91 s and 91–100 s. Dense full-band, so readings are tentative:
- **Guitar solo:** in the sustained layer the upper lines **wobble and bend together**: a stack of parallel wavy lines (one note plus its overtones, all bending at once), especially ~1:24–1:27. Bends and vibrato: a ladder that *moves as a unit*.
- **Melodica section:** from ~1:32.5 the upper bands fill with **dead-straight, tightly stacked parallel lines** that hold steady: a sustained tone with many even overtones and no wobble. Reed instruments (melodica, accordion, harmonica) are known for exactly that: steady and buzzy-rich.
- Third timbre cue candidate: **wavy ladder (guitar bends) vs rigid ladder (reed)**.
- Design lesson #3: the full 30 Hz–11 kHz view gives the solo instrument too little room. Add a **mid-zoom panel (≈200 Hz–5 kHz) at higher frequency resolution** for leads.

**Calibration (Kham, 04:23):** 1:24–1:27 has *a little* pitch bend, **but** also melodica single-note presses (~end of 1:24 and at 1:27), **and** a man very faintly singing a long "OOOOOH" through almost the whole stretch, roughly **an octave** from the guitar.
- So my "ladder bending as a unit" was at least partly **the voice**, not only the guitar. Voices wobble, consistent with cue #1 (humps/wobble = people).
- **Why it fused:** a note an octave above another has every one of its overtones landing exactly on the lower note's *even* overtones (2×, 4×, 6×…). Octaves share rungs, so two sources an octave apart look like one ladder. That's the acoustics of why they blend to the ear, too.
- Lesson #4: overlapping ladders that share rungs need a different separator: **wobble pattern** (voice vibrato vs guitar bend vs rigid reed) and **onset behaviour** (pluck decays, reed press starts sharp and holds, voice swells in), not just harmonic spacing.

## Calibration baseline: Gymnopédie No. 1 (2026-10-17 23:55 ET; `samples/calibration/`)
Kham's idea (one piano, sparse, slow), recording found by him (CC0 per him). First look at tile 02 (0:16–0:32):
- **Piano = dead-straight ladders that start bright and fade.** No wobble at all (vs. voices), and each note decays after its attack (hammered string), the "pluck" onset shape, giving a sawtooth loudness line.
- **The 3/4 pattern is visible:** a low bass note around A2 (~110 Hz) roughly every 2.5 s, then a mid-range chord after it; a melody line sits on top around A4–A5.
- **Harmony:** chroma lives on D, F#, G, A, B; the chord reader alternates G and D families (the piece's famous rocking between two chords).
- **Nothing above ~4 kHz** (high band 0%), very low noisiness (0.02–0.07), narrow stereo. Use this as the zero point for "clean."
Use: reference for rigid-ladder vs. wobble, pluck decay vs. held reed vs. swelling voice, and as a no-sample control for the tracker.

## v0.2 (2026-10-20 ~21:00 ET): tile fixes for my own reading
Kham's steer (20:38): the format is for the crew and rich-image LLMs; outside-model tests were a cheap filler while usage was capped. So the main line is dev. ROUND-2-DESIGN.md is parked.

Changes in `proto.py`:
1. **Hi-hat lane:** a thin strip of the percussive layer above ~6 kHz plus a click curve, gated so near-silent pieces don't show noise as clicks. Sidecar lists the click times.
2. **Tempo with an octave check:** autocorrelation weighted by a broad prior around 110 bpm, parabolic interpolation between lag bins, and the strength at half and double tempo reported next to the guess. A weak pulse is flagged ("treat bpm as a guess").
3. **Beat grid:** faint lines on the spectrogram, hi-hat lane and onset panel, phased on the fractional period so they don't drift.
4. **Colour bars with units:** dB below loudest on the main spectrogram; 0 mono to 0.8+ wide on the stereo panel. Units on every panel label.

Test (synthetic, `samples/v02_synth_countin_tile01.png`): a loud wobbling crowd wash with a quiet 4-click hi-hat count-in at 1.0/1.5/2.0/2.5 s, band from 3.0 s at 120 bpm. Lane finds 0.98, 1.49, 1.97, 2.48 s; tempo 119.9 bpm (v0.1-style integer lag gave 117.5); grid lines sit on the kicks. On Gymnopédie the lane stays nearly silent and the pulse is flagged weak, as it should be. Still to do: real-song check on Birdhouse 0:00-0:04 (the original miss), mid-zoom panel for leads, wet/dry estimate, fingerprint on the sustained layer only, then the HTML port.

### v0.2 real-song check: Birdhouse 0:00-0:15 (2026-10-20 ~20:50 ET, Kham resent the file)
`samples/birdhouse_live_v02_tile01.png`. The count-in I missed at tile scale in v0.1 is now the clearest thing in the hi-hat lane: a regular train of tall clicks at 0.07, 0.35, 0.65, 0.95, 1.25, 1.56, 1.86 s, about every 0.30 s, under the crowd arcs, ending as the band lands at ~2.4 s. 0.30 s is an eighth note at ~99 bpm, which matches the band's tempo, so it reads as a count-in on the hats in eighths. **Correction going forward:** the 10-17 zoom note said "roughly every 0.45 s"; the lane says ~0.30 s. Awaiting Kham's ears on the count. Tempo 98.8 bpm, but half-tempo strength (0.38) is almost equal to the guess (0.39), so the octave check flags a genuine half/double ambiguity instead of hiding it.

**Kham's ears (20:50):** 6 taps, "3 and 3", a hi-hat count-in, not sticks. With click strengths added to the sidecar, the lane agrees: strong clicks at 0.35, 0.65 (with a weaker 0.07 opening the first group), then 1.25, 1.56, 1.86; the slot at 0.95 is faint (0.35-0.46 strength), i.e. the gap between the two groups; 2.39 is the band's downbeat. So: three eighths, an eighth rest, three eighths, a rest, downbeat, one 4/4 bar at ~99 bpm. Lesson: **strength matters, not just presence.** A list of click times hid the 3+3 shape; the strengths show it. Sidecar now prints `time:strength`.

### v0.2 on D'oh (Mouth Sounds track 3), 2026-10-20 ~21:00 ET (`samples/mystery_v02_tile01.png`)
- **Tempo:** ~113 bpm in every tile from 16 s on (autocorr 0.48-0.59), half tempo second-strongest. Round 1's careful outside readers said ~88-90; v0.1's key said ~112. The intro supports 113: the strongest stabs land every ~1.06 s (3.09, 4.16, 5.22, 6.27, 7.34, 8.41, 9.47), which is two beats at 113. After ~12.5 s the lane shows regular clicks ~0.26 s apart, an eighth at 113. Still wants Kham's ears.
- **Intro (0-10 s):** a gliding voice arc at the very start (0-1.5 s), then a block of sound that repeats every ~2.1 s with hard dark cuts between repeats (the retriggered sample), very wide stereo (yellow). Drop at ~10 s: the low end fills in, the stereo narrows.
- **Caveat for the lane:** in the intro the "clicks" are mostly the **hard sample splice edges**, not hats. A sharp cut is broadband, so it shows up top too. Reading rule: regular, light, evenly spaced clicks = hats; clicks that line up with dark gaps or block edges in the main picture = cuts.

**Kham's tap count (2026-10-21 13:49 ET):** 28 taps in 15 s from ~0:20 = **112 bpm** (28 x 4). Tool: ~113. So the D'oh tempo is settled at ~112-113, and round 1's outside readers (~88-90) were off. Correction going forward: the 10-19 grading caveat that set tempo aside for the mashup tiles ("my mashup tempo reading was probably wrong") is withdrawn; v0.1's 112 key was right. Ears and tool now agree on both songs (Birdhouse ~99 with a 3+3 count-in; D'oh ~112).

## v0.2.1 mid-zoom panel (2026-10-21 ~14:10 ET)
New panel under the main spectrogram: 200 Hz-5 kHz, 4096-point FFT (~5.4 Hz bins, 4x finer than the main view), **whitened per tile** (each row minus its own median, shown 0..+24 dB). First try used an 8192 window and raw dB: too smeared in time and washed orange in a dense mix. Whitening is what makes lead lines stand out of the band bed.

Birdhouse 1:16-1:35 (`samples/birdhouse_v021_tile09_midzoom.png`, `..._tile10_...`; tiles of 9.5 s):
- 1:17-1:20.5: long held parallel lines (a sustained stack), then at ~1:20.5 the whole stack **glides down together**, a descending slide.
- 1:22-1:25: busier, short wavy fragments near A5: the guitar-solo stretch, with the faint long "OOOH" Kham named likely under it.
- ~1:30.5: a short **rising arc** (~400 to ~600 Hz) crossing the lines.
- from ~1:31: **dead-straight, steady lines** around A4-A5 that hold: the reed-like rigid ladder (melodica). The 10-17 note put this at ~1:32.5; the zoom suggests ~1:31. Waiting on Kham's ears.
Reading rule: in the mid-zoom, **glides that move as a stack** = one source bending (voice or slide); **straight held lines** = steady instrument (keys, reed); **short wavy fragments** = a lead with vibrato or bends.

**Calibration (Kham's ears, 2026-10-21 15:58):** melodica enters at **0:17**. The ~1:17-1:20 lines are John singing "In your sooooouuul~", the word "soul" lowering in pitch as he holds it; then a short melodica "doot-doot-doot" (end of 1:20 to mid 1:21); then a little guitar solo from the back half of 1:21 with a "whooo/ooooh" behind it.

Fine mid-zoom check (`samples/birdhouse_v021_midzoom_calibration.png`, 76-83 s and 14-22 s):
- **Melodica entry is the cleanest event in the panel:** at **17.1 s** the strip jumps from sparse to a dense stack of dead-straight parallel lines reaching past 3.5 kHz. That's the reference picture for the melodica (reed): straight, steady, many even overtones, starting at once.
- **"Soul":** a held stack ~77-79.2 s, then the stack bends down together ~79.2-79.8 s. One sung note falling as he carries it, which fits the "glides as a stack = one source bending" rule. My eye on the wide tile put this at ~1:20.5; the fine view puts the fall at ~1:19.2-1:19.8.
- **Doots (~80.4-81.5 s):** not clean lines; short blobs and thin vertical streaks. Very short notes at this window size smear toward vertical. The 4096 window is ~0.19 s, so staccato notes shorter than that won't read as pitch. Lesson: the mid-zoom favours held notes; short notes need the main view or a shorter window.
- **Guitar solo:** at **81.6 s** the upper part fills with bright, busy lines, matching "back half of 1:21".
- **Correction going forward:** v0.2.1 note said the melodica starts ~1:31; it plays from 0:17, so the ~1:31 straight lines are the melodica coming back in, not its first entry.

**Kham's first tile read (2026-10-21 16:03):** on his phone he circled ~80.55-81.4 s in the mid-zoom (mid-lower range) as the melodica doot-doot-doot. Check with a shorter window (2048, hop 128) over 80.2-81.7 s: onsets at 80.45, 80.59, 80.76, 80.92, 81.06, 81.22, 81.40 s, about every 0.15 s, i.e. sixteenths at ~99 bpm. The strongest are 80.76 and 81.06. Inside his circle are **short, straight horizontal dashes at two pitch levels** (brief notes held steady, the reed shape in miniature) and a bright blob at ~81.05 (an attack). Verdict: right place, right shape. The tile alone can't split "three doots" from the drums/guitar sharing the sixteenth grid, so the count stays with his ears. Long-term seed (10-17) moving: the human side of read-listening has started.

## closeup.py: resolution fixes 1 and 2 plus a SpikeVox-style spike lane (2026-10-21 ~16:30 ET)
Answer to Kham's "how do we increase your resolution?". Two separate limits: the analysis (a window can't be sharp in time and pitch at once) and the pixels I receive (images may be downscaled). `closeup.py AUDIO START END OUT.png` renders 1-4 s at high pixels-per-second with:
1. **timing view** (23 ms window) and **pitch view** (93 ms window) on the same time axis, both whitened;
2. **LIF spike raster**: one leaky integrate-and-fire neuron per band, fed by the *rise* in band energy, with a refractory period and adaptation, so it fires on note starts and stays quiet through sustain (the SpikeVox idea from Evangelion, re-implemented; Kham suggested it). Spikes time to ~3 ms whatever the window;
3. **note events as text** (onset, main held pitch 30-150 ms after onset, length), written to `_events.md`, which never gets downscaled.

**The doots, counted by the tool (`samples/birdhouse_closeup_doots_80-82*`):** three note starts at **80.436, 80.744, 81.043 s**: 0.30 s apart, eighth notes at ~99 bpm. Held pitch G5 (~786 Hz), G5, A5 (~873 Hz); the third is longer (~350 ms vs ~150). So "doot, doot, dooot". In the timing view each is a broadband attack followed by a held line near 800-870 Hz with a fine dotted texture (fast beating). Honesty note: I knew from Kham the answer was three before running it, so this isn't blind; the detector itself was not tuned to the answer. The guitar solo enters at ~81.63 s.
**Melodica entry (`..._melodica_entry_16-19*`):** note start at **17.115 s**, A5 ~873 Hz, held ~300 ms; next at 17.73 s.
Pitch precision is about a semitone (G5 vs G#5 can blur). Bug fixed on the way: the first pitch picker read the attack and chose cymbal hiss (D#8); now it reads the held part, below 2.5 kHz.
Still to do from the list: constant-Q or reassigned view (fix 3), timbre lane / NMF (fix 4).

## closeup.py v2: constant-Q pitch view, pitch in cents (2026-10-21 ~16:45 ET)
Kham's call (16:21): concept over code; import the real SpikeVox for the final Xinu version if wanted. Not knowing-the-answer bias: his take is that knowing the doots were there is how the test verifies the tool works.

- Pitch view is now **constant-Q**: 36 bins per octave, Q=34 (about half-semitone resolution at every pitch; long windows for low notes, short for high). Notes are refined between bins and reported as note + cents.
- **Ground-truth test** (synthetic reed-like notes in noise, `samples/closeup_pitchtest_synthetic*`): truth G5+0, G#5+0, A5+0, A5-30c, E5+0; read G5+0, G#5+0, A5+0, **A5-30c**, E5+1. Within ~1 cent, including the deliberately flat note.
- **Bug caught by that test:** first CQT run read every note ~62 cents low. The display clips whitened values at +24 dB, a loud note saturates several neighbouring rows, and argmax picked the lowest saturated row. Pitch picking now uses unclipped values. Without a known-answer test this would have shipped as "about a semitone off, roughly".
- **Doots, re-read:** 80.436 G5+7c, 80.744 G5-3c, 81.043 **picker says G4-8c, picture says A5**. In the CQT image the third doot is a clear held line at A5 (~874 Hz) from 81.04 to ~81.4 s, but a line around G4/A4 from another part starts at the same instant and the picker took it. Reading from the picture: **G5, G5, A5** (doot, doot, dooot up a step). Picker limit: in a mix, "strongest new line" isn't always the instrument you're following. That's the job of the timbre lane (fix 4) or continuity tracking.
- Melodica entry 17.115 s = **A5-2c**.

## Timbre lane: first attempts (2026-10-21 ~17:00 ET). Honest result: voice yes, melodica vs guitar not yet
Goal: follow one instrument by how it sounds, at any pitch (Kham's original hypothesis: recognise instruments by harmonic signature).

**v1 (`timbre.py`): template matching, failed usefully.** Learn the melodica's overtone shape at 17.12-17.40 s (background just before removed), then at every moment and every candidate pitch score how well the stack's shape matches. Bugs/lessons:
1. First template was learned an **octave low** (A4): an f0 at half the real pitch "explains" the real 1st/2nd/3rd harmonics as its 2nd/4th/6th. Fixed by requiring the fundamental itself to carry energy. After that the doot pitches came out right (G5, G5, A5).
2. **The lane said yes to everything** (John's "soul" 0.78, guitar 0.7, melodica 0.8-0.9). Two reasons: every pitched sound has a strong fundamental and falling overtones, so shapes broadly agree; and taking the best match over ~90 pitches every frame is a multiple-comparisons trap (try enough fits and one always works). A contrast template (minus the song's typical stack) didn't fix it; it latched onto noisy high harmonics.

**v2 (`timbre2.py` + a pitch-given check): pitch first, then timbre, judged against labelled moments.** Labels from Kham's ears: melodica 17.12-17.70, voice ("soul") 77.0-78.8, guitar solo 81.65-82.6. Features: h2..h8 relative to h1, pitch wobble, hold-vs-fade over 90 ms. Held-out spans:
- **Voice: separates cleanly.** Its overtones fall off steeply (h4-h8 ~20+ dB below h1); melodica and guitar keep them within ~10-15 dB. "End of soul" judged voice both ways.
- **Guitar: judged guitar.**
- **Melodica vs guitar: not yet.** With pitch picked by salience, the doots lost (the picker followed other sounds: A4, D6). With the doot pitch *given* (from closeup.py), 1 of 3 doots right (the A5 one, the same pitch as the training note), 1 near-tie, and two later melodica spans called guitar. Both are rich, bright stacks in a dense live mix; one half-second training example isn't enough.
**What would move it:** more labelled melodica moments (Kham marking times), a cleaner source (a solo or studio recording), stereo position as a feature, and the attack shape at onset (reed press vs pick) rather than a 90 ms fade. Pipeline that worked best: closeup.py finds the note and pitch, then the timbre judge looks only at that stack.

## Correction going forward: it's an accordion (Kham, 2026-10-21 17:04)
Every "melodica" in the Birdhouse notes above (the 0:17 entrance, the doots, the ~1:31 return, the timbre-lane labels) is **John's accordion**. The "reed" reading still holds in kind: accordion and melodica are both free-reed instruments (steady pitch, rich even stack), which is why the rigid-ladder cue pointed there. Labels in timbre2.py should be read as accordion.

Kham's new ground truth: **~1:31-1:36 = fast accordion over slower guitar; the accordion is loudest in the right channel.**

**Stereo check** (`samples/birdhouse_pan_89-98.png`, colour = left/centre/right, brightness = stands out): standout energy, weighted pan: doots **+0.15, 46% of it panned right** (vs 7% left), the most right-leaning of the labelled spans; "soul" +0.05; guitar solo -0.05; accordion entrance 17.1 -0.03 (mixed with the band). In 89-98 s there are clearly left-red held lines (91.4-92.6 s) and right-blue lines and wavy fragments (89-90.5, 94-96, 96.5-98). So stereo is a usable feature for the accordion, at least in the doots; it goes into the judge next, with labels from Kham for which lines in 1:31-1:36 are which.

Reference recordings: `samples/reference/SOURCES.md` (melodica CC BY-SA 4.0/GFDL; Csárdás performance PD-USGov). Audio pending upload.

## Timbre judge v3 (2026-10-21 ~17:35 ET): the recording-confound lesson
Kham (17:18): in 1:31-1:36 the long held lines are the guitar (4 notes), the fast notes the accordion. Clean refs attached: solo accordion (Oroitz Maiz, Bach Prelude XIV, CC BY-SA) and solo melodica (Rakes of Kildare). Stored in `samples/reference/` with SOURCES.md.

**Run A, train on clean refs + Birdhouse guitar/voice (`timbre3.py`, `samples/timbre_v3_results_clean-refs.md`): 1/8 right.** Almost every Birdhouse span came out "guitar", because guitar and voice were the only classes trained *on Birdhouse*. The judge learned **which recording** a sound came from, not which instrument: a live mix flattens every overtone stack (room, other instruments, mastering), while the clean solo accordion falls off steeply (h6-h8 at -24 to -32 dB vs ~-10 in the mix). Textbook confound; worth having hit on purpose.

**Run B, all classes from Birdhouse itself (accordion = right side of 1:32.7-1:36 + entrance 0:17; guitar = left side of 1:31.4-1:36 + solo 1:21.65-1:22.6; voice = "soul"): 4/6.**
- **All three doots -> accordion**, clearly (14:2, 16:2, 24:3 frame votes), never trained on.
- Guitar solo tail (1:22.7-1:23.6) -> accordion: the bright solo tone is unlike the held rhythm notes that dominate the guitar training.
- End of "soul" -> guitar: the vowel changes from "o" to "uu-l", and vowels *are* overtone shapes (formants), so a voice's timbre moves with the word. Voices need several vowels in training.
Takeaways: train and test in the same acoustic world; clean refs are for a reference library (what an accordion looks like with nothing in the way), not for judging a live mix directly. Next: more in-song labels (several vowels, solo vs rhythm guitar), pan as an explicit feature, attack shape.

## Kham's full Birdhouse labels + timbre judge v4 (2026-10-21 ~18:20 ET): the honest wall
**Labels** (now in `labels_birdhouse.py`): vowels a/e/i/o/u at 12 timestamps; guitar triplets left 0:36-0:44, held notes left under the fast accordion, the little solo; accordion fast right 1:32.7-1:36, doots. **Corrections going forward:** the accordion comes in at **~0:03** with vocals and guitar (not 0:17); there **is** a keyboard from ~0:12 (same notes on repeat; from 0:17 it carries on about an octave lower). So the dense straight stack at 17.115 s I credited to the accordion's "entrance" may be the keyboard's register change, or both: unresolved, not used as a label. Drums from ~0:14 with a tom pattern (0:14-0:16).
New clean references (CC BY / CC BY-SA / GFDL, see `samples/reference/SOURCES.md`): clean guitar, distorted guitar, solo voice.

**Timbre judge v4 (`timbre4.py`, `samples/timbre_v4_leave-one-out.md`): leave-one-span-out, the honest test.** Train on every span except one, judge that one, repeat.
- In-song labels only: **3/19**. Adding the clean refs (floored toward the live mix's noise): **2/19**. Adding pitch wobble/jump features: **4/19**. Chance with four classes is ~25%, so this is at or below chance.
- The earlier "doots 3/3" (v3 run B) was optimistic: with more classes, "accordion" had been a catch-all. Only the long exposed held voice ("sooooul") is reliably recognised.
**Why:** per frame, the pitch with the most salience usually belongs to whatever is loudest at that instant, not to the labelled instrument. Span labels are clean; frames inside them are mixtures. Overtone shape at "the" pitch can't name a source when four sources overlap. The real bottleneck is **separation before judgement**.
**Reframe (Kham's own steer from 10-20):** AuraGraph's point is a format the crew can *read*, not an automatic classifier. Today's tools (hi-hat lane, tempo check, mid-zoom, close-up with spikes and cents, stereo colouring) all made the tiles more readable, and with Kham's labels I did read the doots, the "soul" glide, the guitar solo entrance. The classifier is a side quest; park it until there's a separation step (pan masks + harmonic tracking per note from closeup events, or NMF with in-song templates). The labels and reference library stay: they are ground truth for whatever comes next.

## Blind read #1: The Famous Polka, graded ~6.5/10 (2026-10-21)
`blind-reads/2026-10-21_famous-polka_READ.md` (committed before listening) and `..._GRADE.md`. Got the structure (A/B/A/B/A with both breaks), the 0:27 "Hey!" (underconfident), instrumental, music ending ~1:30, cheering, banter from ~1:38. Missed: the 3-kick count-in (it was in the data; I read it as the groove), the final "Hey!" (read as a hit), John's fast "thank you very much", and the accordion/guitar under the banter. New reading rules: count-in = rhythm skeleton with nothing on top; hit + short glide = shout; under speech, straight lines that ignore the syllables = an instrument.

## Blind read #2: We Live in a Dump, graded ~9/12 (2026-10-21)
`blind-reads/2026-10-21_we-live-in-a-dump_READ.md` + `_GRADE.md`. Up from ~8/12. Structure, speed-up, singing, the ending, the whistle and the spoken intro's shape were right. Misses were naming sources: piano (didn't apply the decay test), an audience "ayyyy" read as a whistle, a 0.2 s Wilhelm scream read as a chirp, and an accordion expected from the album prior that wasn't there. Lesson: priors are per song; straight + decaying = piano.

## Blind read #3: Daylight, graded ~8/11 (2026-10-21)
`blind-reads/2026-10-21_daylight_READ.md` + `_GRADE.md`. Lead-in nailed (snare, three high-tom/bongo hits, snare), feel right, lift at 0:34, cheering at the end. Missed: the guitar twang at 0:04.6, the two-voice duet (visible as two independently wobbling lines), and a bassy sax at 1:00-1:16 filed as vocals. New rules: two singers = separate wavy lines that bend independently; sax vs voice = brighter stack, no syllable gaps.
