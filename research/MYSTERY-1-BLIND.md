# Mystery track #1: blind read (committed BEFORE grading)

Kham's pick, a Mouth-style mashup, sent 2026-10-17 07:05 ET with no title or hints. Length 1:53.7.
Tools: proto.py (8 tiles @16 s), zoom.py on 0–10.5 s and 23–32 s. Samples: `samples/mystery_*`.

## Guesses
1. **Intro (0–10 s) is a cut-up, stop-start collage, not a band playing.**
   - 0–1.5 s: a voice-like phrase, wobbly rich ladder gliding *up* (voice, maybe talky/sung).
   - 1.5 s: hard cut, bright full-band hit, then a *falling* glide (1.5–2.2 s).
   - Then the same ~1.3 s block three times (≈2.8–4.1, 4.9–6.2, 7.0–8.4): a held line with little regular dips + plucky/chordal hits. Identical shape each time = **one sample repeated**, not played again.
   - Between blocks (≈4.1 and 6.25): a full-height stab with a fast tail into near-silence. Dramatic hit-then-gap edits.
   - 8.4–9.9 s: the rising voice phrase from 0 s comes back (same shape) = a bookend.
   - **10.0 s: the drop.** Bass and full kit arrive at once.
2. **Body (10 s–1:52) = an instrumental bed from one song + vocals from another.**
   - Bed: heavy blocky bass (55–111 Hz), steady drums, ~112 BPM. Key reads as **F major / D minor** (chroma: D, C, F rows dominate; chords F, Dm, C, some Gm).
   - Lead vocal: wobbly curving lines ~400–900 Hz riding on top.
   - Possible **third source**: higher arch-shaped wobbly lines ~2–4 kHz at ~29.5–31.5 s (and elsewhere), voice-like but too high for the lead. Guess: a second, maybe pitched-up, vocal.
3. **Sections by numbers:**
   - 48–64 s: low end jumps to 68%, mids drop to 16% → vocals thin out, bass-heavy break/bridge.
   - 64–96 s: stereo widest (0.65) → chorus-like, bigger.
   - 96–112 s: brightest and noisiest of the track → final big chorus, cymbals up.
   - 112–113.7 s: sudden drop to quiet mid-only tail → hard stop with a little leftover sound.
4. **Number of sources:** at least 2 songs, likely 3 (bed + lead vocal + intro/high-voice samples). Confidence: medium on the bed/vocal split; low on exactly how many.

## Grading (Kham, 2026-10-17 07:16 ET), added after the blind read
- Track: **Mouth Sounds, track 3, "D'oh"** (1:54).
- The intro "voice-like" phrases are **Homer Simpson's "D'oh!", pitch-corrected and played as a percussion sample**. So: right that they were a voice (wobbly ladder) and right that they were one sample repeated, wrong about their *role* (I read them as a vocal bookend + separate repeated block; they're the drum kit).
- Lesson #5 for FINDINGS: in a mashup, a voice ladder can be doing a drum's job. Role ≠ source. Read the timing (on the grid, repeated identically) to get the role, and the shape (wobble, overtones) to get the source.
- Overall: "genuinely really good" for a blind read. Body sources: still to look up / ask Kham (lemondemon.fandom D'oh page and WhoSampled wouldn't load).

## Sources (Kham found them: Lemon Demon wiki + WhoSampled screenshots, 07:22–07:24)
Six sources, per WhoSampled:
- Homer Simpson, "D'oh!" (The Simpsons): dialogue, pitch-corrected, played as percussion
- Austin Powers, "Yeah baby!" (1997 film): dialogue, recurring drop-in
- Fred Newman, *Doug* theme: vocals (the verse section)
- Sir Mix-a-Lot, "Baby Got Back": multiple elements (the looped hook section)
- Dave Matthews Band, "Ants Marching": multiple elements (likely part of the bed; check)
- Talking Heads, "Once in a Lifetime": vocals (final section)
Kham also pasted the full lyrics so I could follow the structure (not copied here).

