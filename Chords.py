# Chords

chord_dict = {
'':['major','1','3','5'],
'm':['minor','1','b3','5'],
'min':['minor','1','b3','5'],
'5':['power cord','1','5'],
'+':['augmented','1','3','#5'],
'aug':['augmented','1','3','#5'],
'dim':['diminished','1','b3','b5'],
'sus4':['suspended 4th','1','4','5'],
'sus2':['suspended 2nd','1','2','5'],

'6':['major add 6th','1','3','5','6'],
'6/9':['major add 6th & 9th','1','3','5','6','9'],
'm6':['minor add 6th','1','b3','5','6'],
'mb6':['minor add flat 6th','1','b3','5','b6'],
'm6/9':['minor add 6th & 9th','1','b3','5','6','9'],

'm7':['minor 7th','1','b3','5','b7'],
'dim7':['diminished 7th','1','b3','b5','bb7'],
'm7b5':['minor 7th flat five','1','b3','b5','b7'],
'm(maj7)':['minor major 7th','1','b3','5','7'],

'7':['dominant 7th','1','3','5','b7'],
'maj7':['major 7th','1','3','5','7'],
'maj7b5':['major 7th flat 5th','1','3','b5','7'],
'maj7#11':['major 7th sharp eleven','1','3','5','7','#11'],

'7b5':['seventh flat five','1','3','b5','b7'],
'7b9':['seventh flat nine','1','3','5','b7','b9'],
'7#9':['seventh sharp nine','1','3','5','b7','#9'],
'7b5(#9)':['dominant 7th, flat 5th, sharp 9th','1','3','b5','b7','#9'],
'7#11':['dominant 7th, sharp 11th','1','3','5','b7','#11'],

'7#5':['dominant augmented 7th','1','3','#5','b7'],
'+7':['dominant 7th, sharp 5th','1','3','#5','b7'],
'maj7#5':['major 7th','1','3','#5','7'],
'aug7':['augmented 7th','1','3','#5','b7'],
'7b9#5':['augmented 7th flat nine','1','3','#5','b7','b9'],
'7#9#5':['augmented 7th sharp nine','1','3','#5','b7','#9'],
'+7b9':['dominant 7th, sharp 5th, flat 9th','1','3','#5','b7','b9'],
'+7#9':['dominant 7th, sharp 5th, sharp 9th','1','3','#5','b7','#9'],
'+7#5b9':['dominant 7th, sharp 5th, flat 9th','1','3','#5','b7','b9'],
'7sus4':['seventh suspended 4th','1','4','5','b7'],

'add9':['major add 9th','1','3','5','9'],
'+9':['9th, sharp 5th','1','3','#5','b7','9'],
'm(add9)':['minor add 9th','1','b3','5','9'],
'maj9':['major 9th','1','3','5','7','9'],
'm9':['minor 9th','1','b3','5','b7','9'],
'9':['dominant 9th','1','3','5','b7','9'],
'm9b5':['minor 9th, flat 5th','1','b3','b5','b7','9'],
'm9(maj7)':['minor 9th (major 7)','1','b3','5','7','9'],
'9#5':['dominant 9th sharp 5th','1','3','#5','b7','9'],
'9b5':['dominant 9th flat 5th','1','3','b5','b7','9'],
'9sus4':['9th suspended 4th','1','4','5','b7','9'],

'maj11':['major 11th','1','3','5','7','9','11'],
'm11':['minor 11th','1','b3','5','b7','9','11'],
'11':['11th','1','3','5','b7','9','11'],
'#11':['sharp 11th','1','3','5','b7','9','11'],

'maj13':['major 13th','1','3','5','7','9','b13'],
'm13':['minor 13th','1','b3','5','b7','9','11','13'],
'13':['13th','1','3','5','b7','9','13'],
'13sus4':['13th suspended 4th', '1','4','5','b7','9','13'],

'13b9':['13th flat nine','1','3','5','b7','b9','13'],
'13#9':['13th sharp nine','1','3','5','b7','#9','13'],

'test':['test','1','b3','bb5','b7','#9','##13'],
'all':['all', '1', 'b2' , '2' , 'b3' , '3' , '4' , 'b5' , '5' , 'b6', '6' , 'b7', '7']
}

chord_list = list(chord_dict.keys())