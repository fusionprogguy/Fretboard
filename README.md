---
title: "README.md"
author: "fusionprogguy"
date: "Sunday, 31st Jan, 2016"
output: html_document
---

# README

Project: [Fretboard Python Program](Fretboard.py)

This Python project can be used to learn how to play chords and scales on a variety of stringed instruments such as guitar, bass, banjo, mandolin, bouzouki, and ukulele. You can view chords and scales in a text based format, test your knowledge of the fretboard with a note guessing game, train your knowledge of intervals/degrees, show tabs for a sequence of chords, learn about the mathematics of fret lengths, investigate Ted Greene's V-System for categorising chords (eg Close, Drop 2, Drop 3 etc), and explore the Joni Mitchell Tuning notation to identify tuning families for common and alternate tunings.

The purpose of the project was to learn more about chord and scale theory, and provide the user with visual material with which to learn where the notes are located on the fretboard and to practice reaching those notes while playing chords or scales. Another purpose of the project was to learn Python and to try and apply statistical techniques or machine learning once the data structure is in place and sufficient data has been collected on how humans would finger a certain chord or even a scale.

## Main Menu
To run the Fretboard Python program in the command window simply type:

```
python Fretboard.py
```

A menu will appear which reads from the settings file and checks the particular instrument you have chosen as well as any scales or chords you want to see. These chords and scales appear in brackets. When you activate any part of the program, any displays for your fretboard will be shown for your particular instrument. All the work around chords diagrams with fingerings are specific to 6-string guitar as this is the only data I currently have. Future releases will hopefully be able to look for patterns from the guitar tables and apply them to other instruments with similar tuning. 

```
MAIN MENU - 6 STRING GUITAR IN STANDARD TUNING
---------------------------------------------------------
1. Change Settings
2. All Notes on Fretboard
3. Scale in 12 keys (Major)
4. Scale Tabs (Major)
5. Chord Inver. in 12 keys (Maj7)
6. Chord Diagram in 12 keys (Maj7)
7. Mental Fretboard Trainer
8. Visual Fretboard Trainer
9. Semi-tone Interval Trainer
10. Finger Reach
11. Chord Chart (Maj7)
12. Your Chord Sequence (Tabs)
13. Chord Progressions
14. Play Notes of Scales
15. Joni Mitchell Tunings Notation
16. Ted Greene's V-System
17. Testing V-System
18. Exit

Please Select: 
```

You can then make your selection by entering a number for the menu item you'd like to explore. Most options should function, although as the project is not finished, there may still be bugs and list items that haven't been tested or completed in a while.


## Settings File

The [settings.txt](settings.txt) file contains important parameters which give the program the variables with which to work. 

The first half of the file contains the settings and looks something like this:

```
Instrument: Guitar
Strings: 6
Tuning: Standard
Root Note: F#
Chord Name: maj7
Scale: Major
Training String:
Start Training Fret: 0
End Training Fret: 12
Number of Questions: 5
Load And Save Score: N
Start Chord Fret: 0
End Chord Fret: 17
Print Log: No
```

The most important variables are the instrument and the number of strings. For a list of the available instruments, string numbers and alternate tunings see [Tunings.py](Tunings.py). Ignore the instrument + string, and use the rest of the string for the name of the tuning eg 'Standard' or 'Open D Minor'. To find the available Chord Names view [Chords.py](Chords.py). The convention for Chord Name for major chords for instance is a blank ('') while for minor it is simply 'm'. To find the available Scales view [Scales.py](Scales.py). The spelling of the tunings, chords, and scales must match exactly, including lower/upper caps. Generally the shorter names are used in the settings file.

The second half of the file describes the individual variables. You can edit the first half to change the way information will be displayed in various parts of the program. If you make any manual changes to the settings files and want it to take effect you must stop the Python program and run it again. The menu item "Change Settings" may change the variables in memory but currently does not save them to the text file. Later updates may change this.


## Updating Chords, Scales, Tunings and Progressions File

If you want to add your own chords, scales, tunings and progressions, all you need to do is keep the provided format consistent, and simply add a line with your desired information.

For example, if you wanted to add a diminished chord you'd write the line in [Chords.py](Chords.py):
```
'dim':['diminished','1','b3','b5'],
```
The first quote 'dim' would be how you'd enter it under 'Chord Name:' in [settings.txt](settings.txt). The second quote 'diminished' might be spelled out when the program runs and shows you chords for 12 keys for the diminished scale, for instance. 

If you wanted to add a new tuning for an instrument such as a 7-string guitar, with the tuning name 'Big Guitar', you'd use a format of _instrument_ _string no_ _short tuning name_ : [_list of open string notes_] eg.
```
    'Guitar 7 Big Guitar': ['G', 'C', 'E', 'G', 'C', 'E', 'G'],
```
If you wanted to add new scales, the format is a bit trickier. It has three parts - "Scale" (name of the scale), "H_Steps" (half steps), "L_Steps" (intervals). The element H_Steps is not vital for the running of the program as it is used only as a display, so can be left blank eg "H_Steps": ''

