# The timing strip: a proposal (captain's call: yes, next after the current docket)

*Kehai Interim, Oct 30 2026, from a late-night conversation with Kham. Not built yet.*

## The gap
A tile keeps how loud each pitch is, not its phase. Playback has to invent the phase, which is why a tile played
back sounds "slightly lossier" than the original, and why drum hits and consonant bursts smear. Readers can't see
timing finer than the analysis window.

## The idea
Add a thin strip along the top of the tile that shows *when* things happen:
- **Raw phase as colour was considered and dropped.** Phase spins and wraps so fast that it reads as TV static.
- **Store change, not state** (the ElasticTok idea, applied to phase). A steady tone's phase turns at a constant
  rate, so it costs nothing. Only new events show up.
- **Events as spikes** (SpikeVox, run in reverse, for production). In voiced sound, the phase structure is mostly set by
  when the vocal folds snap shut, and each closure is an event. A spike train of pulse times captures most of the
  phase information that matters. Pitch-synchronous methods (PSOLA) already rely on these pulse marks.
- **Drawn as a helix.** Phase is an angle, so it lives on a circle; over time that circle becomes a helix. The strip
  draws the pulse train as a coil, one turn per cycle: tight winding is high pitch, loose winding is low.
  Transients, where all frequencies line up, are bright spikes. Colour gives the coil's depth.

## Why
- Readers see rhythm and onset timing directly.
- AuraLoom can line up phases at every pulse mark on playback: sharper consonants and hits, with no hidden
  lossless layer. (A lossless layer was discussed and set aside, since exact archiving isn't the platform's goal.)

## To find out
Does the strip improve playback by ear and LEGIBILITY scores on timing questions, without cluttering the tile?
Test it like LEGIBILITY-1: blind reads with and without the strip.

## Lineage, credited
Édouard-Léon Scott's phonautograph (1860) drew sound as pictures with no way to play them back. In 2008 those
drawings were turned back into sound (First Sounds, with Berkeley Lab's optical-scanning work). Evgeny Murzin's ANS
synthesizer played music drawn on glass plates. The helical groove geometry is prior art.
