# Inversion 1: can a tile be played back?

*Kehai Interim, 2026-10-29. Prompted by Kham asking whether publishing tiles of copyrighted songs is fine "unless it is possible to reconstruct the actual songs from our data". So we tested whether it is.*

## The test

1. Render the first 15 s of a recording the way `proto.py` does:
   - 160 log-spaced bands, 30 Hz – 11 kHz
   - clipped to −80…0 dB
   - quantised to 8-bit colour
   - about 1,000 px across
2. Throw the original audio away. Keep only that grid.
3. Spread each band's level back over its FFT bins, then run 60–80 rounds of Griffin-Lim to invent phase that fits.
4. Score the rebuild against the original:
   - **melody:** pitch-class agreement per frame, with a time-shifted baseline as "chance"
   - **rhythm:** onset-envelope correlation

The four test recordings are all freely licensed (`samples/reference/SOURCES.md`): a melodica, a clean guitar, an organ prelude, and a sung chant. Script: `prototype/invert_sweep.py`.

## First result: yes, the tune comes back

| | melody | rhythm |
|---|---|---|
| AuraGraph v0.2.1 resolution | 0.94 (chance 0.24) | 0.91 |

The rebuilt waveform is nothing like the original (SNR −7 to −10 dB). Phase is gone, so it sounds smeared and slightly ghostly. But the notes are the same notes at the same times. Kham's description: *"it sounds like a cover… not the recording, a new performance of the original piece."* A spectrogram tile is sheet music with timbre stapled on.

Listen: `samples/inversion/melodica_original_15s.mp3` vs `melodica_rebuilt_160bands_1000px.mp3`.

## The sweep

Averaged over the four recordings:

| bands | px across 15 s | bits | melody (chance) | rhythm |
|---|---|---|---|---|
| 160 | 1000 | 8 | **0.94** (0.24) | **0.91** |
| 160 | 1000 | 3 | 0.86 (0.22) | 0.73 |
| 80 | 1000 | 8 | 0.87 (0.22) | 0.88 |
| 40 | 1000 | 8 | 0.68 (0.19) | 0.84 |
| 24 | 1000 | 8 | 0.30 (0.14) | 0.82 |
| 12 | 1000 | 8 | 0.14 (0.11) | 0.80 |
| 160 | 250 | 8 | 0.94 (0.24) | 0.37 |
| 160 | 100 | 8 | 0.88 (0.23) | 0.24 |
| 160 | 50 | 8 | 0.76 (0.22) | 0.18 |
| 160 | 25 | 8 | 0.62 (0.21) | 0.26 |
| 40 | 100 | 8 | 0.66 (0.19) | 0.16 |
| 24 | 100 | 4 | 0.28 (0.15) | 0.17 |
| 12 | 50 | 4 | 0.13 (0.11) | 0.15 |

## What it says

- **Melody lives on the frequency axis; rhythm lives on the time axis.** They come apart cleanly.
  - At 24 bands (about a third of an octave each), the tune is nearly gone (0.30 vs 0.14 chance), but the rhythm survives (0.82).
  - At 100 px, the rhythm is smeared (0.24), but the tune is still there (0.88).
  - Listen: `melodica_24bands_fulltime.mp3` and `melodica_160bands_100px.mp3`.
- **Colour depth barely matters.** Even 3 bits (8 brightness levels) keeps 0.86 of the melody.
- **Readable ⇔ playable, for melody.** The pitch detail that lets a model read a tune off a tile (`blind-reads/`) is exactly the detail that lets Griffin-Lim play it back. You can't have a tile that shows the melody to a reader but hides it from a decoder. They're the same information.
- **Structure without the tune is possible.** A low-band tile (≤24 bands) keeps rhythm, dynamics, density, brightness, and where sections change, but loses the tune.

## Publishing policy (what we do with this)

- **Derived plots** (fingerprints, self-similarity, trackers) can't be played back. They're published.
- **Full-resolution tiles of copyrighted songs:** these play back as a recognisable rough cover of the tune. Kham's reasoning is that a new performance of the piece, uncharged and attributed, is fair. Kehai's caution is that covers are normally *licensed* (a compulsory mechanical licence, or venue performance licences), not fair use. The research case is better: short excerpts, transformative analysis, no market substitute. Decision for now:
  - short excerpt tiles next to their written analysis are OK
  - whole songs tiled end to end stay off the repo
  - a structure-only tile (≤24 bands) is a safe way to show a whole song
- **Freely licensed audio** (`samples/reference/`) can be shown at any resolution, with its licence carried along. The melodica rebuilds here are share-alike derivatives of a CC BY-SA 4.0 recording (performer Troy Banarzi, via Wikimedia Commons), so they're CC BY-SA 4.0 too.

*Not legal advice: neither of us is a lawyer.*

## Prior art

Riffusion (Forsgren & Martiros, 2022) generated spectrogram *images* with Stable Diffusion and played them through phase reconstruction. Same trick, other direction. Griffin-Lim itself dates from 1984.
