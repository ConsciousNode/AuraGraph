# timbre judge v3: clean references + Birdhouse labels, pan masks

training frames: accordion 7190, melodica 3582, guitar 107, voice 155

centroids (h2..h8 rel. h1, dB):
- accordion: [-11.0, -7.4, -14.1, -14.7, -24.4, -24.2, -29.2, -27.3, -32.0]
- melodica: [-7.0, -6.9, -9.3, -7.9, -9.7, -9.2, -13.8, -13.9, -22.6]
- guitar: [-1.5, -6.6, -5.2, -5.5, -9.1, -12.2, -10.2, -11.3, -12.3]
- voice: [4.1, -7.1, 0.5, -8.1, -4.5, -0.1, -15.3, -17.6, -18.7]

## held-out spans (frames voted)
- doot 1 (truth accordion) -> **guitar** {'accordion': 0, 'melodica': 2, 'guitar': 14, 'voice': 0} pitch ~A4
- doot 2 (truth accordion) -> **guitar** {'accordion': 0, 'melodica': 5, 'guitar': 13, 'voice': 0} pitch ~G5
- doot 3 (truth accordion) -> **guitar** {'accordion': 0, 'melodica': 11, 'guitar': 16, 'voice': 0} pitch ~A5
- entrance 0:17 (truth accordion) -> **guitar** {'accordion': 0, 'melodica': 24, 'guitar': 26, 'voice': 0} pitch ~F#5
- fast part 1:32.7-1:36, right side (truth accordion) -> **guitar** {'accordion': 4, 'melodica': 41, 'guitar': 136, 'voice': 1} pitch ~E5
- 1:32.7-1:36, left side (truth guitar) -> **accordion** {'accordion': 36, 'melodica': 33, 'guitar': 28, 'voice': 3} pitch ~E5
- solo tail 1:22.7-1:23.6 (truth guitar) -> **guitar** {'accordion': 0, 'melodica': 2, 'guitar': 72, 'voice': 3} pitch ~C#5
- end of 'soul' 1:19-1:19.6 (truth voice) -> **accordion** {'accordion': 33, 'melodica': 5, 'guitar': 4, 'voice': 10} pitch ~D#4

spans right: 1/8
