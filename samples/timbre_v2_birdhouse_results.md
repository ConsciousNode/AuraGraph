# timbre lane v2: pitch by salience, timbre at that pitch, nearest-centroid judge
centroids (h2..h8 rel. h1 in dB, pitch wobble/20 cents, level change over 90 ms /2 dB):
- melodica: [-5.9, -7.1, -5.8, -7.3, -10.7, -12.9, -11.3, 10.0, -1.4]
- voice: [-3.2, -7.1, -17.3, -24.2, -23.0, -23.5, -16.9, 0.8, -0.1]
- guitar: [-3.1, -2.8, -3.3, -3.8, -8.3, -12.6, -9.7, 10.0, -1.2]

## held-out test (frames voted per span)
- 80.43-80.62 s truth **melodica** -> guitar {'melodica': 7, 'voice': 0, 'guitar': 10}  pitch ~A4
- 80.74-80.95 s truth **melodica** -> guitar {'melodica': 1, 'voice': 0, 'guitar': 17}  pitch ~D6
- 81.04-81.36 s truth **melodica** -> guitar {'melodica': 8, 'voice': 2, 'guitar': 17}  pitch ~A5
- 79.00-79.60 s truth **voice** -> voice {'melodica': 8, 'voice': 40, 'guitar': 4}  pitch ~D#4
- 82.70-83.60 s truth **guitar** -> guitar {'melodica': 17, 'voice': 7, 'guitar': 53}  pitch ~B5

spans right: 2/5