```
ListScales.append({"Scale": 'Dorian',  "H_Steps": 'R, W, H, W, W, W, H, W', "L_Steps": ['1', '2', 'b3', '4', '5', '6', 'b7']})
```

## Notes

Editing of this file is not advised as this file contains the available note names and variables that the program will use. Variable names should not be changed, but if there are any mistakes in the lists, these can be modified. notes_sharp and notes_flat are used a lot in the program, however some variables are only used in the Semi-tone interval trainer where you can test your knowledge of natural and accidental notes, and various octaves. 

Generally more testing has been done with notes that use flats than sharps. Hopefully future testing will ensure both notation can be consistently used throughout the program.

## Ted Greene

Greene created a system for categorising four-note chords into 14 voicing groups. For each note in the chord Greene would place them in one of the four choral voice names.

The voices are:
S for Soprano, the highest sounding note in the chord
A for Alto, the second highest note in the chord
T for Tenor, the third highest note in the chord
B for Bass, the lowest note in the chord

You can start on any note of the chord and determine where it lies. This is how you would examine the Emaj7 chord to find the voice name for each note.

```
Chord Name:  Emaj7
Intervals:   1, 3, 5, 7
Chord Notes: E, Ab, B, Eb

           E  A  D  G  B  E
     5fr.  :  :  :  :  E  :
           ----------------
           :  +  Ab :  :  :
           ----------------
           +  +  :  :  :  B
           ----------------
           :  :  :  Eb :  :
           ----------------
           :  :  +  +  +  :
           ----------------
Notes:           Ab Eb E  B
Intervals:       3  7  1  5
Voices:          B  T  A  S
```

![alt text](https://github.com/fusionprogguy/Fretboard/blob/master/TedGreene1.png "V-2: ABST Chord")

If you use the chord tone path 1, 3, 5, 7, you come up with ABST.

When walking through the chord tone path one should also note that higher octaves need to be converted to lower octave equivalents, so 9th = 2nd, 11th = 4ths, and 13th = 6th. Once you have done this and have the chord tone path order you can look up which system the chord belongs to in Ted Greene's Master Table.
    
![alt text](https://github.com/fusionprogguy/Fretboard/blob/master/MasterTable.png "Master Table")

## Future Updates

### Expanding the Chord Database
One of the goals for the future will be to use the database of almost 3000 chords as a basis for a computer program to generate new voicings. Currently only a small sample of around 5% of the chords is provided as an example to run the program. Most of my current work is getting the program to identify chords as belonging to one of the 14 V-System groups that Ted Greene has developed which relate to various drop voicings. See [Method 1 - How To Recognize Voicings](http://www.tedgreene.com/images/lessons/v_system/03_Method1_HowToRecognize.pdf)
I'm currently starting to work on a function to generate drop voicings of any 4-note close chord to see if this will expand the chord dictionary. After the drop function works for any close voicing, I will create a function to generate all of the 14 kinds of voicings, and discard any voicings which are spread too far apart for the human hand. 

### Chord Data Analysis
I imagine that various statistical techniques such as [k-means clustering ](https://en.wikipedia.org/wiki/K-means_clustering) could be used to group chords in a new way. I also imagine that machine learning could be applied to come up with realistic finger positions for existing and new chords. The data could be split to test the ability of the machine learning program to replicate the ringer position columns of the database.

### Music Theory
As my knowledge of music theory grows, I will try to incorporate this into the program. Feel free to fork this project and make modifications, or to send me feedback.


## Installation of Python

If you don't have Python installed you can use various online webpages to run the code from your browser. If they have multiple version of Python available select the older one. Both websites provide an online compiler which allows you to compile source code and execute it online in more than 60 programming languages.

Two web pages that allow you to run source code are:

1. [http://www.tutorialspoint.com](http://www.tutorialspoint.com/execute_python_online.php)

2. [http://ideone.com](http://ideone.com/)

Simply copy and paste [Fretboard.py](Fretboard.py) and press "Execute" in tutorialspoint or "Run" in ideone.


## Credits

After having writen the code I've found other software developers who are into music and providing useful programs online for those wanting to learn the fretboard. 

Their guitar scale generator can be found here:
[http://www.fachords.com/guitar-scale-generator](http://www.fachords.com/guitar-scale-generator)

One limitation in comparison to my program is that Fachords only provides tunings for 6-string guitars, whereas my program offers bass and guitar from 4-7 strings. The code is easily modifiable to add more stringed instruments and tunings.


## Music Theory for Beginners

For those new to music theory, here are some introductions to how scales and modes work, and the respective intervals between notes.

[https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes)
[https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals](https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals)
[https://en.wikipedia.org/?title=Scale_(music)](https://en.wikipedia.org/?title=Scale_(music))


## License

The scales and chords and related code in the files related to this project is distributed AS-IS and no responsibility implied or explicit can be addressed to the authors for its use or misuse. Any commercial use is prohibited without express permission.


## Contact

e-mail: steven.muschalik@gmail.com
Twitter: @StevenMuschalik
