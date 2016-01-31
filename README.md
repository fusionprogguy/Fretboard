---
title: "README.md"
author: "fusionprogguy"
date: "Monday 1st of Feb, 2016"
output: html_document
---

# README

Project: [Fretboard Python Program](Fretboard.py)

This Python project can be used to learn how to play chords and scales on a variety of stringed instruments such as guitar, bass, banjo, mandolin, bouzouki, and ukulele. You can view chords and scales in a text based format, test your knowledge of the fretboard with a note guessing game, train your knowledge of intervals/degrees, show tabs for a sequence of chords, learn about the mathematics of fret lengths, investigate Ted Greene's V-System for categorising chords (eg Close, Drop 2, Drop 3 etc), and explore the Joni Mitchell Tuning notation to identify tuning families for common and alternate tunings.

The purpose of the project was to learn more about chord and scale theory, and provide the user with visual material with which to learn where the notes are located on the fretboard and to practice reaching those notes while playing chords or scales. Another purpose of the project was to learn Python and to try and apply statistical techniques or machine learning once the data structure is in place and sufficient data has been collected on how humans would finger a certain chord or even a scale.

## Main Menu
To run this project you will need to install Python or run it in a web browser. See the section below called "Installation of Python" for further details. Assuming you have Python installed and you are in the same folder as the Python files in this project, in the command window simply type:
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
## Chord Diagrams

Chord Diagrams are an important tool in learning how to play chords and understanding the building blocks of music. Chord diagrams are a visual representation of the fretboard at a given position. The current database contains almost 3000 chords, with details of the fret position on each string, the notes for each string, the intervals for each string and the fingers used for each string.

I found the dots in most chord diagrams lacking in information, so decided that I wanted three views for each chord. You can view the Notes, Intervals, or Finger Positions, depending on what is most important to you. 

When running the Ted Greene menu, you get to see three views of a chord. The interval information is gathered from both the interval details from Chord Finger Positions.csv and Chords.py. One of them from Chords.py contains higher octaves (eg 9), whereas the csv file details do not and are converted to lower octave equivalents (eg 2) because Ted Greene converts them down as part of his V-System. The following is sample output from a close position Dm9 chord 

```
Chord Name:  Dm9
Compact form: x-x-15-14-13-12 x-x-4-3-2-1
Intervals:   1, b3, 5, b7, 9 / 2 b3 5 b7 
Chord Notes: F, A, C, E

       Notes                 Intervals             Finger Pos  

       E  A  D  G  B  E      E  A  D  G  B  E      E  A  D  G  B  E  
 12fr. +  +  :  :  :  E      +  +  :  :  :  9      +  +  :  :  :  1  
       ----------------      ----------------      ----------------
       +  :  :  :  C  :      +  :  :  :  b7 :      +  :  :  :  2  :  
       ----------------      ----------------      ----------------
       :  :  :  A  :  :      :  :  :  5  :  :      :  :  :  3  :  :  
       ----------------      ----------------      ----------------
       :  +  F  :  :  :      :  +  b3 :  :  :      :  +  4  :  :  :  
       ----------------      ----------------      ----------------
       :  :  :  :  :  :      :  :  :  :  :  :      :  :  :  :  :  :  
       ----------------      ----------------      ----------------

       x  x  F  A  C  E      x  x  b3 5  b7 9      x  x  b3 5  b7 9  
```

I begin each chord diagram with a starting fret, which is most likely the first fret you will use. If you want to limit the range of chords that may be shown, you can update this in [settings.txt](settings.txt) under 'Start Chord Fret' and 'End Chord Fret'. Currently I have restricted the Chord Database to chords between fret 0-5, though the full version has chords up to fret 17. 

Generally I show 5 frets as a default, however it changes if the chord is stretched over more than 5 frets.

When a certain fret or string is not part of the chord, i use ":"
When a certain note is part of the chord, but not used in that particular fingering, I use "+"
If there is note, interval or finger used for a particular string, the fret contains the relevant detail.

As a beginner you may need help identifying the fingers to use, so your focus may be on "Finger Pos". As you increase your knowledge of chord construction, intervals may become more important. Finally, when you want to focus on fretboard note knowledge, the note diagram will be useful. I have also modified the final line to include muted strings with the notes and intervals because it means you don't have to look at two different parts of the chart to identify them. 

In Finger Position each finger is allocated to a number. This applies to your right or left hand, regardless if you are right or left handed, however the programming was implemented for right-handed people. Future versions may be able to swap strings for left-handed users.

```
1 = index finger
2 = middle finger
3 = ring finger
4 = little / pinky finger
```

## Fretboard Diagrams

