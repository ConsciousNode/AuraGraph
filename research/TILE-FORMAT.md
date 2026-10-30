# The AuraGraph tile container, v0.3

*Draft, 2026-10-29. Kehai (lead), with Kham. Status: working in `prototype/` and AuraLoom v0.6; open for comments.*

## The idea
A tile is an **ordinary PNG**. Any model, browser, image viewer or person can open it with nothing special installed. Inside the file is one small text chunk, keyword `auragraph`, holding JSON that says what the pixels mean. A photo carries its camera settings the same way.

So the format is ours by name and by spec, but open: any tool can read it, anyone can write it, and a tile with the chunk stripped is still a picture.

**Extension: `.aura.png`.** Kham's idea: a custom extension so tiles are easy to tell from other pictures. That's housekeeping, not a gate; the platform still takes any picture. The double extension keeps tiles opening as PNGs in every chat uploader, viewer and model, where a bare `.aura` would be refused.

## Two readers, two channels
- **Tools** read the chunk. AuraLoom uses it to put a clip back at its real time and pitch.
- **Models** only see pixels. When a tile is uploaded to a chat, the chunk never reaches the model. So anything a model needs to know (time ticks, pitch ticks, the C6·d3 grid) has to be **drawn into the picture**. That's the machine view (seeds 13 and 14), still to come.

The chunk is never the only place an important fact lives.

## Fields
| field | meaning |
|---|---|
| `format` | `"auragraph-tile"` |
| `v` | `"0.3"` |
| `t0`, `t1` | seconds covered: left edge of the first column to right edge of the last |
| `f0`, `f1` | Hz at the bottom edge of the bottom row and the top edge of the top row |
| `axis` | `"log"`: rows evenly spaced in log frequency (the only axis so far) |
| `bands` | number of rows |
| `db` | `[lo, hi]`: brightness 0 = `lo` dB, brightness 1 = `hi` dB, relative to the loud end of the piece (plain.py: `[-80, 0]`; AuraLoom: `[-60, 0]`) |
| `cmap` | `"magma8"`: the 8-stop magma that AuraLoom and Paint-a-Tile draw with, so a colour reads back as an exact level |
| `sr`, `hop` | the analysis it came from, when there was one |
| `src` | what made it (`plain.py:<file>`, `clip.py`, `AuraLoom`, the app) |
| `analysis` | `v1` (one FFT size, a fixed 80 dB) or `v2` (a 4096-point FFT for the bands below ~290 Hz; range from the noise floor). Read `db` for the range actually used. |
| `parent`, `px` | for a clip: the tile it was cut from and the pixel box `[x0, y0, x1, y1]` |
| `notes` | pinned notes (seed 10): see below |

Everything except `format` and `v` is optional. A tile with no bounds is read as the full 30 Hz–11 kHz, stretched over the loop, which is the old behaviour.

## The filename fallback
Chat apps, messengers and some editors strip PNG chunks. The bounds also ride in the name:

```
anything_t12.30-13.10_f200-800.aura.png   seconds and Hz; "k" is allowed: _f1.2k-4k
```

When both are present, the chunk wins.

## Clips (seed 9)
`clip.py` cuts a piece of a tile. The cut snaps outward to whole pixels, and the clip records the exact seconds and Hz of the pixels it really holds, in both the chunk and the filename. A clip of a clip works the same way. AuraLoom's tile import then makes the loop exactly the clip's length (0.5 s minimum; a shorter clip plays and then goes quiet) and places every row at its real pitch.

**Test (2026-10-29):** I made a plain tile of the CC BY-SA melodica reference (*Rakes of Kildare*) and cut a clip at 2.98–5.00 s, 296 Hz–2.51 kHz. I imported it into AuraLoom (Ghost, Griffin-Lim), then compared the strongest pitch per frame in the rebuild with the original recording over the same span and band:
- **with bounds:** median error **0 cents** (0–14 cents across runs, since Griffin-Lim starts from random phase); about 80% of frames within 50 cents. With the chunk stripped but the bounds still in the filename, the result is the same. The misses are mostly frames where the original's strongest peak was the 3rd overtone (2369 Hz over a 786 Hz note) and the rebuild's was the fundamental. That's the same note, but a different peak won.
- **same pixels, bounds stripped:** median error **999 cents** (about 10 semitones); 3% within 50 cents.

## Pinned notes and the grid (seed 10, 10a)
**The grid** divides the tile's own frame: columns **A–H** across its time, rows **1–8** up its pitch (evenly in log frequency, like the rows themselves). Each cell splits the same way in lowercase, so `C6·d3` is cell C6, sub-cell d3, and another level (`C6·d3·a8`) is finer still. On a 12 s full-range tile, a two-level cell is about 0.19 s wide and 1.6 semitones tall.

**A note** in `notes`:
```json
{"n": 3, "ref": "E4·a7", "t0": 5.99, "t1": 6.18, "f0": 478.0, "f1": 524.0,
 "pt": [6.0, 523.0], "by": "Kham", "kind": "question", "re": null,
 "text": "this is the high C, right?", "when": "2026-10-29T16:50"}
```
- `ref` plus its resolved cell (`t0`–`t1`, `f0`–`f1`) is always both: the reference never travels without real units.
- `pt` is the exact spot when a note was pinned by clicking (or with `notes.py --at`), because a cell is wider than a note.
- `kind` is `note`, `question` or `answer`; `re` is the number of the note it answers.

**Exporting keeps the grid still.** AuraLoom exports a tile over its own frame (a clip stays a clip), so a reference means the same spot before and after the round trip. Stretch is a lens: the loom tracks how much it has stretched, so notes stay in real seconds.

**Three ways a note can travel:**
- inside the tile's chunk (AuraLoom ⤓ Tile, `notes.py add`)
- as text (⧉ Copy as text, `notes.py md`), when the chunk can't make it, as in chat uploads
- drawn into a grid copy (`notes.py grid`), so a model sees the grid, the bounds and the pins in the pixels

Demo: `samples/notes-demo/`. In it, a question about a "high C" is answered by checking the recording: it was an E5.

## Tools
- `prototype/tilemeta.py`: read and write the chunk; the magma8 LUT and its inverse; the filename bounds. Run it on a PNG to print what the tile says about itself.
- `prototype/plain.py`: audio → plain tile (no axes or panels, 160 bands, one column per hop) with the chunk.
- `prototype/clip.py`: tile → clip that knows where it is.
- `prototype/notes.py`: list, add (by grid reference or by seconds + Hz), remove and reply to pinned notes; print them as markdown; draw a grid copy for models.
- AuraLoom v0.5–0.6: reads the chunk or the filename on tile import, writes the chunk on ⤓ Tile and in `weave.py` renders, and has the Pin thread, # Grid and the 📌 Notes panel.

## Open
- Whether to also embed a **compact score** for synthetic tiles (AuraLoom scores), so a tile made from a score carries its own answer key. That would be useful for the training test (seed 15).
- Whether a stereo or loudness-slice tile (seed 11) needs a `channels` field saying what R, G and B mean.
