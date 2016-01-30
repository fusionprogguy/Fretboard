# coding=utf-8

# Progressions

# Roman Numerals
#               ['1', 'b2', '2',  'b3',  '3',   '4',  'b5', '5', 'b6',  '6',  'b7',   '7']
roman_numeral = ['I', 'ii', 'II', 'iii', 'III', 'IV', 'bV', 'V', 'vi', 'VI', 'vii', 'VII']
roman_numeral_major = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']              # major = 1-3-5
roman_numeral_minor = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']              # minor = 1-b3-5
roman_numeral_diminished = ['io', 'iio', 'iiio', 'ivo', 'vo', 'vio', 'viio']  # diminished = 1-b3-b5.
roman_numeral_augmented = ['I+', 'II+', 'III+', 'IV+', 'V+', 'VI+', 'VII+']   # augmented = 1-3-♯5
roman_numeral_dimsus = ['iosus2', 'iiosus2', 'iiiosus2', 'ivosus2', 'vosus2', 'viosus2', 'viiosus2']  # diminished suspended / diminished 7th

roman_pos = {
'I':0, 'ii':2, 'II':2, 'iii':4, 'III':4, 'IV':5, 'V':7, 'vi':9, 'VI':9, 'vii':10, 'VII':11, 'VIII':12,   # Major
'i':0, 'iv':5, 'v':6,                                                                                    # Minor
'io':0, 'iio':1, 'iiio':3, 'ivo':5, 'vo':7, 'vio':9, 'viio':10,                                          # diminished
'I+':0, 'II+':2, 'III+':3, 'IV+':5, 'V+':7, 'VI+':9, 'VII+':11,                                          # Augmented
'iosus2':0, 'iiosus2':2, 'iiiosus2':3, 'ivosus2':5, 'vosus2':7, 'viosus2':9, 'viiosus2':10
}

roman_scale_dict = {
# Triads for different scales: http://simianmoon.com/snglstringtheory/scales/modesandprogressions.html
'Major': ['I' 'ii' 'iii' 'IV' 'V' 'vi' 'viio'],
'Ionian': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'viio'],
'Dorian': ['i', 'ii', 'bIII', 'IV', 'v', 'vio', 'bVII'],
'Phrygian': ['i', 'bII', 'bIII', 'iv', 'vo', 'bVI', 'bvii'],
'Lydian': ['I', 'II', 'iii', '#ivo', 'V', 'vi', 'vii'],
'Mixolydian': ['I', 'ii', 'iiio', 'IV', 'v', 'vi', 'bVII'],
'Aeolian': ['i', 'iio', 'bIII', 'iv', 'v', 'bVI', 'bVII'],
'Locrian': ['io', 'bII', 'biii', 'iv', 'bV', 'bVI', 'bvii'],
'Melodic Minor': ['i', 'ii', 'bIII+', 'IV', 'V', 'vio', 'viio'],
'Harmonic Minor': ['i', 'iio', 'bIII+', 'iv', 'V', 'bVI', 'viio'],
'Spanish Major': ['I', 'bII', 'iiio', 'iv', 'vo', 'bVI', 'bvii'],
'Altered Dominant bb7:': ['io', 'biii', 'biiio', 'bIV+', 'bv', 'bVI', 'bbVII'],
'Javanese': ['i', 'bII+', 'bIII', 'IV', 'vo', 'vio', 'bvii'],
'Lydian Augment': ['I+', 'II', 'III', '#iv', '#vo', 'vi', 'vii'],
'Overtone': ['I', 'II', 'iiio', '#ivo', 'v', 'vi', 'bVII+'],
'Super Locrian': ['io', 'bii', 'biii', 'bIV+', 'bV', 'bVI', 'bviio'],
'Pentatonic Major': ['I ', 'II5', 'iii(no5) ', 'V5 ', 'vi'],
'Egyptian': ['I5 ', 'ii(no5)', 'IV5', 'v ', 'bVII'],
'Pentatonic Minor': ['i ', ' bIII ', ' IV5', 'v(no5)', 'bVII5'],
'Gypsy Minor': ['i', 'IIb5', 'bIII+', '#ivosus2', 'V', 'bVI', 'vii'],
'Oriental': ['Ib5', 'bII+', 'iiiosus2', 'IV', 'bV', 'vi', 'bvii'],
'Byzantine': ['I', 'bII', 'iii', 'iv', 'Vb5', 'bVI+', 'viiosus2']
}

scale_type = ['major', 'minor', 'diminished', 'augmented']

