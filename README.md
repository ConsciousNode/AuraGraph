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

**Live page:** https://consciousnode.github.io/AuraGraph/ · **App:** [AuraGraph v0.2](https://consciousnode.github.io/AuraGraph/app.html) · **Toy:** [Paint a Tile, Hear a Tile](https://consciousnode.github.io/AuraGraph/toys/paint-a-tile.html)

## Status: app v0.2, research continuing

**`app.html`** is the tool. It's one HTML file with no libraries, it works offline, and nothing is uploaded. Drop in a recording and you get:
- **reading tiles in the machine view** that LEGIBILITY-1 picked: gray brightness, the C6·d3 grid burned in, every semitone ticked, every C and A labelled
- **data tiles** (`.aura.png`, with their bounds inside), which AuraLoom plays back
- **a READ-ME-FIRST** for the model, including the four habits that fooled the blind readers
- all of it in one zip

Its analysis is a port of `prototype/plain.py`, checked against it: identical levels, zero pixels off. **v0.2** (analysis v2) fixes two things a real recording showed:
- **Bass rows:** below ~290 Hz the bands are read from a 4096-point FFT, so they mostly stop copying each other. 8192 points was tried and dropped, because it smeared kick drums into blobs.
- **Background:** the loudness range follows the recording's own noise floor (40–80 dB), so a room's hiss goes near-black instead of mid-gray.

`plain.py --v1` keeps the analysis LEGIBILITY-1 tested. The Python prototypes stay as the research bench. Everything here is working notes, written as we went, with the corrections left in.

**[How to Read a Tile](HOW-TO-READ.md)** is the full guide: what sound looks like, how readers fool themselves (measured), and AuraGraph specifics, with worked examples. The short version:
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
| `research/INVERSION-1.md` | Can a tile be played back? Yes: 94% of the melody returns from the picture alone. A resolution sweep shows melody lives on the pitch axis and rhythm on the time axis. Includes the publishing policy that follows. |
| `research/SPEC-SEEDS.md` | Applications beyond the base platform: tile → sound, painting music, a model that sings by drawing, diffusion-made music, music as a PNG. |
| `toys/paint-a-tile.html` | Single-file toy: paint a tile and hear it (Griffin-Lim in the browser), or turn a recording into a tile and back. Lo-fi knobs for pitch detail, time detail and levels. |
| `app.html` | The AuraGraph app (see Status). |
| `HOW-TO-READ.md`, `guide/` | The reading guide, with worked examples whose contents are known exactly. Each section is tagged tested, observed or reasoned. |
| `research/LEGIBILITY-1.md`, `research/legibility-1/` | Which drawing models read best: 6 renderings, 6 synthetic clips, 24 blind readers from four model families, with the answer key committed first. Gray with the grid wins; readers bend real marks to fit a question's premise, whatever the drawing. Reads unedited, grades in `grades.py`. |
| `research/TILE-FORMAT.md` | The tile container, v0.3: an ordinary PNG with a small `auragraph` data chunk saying what its pixels cover (seconds, Hz, axis, loudness range), plus a filename fallback. Clips that know where they are, with the test. |
| `research/LISTENING-QUEUE.md` | What's next to listen to. |
| `prototype/` | The Python tools: `proto.py` (tiles + sidecar), `closeup.py` (fine timing and pitch), `fingerprint.py`, `timbre*.py`, `selfsim.py`, `tracker.py` (find a sample wherever it recurs, at any pitch shift), `zoom.py`, `bands.py`, and the container tools `tilemeta.py`, `plain.py` (audio → plain tile with its bounds inside), `clip.py` (cut a clip that remembers where it was), `views.py` (the LEGIBILITY-1 renderings and the machine view) and `notes.py` (pinned notes on the C6·d3 grid, both directions, plus a grid copy for models). Needs numpy, scipy, matplotlib and an audio decoder. |
| `samples/notes-demo/` | A CC BY-SA melodica tile with pinned notes going both ways, its grid copy, and the notes as text. |
| `samples/inversion/` | A CC BY-SA melodica recording and three rebuilds of it from tiles. |
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