## Grade, roughly
- Intro collage: **right that it was a collage of repeated samples**, wrong about role (Homer = drums).
- "Two songs, likely three": **undercounted.** It's six.
- "A third, higher, maybe pitched-up voice": the "yeah baby" drop-ins are a pitched voice sample that recurs through the track. Plausible match; verify by timestamp tomorrow.
- Section guesses (48–64 s bass-heavy/thin vocals, final bright push, hard stop): need timestamps against the vocal map. Hypothesis to test: the bass-heavy stretch = the looped hook section.
- Funniest result: Kham's "Austin Powers pitched up and bitcrushed" joke at 07:01 was real. He picked this track because of it.

## Next test (agreed with Kham, 07:35)
Self-similarity map of the whole track (which seconds look like which other seconds) → find loops and section boundaries from sound alone → only then check against Kham's lyric map. Purpose: tell "lyrics help me see" apart from "lyrics tell me what to see."

## Self-similarity test (2026-10-17 20:40 ET), sound only, written BEFORE comparing to the lyric map
Tool: `selfsim.py` (chroma + timbre, 0.25 s frames, diagonal smoothing, checkerboard novelty). Image: `samples/mystery_selfsim.png`.
- **Section boundaries (novelty peaks):** 9.5, 16.9, 35.5, 42.4, 51.9 s. Strongest by far: 9.5 s (the drop).
- **Intro returns at the end:** the 0–10 s block lights up again at ~110–113 s → the track closes on intro material (the D'oh/"yeah baby" kit?).
- **Intro material also echoes at ~12–17 s and ~33–42 s** (stripes in the intro rows) → the D'oh percussion keeps poking through the early body, less after ~43 s.
- **Body = loop-built:** dense parallel diagonals everywhere; strongest repeat period ≈ **4.28 s** (= 2 bars at ~112 BPM), also 2.14 s (1 bar) and 8.57 s (4 bars).
- **After ~52 s no strong boundaries:** one long sustained looped section to the end, with a mild bump ~93 s. Guess: the looped-hook section starts ~42–52 s and the final section (the last source) layers on top of the loop rather than replacing it, which is why the detector doesn't see a hard change.
- Ordering check vs. Kham's lyric map (no timestamps in it): intro drops → verse section → long repeated-hook section → final section over the hook. Plausibly matches; needs Kham's ears for actual times.

## Kham's ears on the intro (2026-10-17 20:51 ET)
- ~9 s = song starts proper (matches the 9.5 s boundary).
- 0 s: **down-pitched "Yeah baby!"** over the D'oh-D'oh-D'oh; ~8 s: **up-pitched "yeah baby"**. So my "voice phrase + bookend" was the same sample at two pitches. Quick check: f0 ≈ 140 Hz at 0–1.5 s vs ≈ 194 Hz at 8.4–9.9 s (the strongest peak jumps 151 → 398 Hz); the second is higher, as he said.
- The D'ohs sound reedy, harmonica-like (filtered, or doubled with the source song's harmonica): explains the "held line with little regular dips" I saw, a rigid reed-style ladder. The D'oh kit runs through the whole song; extra D'ohs are also tied to the vocal track.
- Lesson #6: same sample at different pitches looks like "same shape, shifted up". Check whether a returning phrase is a transposition before calling it a new source. Kham: this will be the most-used lesson for Mouth albums and sample-heavy music generally (hip hop etc.).
- Pixie saw the selfsim image: "I love that!" / "that's really cool."

## Ground-truth timeline (Kham, listening, 2026-10-17 21:05 ET) vs. selfsim boundaries
| Kham's ears | Event | selfsim | Score |
|---|---|---|---|
| ~9 s | song proper starts | 9.5 s | ✅ |
| ~19 s | vocals start (Ants Marching verse) | 16.9 s | ~ (2 s early; drums/bed change before the vocal?) |
| ~33 s | → "I like big butts…", then looped | 35.5 s | ✅ (~2.5 s) |
| ~43 s | Doug theme starts | 42.4 s | ✅ |
| ~48–49 s | high "yeah baby" + laugh track | — | missed (short event, not a section) |
| ~51 s | Porkchop barks | — | (inside the 51.9 peak) |
| ~52 s | Doug "doo-doo" melody starts | 51.9 s | ✅ |
| 52–70 s | mostly looped hook + Doug doo-doos | no boundary | ✅ matches "one long loop" |
| ~1:10 (70 s) | Once in a Lifetime verse starts | — | **missed**: layered over the loop, as predicted, so no hard change |
| ~1:34 (94 s) | "Letting the days go by" section | mild bump ~93 s | ✅ (weak but there) |
| ~1:52 | everything drops out, ends on the last vocal line | ~110–113 corner | ✅ timing; ❌ my *reason* |

