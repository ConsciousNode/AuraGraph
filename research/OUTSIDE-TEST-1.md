# AuraGraph outside test #1 (key + rubric, written BEFORE any answers come back)
*Kehai Interim, 2026-10-18 ~22:15 ET. Idea: Kham. He runs the pack past other models (Grok, Gemini, etc.) in fresh chats and pastes their answers back; Kehai grades against this key.*

## Design
- Pack: 6 tile images (renamed image_1..6, titles contain only time ranges, no song names) + two prompts. Prompt A = blind, no guide. Prompt B = same questions plus a rough reading guide.
- One fresh chat per (model x arm). Never run B before A in the same chat (guide leakage). Paste answers back verbatim.
- Optional arm C (Kham's call, not required): same questions with the *original audio* of one clip (safest: Gymnopedie, CC0) to compare reading tiles vs native hearing.
- **Caveat:** the guide in prompt B was written from cues learned on these same songs (Birdhouse, D'oh). It is in-sample. A fair second round needs unseen songs.
- Models may downscale images, so note which model and any visible limits.

## Image map
1 = mystery 0:48-1:04 · 2 = Gymnopedie No.1 0:16-0:32 · 3 = Birdhouse (live) 3:15-3:30 · 4 = mystery zoom 0-10.5 s · 5 = Birdhouse (live) 0:00-0:15 · 6 = mystery 0:00-0:16
("mystery" = Mouth Sounds track 3, "D'oh", a mashup. Ground truth per Kham + WhoSampled; body sources only partly mapped to times.)

## Key (what a good answer includes)
**Image 1 (mashup, 48-64 s):** bass-heavy (low band ~68%, mids ~16%); steady drums, ~112 BPM; harmony mostly F major (F, C); vocals thin out here (break); instrumental bed with samples layered on top.
**Image 2 (piano):** ONE instrument, struck (bright start, decay); dead-straight lines, no wobble; slow triple feel: low bass note then mid chord each bar, melody above; nothing above ~4 kHz, very clean and quiet; narrow stereo; D / G harmony area.
**Image 3 (Birdhouse end):** band holds a final chord (long flat lines, A strong) that decays; one huge broadband hit around 3:21; then a crowd: gliding arcs, swoop(s) (descending whoo ~3:24); a whistle near the end of the window (single clean high line ~3.9 kHz).
**Image 4 (D'oh zoom):** voice-like sampled phrase(s) (wobbly ladder) used as percussion; one identical ~1.3 s block repeated three times = repeated sample; hard stabs then gaps; at ~10 s a drop with bass and full drums.
**Image 5 (Birdhouse start):** crowd cheering at the start (arcs, no low end) with a hi-hat count-in in the very top rows; band arrives ~2.4 s (bass and kick blocks) as a man starts singing; at ~12.3 s low end drops out and a sustained bright overtone ladder (keyboard) appears; drums and vocals resume.
**Image 6 (D'oh 0-16 s):** collage-like intro of sampled voice used as percussion; hard drop at ~10 s into bass + drums (~112 BPM); lead vocal on top (~400-900 Hz); F / D-minor area.

## Rubric (per image: 4-6 key items)
- +1 per key item stated correctly (credit for the right idea in different words).
- 0 for omitted items. -1 per **confident wrong claim** (stated as fact, contradicted by the key). Wrong-but-hedged = 0.
- Roles vs sources: extra +1 on images 4/6 if a sample voice is identified as doing a percussion job.
- Note separately: any claim of a song title or artist (should be none), "can't tell" used honestly (good), claims about things not in the picture.
- Report: score per image per arm, hallucination count, and whether the guide helped or hurt.

## Results: blind grading (Kehai, 2026-10-19 ~02:50 ET, written BEFORE the X-label mapping was revealed)
Raw answers: `outside-test-1/blind_results_X1-X10.txt`. Images were mapped by their on-tile headers, not by the "Image N" numbers the models used (X7 and X9 saw the tiles in a different order). Half points for partial credit. "Confident wrong" = High or Medium-high confidence, or no hedge at all, and contradicted by the key.

**Grading caveats.** (1) For the mashup tiles (images 1 and 6) the committed key's tempo (~112 BPM) and harmony (F major) came from my own tool, not from Kham's ears. Two careful readers measured ~88-90 BPM instead, so I did not score tempo/harmony there, only bass, drums, voices, sample repeat and the drop. (2) Stereo width on image 2 not scored (the key said "narrow", the panel looks moderate, models disagreed). (3) Some answers came from models that ran their own measurements or sub-queries (X4, X5), so this is not a pure "look at a picture" test. (4) X9 ignored the confidence instruction entirely.

| Label | img1 | img2 | img3 | img4 | img5 | img6 | total /28 | confident wrong |
|---|---|---|---|---|---|---|---|---|
| X1 | 3 | 5.5 | 4.5 | 4.5 | 3.25 | 3.5 | **24.25** | 0 |
| X6 | 3 | 5.25 | 4.5 | 4.5 | 2.5 | 3 | **22.75** | 0 |
| X5 | 2.25 | 3.25 | 3.75 | 2.25 | 0.5 | 0.75 | **12.75** | 2 |
| X8 | 1.5 | 1.5 | 2.25 | 1.5 | 0.25 | 0.75 | **7.75** | 1 |
| X3 | 2 | 2 | 1.5 | 0.75 | -0.75 | 0.75 | **6.25** | 1 |
| X2 | 2 | 0.25 | 3 | -1 | 0.5 | 0 | **4.75** | 3 |
| X9 | 1.25 | 0.75 | 1.5 | 1.75 | 0 | -0.5 | **4.75** | 3 |
| X10 | 2.25 | -0.75 | 2 | -1.25 | 1 | 1 | **4.25** | 4 |
| X4 | 0.75 | 0.75 | 0.5 | 1.25 | 0 | 0.25 | **3.5** | 0 |
| X7 | 1.25 | 0.5 | 1 | 0.25 | -0.75 | 0.5 | **2.75** | 1 |
(img: 1 = mashup 0:48, 2 = piano, 3 = Birdhouse end, 4 = D'oh zoom, 5 = Birdhouse start, 6 = D'oh start.)

**My guess at the arms (from vocabulary only, to be checked):** guide arm B = X1, X3, X4, X5, X6 (they say "ladder", "needle", "comb"; X4 quotes the guide's feature list outright). Arm A = X2, X7, X8, X9, X10. If right: B mean 13.9, A mean 4.85. But X3 and X4 are in the B group and scored low, and X1/X6 look so alike that they may be the same model, so the guide is not the whole story.

## Findings to carry into the reader's guide
1. Piano control (img 2) sorted the models: two got solo struck instrument + decay + no drums + slow + D/G harmony; four called it synths/guitar with drums.
2. Nobody found the hi-hat count-in as such (img 5). Same blind spot as my own first read: the crowd wash hides it. Supports a dedicated high-band transient lane.
3. Four answers called the Birdhouse opening a steady loop for all 15 s and missed the crowd intro, the entrance at 2.4 s and the break at 12.3 s.
4. The D'oh sample (img 4): the best readers called it a retriggered sample (identical repeats). Four others called it piano/plucked strings: a short, fast-decaying voice sample looks like a struck note. New cue for the guide: check for glide/wobble inside the note, not just onset shape.
5. Calibration varied a lot: X4 hedged everything (0 wrong, little information); X10 stated many "High" claims and 4 were wrong; X9 gave no confidence levels.
6. Stereo-width panel was read as "narrow" and "wide" for the same tile by different models. Needs a labeled color bar.
7. Tempo: X1 and X6 independently got ~98 BPM on Birdhouse 0:00-0:15, so my tool's 99.4 may be fine. For the mashup tile they got ~88-90, versus my key's 112. My mashup tempo reading was probably wrong.

## Unblinded (Kham, 2026-10-19 02:10 ET; grades above were committed first)
| Label | Model | Arm | Score |
|---|---|---|---|
| X1 | Gemini | B (guide) | 24.25 |
| X6 | Gemini | A (blind) | 22.75 |
| X5 | Kimi | B | 12.75 |
| X2 | Kimi | A | 4.75 |
| X3 | Grok | B | 6.25 |
| X7 | Grok | A | 2.75 |
| X4 | Lumo | B | 3.5 |
| X8 | Lumo | A | 7.75 |
| X9 | DeepSeek | B | 4.75 |
| X10 | DeepSeek | A | 4.25 |

Guide effect (B minus A) per model: Gemini +1.5, Kimi +8.0, Grok +3.5, DeepSeek +0.5, Lumo -4.25. Arm means: B 10.3, A 8.45 (+1.85). My vocabulary-based arm guess was right for 8 of 10 labels (wrong on X6 and X9). My earlier "guide ~ 3x" reading was a model effect, not a guide effect: Gemini did very well with or without the guide. n = 1 per cell and the guide is in-sample, so treat as a pilot.
Arm C (Gemini audio) not completed: that Gemini surface could not process audio.

## Researcher notes from the master document (added after unblinding, 2026-10-19)

Source: Kham's unredacted master file (controls, image-only runs, and both prompt arms for all five subjects). Grades above are unchanged; these notes change how to *read* them. Corrections go forward, not into earlier sections.

**1. Lumo does not see the images.** Researcher note: Lumo is a bolted-on image pipeline; it receives a text description. In its Prompt B run it said it "interrogated" the images with parallel questions, then did a second pass, and the two passes disagreed on tempo density, stereo width and chroma classes, so it downgraded those to "can't tell". Consequences:
- Lumo's scores (X8 7.75 A, X4 3.5 B) measure the describer plus Lumo, not Lumo reading tiles. Its guide effect (-4.25) is not interpretable as a guide effect: the guide made it ask sharper questions of a describer that answered inconsistently, and honest hedging scores low on a rubric that rewards correct commitments.
- Lumo is the one subject that is a genuinely different channel (text description of a picture). Keep it in the table, flag it, and exclude it from the guide-effect mean.
- Recomputed guide effect over the four direct-vision models: B mean 12.0, A mean 8.6, difference about +3.4 (was +1.85 with Lumo).

**2. Kimi's +8.0 is partly tool use.** In Prompt B, Kimi said it would zoom into panels computationally, then ran onset autocorrelation, sampled chroma rows and measured stereo width. Its Prompt A run did no such thing. So the B-A gap mixes "guide" with "ran its own measurements". It is still a useful result (tile reading plus measurement beats eyeballing), but it is not a clean guide effect. Kimi's measured tempo for image 1 was 116/142 BPM, which disagrees with the careful readers (~88-90) and with my own tool (112), so measurement did not rescue tempo.

**3. DeepSeek Prompt B had stray text.** Its answer opens "The text you pasted looks like an error message from a previous AI model that failed to load the images." The pasted material looks like a prior failed attempt rather than the clean prompt. It still analysed all six images, so X9 is graded as-is, but its near-zero guide effect (+0.5) is weakly informative.

**4. Controls (no images) came out clean.** Prompt A alone: DeepSeek reviewed the prompt text as if it were an existing analysis; Grok produced image-by-image readings with no images (a hallucination, worth a closer look, see 5); Kimi, Lumo and Gemini said no images arrived. Prompt B alone: DeepSeek, Kimi, Lumo and Gemini said no images arrived. So the prompt texts do not leak the key, and graded content in the real runs came from the tiles, with the Grok caveat below.

**5. Grok control A needs a flag.** Grok's no-image control to Prompt A produced full per-image readings ("Image 1 (0-10 s) ..."), i.e. confident confabulation from no data. That is a separate, publishable-sized finding about that surface's behaviour and a reminder that "confident wrong" can be produced with zero input. Worth keeping: any future test should include a no-image control per model. (Not yet checked whether the control's invented readings overlap with its real-run answers; a follow-up.)

**6. Image-only runs show what the tiles announce by themselves.** All subjects that processed images named the tool and layout from the headers. Kimi inferred track grouping from tile numbers (04/8 and 01/8 same track). Gemini matched image 4 to the first 10.5 s of image 6 by visual comparison. DeepSeek read image 4's glide lines as "sweeping downward glissando" unprompted. Kimi misread image 4's range as 0:00-10:50 (it is 10.5 s). Implication: the headers already carry real information; a legend tile should make the units and range explicit, and a zoom tile should say it is a zoom of which tile.

**7. Platform quirks to record for method.** Lumo image-only needed "." as the prompt; Grok's platform auto-added "refer to the attached content" on the image-only run. Neither touches the graded arms (A and B prompts were identical text across subjects) but they are logged for reproducibility.

**What this does to the earlier findings.** The model effect still dominates (Gemini 22.75-24.25 with or without guide). The guide helps most where the model can do something with it (Kimi with tools, Grok), is neutral for a model already at ceiling (Gemini), and is uninterpretable for a text-describer pipeline (Lumo). The honest summary: guide effect about +3 on four direct-vision models, noisy, with one tool-use confound. Round 2 should use unseen songs, a no-image control per model, a rule on tool use (allow it, but record it per arm), and a note on whether the subject sees pixels or a description.

### Addendum to note 3 (2026-10-19, from Kham)
Kham confirmed the stray text in DeepSeek's Prompt B run was part of DeepSeek's own control-B response ("I can't analyze these yet because no images are visible...") pasted on top of Prompt B by accident. That explains why X9 called it "an error message from a previous AI model that failed to load the images." So X9 saw Prompt B plus a prior "no images visible" message. It still read all six images, and its score (4.75) is close to its A arm (4.25), so the practical effect looks small, but it is a known deviation: X9 is not a clean arm-B run. Treat DeepSeek's +0.5 guide effect as unreliable. Round 2: paste prompts from a saved file, not by hand.

**Correction to the addendum (forward):** Kham pasted directly from the saved prompt file, so my "paste from a saved file" suggestion above does not apply. The cause of the stray block is unknown (candidates: the chat input restored an old draft, a stale clipboard, or an over-wide selection). Round 2 procedure: look at the input box before sending, and mark prompt boundaries in the file (e.g. "=== PROMPT B START ===") so a stray block is visible.

### Addendum 2 to note 3: X9 probably never received Prompt B (2026-10-19, from Kham's screenshot and the master doc)
Kham's screenshot of the DeepSeek chat shows the six images attached and the sent message beginning with the first part of DeepSeek's own control-B reply ("I can't analyze these yet because no images are visible/attached..."), only part of that reply, and Kham checked that the saved Prompt B file does not contain it. We cannot see whether Prompt B follows it in the bubble (the screenshot is cut off). Evidence from the response itself that Prompt B and the guide were NOT received:
- X9 has zero confidence labels and zero "can't tell" statements; Prompt B asked for both. DeepSeek's arm-A run (X10) has 33 confidence mentions.
- X9 uses none of the guide's vocabulary (needles, ladders, smudges, stripes, humps, pure/rich).
- X9's five-field layout (Sources present / Rhythm/tempo feel / Harmony/key / Structure/changes / Space/width) matches the stray text, not the prompt.
- X9 saw the images in a different order (its "Image 3" is the zoom).
- My own vocabulary-based arm guess labelled X9 as arm A (the one miss besides X6 that I recorded); that is consistent with no guide.
Verdict: X9 is an images-plus-stray-text run, not a valid arm-B run. Keep its score (4.75) in the table as recorded, mark it INVALID for the guide comparison, and treat the earlier "X9 ignored the confidence instruction" caveat as explained by this.

Revised guide effect, valid direct-vision pairs only (Gemini, Kimi, Grok): B mean 14.4, A mean 10.1, difference about +4.3 over three models. Lumo (description pipeline) and DeepSeek (X9 invalid) are excluded. Direction is positive in all three, magnitude is noisy (n=1 per cell, Kimi tool-use confound), and Gemini is near ceiling either way.

## Rerun: X11 = DeepSeek Prompt B, done properly (Kham, 2026-10-19 ~03:50 ET; graded NON-BLIND by Kehai)
Raw answer: `outside-test-1/rerun_X11_DeepSeek_B.txt`. Fresh chat, tiles in canonical order (mapped by on-tile headers anyway). **Graded non-blind**: I already knew this was DeepSeek B when I read it, so treat the grade as slightly less clean than X1-X10. Same key, same rubric, same caveats (mashup tempo/harmony not scored, image-2 stereo not scored). X9 stays in the record as an invalid run.

Evidence the guide arrived this time: the answer opens "based on the visual cues provided in your guide", uses "ladders", "wobbly/curved", "stripes", gives a confidence level on nearly every claim and cites panels ("based on Panels 1 & 2").

| img | score | notes |
|---|---|---|
| 1 mashup | 1.75 | drums +1, instrumental bed +0.5, vocals "buried, low confidence" +0.25; bass-heaviness not stated |
| 2 piano | -1.5 | struck instrument named among options +0.5; confident wrong: drums "High", and a "new lead sound enters at 23 s... High" (key: one instrument, dead-straight lines, no drums). A "gliding wobbly line" was claimed at Medium, so unpenalised |
| 3 Birdhouse end | 0.75 | sustained wash +0.75, found the 201 s event +0.75, noticed glides +0.25; confident wrong: crowd read as "sequenced synth / stutter, High" -1 |
| 4 D'oh zoom | 0.25 | noticed wobble/pitch bend and said pianos don't do this +0.5, stabs then gaps +0.75; confident wrong: "piano/harp/plucked synth, High" -1 (same misread as four other answers) |
| 5 Birdhouse start | 0.25 | entrance at 2.5 s exactly +1, quiet intro +0.25; confident wrong: "low-frequency rumble" for the crowd intro -1; missed hi-hats, singer, and the 12.3 s break |
| 6 D'oh start | 1.5 | lead voice +1, drums +0.5; "no major structural changes" was Medium so unpenalised, but it missed the drop at ~10 s |
| **Total** | **3.0 / 28** | **5 confident wrong** (highest count of any answer; X10 had 4) |

**Revised guide effect, four direct-vision models (valid pairs):** Gemini +1.5, Kimi +8.0, Grok +3.5, DeepSeek -1.25. B mean 11.6, A mean 8.6, difference about **+2.9**. Lumo (description pipeline) still excluded; Kimi still has the tool-use confound.

**What X11 adds beyond the number.**
- The guide changed DeepSeek's *format* (confidence labels, panel citations, "can't tell" on chroma) far more than its *accuracy*. The same cue-based reasoning that helped some models gave DeepSeek more confident wrong answers: calibration got worse (5 confident wrong vs 4).
- One cue transferred correctly: on image 4 it used wobble-inside-the-note to say "standard pianos don't do this", then still called the base instrument piano/harp. Cues were partly applied, not integrated.
- A possible guide-induced false positive: on the piano tile it claimed a wobbly lead entering at 23 s, which fits over-applying "wavy = voice or bent string". Worth a look at that tile (is there any real wobble at ~23 s?).
- Takeaway for the guide: a cue list needs counter-cues ("what a plain piano looks like", "crowd looks like arcs, not a synth") and a calibration instruction (High only when two panels agree), otherwise weaker readers use it to sound surer, not to be right.

### Key check on image 2 (2026-10-19 ~04:00 ET, prompted by Kham's remark that the tile looked "all wobbly")
Kham later said he can't read the tiles, so the remark was an impression, not ground truth. Checked anyway: (a) the sustained-panel harmonic lines are flat; the wavy shapes are the stereo-width ribbon, loudness curve and onset floor. (b) Rough pitch tracking of the clip (clip_1.mp3, 0:16-0:32): clean mid/high partials are steady (442 Hz range ~5 cents, 737 Hz ~1.6, 789 Hz ~1.5); some low partials (220-300 Hz) wander 20-60 cents, most likely tracker hopping between neighbouring notes and decay tails at limited low-frequency resolution, since a true vibrato or tape wobble would show in the high partials too. Conclusion: the key ("one struck instrument, steady pitch, no wobble") stands and X11's image-2 grade is unchanged. Likely source of X11's "new lead at 23 s": the loudest chord of the clip (~23.5 s) has a bright stack of upper harmonics that reads as a denser new texture; with the guide's "wavy = voice/bent string" cue that becomes a false lead. Candidate counter-cue for the guide: a louder strike brightens the whole harmonic stack at once; a new instrument adds its own separate line.

### Where "wobbly" was seen (Kham, 2026-10-19 ~04:00 ET, annotated screenshot of image 2)
Kham circled the bottom panel at ~22.5-23.5 s (jagged orange onset floor, blue loudness line with its step-and-sag shape) as what looked "wobbly". That is amplitude/onset texture, not pitch: the two tall spikes are real strikes (~22.7 s, ~23.6 s); the jagged floor is room/pedal/decay noise on the onset detector. Guide wording fix for round 2: state that the wobble/glide cue applies only to horizontal lines in the top three panels (pitch), never to the loudness or onset traces. Likely contributor to X11's false "wobbly lead at 23 s" on the piano tile. Also note the chroma panel's dotted/fading blocks are decay and re-strikes, not a changing note.