When you select "Scale in 12 keys (Major)" in the menu, you will be shown a horizontal fretboard diagram for 12 keys with a Notes view, and an Interval view. Details of how the scale is constructed in terms of intervals/degrees and whole/half steps is also shown. To display a different scale you can edit the file [settings.txt](settings.txt) and go to the line 'Scale: Major' and update it to any scale found in [Scales.py](Scales.py) such as 'Major Blues'. If you want to print out a text file you need have the line "Print Log: Yes" in the settings file. You should be able to then open the text file eg "log_guitar_maj7_major-sat_jan_30_22_49_10_2016.txt" and print it out, or paste it into an editor to increase the font size.

```
Scale Name:  A Major
Steps:       R, W, W, H, W, W, W, H
Intervals:   1, 2, 3, 4, 5, 6, 7
Scale Notes: A, B, Db, D, E, Gb, Ab
 
   E|----|--Gb|----|--Ab|---A|----|---B|----|--Db|---D|----|---E|
   B|----|--Db|---D|----|---E|----|--Gb|----|--Ab|---A|----|---B|
   G|--Ab|---A|----|---B|----|--Db|---D|----|---E|----|--Gb|----|
   D|----|---E|----|--Gb|----|--Ab|---A|----|---B|----|--Db|---D|
   A|----|---B|----|--Db|---D|----|---E|----|--Gb|----|--Ab|---A|
   E|----|--Gb|----|--Ab|---A|----|---B|----|--Db|---D|----|---E|
                 O         O         O         O             OO  
 
   5|----|---6|----|---7|---1|----|---2|----|---3|---4|----|---5|
   2|----|---3|---4|----|---5|----|---6|----|---7|---1|----|---2|
   G|---7|---1|----|---2|----|---3|---4|----|---5|----|---6|----|
   4|----|---5|----|---6|----|---7|---1|----|---2|----|---3|---4|
   1|----|---2|----|---3|---4|----|---5|----|---6|----|---7|---1|
   5|----|---6|----|---7|---1|----|---2|----|---3|---4|----|---5|
                 O         O         O         O             OO  
```

## Notes

Editing of the [Notes.py](Notes.py) file is not advised as this file contains the available note names and variables that the program will use. Variable names should not be changed, but if there are any mistakes in the lists, these can be modified. _notes_sharp_ and _notes_flat_ are used a lot in the program, however some variables are only used in the Semi-tone interval trainer where you can test your knowledge of natural and accidental notes, and various octaves. 

Generally more testing has been done with notes that use flats than sharps. Hopefully future testing will ensure both notation can be consistently used throughout the program.

## Ted Greene

Greene created a system for categorising four-note chords into 14 voicing groups. For each note in the chord Greene would place them in one of the four choral voice names.

The voices are:
*   S for Soprano, the highest sounding note in the chord
*   A for Alto, the second highest note in the chord
*   T for Tenor, the third highest note in the chord
*   B for Bass, the lowest note in the chord

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

When you use the chord tone path order 1 -> 3 -> 5 -> 7 and look up the associated voicings you come up with ABST.

When walking through the chord tone path one should also note that higher octaves need to be converted to lower octave equivalents, so 9th = 2nd, 11th = 4ths, and 13th = 6th. Once you have done this and have the chord tone path order you can look up which system the chord belongs to in Ted Greene's Master Table.
    
