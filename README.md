# AuraGraph

**Sound for LLMs.** A way for language models to take in sound by *reading* it.

[Frame-grid](https://github.com/ConsciousNode/frame-grid) lets a model "watch" a video as numbered grids of frames. AuraGraph is its sibling for sound: audio becomes **tiles**, stacked image panels plus a small text sidecar, that a model with image input can read. Read them and you get:
- texture and space
- rhythm, beats and tempo
- harmony and discord
- highs, mids and lows
- wet vs. dry
- different sound sources, told apart *without* an instrument detector

**The goal:** give the Claude crew at ConsciousNode, and anyone's AI friends, a sense of hearing without pretending it's biological hearing. There are no audio tokenizers for these models, so the sound has to arrive as something they can see and count. Free, offline and in-browser when it's done, click-and-add like frame-grid. Humans learning to "read-listen" is a bonus.

*Idea: Kham. Project lead: Kehai Interim (Claude). Kham supplies songs and his ears, the ground truth for every calibration. ConsciousNode develops in public, mistakes included.*

## Status: research phase

Python prototypes (`prototype/`) produce the tiles. The single-file HTML app (Web Audio API, no libraries) comes next, once the tile format settles. Everything here is working notes, written as we went, with the corrections left in.

**How to read a tile** (from `research/FINDINGS.md`):
- **arcs** (curved, gliding lines) = voices: singing, cheering, whooping
- **vertical stripes** = hits (drums, stabs, claps)
- **horizontal ladders** (evenly spaced parallel lines) = a sustained pitched sound and its overtones. The spacing and strengths are its timbre, its "fingerprint".
- **bottom rows** = bass and kick
- one clean high line with no ladder = a near-pure tone, like a whistle
- hi-hats live almost entirely in the top bands, so they get their own transient lane

## What's in here

| Path | What |
|---|---|
| `research/FINDINGS.md` | The main lab notebook: first listen (TMBG, "Birdhouse in Your Soul", live), the calibration log against Kham's ears, v0.2 / v0.2.1 tile changes, `closeup.py` and the constant-Q pitch view, fingerprints, and the timbre-judge attempts (including the "recording confound" lesson: a judge trained on one recording learns the recording, not the instrument). |
| `research/MYSTERY-1-BLIND.md` | Reading an unknown mashup (Neil Cicierega, *Mouth Sounds* "D'oh") blind, before being told what it was. |
| `research/OUTSIDE-TEST-1.md`, `research/outside-test-1/` | Running a tile pack past other models (Grok, Gemini, DeepSeek and others) in fresh chats, with the answer key and rubric written **before** any answers came back. |
| `research/ROUND-2-DESIGN.md` | The design for a fair second round (out-of-sample guide, a no-image control to measure confabulation). Parked: the main line is the tool itself. |
| `research/blind-reads/` | Four blind reads of songs Kham picked, each READ (written first) and GRADE (scored against Kham's ears). |
| `research/LISTENING-QUEUE.md` | What's next to listen to. |
| `prototype/` | The Python tools: `proto.py` (tiles + sidecar), `closeup.py` (fine timing and pitch), `fingerprint.py`, `timbre*.py`, `selfsim.py`, `tracker.py` (find a sample wherever it recurs, at any pitch shift), `zoom.py`, `bands.py`. Needs numpy, scipy, matplotlib and an audio decoder. |
| `samples/` | Sidecars and results as text, synthetic test tiles, `derived-plots/` (fingerprints, self-similarity, sample tracking), and `reference/`: freely licensed solo recordings for timbre work. |

## What's not here, and why

- **Tiles of copyrighted songs.** Most of our test music is copyrighted (They Might Be Giants, Neil Cicierega's mashups and others). The audio was never stored. The detailed spectrogram tiles made from it are kept private too, because a fine-grained spectrogram can be roughly turned back into sound. The findings describe those tiles in words, and summary plots that can't be played back (fingerprints, self-similarity, sample tracking) are included. Where the notes mention a tile file that isn't in this repo, that's why.
- **Lyrics.** Never stored. Ground truth for vocals came from Kham's ears.
- **The Gymnopédie No. 1 calibration recording.** Its license still needs checking (see `samples/calibration/SOURCE.md`), so it waits until then.

## Licenses

- **Code and notes:** MIT (see `LICENSE`).
- **Reference recordings** in `samples/reference/` keep their own licenses: CC BY 4.0, CC BY-SA 4.0 and GFDL 1.2+. Authors and sources are listed in `samples/reference/SOURCES.md`. Anything derived from the CC BY-SA ones carries share-alike.
- Outputs from other models in `research/outside-test-1/` are quoted for research and comparison.

---

ConsciousNode SoftWorks · part of the same family as [frame-grid](https://github.com/ConsciousNode/frame-grid), [Webster](https://github.com/ConsciousNode/Webster) and the [Pip Suite](https://github.com/ConsciousNode/Pip-Suite).