# Common Progressions
# Progressions from here: https://thornepalmer.wordpress.com/2011/12/29/the-10-most-used-chord-progressions-in-pop-and-rock-and-roll/
progression_dict = {
    'I–V–vi–IV': ['I', 'V', 'vi', 'IV'],  # eg. (G – D – Em – C)  or eg. (Gm Dm E Cm)
    'I–vi–IV–V': ['I', 'vi', 'IV', 'V'],  # eg. (G – Em – C – D)
    'I–V–vi–iii–IV–I–IV–V': ['I', 'V', 'vi', 'iii', 'IV', 'I', 'IV', 'V'],  # eg. (G – D – Em – Bm – C – G – C – D)
    'I–I–I–I–IV–IV–I–I–V–V–I–I': ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'V', 'I', 'I'],  # eg. (G – G – G – G – C – C – G – G – D – D – G – G)
    'ii–IV–V': ['ii', 'IV', 'V'],  # eg. (am – C – D)
    'I–IV–V–IV': ['I', 'IV', 'V', 'IV'],  # eg. (G – C – D – C)
    'V–IV–I': ['V', 'IV', 'I'],  # eg. (D – C – G)
    'vi–IV–I–V': ['vi', 'IV', 'I', 'V'],  # eg. (em – C – G – D)
    'vi–V–IV–III': ['vi', 'V', 'IV', 'III'],  # eg. (em – D – C – B)
    'vi–V–VI–V': ['vi', 'V', 'VI', 'V'],  # eg. (em – D – C – D)
    'ii–I–V–bVII-VI': ['ii', 'I', 'V', 'VI', 'VI'],  # eg. (am – G – D – F - E)
    'ii–I–vii–bVII-VI': ['ii', 'I', 'vii', 'VI', 'VI'],  # eg. (am – G – Gb – F - E)
    'i-V-bVII-IV-bVI-bIII-iv-V': ['i', 'V', 'VI', 'IV', 'vi', 'bIII', 'iv', 'V']
    #http://simianmoon.com/snglstringtheory/chords/prog1.html
    #jazz progressions: ii-V. The next being ii-V-I. these can be extended to : vi-ii-V-I, iii-vi-ii-V-I, viio-iii-vi-ii-V-I, IV-viio-iii-iv-ii-V-I. ( in the key of c the last one would be F-Bo-Em-Am-Dm-G-C.)
}

#COMMON MODAL PROGRESSIONS
#progression_mode = {
#Below is a list of some common progressions by mode:
# Ionian: I-IV, I-V, I-IV-V, I-ii-IV-V, I-V-IV, I-vi-V-IV, I-iii-IV-V, I-ii-iii-IV, ii-V-I, I-vi-ii-V, I-iii-vi-ii-V, I-V-vi
# Dorian: i-ii, i-ii-bIII, i-IV, i-ii-bIII-IV, i-IV-v, i-bVII
# Phrygian: i-bII, i-bII-bIII, i-bII-bIII-iv, i-vo
# Lydian: I-II, I-II-iii, I-II-V
# Mixolydian: I-IV-bVII, I-bVII, I-IV-v
# Aeolian: i-iv, i-v, i-iv-v, bVI-bVII-i, iio-v-i, bIII-bVII-i, i-bIII, i-bVI, i-iio-bIII-iv, i-bVII, i-bVI-v, I5-bVII5-bVI5-V5
# Locrian: io-bII, or bV/1-bVI/1
# Harmonic Minor: i-V, i-iio-bIII+-iv, i-iv-V, i-V-bVI
# Spanish Major: I-bII, I-bvii
# Melodic Minor: i-IV, i-ii-bIII+-IV, i-IV-V
#}

chord_type = {
    # file: http://www.tsmp.org/keyboard/lias/pdf/symbols.pdf
    'Major Triad': ['','M','maj'],                                   # eg C
    'Minor Triad': ['m', '-', 'mi', 'min'],                # eg Cm, C-, Cmi, Cmin'
    'Diminished Triad': ['o, dim'],                        # eg Co, Cdim
    'Augmented Triad': ['+', 'aug', '(#5)'],               # eg C+, Caug, C(#5)
    'Minor Seventh': ['m7', '-7', 'mi7', 'min7'],          # eg Cm7, C-7, Cmi7, Cmin7
    'Dominant Seventh': ['7','dom7'],                      # eg C7
    'Augmented Seventh': ['+7', 'aug7', '7(#5)','7(aug5)'],
    'Major Seventh': ['maj7', '∆7', 'ma7', 'M7'],         # eg Cmaj7, C∆7, Cma7, CM7
    'Diminished Seventh': ['o7', 'dim7'],                 # eg Co7, Cdim7
    'Half Diminished Seventh': ['m7(b5)', 'Ø7', '-7(b5)','min7dim5']  # eg Cm7(b5), CØ7, C-7(b5)
}