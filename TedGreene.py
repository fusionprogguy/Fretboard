# Ted Greene's Master Formula Table
# http://www.tedgreene.com/images/lessons/v_system/03_Method1_HowToRecognize.pdf

greene_table = {
    'V-1': ['BTAS', 'SBTA', 'ASBT', 'TASB'],
    'V-2': ['TABS', 'STAB', 'BSTA', 'ABST'],
    'V-3': ['ABTS', 'SABT', 'TSAB', 'BTSA'],
    'V-4': ['STBA', 'ASTB', 'BAST', 'TBAS'],
    'V-5': ['BATS', 'SBAT', 'TSBA', 'ATSB'],
    'V-6': ['B-TAS', 'SB-TA', 'ASB-T', 'TASB-'],  # (V-1 with B an octave lower)
    'V-7': ['TAB-S', 'STAB-', 'B-STA', 'AB-ST'],  # (V-2 with B an octave lower)
    'V-8': ['TBSA', 'ATBS', 'SATB', 'BSAT'],
    'V-9': ['TABS+', 'S+TAB', 'BS+TA', 'ABS+T'],  # (V-2 with S an octave higher)
    'V-10': ['T-AB-S', 'ST-AB-', 'B-ST-A', 'AB-ST-', 'TA+BS+', 'S+TA+B', 'BS+TA+', 'A+BS+T'],
    # (V-2 with both B and T an octave lower, or A and S an octave higher)
    'V-11': ['S+TBA', 'AS+TB', 'BAS+T', 'TBAS+'],  # (V-4 with S an octave higher)
    'V-12': ['AB-TS', 'SAB-T', 'TSAB-', 'B-TSA'],  # (V-3 with B an octave lower)
    'V-13': ['B-T-AS', 'SB-T-A', 'ASB-T-', 'T-ASB-', 'BTA+S+', 'S+BTA+', 'A+S+BT', 'TA+S+B'],
    # (V-1 with both B and T an octave lower, or A and S an octave higher)
    'V-14': ['BTAS+', 'S+BTA', 'AS+BT', 'TAS+B']  # (V-1 with S an octave higher)
}

#Is the extra octave between B and T? If so, then...
# If you looked up V-1, you have a V-6.
# If you looked up V-2, you have a V-7.
# If you looked up V-3, you have a V-12.
#Is the extra octave between T and A? If so, then...
# If you looked up V-1, you have a V-13.
# If you looked up V-2, you have a V-10.
#Is the extra octave between A and S? If so, then...
# If you looked up V-1, you have a V-14.
# If you looked up V-2, you have a V-9.
# If you looked up V-4, you have a V-11.


def ted_greene_method1_text():
    # http://www.tedgreene.com/images/lessons/v_system/03_Method1_HowToRecognize.pdf
    print ""
    print "TED GREENE'S V-SYSTEM - METHOD 1"
    print "---------------------------------------------------------"
    print ""
    print "Greene created a system for categorising four-note chords into 14 voicing groups"
    print "For each note in the chord Greene would place them in one of the four choral voice names."
    print ""
    print "The voices are:"
    print "S for Soprano, the highest sounding note in the chord"
    print "A for Alto, the second highest note in the chord"
    print "T for Tenor, the third highest note in the chord"
    print "B for Bass, the lowest note in the chord"
    print ""
    print "You can start on any note of the chord and determine where it lies. This is how you would"
    print "examine the Emaj7 chord to find the voice name for each note."
    print ""
    print "Chord Name:  Emaj7"
    print "Intervals:   1, 3, 5, 7"
    print "Chord Notes: E, Ab, B, Eb"
    print ""
    print "           E  A  D  G  B  E"
    print "     5fr.  :  :  :  :  E  :"
    print "           ----------------"
    print "           :  +  Ab :  :  :"
    print "           ----------------"
    print "           +  +  :  :  :  B"
    print "           ----------------"
    print "           :  :  :  Eb :  :"
    print "           ----------------"
    print "           :  :  +  +  +  :"
    print "           ----------------"
    print "Notes:           Ab Eb E  B"
    print "Intervals:       3  7  1  5"
    print "Voices:          B  T  A  S"
    print ""
    print "Chord Paths"
    print "You can start on any interval as long as you move from left to right through "
    print "the ascending chromatic order of chord tones in a circular fashion as follows."
    print ""
    print "Intervals              Voices"
    print "1 -> 3 -> 5 -> 7  =>  A B S T"
    print "3 -> 5 -> 7 -> 1  =>  B S T A"
    print "5 -> 7 -> 1 -> 3  =>  S T A B"
    print "7 -> 1 -> 3 -> 5  =>  T A B S"
    print ""
    print "Ted Greene had six main groups of chords which followed this circular, chronological order of chord tones."
    print "Once you have figured out one of the chord paths for your chord, you can simply look it up in the table."
    print ""
    print "V-SYSTEM MASTER TABLE (PART 1)"
    print "V-1: BTAS, SBTA, ASBT, TASB"
    print "V-2: TABS, STAB, BSTA, ABST"
    print "V-3: ABTS, SABT, TSAB, BTSA"
    print "V-4: STBA, ASTB, BAST, TBAS"
    print "V-5: BATS, SBAT, TSBA, ATSB"
    print "V-8: TBSA, ATBS, SATB, BSAT"
    print ""
    print "For less commonly used chords with greater than an octave between adjacent voices there are eight"
    print "more groups which reference the main six groups. I have used a +/- sign after a voice to"
    print "indicate if the note is an octave higher (+) or an octave lower (-)"
    print ""
    print "V-SYSTEM MASTER TABLE (PART 2)"
    print "V-6: B-TAS, SB-TA, ASB+T, TASB-                                         ( V-1 with B- )"
    print "V-7: TAB-S, STAB-, B-STA, AB-ST                                         ( V-2 with B- )"
    print "V-9: TABS+, S+TAB, BS+TA, ABS+T                                         ( V-2 with S+ )"
    print "V-10: T-AB-S, ST-AB-, B-ST-A, AB-ST-, TA+BS+, S+TA+B, BS+TA+, A+BS+T    ( V-2 with both B-T-, or A+S+ )"
    print "V-11: S+TBA, AS+TB, BAS+T, TBAS+                                        ( V-4 with S+ )"
    print "V-12: AB-TS, SAB-T, TSAB-, B-TSA                                        ( V-3 with B- )"
    print "V-13: B-T-AS, SB-T-A, ASB-T-, T-ASB-, BTA+S+, S+BTA+, A+S+BT, TA+S+B    ( V-1 with both B-T-, or A+S+ )"
    print "V-14: BTAS+, S+BTA, AS+BT, TAS+B                                        ( V-1 with S+ )"
    print ""
    print "When walking through the chord tone path one should also note that higher octaves need to be"
    print "converted to lower octave equivalents, so 9th = 2nd, 11th = 4ths, and 13th = 6th"
    print ""
    print "The V-System only sometimes works with chords that use open strings, however Ted mostly played chords with"
    print "fretted notes only. That way he could easily transpose his progressions and arrangements. When he did"
    print "include an open string, most commonly it would be an open E or A bass note. D"
    print ""

#Drop 3 is good for solo accompaniment without a bass player.
#Drop 2 & 4 chords are great strumming chords
#Drop 2 & 3 are good for finger style
#Partial chords are three note chords that are good for quick tempos or more compact sounds. Partial Chords are so names as they leave out a note from a four note voicing such as a Drop 2.
#https://www.scribd.com/doc/289955507/The-Barry-Harris-Harmonic-Method-for-Guitar