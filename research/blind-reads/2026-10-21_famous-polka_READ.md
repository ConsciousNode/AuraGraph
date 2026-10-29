# Blind read #1: "The Famous Polka" (TMBG, Live at the Music Hall of Williamsburg, disc 1 track 4, 2:08)
*Kehai Interim, written 2026-10-21 ~18:35 ET, committed BEFORE Kham listens and grades.*
Tools: proto.py v0.2.1 tiles (16 s), closeup.py, low-band onset counting, stereo pan measurement. No timbre judge (it failed its fair test today).
**Prior knowledge, flagged:** I know the title and that a studio version exists on *Flood*; I believe it's an instrumental. I tried to read only from the data; where prior knowledge could leak in, it's marked.

## Overall shape (high confidence)
- **~1:30 of music, then the crowd, then talking.** The low end (bass/kick) runs from the first frame to a final hit at **~1:29.5**, then disappears for the rest of the track.
- **1:29.6 to ~1:37: cheering** (overlapping gliding arcs 0.9-1.8 kHz, no low end).
- **~1:37 to 2:08: speech, stage banter**, not singing: syllable-sized bursts with gliding, speech-like harmonics, pitch around 120-250 Hz (an adult man talking, maybe more than one), pauses, crowd reactions in between. Medium-high confidence it's talk, low confidence on how many people.

## Tempo and feel (high confidence on the number, medium on the description)
- Bass/kick hits about every **0.348 s = ~172 per minute** through the song. The tool's "87 bpm" is half of that (the bar pulse); its double-tempo check was as strong or stronger, which fits.
- Feel: a fast two-step **oom-pah**. The stereo-width panel shows wide low-frequency blobs on alternating beats (a low note on one beat, something else on the next), which is the polka pattern.
- **Slight push at the end:** the last section (1:14-1:29.5) runs ~178/min vs ~172 earlier. Medium confidence (about a 3-4% speed-up).

## Sections (medium-high confidence on times)
| Time | What I read |
|---|---|
| 0:00-0:27 | **A**: oom-pah groove from the very first frame (no count-in visible; the band is already going, or the track was cut tight). A short low-end gap ~0:01.0-0:01.4. Fast melody on top: short, straight-pitched notes stepping quickly in the A4-A6 range. |
| 0:27-0:37 | **B / break**: the steady oom-pah breaks up into syncopated hits with gaps, sustained chords ringing between them, sparser texture. A bright gliding blob around **0:27.3** (possible shout/"whoo" from the band or crowd; low confidence). |
| 0:37-1:04 | **A** again. |
| 1:04.5-1:14.3 | **B / break** again, same pattern as the first (the gaps line up the same way). |
| 1:14.3-1:29.5 | **A** final, slightly faster, ending on a hit at ~1:29.5. |

## Instruments (medium-low confidence; this is the hard part)
- **Bass + kick** on the "oom", **chords** on the "pah". Drums present throughout the A sections.
- **Lead melody:** rapid, steady-pitched notes (straight lines, no vibrato), the free-reed look from Birdhouse. Consistent with **accordion**, possibly doubled by guitar. I can't prove which from timbre (the judge failed today), and knowing John plays accordion biases me. The lead energy leans slightly **left** (25% of standout lead energy left vs 12% right), unlike Birdhouse's right-side accordion, so either it's mixed differently or it's not the accordion carrying the line.
- **Vocals: I see no clear singing** in the music part (no long wobbly vowel stacks like Birdhouse's). Medium confidence; my prior also says instrumental, so this isn't independent.
- Harmony: chroma centers on C, G, D, A; the chord reader wanders between C, G, Am, D. Major key, probably **C or G**. Low confidence.

## Questions for Kham's ears (what I most want graded)
1. Is it instrumental? Is there a shout at ~0:27?
2. Lead instrument(s): accordion, guitar, both? Which side?
3. Are 0:27-0:37 and 1:04-1:14 the same "break" section?
4. Does it speed up at the end?
5. After ~1:30: cheering, then talking? Who's talking, roughly?