![alt text](https://github.com/fusionprogguy/Fretboard/blob/master/MasterTable.png "Master Table")

# Future Updates

## Tabs
 So far the program does not provide tabs, however it does produce nice text-based diagrams of chord diagrams and fretboard diagrams. Once this tab feature is implemented, I may add various Exercises that are shown in fretboard and tabs format. For example, the tab format for a A minor blues pentatonic scale for a 4-string bass would look like this:
 
 ```
G|-----------------------5--7--8--7--5-----------------------|
D|-----------------5--7-----------------7--5-----------------|
A|--------5--6--7-----------------------------7--6--5--------|
E|--5--8-----------------------------------------------8--5--|
 ```
 
## Expanding the Chord Database
One of the goals for the future will be to use the database of almost 3000 chords as a basis for a computer program to generate new voicings. Currently only a small sample of around 5% of the chords is provided as an example to run the program. Most of my current work is getting the program to identify chords as belonging to one of the fourteen V-System groups that jazz great Ted Greene has developed which relate to various drop voicings. See [Method 1 - How To Recognize Voicings](http://www.tedgreene.com/images/lessons/v_system/03_Method1_HowToRecognize.pdf)

## Inversions
I will be creating a small function to generate same-string inversions of chords. Hopefully this may yield a few more chords for the Chord Database.
See [How Systematic Inversions Relate to the V-System](http://www.tedgreene.com/images/lessons/v_system/27_How_Systematic_Inversions_Relate_to_the_V-System.pdf)

## Drop Voicings / Close Voicings
I'm currently starting to work on a function to generate drop voicings of any 4-note close chord to see if this will expand the chord dictionary. Popular voicings include Drop 2, Drop 3, Drop 2 & 4 and more. You can even have chords with multiple octave drops! I may also need to make alterations by moving non-dropped voices into unison positions. After the drop function works for any close voicing, I will attempt to create a function to generate all of the fourteen possible kinds of voicings and discard any voicings which are spread too far apart for the human hand. So far it may be the most challenging endeavour as I do not yet know of a way of identifying reasonable voicings out of the chaos of possibilities. Once I've got that works it will hopefully lead to an almost comprehensive chord dictionary of 3 and 4-note chords, and give me the framework to perhaps systematize chords with up to 5 or 6 notes. 

## Music Theory
To deepen my understanding of Drop 2 chords I will be examining the work of Randy Vincent in his book [Jazz Guitar Voicings - Vol.1: The Drop 2 Book](http://www.amazon.com/Jazz-Guitar-Voicings-Vol-1-Drop/dp/1883217644/). I may also learn more theory through his book ['Three-Note Voicings and Beyond'](http://www.amazon.com/Three-Note-Voicings-Beyond-Randy-Vincent/dp/1883217660/)

As my knowledge of music theory grows, and as I collect the gems that have been discovered by guitar masters, I will try to incorporate what I learn into the program. I've recently come across some work by jazz guitar legend Pat Martino, who has a unique vision of the fretboard that he calls [Sacred Geometry](http://truefire.com/blog/guitar-lessons/pat-martino-guitar-lesson-sacred-geometry/). 

For those new to music theory, here are some introductions to how scales and modes work, and the respective intervals between notes.

[https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes)
[https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals](https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals)
[https://en.wikipedia.org/?title=Scale_(music)](https://en.wikipedia.org/?title=Scale_(music))

There is so much to learn that it would even take a dedicated music student many years to practice, learn and master. However, maybe in the not-to-distant future, machines will match and even surpass human masters both as music performers and as educators. Hopefully my research will provide new insights about music and help organise the information. I believe music should be alive, so it can be generated on the fly, in an interactive fashion, in contrast to books which though useful, remain static. This way as you get scales and chords under your fingers, you can modify the parameters of the program to provide you with exercises which challenge you as you develop your skills.  

##Chord Data Analysis & Machine Learning
I imagine that various statistical techniques such as [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) could be used to group chords in a new way. Ted Greene was starting to explore S-note chords and how to organise them. Perhaps with the tools of statistics and machine learning I will be able to provide an overview of possible solutions. I also imagine that machine learning could be applied to come up with realistic finger positions for existing and new chords. The chord database could be split to test the ability of the machine learning program to replicate the finger position columns of the database. As I learn more about statistics and machine learning I hope to implement my discoveries in future updates.


# Installation of Python

You can download Python online for [free](https://www.python.org/downloads/). You will have to set up the files in the same folder for the program to run properly. 
If you can't install software on your machine, or prefer not to download and install Python you can use various online web pages to run the code from your browser. You will have to upload my files however into the same folder. If the webpages have multiple version of Python available select the older one. Both websites provide an online compiler which allows you to compile source code in a browswer and execute it online.

Two web pages that allow you to run Python source code are:
1. [http://www.tutorialspoint.com](http://www.tutorialspoint.com/execute_python_online.php)
2. [http://ideone.com](http://ideone.com/)
Simply copy and paste the content of each file, using the same names and press "Execute" in tutorialspoint or "Run" in ideone.


# App Development

I may soon be wrapping up development of this Python program in the coming months and be moving towards iOS app development. I will be using the same ideas and concepts found in this program, but for a palm tablet or hand-sized smart phone. Using a old terminal console is perhaps not the friendliest way to interact with software, so I hope my future app will reach many more people by being more user-friendly. I am very excided about the new project as it will provide a much higher level of interactivity with the software as well a provide much more pleasing graphics. Perhaps the Python project can be used to help me organise a database of chords and theory, while the app will use any results of the analysis and categorisations to help the musician find just the right chord and voicing for their harmonic situation.


# Credits

After having writen the beginning of this code I've found other software developers who are into music and provide useful programs online for those wanting to learn the fretboard. One guy who approached the fretboard visually, in the way that I think about music was Giancarlo from [http://www.fachords.com](http://www.fachords.com/). He doesn't use staves and doesn't have tabs at the forefront because you interact with the fretboard as you do with the instrument in real life. I would not discourage anyone from learning staves or tabs because it is a good investment if you want to be able to play other people's music, but for the beginner it can appear to be another hurdle that gets in the way of practicing your instrument. 

The purpose of Fachords seems to be the same as mine - make music and its theoretical foundations more accessible by allowing the user to interact with it. Fachords is easy and fun to use, and I hold it up as the bar by which to measure the usability of a software guitar program. 


# License

The scales and chords and related code in the files related to this project is distributed AS-IS and no responsibility implied or explicit can be addressed to the authors for its use or misuse. Any commercial use is prohibited without express permission.


# Contact

If you have any tables of music-related information that could be codified, know of interesting music or guitar related APIs, or insightful music theory to offer, please contact me. Also feel free to fork this project and make modifications or to send me feedback or advice. 

e-mail: steven.muschalik@gmail.com
Twitter: @StevenMuschalik