**Correction:** I said "the intro returns at the end." Wrong reason. The corners lit up because both the intro and the ending are *sparse* (no bass loop), so they resemble each other by emptiness, not by sharing material. Lesson #7: self-similarity can match on *absence*; check what's actually present before calling it a return.
**Score:** 5 of 7 structural changes found from sound alone; the misses are exactly the "layered on top of a loop" kind, which the novelty detector can't see by design. Fix idea: per-layer novelty (run selfsim separately on the vocal band vs. the bass/drum band).

## Kham (21:07): the looped hook gets progressively more crushed and wobbly
Quick whole-mix check (10 s windows, 35–115 s): high-band (4–10 kHz) vs mid energy rises 0.70 → 1.02 from 35 to 75 s, dips at 75–95 s, peaks 1.19 at 95–105 s; flatness ~flat. **Inconclusive**: other layers (Doug theme, cymbals, the final section) enter at the same times, so the whole mix can't isolate one loop's degradation. Needs stems or the sample tracker: track the hook snippet and measure its own noise and pitch wobble per repeat. Good target test for the sample tracker.

## Layered vocals, final section (zoom 96–102 s, `samples/mystery_zoom_96-102.png`)
Kham: the last part stacks the original sampled song, the Doug theme, the hook loop, and the final source's multi-tracked vocal; does the stacking make it look like an instrument?
Read: the vocal-range lines (bands ~75–110) are **thick and smeared** rather than crisp single lines: several near-identical voices at slightly different pitches/timings blur into one fat band (a "chorus" look, closer to a pad than a solo voice). But they still **curve together with speech-like contours** (e.g. the rising line ~99.8–100.5 s), which a sustained instrument mostly doesn't do. Rule of thumb (hypothesis): stacked voices = thick + wobbly + speech-shaped; pad/synth = thick + rigid. Broadband vertical bursts (~every 0.5 s) could be consonants or cymbals — can't tell apart in the full mix.
- Kham (21:12): the ~0.5 s vertical bursts are probably the **Doug theme's a cappella percussion** (beatboxed mouth pops), not cymbals or consonants. Second case in one track of a *voice doing the drums* (after Homer). Lesson #5 again: role ≠ source. Beatbox pops = broadband vertical bursts, sharp attack, fast decay, very similar to real drums in the picture; telling them apart may need the low end (a real kick has a pitched low "body", a mouth pop usually doesn't) — test later.

## Sample tracker v0 (`tracker.py`), first run (2026-10-17 21:20 ET)
Snippet: one D'oh, 4.95–5.45 s. Semitone-binned spectrogram, slid over every offset × every shift −12..+12. Image `samples/mystery_tracker_doh.png`.
- **Intro (strong matches 0.58–1.00, all at original pitch):** 2.83 / 3.23 / 3.62 · 4.95 / 5.34 · 7.08 / 7.48 / 7.87 · 9.20 s → hits every **0.39 s in threes** = "D'oh d'oh d'oh" found by shape alone.
- **Body (weak matches 0.31–0.41, buried in the mix — treat as candidates):** triplets at **19.11 / 19.50 / 19.90 s** and **23.34 / 23.73 / 24.13 s**, both shifted **+7 semitones**; singles at 29.35 and 31.46 s at **−5**; scattered others (+5, +4, −1, −3) through 33.6 s; one at original pitch at **111.8 s**.
- Why I believe the body triplets despite the weak scores: same exact 0.39 s spacing as the intro triplets. Coincidence is unlikely. And they start at ~19 s, exactly when Kham said the vocals come in, matching "D'ohs tied to the vocal track", re-pitched to sit in the song's key.
- Note: +7 and −5 are the same note an octave apart, so the 29–31 s D'ohs land on the same pitch class as the 19–24 s ones.
- Limits: weak scores in the dense mix; little found 34–110 s (could be absent, or too buried for a whole-mix template). Needs Kham's ears to confirm 19 s / 23 s D'ohs and the 111.8 s one.

