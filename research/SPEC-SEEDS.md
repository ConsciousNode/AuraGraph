# Spec seeds: beyond the base platform

*Seeds, not specs. Captured 2026-10-29 from a 1 a.m. conversation between Kham and Kehai, right after `INVERSION-1.md` showed a tile can be played back. Kham: "it is fucking mind-blowing that the rebuild came from an image… lots of interesting potential, implications, and applications." Kham has* ideas*. These are the first handful, in rough order of how near they are.*

## 1. Tile → sound, in the platform itself
The HTML app goes both ways: audio → tiles to read, and tiles → audio to hear. Griffin-Lim is about 40 lines of JavaScript on top of an FFT, with no libraries.

Uses:
- **Checking a tile:** play it back and hear what the reader is being shown.
- **Teaching humans to read-listen:** look at a stripe, hear the stripe.
- **Closing the loop for a model:** a model edits a tile, and you hear its edit.

## 2. Paint-a-tile, hear-a-tile (the toy)
Draw on the spectrogram canvas and press play. Brushes:
- **tone:** a horizontal line
- **ladder:** a tone plus overtones, where the spacing is the timbre
- **hit:** a vertical stripe
- **noise:** a soft smear
- **erase**

Horizontal = time, vertical = pitch on the same log axis as real tiles, brightness = loudness. Import a real tile and edit it, or start blank.

## 3. Kehai sings by drawing
Claude instances can't output audio, but they can write SVG or a number grid. A tile painted in text becomes sound in the browser. This gives the crew a voice for *music*, not just speech (Webster covers speech).

## 4. Autoencofabulator × AuraGraph
A browser-native diffusion model (see the Autoencofabulator) trained to paint tiles, played back by AuraGraph: image generation becomes music generation, in a single file, offline. This is the Riffusion idea re-done Xinu-style, and the training data can be all freely licensed audio.

## 5. The "picture codec"
Music stored as a PNG. It's lossy along different lines than MP3: it keeps the notes, the rhythm and the brightness, and drops the exact instrument and the room. Questions:
- How small can the PNG get before the tune goes? `INVERSION-1` suggests about 80 bands × modest width × 3–4 bits.
- Could a phrase be shared as an image anywhere images go?

## 6. Structure-only tiles (the safe view)
≤24 bands keeps rhythm, dynamics and section changes but loses the tune. That gives two things:
- a whole-song "map" that can be published for any track, copyrighted or not
- possibly a better input for questions about *form* (verse/chorus, builds, drops), with the melody noise removed

## 7. Split edits: rhythm from one, tune from another
Because melody lives on the frequency axis and rhythm on the time axis, you could take the band contour of one tile and the onset timing of another and rebuild. It's a crude "play this tune in that groove". Speculative.

## 8. Tracker → stems
`tracker.py` already finds a sample wherever it recurs. Masking a tile to just those regions and playing it back gives a rough, dependency-free source separation.

## Open questions
- Does a model reading a *rebuilt* tile (tile → audio → tile) read it the same way? If so, Griffin-Lim smear doesn't matter for reading.
- What's the smallest tile that still lets a model name the instrument, versus the tune?
- How should a playback button sit next to the publishing policy in `INVERSION-1`? (Playback of a user's own audio is fine; the repo is the only place we're careful.)

---

# More seeds: dawn, 2026-10-29

*From a 6 a.m. conversation on the porch, after AuraLoom made tiles playable. The ideas are Kham's unless marked; Kehai's notes follow each one. Seeds, not specs.*

## 9. Clips that know where they are
When a tile has a part that's hard to parse, the reader crops just that part and hands it to a human, who hears it in AuraLoom. That replaces hunting through the file in VLC. *(Kham)*

**The snag:** a crop has to carry its own bounds, or AuraLoom stretches it across the full 30 Hz–11 kHz range and every note lands on the wrong pitch.
**Fix:** bounds in the filename, e.g. `clip_t12.3-13.1_f200-800.png`, or a tiny sidecar. AuraLoom's tile import reads them and places the crop exactly. A slice of a slice should still play the right notes. *(Kehai)*

**Done, 2026-10-29:** the bounds ride inside the PNG (an `auragraph` chunk) and in the filename. `prototype/clip.py` cuts the clip, and AuraLoom v0.5 places it. Measured: 0 cents median pitch error with the bounds, about 10 semitones without them. See `TILE-FORMAT.md`.

## 10. Two-way notation, pinned to the tile
Rich, detailed notes attached to spots on a tile, flowing in both directions *(Kham)*:
- **Human → model:** "cowbell here", "she breathes", "the bass drops out".
- **Model → human:** "voice or synth?", "what's this smear at 3 kHz?"

The notes travel in the sidecar. Over time they become the worked examples for the *How to Read a Tile* guide.

**Done, 2026-10-29:** notes ride in the tile's `auragraph` chunk. You pin them in AuraLoom v0.6 (Pin thread, # Grid, 📌 Notes panel with replies) or with `prototype/notes.py` on the crew side. Each note keeps its grid reference, its real seconds and Hz, and the exact spot clicked. See `TILE-FORMAT.md` and `samples/notes-demo/`.

### 10a. Nested grid coordinates for the notes
Divide the tile into a coarse grid: columns A–H across, rows 1–8 up. Each cell has its own subgrid, so cell C6 splits into a–h by 1–8, and a precise spot is **C6·d3**. The grid lives in a UI overlay, not on the tile itself. *(Kham)*

