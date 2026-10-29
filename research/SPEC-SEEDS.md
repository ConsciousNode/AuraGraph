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