## Tracker confirmations + "yeah baby" pitch map (2026-10-17 21:29 ET)
Kham (headphones): 19 s = the verse starts, with a D'oh tied to each word ✅ (tracker's +7 triplets); extra "yeah baby" at 21 s and 26 s, which sound un-pitched ("they sound like Mike Myers"); a vocal break from the end of 21 s to the end of 22 s ✅ (the tracker's gap between the 19.90 and 23.34 triplets).
Prediction before running: if 21/26 s are the original, they should sit between the down-pitched intro one and the up-pitched 8 s one, with the same shift as each other.
Tracker run, snippet 0.0–1.4 s ("yeah baby" #1), `samples/mystery_tracker_yeahbaby.png`:
| time | shift vs. intro | reading |
|---|---|---|
| 8.03 s | **+5** | the up-pitched one (f0 check said +5.6) ✅ |
| 21.36 s | **+3** | Kham: sounds unpitched ✅ |
| 25.73 s | **+3** | Kham: sounds unpitched ✅ (same shift as 21 s) |
| 48.55 s | **+5** | Kham: high-pitched one with the laugh track ✅ (same as 8 s) |
| 14.42 (−4), 29.86 (−3), 42.96 (−5), 53.06 (+4) | — | unconfirmed candidates |
**Inference:** Mike Myers' original sits at the +3 level. So the intro "yeah baby" is the original pitched **down ~3 semitones**, and the 8 s and 48 s ones are pitched **up ~2**. Neil used three versions: low, original, and high. Prediction held.
**All four candidates confirmed by Kham (21:34):** 14.42 s (−4) very down-pitched + slightly slowed ✅ · 29.86 s (−3) down-pitched + slowed ✅ · 42.96 s (−5) down-pitched ✅ · 53.06 s (+4) through a weird compressed filter ("like a musical birthday card") ✅.
**Tracker score on "yeah baby": 8 of 8 hits are real, zero false positives.** Relative to the original Mike (the +3 level): 14 s ≈ −7, 30 s ≈ −6, 43 s ≈ −8, 53 s ≈ +1 (birthday-card band-limited).
Kham (21:35): had never noticed the 43 s one despite living in the album for about a month; the tracker found something his ears had missed.
Lessons: (a) a slowed version still matched without time-stretch modeling, but scores drop (0.30–0.46). v1 should also search time-scales (0.8–1.25×). (b) Heavy filtering (the birthday card) still matched by pitch shape. Shape survives timbre damage.

## Decay test: does the looped hook get more crushed? (2026-10-17 21:38 ET)
Tracker on one clean hook repeat (35.6–36.6 s): repeats every **~2.12 s** (one bar) from 35.6 to ~95 s, plus 103.4 and 105.6 s; none ~97–103 s. `samples/mystery_tracker_hook.png`.
Per repeat: match to the clean first copy; "grit" = 5–10 kHz hiss ÷ 200 Hz–2 kHz body; "wobble" = median frame-to-frame jitter of the dominant 80–400 Hz pitch.
- **Constant-layer window 52–70 s (hook + Doug doo-doos only):** match falls −0.074 per 10 s (r = −0.74); **grit rises +0.20 per 10 s (r = +0.73)**. → **More crushed: supported.** The copies get hissier and less like the original while the other layers stay the same.
- Whole run 35–96 s: match falls strongly (r = −0.87), but grit is flat overall, because new layers (Doug at 43 s, the final source at 70 s) change the body band and swamp the measure. Confounded; the 52–70 s window is the fair test.
- **Wobble: inconclusive.** The metric is too crude (the dominant 80–400 Hz peak is often the bass, and several repeats read 0.00). Needs a proper pitch tracker on the hook's own voice, or stems.
Verdict: Kham's "slowly gets more crushed": **confirmed in the fair window.** "More wobbly": not yet measurable.