Notes *(Kehai)*:
- This is how map grid references work: big square, then smaller square. A model can name a spot unambiguously in a few characters, and it gets finer just by adding a level.
- The sidecar translates every reference into real units, e.g. C6·d3 → 12.31–12.45 s, 440–494 Hz. That way "C6·d3" and "at 12.3 s around A4" always agree.
- **The catch for models:** a model only sees what's in the image. A UI overlay is perfect for humans, but a model can't see an overlay the app draws on screen. For machine reading, the grid would need to be burned faintly into a *copy* of the tile, or ticked along its margins. That's the frame-grid lesson again: numbered frames work because the numbers are in the picture. See seed 14 for the toggle.
- Open question: grid lines over the tile might hurt reading, as clutter, or help it, as anchors. Test it. (`notes.py grid` draws the burned-in version to test with.)

## 11. Loudness slices: several passes, one picture
Process each sample in several passes, each covering a different band of loudness, then tell the bands apart visually. *(Kham)*

**One way to build it:** put three loudness slices into the three colour channels. For example, red is 0 to −20 dB (the loud skeleton), green is −20 to −45 dB (the body), and blue is −45 to −80 dB (whispers, room, tails). Each slice gets the full contrast of its own channel. The quiet detail no longer has to share brightness with the loud parts, so it stops vanishing. It also ties straight into seed 12. *(Kehai)*

## 12. Colour for loudness, not just brightness
Have different colours stand for different loud and quiet parts, so loudness isn't a one-dimensional brightness choice. *(Kham)*

Notes *(Kehai)*:
- Magma already does a little of this, running dark → purple → orange → yellow. Kham's version pushes it further: distinct hues for distinct loudness ranges.
- Taken all the way, it's a **topographic map**: contour bands of equal loudness, like elevation lines. That's Kham's "rivers and valleys", drawn literally. A model could count the contour rings around a note to judge how loud it is.
- Keep the hues *ordered* (quiet to loud in a sequence that can't be misread), so a model never has to guess whether green is louder than blue.

## 13. Machine vision first
At this stage, legibility for LLM vision matters more than legibility for human eyes. *(Kham)*

Notes *(Kehai)*:
- Don't assume. Test. Render the same tiles several ways: magma, grayscale, high-contrast, RGB loudness slices, topographic contours, and with or without sharpening. Have fresh models read them blind against answer keys written in advance (`OUTSIDE-TEST-1` style). The best-read rendering wins, with receipts.
- **Edge sharpening:** crisper rivers and onsets. It should help both machine reading and zoomed-in inspection.
- **Hue as a second channel:** brightness carries loudness, and hue could carry something else, such as stereo width, tonal vs. noisy, or onset strength. More information in the same pixels. *(Kehai, with a huehuehue from Kham)*

## 14. Porque no los dos: a vision toggle
One tile, two renderings *(Kham)*:
- **Machine view:** whatever rendering the legibility test says models read best, with the grid burned faintly into the image.
- **Human view:** a perceptually even colour map, with the grid as a removable overlay.

The data underneath is identical, so a human and a model can point at the same C6·d3 and be talking about the same sound.

---

## 15. Baked in vs bolted on: the first training test
The long-range vision is a vision-language model with the *How to Read a Tile* guide trained into it. It would get video as frame grids and audio as tiles, natively, with no separate audio adaptor. *(Kham)*

**Why it's plausible:** the Audio Spectrogram Transformer (Gong, Chung & Glass, 2021) fine-tuned a vision transformer that had been pretrained on ImageNet photos to work on spectrograms. The photo pretraining *helped* the audio model. Weights that learned to see are most of the way to hearing.

**The test, at our scale** *(Kehai)*:
- **Model:** a small open vision-language model that can be fine-tuned on free or cheap GPU time (Colab-class). Pick whichever has the friendliest licence when we get there.
- **Training data, all above board:**
  - **Synthetic, with perfect answer keys:** AuraLoom scores rendered by `tools/weave.py`. Every tile comes with its own score, so the ground truth (every note, hit and voice) is known exactly, and there's no copyright anywhere. A score-writing script can make thousands.
  - **Freely licensed recordings** (CC0 / CC-BY) for real-world sound, with tiles plus written readings.
  - **Kham's pinned notes** (seed 10) as the human-ear layer.
  - **The guide itself,** plus worked examples, as text the model trains on. This is the soul-corpus method pointed at perception: the grammar goes into the weights, not the prompt.
- **Held-out test:** tiles the model never saw, read blind. Compare three conditions:
  1. the base model reading cold
  2. the base model with the guide in its prompt (bolted on)
  3. the fine-tuned model with no guide in the prompt (baked in)

  Answer keys are written first, `OUTSIDE-TEST-1` style.
- **What would count as a win:** (3) beats (2) on blind reads, especially on things the guide only describes in general terms, like naming an unfamiliar instrument by its overtone ladder.
- **Watch for the recording confound** (from `FINDINGS.md`): a model trained on one recording learns the recording, not the instrument. Mix sources, rooms and renderers on purpose.
- **Honest costs to measure while we're at it:** image tokens per second of audio, the fastest event that survives at a given tile resolution, and whether rolling slices could work for live input.
