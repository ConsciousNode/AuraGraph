"""Ground-truth labels for "Birdhouse in Your Soul" (TMBG, live at Music Hall of Williamsburg).
All from Kham's ears (2026-10-17 and 2026-10-21). Times in seconds. side = which stereo side
to keep (None = whole mix). Spans are mine, built around the moments he named.

Instruments (Kham): John on accordion from ~0:03 (with vocals and guitar); keyboard from ~0:12,
same few notes on repeat, then from 0:17 it continues about an octave lower; drums from ~0:14
(tom pattern bum-buh bum-buh bum-bum buh-duh-dum, 0:14-0:16); hi-hat count-in 3+3 at the very start.
"""

VOICE = {   # (start, end, vowel, word)
    "a1": (29.0, 30.2, "a", "a little"),
    "e1": (47.7, 48.9, "e", "meee"),
    "e2": (112.7, 113.9, "e", "meee"),
    "e3": (114.8, 116.0, "e", "ancestryyy"),
    "e4": (118.7, 119.9, "e", "freee"),
    "i1": (109.7, 110.7, "i", "I am"),
    "i2": (120.8, 121.8, "i", "I respect"),
    "i3": (122.8, 123.8, "i", "I'd be"),
    "o1": (19.6, 20.8, "o", "ooover / yoooouuu"),
    "o2": (31.8, 33.4, "o", "sooooul"),
    "o3": (77.0, 78.8, "o", "sooouuul (held)"),
    "u1": (129.6, 130.8, "u", "bluuuebird"),
}

GUITAR = {
    "triplets_left": (36.0, 44.0, "left", "little triplets, louder left"),
    "held_left": (91.4, 92.6, "left", "4 held notes under the fast accordion"),
    "held_left2": (92.7, 96.0, "left", "held notes under the fast accordion"),
    "solo": (81.65, 82.6, None, "little solo, back half of 1:21"),
    "solo_tail": (82.7, 83.6, None, "end of the little solo"),
}

ACCORDION = {
    "fast_right": (92.7, 96.0, "right", "fast notes over the slow guitar, loudest right"),
    "doots": (80.43, 81.36, None, "doot doot dooot (G5 G5 A5)"),
}

KEYBOARD = {
    "repeat": (12.3, 14.0, None, "same notes on repeat, before the drums"),
}
