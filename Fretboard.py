#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import random
from random import randint
import numbers
# Load the settings file and instrument dimension files
import Settings
# from Settings import *  # Load the Settings.txt file
from Dimensions import *  # Load the instrument Dimensions
# Load the list of Notes and dictionaries for Scales, Chords and Tunings
from Notes import *  # Load the types of Notes
from Scales import *  # Load the Scales
from Chords import *  # Load the Chords
from Tunings import *  # Load the Tunings
from Progressions import *  # Load the Tunings
from TedGreene import *  # Load Ted Greene
from Exercises import *  # Load the Exercises
from Frequency import *  # Load the Sound Frequencies
# Make all print statements in this program also go to a file
import sys

import heapq  # For sorting lists

if Settings.print_log.lower() == "yes" or Settings.print_log.lower() == "y":
    import os
    import datetime
    class Logger(object):
        def __init__(self, filename="Default.log"):
            self.terminal = sys.stdout
            self.log = open(filename, "a")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

    ## Save all print statements in this program to a file with the format: log_guitar_minor_7th_major-wed_nov_04_23_13_39_2015
    filename = 'log_' + Settings.instrument + '_' + Settings.chord_name + '_' + Settings.string_scale + '-' + str(
        time.asctime(time.localtime(time.time()))) + '.txt'
    filename = filename.replace(':', '_').replace(' ', '_').lower()
    sys.stdout = Logger(filename)


def show_tabs(root_note, notes_per_string, start_interval, num_octaves, bool_flat, bool_scale):
    # notes_per_string is the maximum number of notes that you can use on any string
    # string_order is a list of strings numbers to follow. For example [6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6] will start at the bottom string, go to the top, then down again.
    # start_interval can be any interval eg '1', 'b3', '5' etc but will typically be '1', on which the scale will start. The same applies to end_interval.
    # num_octaves will typically be 1, 2 or 3.

    try:  # See if the dict_tuning in the Settings.txt can be found
       bool_sharp_open = bool_sharp_scale(tuning_dict[Settings.dict_tuning])
    except KeyError:
       print "Error: Can't find", "'"+Settings.dict_tuning+"'", "in tuning_dict. Change tuning in settings.txt"

    fret_sym = unichr(124)

    # bool_scale = False
    if bool_scale == True:  # If you want a fretboard with scales
        # Find the Index of the chosen scale
        scale_interval = ""
        scale_steps = ""
        for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
            # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
            if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
                scale_steps = Scale["H_Steps"]
                scale_interval = Scale["L_Steps"]
                break
    else:  # If you want a fretboard with chords
        scale_interval = chord_dict[chord_short][1:]

    valid_notes = return_scale_notes(root_note, scale_interval)

    print ""
    print "Scale Name:  ", root_note, Settings.string_scale
    print "Steps:       ", scale_steps
    print "Intervals:   ", ' '.join(scale_interval)
    print "Scale Notes: ", ' '.join(valid_notes)
    print ""
    show_fretboard(tuning_dict, notes_sharp, notes_flat, valid_notes, bool_flat=True, bool_scale=True, bool_interval=False)

    # Find the lowest sounding note in the chord
    #jm_tuning_add = [0 for i in range(int(Settings.string_no))]
    #for i in range(1, int(Settings.string_no)):
    #    jm_tuning_add[i] += jm_tuning_add[i-1] + joni_mitchell_tuning(Settings.dict_tuning)[i]  # For standard tuning the result is ['E',5,5,5,5,4,5] so the addition becomes 0, 5, 10, 15, 19, 24

    seg = " " * 5
    bool_octave_leap = False
    out_of_reach = False

    legend = [seg for i in range(3)]  # First line = Note, Second line = Interval, Third line = Fret
    string_notes = ['' for i in range(int(Settings.string_no)+2)]  # Fret numbers eg 3

    for string_no, open_string in enumerate(tuning_dict[Settings.dict_tuning]):
        seg = " " * (4 - len(open_string))
        string_notes[string_no] += seg + open_string + fret_sym

    string_no = 0
    inte = start_interval - 1  # degree of the interval eg for Major scale 1 = '1', 2 = '2', etc
    last_fret = 0
    octave = 0
    while string_no < int(Settings.string_no):
        o_string_note = tuning_dict[Settings.dict_tuning][string_no]    # Open string of the instrument
        sum_valid_notes = 0                                             # Check that you don't exceed the number of notes per string

        while sum_valid_notes < notes_per_string and octave <= num_octaves:
            semitones = return_semitones(scale_interval)[inte % len(scale_interval)]
            interval = steps[semitones]                                 # eg 1 2 b3 3 b5
            step_from_note = (notes.index(root_note) + semitones)
            fret_note = notes[step_from_note % 12]                      # eg B Db D Eb F Gb G
            fret = return_semitone_distance(o_string_note, fret_note)   # Fret number to appear on the tab lines for each string
            # fret = notes.index(o_string_note) + step_from_note

            if semitones == return_semitones(scale_interval)[start_interval - 1 % len(scale_interval)]:
                octave += 1
                #print "octave", octave

            # store the first finger used on the string and the last finger.
            if sum_valid_notes == 0:
                start_fret = fret
            else:
                end_fret = fret
                # check if the reach is too far from the starting fret to the last finger on the same string
                if abs(end_fret - start_fret) > 5:
                    if abs(end_fret + 12 - start_fret) > 5:  # Check if the octave is also out of reach
                        # print "BREAK 1", o_string_note, "s", start_fret, "e", end_fret, "distance", abs(end_fret - start_fret), abs(end_fret + 12 - start_fret)
                        out_of_reach = True
                        break
                    else:  # If the octave on the same string is within reach, move the fret one octave higher.
                        # print "Add 12", o_string_note, "s", start_fret, "e", end_fret, "distance", abs(end_fret + 12 - start_fret)
                        fret = fret + 12
                        bool_octave_leap = True

            # print o_string_note, string_no, interval, semitones, fret, fret_note
            if fret >= 0:
                for fill in range(int(Settings.string_no)):  # Fill in blanks for each string
                    m = max(len(fret_note), len(str(fret)), len(str(interval)))+2   # Have a buffer of at least 2 chars for fret number / note / interval
                    if fill == string_no:
                        seg_fret = "-" * (m - len(str(fret)))            # Fret number
                        seg = " " * (m - len(fret_note))                 # Fret note
                        seg_int = " " * (m - len(str(interval)))         # Fret interval
                        seg_int_blank = " " * (m - len(str(fret)))       # Fret blank
                        string_notes[string_no] += seg_fret + str(fret)  # Fret number
                        legend[0] += seg + fret_note                     # Fret note
                        legend[1] += seg_int + interval                  # Fret interval
                        legend[2] += seg_int_blank + str(fret)           # Fret number
                    else:
                        seg = "-" * m
                        string_notes[fill] += seg

            sum_valid_notes += 1
            inte += 1
        last_fret = end_fret
        string_no += 1

    #if out_of_reach or bool_octave_leap:
    for string in reversed(string_notes):
        print string
    for leg in legend[:-1]:
        print leg
    print ""

def scale_tabs_all_keys():
    # Print out the fretboard for all root notes
    notes_on_string = 3
    octaves = 2
    start_on = 1

    print " "
    print " "
    print Settings.string_scale.title(), "Scale for 12 keys"
    print "---------------------------------------------------------"
    print "Notes per string:", notes_on_string, "  Start on interval:", start_on, "  Octaves:", octaves

    # Print the scales for each of the 12 keys
    for Scale in ListScales:
        Settings.string_scale = Scale["Scale"]
        scale_interval = Scale["L_Steps"]
        if len(scale_interval) > 6:
            #for root_note in notes_flat:
            show_tabs('C', notes_on_string, start_on, octaves, bool_flat=True, bool_scale=True)


def show_fretboard(tuning_dict, notes_sharp, notes_flat, valid_notes, bool_flat, bool_scale, bool_interval):
    # This function prints a character map of the fretboard
    # tuning_dict contains the dictionary for all the tunings
    # tuning contains the tuning for the instrument
    # valid_notes contains a list of notes that it will show
    # bool_interval is True or False and shows either notes or intervals

    # print "Tuning:", tuning_dict[tuning]
    # print "Valid notes:", valid_notes

    # if any of the open strings are sharp or flat

    try:  # See if the dict_tuning in the Settings.txt can be found
       bool_sharp_open = bool_sharp_scale(tuning_dict[Settings.dict_tuning])
    except KeyError:
       print "Error: Can't find", "'"+Settings.dict_tuning+"'", "in tuning_dict. Change tuning in settings.txt"

    fret_sym = unichr(124)
    chord_short = shorten_chord(Settings.chord_name)

    # bool_scale = False
    if bool_scale == True:  # If you want a fretboard with scales
        # Find the Index of the chosen scale
        scale_interval = ""
        scale_steps = ""
        for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
            # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
            if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
                scale_steps = Scale["H_Steps"]
                scale_interval = Scale["L_Steps"]
                break
    else:  # If you want a fretboard with chords
        scale_interval = chord_dict[chord_short][1:]

    if bool_flat:
        notes = list(notes_flat)
        valid_n = list(flat(valid_notes))  # Makes all the valid_notes flat
    else:
        notes = list(notes_sharp)
        valid_n = list(sharp(valid_notes))   # Makes all the valid_notes sharp

    #print "valid notes", valid_n, bool_flat
    #print "note", notes
    #print "notes", id(notes), "valid_n", id(valid_n), "notes_flat", id(notes_flat), "notes_sharp", id(notes_sharp)
    for open_string in reversed(range(len(tuning_dict[Settings.dict_tuning]))):
        string_notes = ""
        o_string_note = tuning_dict[Settings.dict_tuning][open_string]  # Open string of the instrument

        for fret in range(13):
            # print open_string, fret, O_string_note
            step_from_note = (notes.index(flat(o_string_note)) + fret) % 12
            fret_note = notes[step_from_note]

            if fret_note in flat(valid_notes) or fret_note in sharp(valid_notes):    # fret_note is valid as either sharp or flat
                if bool_flat:
                    #print fret_note, notes_flat.index(fret_note)
                    inte = flat(valid_notes).index(flat(fret_note))
                else:
                    #print fret_note, notes_sharp.index(fret_note)
                    inte = sharp(valid_notes).index(sharp(fret_note))

                #print fret_note, inte, scale_interval[inte]
                if bool_interval == True:     # testing to replace the fret note name with the interval name instead
                    if inte <= len(scale_interval):
                        fret_note = scale_interval[inte]
                    else:
                        print "STOP", fret_note, "inte", inte, "len", len(scale_interval), valid_notes

            if fret > 0:  # after the first fret
                seg = "-" * (4 - len(fret_note))  # repeat the "-" chacter (4 times - the length of the fret note)
                if flat(notes[step_from_note]) in flat(valid_notes) or sharp(notes[step_from_note]) in sharp(valid_notes) or fret_note in scale_interval:
                    string_notes = string_notes + seg + fret_note + fret_sym
                else:
                    string_notes = string_notes + "----" + fret_sym
            else:  # before the first fret
                if fret == 0:
                    if bool_sharp_open:  # if there any sharps in any of the the open tuning
                        if len(o_string_note) == 2:
                            string_notes = string_notes + fret_note + fret_sym
                        else:
                            string_notes = " " + string_notes + fret_note + fret_sym
                    else:
                        seg = " " * (4 - len(fret_note))
                        string_notes = seg + string_notes + fret_note + fret_sym

        print string_notes

    # print dots and/or fret numbers below the fretboard
    dots = ""
    frets = ""
    logical_frets = False  # Either prints False = fret numbers or True = dots

    frets = " " * 3
    dots = " " * 3

    for fret in range(13):
        step_from_note = (fret) % 13
        dot = notes_dots[step_from_note]

        if fret <> 0:
            dots = dots + dot
            if fret < 10:
                frets = frets + "  " + str(fret) + "  "
            else:
                frets = frets + " " + str(fret) + "  "
        else:
            dots = dots
            frets = frets + str(fret) + "  "
    if logical_frets == False:
        print dots
    else:
        print frets


def show_fretboard_training(tuning_dict, notes_sharp, notes_flat, valid_notes, bool_scale, bool_interval,
                            bool_trainer, o_string_train, fret_min, fret_max):
    # This function prints a character map of the fretboard

    # tuning_dict contains the dictionary for all the tunings
    # tuning contains the tuning for the instrument
    # valid_notes contains a list of notes that it will show
    # bool_interval is True or False and shows either notes or intervals

    # print "Tuning:", tuning_dict[tuning]
    # print "Valid notes:", valid_notes

    # if any of the open strings are sharp or flat
    bool_sharp_open = bool_sharp_scale(tuning_dict[Settings.dict_tuning])
    fret_sym = unichr(124)
    note_random = ''
    chord_short = shorten_chord(Settings.chord_name)

    # If you want to use the trainer pick a random open string (vertical) and a random fret (horizontal)
    if bool_trainer == True:
        fret_random = randint(fret_min, fret_max)  # Randomly pick a number between the min and max range

        if o_string_train in tuning_dict[Settings.dict_tuning]:  # If the chosen string is in the open tuning.
            o_string_random = o_string_train
        else:  # If no open string has been provided for training or not a valid choice
            o_string_random = random.choice(
                tuning_dict[Settings.dict_tuning])  # Randomly pick an open string from the chosen tuning

        notes = notes_flat
        step_from_note = (notes.index(o_string_random) + fret_random) % 12
        note_random = notes[step_from_note]
        print "Open String:", o_string_random, " Fret:", fret_random  # , " Min:", fret_min, " Max:", fret_max, " Random note:", note_random

    # bool_scale = False
    if bool_scale == True:  # If you want a fretboard with scales
        # Find the Index of the chosen scale
        scale_interval = ""
        scale_steps = ""
        for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
            # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
            if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
                scale_steps = Scale["H_Steps"]
                scale_interval = Scale["L_Steps"]
                break
    else:  # If you want a fretboard with chords
        scale_interval = chord_dict[chord_short][1:]

    for open_string in reversed(range(len(tuning_dict[Settings.dict_tuning]))):
        string_notes = ""
        o_string_note = tuning_dict[Settings.dict_tuning][open_string]  # Open string of the instrument

        if len(o_string_note) > 1:
            if o_string_note in notes_sharp:  # If the open string note contains a sharp
                notes = notes_sharp
            if o_string_note in notes_flat:  # If the open string note contains a flat
                notes = notes_flat
        else:
            notes = notes_flat

        if bool_trainer == True:
            bool_same_O_string = is_equivalent_notes(o_string_note, o_string_random)

        for fret in range(13):
            # print open_string, fret, O_string_note
            step_from_note = (notes.index(o_string_note) + fret) % 12
            fret_note = notes[step_from_note]

            # The fretboard trainer hides the chosen note with an X symbol that you have to guess.
            if bool_trainer == True:
                if bool_same_O_string == True and fret == fret_random:
                    fret_note = 'X'
                else:  # hide all other notes
                    fret_note = ''
            else:  # if we are not using the trainer
                if fret_note in valid_notes:
                    inte = valid_notes.index(fret_note)  # index of the fret_note relative to the root note
                    if inte >= len(valid_notes):
                        print "STOP", fret_note, "inte", inte, "len", len(valid_notes), valid_notes
                    else:
                        # print fret_note, inte, scale_interval[inte]
                        if bool_interval == True:
                            fret_note = scale_interval[
                                inte]  # testing to replace the fret note name with the interval name instead

            if fret > 0:  # after the first fret
                seg = "-" * (4 - len(fret_note))  # repeat the "-" chacter (4 times - the length of the fret note)
                if notes_sharp[step_from_note] in valid_notes or notes_flat[
                    step_from_note] in valid_notes or fret_note == 'X':
                    string_notes = string_notes + seg + fret_note + fret_sym
                else:
                    string_notes = string_notes + "-" * 4 + fret_sym
            else:  # before the first fret
                if fret == 0:
                    if bool_sharp_open:  # if there any sharps in any of the the open tuning
                        if len(o_string_note) == 2:
                            string_notes = string_notes + fret_note + fret_sym
                        else:
                            string_notes = " " + string_notes + fret_note + fret_sym
                    else:
                        seg = " " * (4 - len(fret_note))
                        string_notes = seg + string_notes + fret_note + fret_sym

        print string_notes

    # print dots and/or fret numbers below the fretboard
    dots = ""
    frets = ""
    logical_frets = False  # Either prints False = fret numbers or True = dots

    frets = " " * 3
    dots = " " * 3

    for fret in range(13):
        step_from_note = (fret) % 13
        dot = notes_dots[step_from_note]

        if fret <> 0:
            dots = dots + dot
            if fret < 10:
                frets = frets + "  " + str(fret) + "  "
            else:
                frets = frets + " " + str(fret) + "  "
        else:
            dots = dots
            frets = frets + str(fret) + "  "
    if logical_frets == False:
        print dots
    else:
        print frets

    return [note_random, o_string_random, fret_random]


def show_fretboard_score(score_board, m, n, notes_dots, position):
    # This function prints a character map of the scoreboard on the fretboard
    # The scoreboard has for each row and column a list like ['A',0,1], with the note, positive score, and negative score
    # The position variable will indicate which score or note to display. It can take three values: 0 = note, 1 = positive score, 2 = negative score

    # print dots and/or fret numbers below the fretboard
    dots = ""
    frets = ""
    logical_frets = False  # Either prints False = fret numbers or True = dots

    frets = " " * 3
    dots = " " * 3

    for fret in range(13):
        step_from_note = (fret) % 13
        dot = notes_dots[step_from_note]

        if fret <> 0:
            dots = dots + dot
            if fret < 10:
                frets = frets + "  " + str(fret) + "  "
            else:
                frets = frets + " " + str(fret) + "  "
        else:
            dots = dots
            frets = frets + str(fret) + "  "
    if logical_frets == False:
        print dots
    else:
        print frets

    string_notes = ""
    fret_note = ""
    step_from_note = 0
    fret_score = ""
    string_score = ""
    string_percent = ""

    # The last element has the score, so we leave this out by using [:-1]
    openstrings = [OpenString[0][0] for OpenString in score_board[:-1]]  # Open Letters eg ['B','E','A','D','G']
    bool_sharp_open = bool_sharp_scale(openstrings)
    fret_sym = unichr(124)  # Big round O for the fret dots

    for O_string in range(m, -1, -1):  # rows / open strings
        string_notes = ""
        for fret in range(0, n + 1):  # columns / frets
            if O_string < m and fret < n:
                fret_note = str(score_board[O_string][fret][position])  # Either note, positive or negative score
                if fret > 0:  # after the first fret
                    seg = "-" * (4 - len(fret_note))  # repeat the "-" chacter (4 times - the length of the fret note)
                    string_notes = string_notes + seg + fret_note + fret_sym
                else:  # before the first fret
                    if fret == 0:
                        if bool_sharp_open:  # if there any sharps in any of the the open tuning
                            if len(score_board[O_string][0][position]) == 2:
                                string_notes = string_notes + fret_note + fret_sym
                            else:
                                string_notes = " " + string_notes + fret_note + fret_sym
                        else:
                            seg = " " * (4 - len(fret_note))
                            string_notes = seg + string_notes + fret_note + fret_sym
            if O_string == m and fret < n:  # The score for each fret after the fretboard is displayed
                # Calculate score
                fret_score = str(score_board[O_string][fret][position])
                seg = " " * (5 - len(fret_score))
                string_score = string_score + seg + fret_score

                # Calculate percentages
                if (score_board[O_string][fret][1] + score_board[O_string][fret][2]) > 0:  # Check for divide by zero
                    fret_score = "%.0f%%" % (100 * score_board[O_string][fret][position] / (
                        score_board[O_string][fret][1] + score_board[O_string][fret][2]))
                else:
                    fret_score = ""

                seg = " " * (5 - len(fret_score))
                string_percent = string_percent + seg + fret_score

        if O_string < m:
            # Each open string with the sum of the string total. Format is: string + "Sum X:" + score
            print string_notes, " " + str(score_board[O_string][n][0]) + ":", score_board[O_string][n][position]

    print ""
    # Total Score with totals for each fret + final score out of all the questions
    print string_score[1:], " ", str(score_board[m][n][position]) + "/" + str(
        score_board[m][n][1] + score_board[m][n][2])
    # Total percentages for each fret + final score out of all the questions
    print string_percent[1:], " ", "%.2f%%" % (
        100 * score_board[m][n][position] / (score_board[m][n][1] + score_board[m][n][2]))


def is_equivalent_notes(note1, note2):
    # print note1, note2

    if (note1 == note2) and len(note1) <> 0:  # The note is exactly the same and not blank
        return True

    if len(note1) == 1 and len(note2) == 1 and note1 <> note2:  # The notes have no flats or sharp and are not equal
        return False

    if (len(note1) > 1 or len(note2) > 1) and (
                    len(note1) <> 0 and len(note2) <> 0):  # At least one of the notes has a flat or sharp
        a1 = note1.count('b')
        b1 = note1.count('#')
        a2 = note2.count('b')
        b2 = note2.count('#')

        # Find the position of the first letter eg B from Bb
        inter1 = notes_flat.index(note1[:1])
        inter2 = notes_flat.index(note2[:1])

        step1 = 0
        step2 = 0

        # note1
        if a1 > b1 and b1 == 0:  # has flats
            step1 = -a1
        if b1 > a1 and a1 == 0:  # has sharps
            step1 = b1
        # note2
        if a2 > b2 and b2 == 0:  # has flats
            step2 = -a2
        if b2 > a2 and a2 == 0:  # has sharps
            step2 = b2

        # print note1, note2, inter1+step1, inter2+step2

        if (inter1 + step1) % 12 == (inter2 + step2) % 12:
            return True
        else:
            return False

    if len(note1) == 0 or len(note2) == 0:  # If one of the notes is blank
        return False


def convert_note(notelist):
    # Converts a list of notes from flat to sharp and from sharp to flat. Eg ['A#'] = ['Bb']
    # eg ['A#', 'A', 'Bb', 'Gb', 'F#', 'C', 'h'] => ['Bb', 'A', 'A#', 'F#', 'Gb', 'C']
    notes_reverse = []

    if type(notelist) == str:
        copy_notelist = notelist.split()  # if notelist is a string convert it to a list
        return_string = True
    else:
        copy_notelist = list(notelist)
        return_string = False

    for note in copy_notelist:
        index1 = notes_sharp.index(note) if note in notes_sharp else -1
        index2 = notes_flat.index(note) if note in notes_flat else -1
        #print note, index1, index2
        if index1 >= 0:
            notes_reverse.append(notes_flat[index1])
            continue
        if index2 >= 0:
            notes_reverse.append(notes_sharp[index2])
            continue
        if index1 < 0 and index2 < 0:
            print "Convert: Note", note, "doesn't exist", copy_notelist, type(note), type(copy_notelist)
    #print notelist, notes_reverse

    if return_string == False:
        return notes_reverse
    else:
        return ' '.join(notes_reverse)


def flat(some_notelist):
    if type(some_notelist) == str:
        copy_notelist = some_notelist.split()  # if notelist is a string convert it to a list
        #print "Flat: Was a string", copy_notelist, some_notelist, type(some_notelist)
        return_string = True
    else:
        copy_notelist = list(some_notelist)
        return_string = False

    flat_notelist = [i for i, x in enumerate(copy_notelist)]  # populate flat_notelist with numbers for the size of notelist

    switch = convert_note(copy_notelist)
    # print "Flat: switch", switch
    if len(switch)==len(copy_notelist):
        for idx, note in enumerate(copy_notelist):
            # print idx, note, switch[idx]
            if len(note)==2 and note in notes_sharp :
                flat_notelist[idx] = switch[idx]
            else:
                flat_notelist[idx] = copy_notelist[idx]
    else:
        print "Flat: List", copy_notelist, "has invalid notes", switch, some_notelist

    if return_string == False:
        return flat_notelist
    else:
        return ' '.join(flat_notelist)


def sharp(some_notelist):
    if type(some_notelist) == str:
        copy_notelist = some_notelist.split()  # if notelist is a string convert it to a list
        #print "sharp: Was a string", copy_notelist, some_notelist, type(some_notelist)
        return_string = True
    else:
        copy_notelist = list(some_notelist)
        return_string = False

    sharp_notelist = [i for i, x in enumerate(copy_notelist)]  # populate sharp_notelist with numbers for the size of notelist

    switch = convert_note(copy_notelist)
    # print "Sharp: switch", switch
    if len(switch)==len(copy_notelist):
        for idx, note in enumerate(copy_notelist):
            # print idx, note, switch[idx]
            if len(note)==2 and note in notes_flat:
                sharp_notelist[idx] = switch[idx]
            else:
                sharp_notelist[idx] = copy_notelist[idx]
    else:
        print "Sharp: List", copy_notelist, "has invalid notes", switch, some_notelist

    if return_string == False:
        return sharp_notelist
    else:
        return ' '.join(sharp_notelist)


def bool_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def interval_trainer(no_questions):
    # A game to train your knowledge of the half-steps involved in the 12 intervals
    # half_steps is an integer that references the half steps in an interval
    # eg The half step 0 is interval '1'. The half step 7 is interval '5'

    print ""
    print "INTERVAL TRAINER"
    print "---------------------------------------------------------"

    interval_menu = {}
    interval_menu[0] = "All intervals (1st Octave)"
    interval_menu[1] = "All intervals (2nd Octaves)"
    interval_menu[2] = "All Natural Notes (1st Octave)"
    interval_menu[3] = "All Natural Notes (2nd Octaves)"
    interval_menu[4] = "All Accidentals (1st Octave)"
    interval_menu[5] = "All Accidentals (2nd Octaves)"
    interval_menu[6] = "Exit"

    while True:
        options = interval_menu.keys()
        print ""
        print "INTERVAL MENU"
        for entry in options:
            print str(entry) + ".", interval_menu[entry]
        print ""

        selection = raw_input("Please Select: ").strip()
        if bool_int(selection):  # if selection is an integer
            selection = int(selection)
            if int(selection) % 2 == 0:
                octave = '1st octave (1-12 semi-tones)'  # If selection is an even number
            else:
                octave = '2nd octave (12-24 semi-tones)'  # If selection is an odd number

            if selection == 0:
                interval_choice = steps_1octave
                break
            elif selection == 1:
                interval_choice = steps_2octave
                break
            elif selection == 2:
                interval_choice = steps_natural_1octave
                break
            elif selection == 3:
                interval_choice = steps_natural_2octave
                break
            elif selection == 4:
                interval_choice = steps_accidental_1octave
                break
            elif selection == 5:
                interval_choice = steps_accidental_2octave
                break
            elif selection == 6:
                exit()
        else:
            print "Unknown option", selection, "selected!"
            print ""

    print ""
    print "Your available intervals are"
    print interval_choice
    print ""

    print "Guess the semi-tone for these " + str(no_questions) + " questions for the", octave
    score = 0
    start = time.time()  # timer
    for i in range(0, no_questions):
        random_interval = random.choice(interval_choice)
        print ""
        print "Q." + str(i + 1) + " What semi-tone is interval " + str(
            random_interval) + "? " + "For eg semi-tones between " + Settings.root_note + "-" + \
              return_scale_notes(Settings.root_note, random_interval.split())[0]

        user_semitone = raw_input()
        if str(user_semitone.lower()) == str(steps_octave.index(random_interval)):
            print user_semitone.lower(), "is correct!"
            score = score + 1
        else:
            print "The correct answer is", steps_octave.index(random_interval)

    end = time.time()  # timer
    print ""
    print "SCORE"
    print "You got a score of", str(score) + "/" + str(no_questions), "- that's", "%.2f%%" % (
        100 * score / no_questions), "in", round(end - start, 2), "seconds"


def return_chord_notes(root_note, chord_name):  # root_note is a string
    # Print out the interval, note, half-step, and note for the chosen chord
    # print "Return chord"
    # print "Root note:", root_note
    notes_from_root = list()
    chord_step = list()

    for chord in range(1, len(chord_dict[chord_name])):
        interval = chord_dict[chord_name][chord]  # intervals is a list eg ['1','b3','7']
        #print "Intervals:", interval
        interval_list = list()
        interval_list.append(interval)  # single item in list so that return_semitones has a list as input

        if root_note in notes_flat:  # Check if root note has flats (b) or sharps (#)
            step_from_note = (notes_flat.index(root_note) + return_semitones(interval_list)[0]) % 12
            notes_from_root.append(notes_flat[step_from_note])
        else:
            step_from_note = (notes_sharp.index(root_note) + return_semitones(interval_list)[0]) % 12
            notes_from_root.append(notes_sharp[step_from_note])
    return notes_from_root


def return_scale_interval(scale):
    for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
        # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
        if Scale["Scale"].lower() == scale.lower():  # if the scale matches a scale in ListScales
            scale_interval = Scale["L_Steps"]
            break
    return scale_interval


def return_semitones(intervals):
    # intervals is a list eg ['1','b3','7']
    # returns the semitones for the interval eg [0, 3, 11]
    semitone = 0
    semitones = []

    for inter in intervals:
        step = 0
        b = inter.count('b')  # Count the number of flats in the interval (eg b3)
        h = inter.count('#')  # Count the number of sharps in the interval (eg #5)

        #print inter, b, h, inter[-1], inter[0]
        if b >= 1 or h >= 1:
            if b >= 1:  # flattened more than twice
                interval_temp = inter.rsplit('b', 1)[-1]  # Anything after the "b"
                if inter.count('x') > 0:                  # eg '4xb7' or '5xb7'
                    b = int(inter[0])
                step = -b
            if h >= 1:  # sharpened more than once
                interval_temp = inter.rsplit('#', 1)[-1]  # Anything after the "#"
                if inter.count('x') > 0:                  # eg '4x#7' or '5x#7'
                    h = int(inter[0])
                step = h
        else:
            interval_temp = inter

        try:
            semitone = (steps.index(interval_temp) + step) % 12
        except:
            print "Invalid interval", interval_temp

        semitones.append(semitone)
    return semitones

def return_semitone_distance(root_note, note):  # root_note is a string, note is a string
    # Returns the semi-tones between the two notes root_note and note

    if root_note in notes_flat:
        a = notes_flat.index(root_note)
    else:
        a = notes_sharp.index(root_note)
    if note in notes_flat:
        b = notes_flat.index(note)
    else:
        b = notes_sharp.index(note)
    semitone = (b - a + 12) % 12

    #print root_note, note, a, b, semitone
    #print ""
    return semitone


def return_interval(root_note, note):
    return steps[return_semitone_distance(root_note, note)]


def get_key(key):
    try:
        return int(key)
    except ValueError:
        return key


def joni_mitchell_tuning(tuning):
    # Joni Mitchell tunings notation
    # http://www.jonimitchell.com/music/notation.cfm

    # tuning is a string such as 'Guitar 6 Standard' from the tuning dictionary
    # The function returns a list with semitones between the open strings of the tuning
    # eg. ['E', 5, 5, 5, 4, 5] for the standard guitar tuning ['E', 'A', 'D', 'G', 'B', 'E']

    #print tuning, ":", tuning_dict[tuning]
    semitones = list()
    tune_to_fret = 0
    last_note = tuning_dict[tuning][0]
    semitones.append(last_note)          # add the first note to the list

    for open_string in tuning_dict[tuning][1:]:
        tune_to_fret = return_semitone_distance(last_note, open_string)
        semitones.append(tune_to_fret)   # the remaining elements will be numbers of semitones
        #print last_note, open_string, tune_to_fret
        last_note = open_string
    #print semitones
    return semitones


def show_mitchell_tunings():
    # Joni Mitchell tunings notation
    # http://www.jonimitchell.com/music/notation.cfm

    instrument_short = str(Settings.instrument + " " + Settings.string_no)
    print ""
    print "Joni Mitchell Tuning Notation For", Settings.string_no, "String", str(Settings.instrument).title()
    print ""
    print "Instead of writing out guitar tunings using the note names for each string Joni"
    print "herself uses a notation system of the bottom (lowest pitch) string followed"
    print "by the fret numbers which you play to tune the next highest open string."
    print "For example for a 6-string guitar in standard tuning she would write:"
    print "[E, A, D, G, B, E] = [E, 5, 5, 5, 4, 5]"
    print ""

    a = {}
    for tuning, val in tuning_dict.iteritems():
        if instrument_short.lower() in tuning.lower():
            short_tuning = str(tuning).replace(instrument_short, "").strip()
            jm_tuning = joni_mitchell_tuning(tuning)
            # print val, "=", jm_tuning
            # print (" ".join(val)), "=", " ".join(map(str, jm_tuning))  # Show list without quotes or square brackets
            # print short_tuning + ":", (" ".join(val)), "=", " ".join(map(str, jm_tuning))  # Show list without quotes or square brackets
            a[short_tuning + ": " + (" ".join(val))] = " ".join(map(str, jm_tuning))  # Creating a new dictionary. Format: a={('Standard': 'E 5 5 5 4 5')}

    print "Joni Mitchel Tuning Families"
    print ""
    print "Joni's system of tuning notation makes comparisons between different tunings much easier by"
    print "helping us find open string tuning 'families' which can be sorted by frets as in this list."
    print ""

    # Sort the dictionary by the frets
    # eg Ostrich:  D D D D D D = D 0 0 0 0 0 comes first, and
    # Rusty Cage:  B A D G B E = B 10 5 5 4 5 last
    for k, v in sorted(a.items(), key=lambda t: get_key(str(t[1][1:]).replace(" ", "").replace("#", "").replace("b", ""))):
        print k, "=", v

def return_scale_notes(root_note, intervals):  # root_note is a string, intervals is a list eg ['1','b3','7']
    # Print out the interval, note, half-step, and note for the chosen chord
    # print "Root note:", root_note
    # print "Intervals:", intervals
    # global notes
    notes_from_root = list()
    interval_temp = ""
    for inter in intervals:
        step_from_note = 0
        step = 0
        b = inter.count('b')  # Count the number of flats in the interval (eg b3)
        h = inter.count('#')  # Count the number of sharps in the interval (eg #5)
        if b >= 1 or h >= 1:
            if b >= 1:  # flattened more than twice
                interval_temp = inter.rsplit('b', 1)[-1]  # Anything after the "b"
                if inter.count('x') > 0:                  # eg '4xb7' or '5xb7'
                    b = int(inter[0])
                step = -b
            if h >= 1:  # sharpened more than once
                interval_temp = inter.rsplit('#', 1)[-1]  # Anything after the "#"
                if inter.count('x') > 0:                  # eg '4x#7' or '5x#7'
                    h = int(inter[0])
                step = h
        else:
            interval_temp = inter

        try:
            # find the number of the interval, then add/substract the number of sharps/flats
            step_from_note = (notes.index(root_note) + steps_octave.index(interval_temp) + step) % 12
        except:
            print "root note or interval does not exist", root_note, b, h, intervals, inter, interval_temp

        # add valid notes to notes_from_root
        notes_from_root.append(notes[step_from_note])
    return notes_from_root


def fret_distance(Fret1, Fret2, ratio, fret_length):
    # Calculates the length between the end of Fret1 to the end of Fret2.
    return fret_length * ((ratio ** Fret1) - (ratio ** Fret2)) / (1 - ratio)


def last_fret_stretch(Fret1, HandStretch, ratio, fret_length):
    # Calculates up to which fret you could reach starting at Fret1 with your index finger, up to your pinky finger
    # Returns the last fret you could reach

    LastFret = Fret1 + 1  # Fret1 = Starting fret with index finger
    NextFret = fret_distance(Fret1, LastFret, ratio, fret_length)

    while NextFret <= HandStretch[Fret1 - 1] and LastFret <= 22:
        NextFret = fret_distance(Fret1, LastFret, ratio, fret_length)
        if NextFret > HandStretch[Fret1 - 1]:
            # print Fret1, LastFret, NextFret, NextFret <= HandStretch[Fret1-1], HandStretch[Fret1-1], "Break here!"
            break
        else:
            # print Fret1, LastFret, NextFret, NextFret <= HandStretch[Fret1-1], HandStretch[Fret1-1]
            LastFret += 1

    LastFret -= 1
    return LastFret


def show_stretch_distance():
    print ""
    print "FINGER REACH"
    print "---------------------------------------------------------"
    print ""
    print "How far can your finger reach from each fret?"
    print ""
    print "The first fret will have unit of 1 for the multiplier and be"
    print "multiplied with the ratio 2^(-1/12) = ", "{0:.4}".format(SemiToneRatio), "for each following fret."
    print ""
    print "The length of your first fret is", "{0:.4}".format(
        Fret_1_Length) + "cm", "and up to fret 21 it is", "{0:.4}".format(
        fret_distance(0, 21, SemiToneRatio, Fret_1_Length)) + "cm"
    print ""
    print "fret, multiplier, fret length, sum, last reachable fret, fret span"
    LastReachable = 0
    sum = 0
    for fret in range(1, 22):  # Geometric sequence
        sum = sum + Fret_1_Length * SemiToneRatio ** (fret - 1)
        LastReachable = last_fret_stretch(fret, Reach21, SemiToneRatio, Fret_1_Length)
        print "Fret", fret, ",", "{0:.3}".format(SemiToneRatio ** (fret - 1)) + " units", ",", "{0:.3}".format(
            Fret_1_Length * SemiToneRatio ** (fret - 1)) + "cm", ",", "{0:.3}".format(
            sum) + "cm", ",", LastReachable, ",", LastReachable + 1 - fret


def mental_fretboard_trainer(no_questions):
    # Randomly select one open string from the instrument and the tuning and one random fret

    print ""
    print "MENTAL FRETBOARD TRAINER"
    print "---------------------------------------------------------"

    score = 0
    user_note = ""

    print ""
    print "Let's check your fretboard knowledge with these", no_questions, "questions"

    print ""
    for i in range(0, no_questions):
        print "Q." + str(i + 1), "What is the note on the following string and fret number?"

        rand_string = random.randint(0, int(
            Settings.string_no) - 1)  # Random number up to string number (eg 0-5 for guitar)
        rand_fret = random.randint(Settings.fret_train_min,
                                   Settings.fret_train_max)  # Random fret between the training range

        o_string_note = tuning_dict[Settings.dict_tuning][rand_string]  # Open string of the instrument
        step_from_note = (notes.index(o_string_note) + rand_fret) % 12
        fret_note = notes[step_from_note]

        print "Open String:", tuning_dict[Settings.dict_tuning][rand_string], " Fret:", rand_fret  # Open String

        user_note = raw_input()
        if user_note.title() == fret_note.title():
            print user_note.title(), "is correct!"
            print ""
            score = score + 1
        else:
            print "The correct answer is", fret_note, "=", o_string_note, "+", rand_fret, "= (", notes.index(
                o_string_note), "+", rand_fret, ") % 12 =", step_from_note
            print ""

    print ""
    print "SCORE"
    print "You got a score of", score, "out of", no_questions, "- that's", "%.2f%%" % (
        100 * score / no_questions)  # Percent score


def visual_fretboard_trainer(no_questions):
    print ""
    print ""
    instrument_details = Settings.string_no.title() + " String " + Settings.instrument.title() + " in " + Settings.tuning_short + " Tuning"
    print "VISUAL FRETBOARD TRAINER - " + instrument_details.upper()
    print "---------------------------------------------------------"

    LoadAndSave = False
    if Settings.load_and_save.title() not in ['Y', 'YES', 'N', 'NO']:
        print "Would you like to load your old score and save back to it? Press Y or N"
        while True:
            try:
                YesNo = raw_input()  # User input for Y or N
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue
            if YesNo.title() in ['Y', 'YES', 'N', 'NO']:
                if YesNo.title() in ['Y', 'YES']:
                    print("Will load data")
                    LoadAndSave = True
                    break
                if YesNo.title() in ['N', 'NO']:
                    print("Will not load or save data")
                    LoadAndSave = False
                    break
            else:
                print("Please enter Y/N")
                continue
    else:
        if Settings.load_and_save.title() in ['Y', 'YES']:
            LoadAndSave = True
        if Settings.load_and_save.title() in ['N', 'NO']:
            LoadAndSave = False

    print ""
    print "Guess These " + str(no_questions) + " Random Notes on the Fretboard"
    print ""

    # We measure the user's knowledge of the fretboard by
    # recording for each note a positive and a negative score
    # for how many times they got it right or wrong

    score = 0
    score_pos = 0
    score_neg = 0
    user_note = ''
    string_y = 0
    fret_no = 0
    m = int(Settings.string_no)  # rows / open string
    n = 13  # columns / frets
    initiate_scoreboard = False

    import pickle
    def save_object(obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    if LoadAndSave == True:
        # Open the existing score_board for the given instrument, string no and tuning
        f_scoreboard = 'score_board_' + Settings.dict_tuning + '.pkl'
        f_scoreboard = f_scoreboard.replace(':', '_').replace(' ', '_').lower()
        try:
            with open(f_scoreboard, 'rb') as input:
                score_board = pickle.load(input)
                # print "Loading score_board"
                # print "Pickle size", len(score_board)
                # print score_board
                # print ""
                pass
        except IOError as e:
            print "Unable to open score_board file"  # Does not exist OR no read permissions
            print ""
            initiate_scoreboard = True

    note_board = [[note, 0, 0] for note in notes]  # scores for each note with [Note, positive score, negative score]

    # If the loaded score_board file is empty or the file is missing, create a new score_board
    if LoadAndSave == False or initiate_scoreboard == True:
        score_board = [[0 for j in range(n + 1)] for i in range(m + 1)]  # scores for each note on the fretboard

        # Initialising of list with positive and negative scores. Each element will look like ['A',0,1].
        # The first letter is the note, the second the positive score, the last is the negative score for that note.

        for i in range(0, m + 1):  # rows / open strings
            if i < m:
                o_string_note = tuning_dict[Settings.dict_tuning][i]  # Open string of the instrument
            for j in range(0, n + 1):  # columns / frets
                if i < m and j < n:
                    step_from_note = (notes.index(o_string_note) + j) % 12
                    fret_note = notes[step_from_note]
                    score_board[i][j] = [fret_note, 0, 0]
                if i == m:  # The last row will contain the score (sum) for each fret
                    score_board[i][j] = ["Fret " + str(j), 0, 0]
                if j == n:  # The last column will contain the score (sum) for each open string
                    if i < m:
                        score_board[i][j] = ["Sum " + o_string_note, 0, 0]
                    else:
                        score_board[i][j] = ["Final Score", 0, 0]

    if len(Settings.o_string_train.strip()) == 0:
        print "Training from frets", Settings.fret_train_min, "to", Settings.fret_train_max, "for tuning", tuning_dict[
            Settings.dict_tuning]
    else:
        print "Training on", Settings.o_string_train, "Open string from fret", Settings.fret_train_min, "to", Settings.fret_train_max
    print ""

    for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
        # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
        if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
            scale_steps = Scale["H_Steps"]
            scale_interval = Scale["L_Steps"]
            break

    scale_notes = return_scale_notes(Settings.root_note, scale_interval)

    start = time.time()  # timer
    for i in range(0, no_questions):
        rand_array = show_fretboard_training(tuning_dict, notes_sharp, notes_flat, scale_notes, bool_scale=True,
                                             bool_interval=False, bool_trainer=True,
                                             o_string_train=Settings.o_string_train,
                                             fret_min=Settings.fret_train_min, fret_max=Settings.fret_train_max)

        note_random = rand_array[0]  # Random note chosen in the training module
        O_string = rand_array[1]  # Randomly chosen open string
        fret_no = rand_array[2]  # random fret chosen in the training module

        print ""
        print "Q" + str(
            i + 1) + ": What note is represented by the X on your " + Settings.string_no.title() + " string " + Settings.instrument.title() + "?"
        # print fret_no, "?", "note", note_random, "Ostring", O_string, "string_y", string_y

        # Add the correct note 12x to the list of flat notes. Then randomly select one.
        # This will give you a 50% chance of getting the note right
        pool = [note_random for i in range(0, 11)]  # Temp list to increase the chance of getting the right answer.

        # user_note = random.choice(notes_flat + pool)  # computer plays guessing game with itself
        user_note = raw_input()  # User input for visual fretboard trainer
        score += 1

        # print string_y, O_string, tuning_dict[Settings.dict_tuning][string_y]
        if is_equivalent_notes(user_note, note_random):
            print user_note.title(), "is correct!"
            print ""
            # Positive scores
            # finds all the indexes (eg 0 and 5 on a 6 string guitar) with the same O_string (eg two E's)
            y = [i for i, x in enumerate(tuning_dict[Settings.dict_tuning]) if x == O_string]
            for string_y in y:  # Will add scores to multiple strings if they exist eg to index 0 and 5 on a 6 string guitar for the two E strings
                score_board[string_y][fret_no][1] += 1 / len(
                    y)  # Add a count to the positive count in the score boardeg ['A',1,0]
                score_board[string_y][n][1] += 1 / len(y)  # Sum column for open string
            score_board[m][fret_no][1] += 1  # Sum column for fret
            score_board[m][n][1] += 1  # Final score colum
            score_pos += 1
            note_board[notes.index(note_random)][1] += 1
        else:
            print "The correct answer is", note_random
            print ""
            # Negative scores
            # finds all the indexes (eg 0 and 5 on a 6 string guitar) with the same O_string (eg two E's)
            y = [i for i, x in enumerate(tuning_dict[Settings.dict_tuning]) if x == O_string]
            for string_y in y:  # Will add scores to multiple strings if they exist eg to index 0 and 5 on a 6 string guitar for the two E strings
                score_board[string_y][fret_no][2] += 1 / len(
                    y)  # Add a count to the negative count in the score board eg ['A',0,1]
                score_board[string_y][n][2] += 1 / len(y)  # Sum column for open string
            score_board[m][fret_no][2] += 1  # Sum column for fret
            score_board[m][n][2] += 1  # Final score colum
            score_neg += 1
            note_board[notes.index(note_random)][2] += 1

    end = time.time()  # timer

    print ""
    print "SCORE"
    print "You got a score of", score_pos, "out of", score, "- that's", "%.2f%%" % (
        100 * score_pos / score), "in", round(end - start, 2), "seconds"

    print ""
    print ""
    print "Positive scores on the " + Settings.string_no.title() + " string " + Settings.instrument.lower() + " fretboard"
    print ""
    show_fretboard_score(score_board, m, n, notes_dots, 1)
    print ""
    print ""
    print "Negative scores on the " + Settings.string_no.title() + " string " + Settings.instrument.lower() + " fretboard"
    print ""
    show_fretboard_score(score_board, m, n, notes_dots, 2)
    print ""

    print ""
    print "Scores for each note:"
    print "Note, pos, neg"
    for sum_note in note_board:
        score_pos = sum_note[1]
        score_neg = sum_note[2]
        score = score_pos + score_neg
        if score > 0:  # no divide by zero error
            print sum_note, "-", "%.2f%%" % (100 * score_pos / (score_pos + score_neg))
        else:
            print sum_note

    if LoadAndSave:
        try:
            # Save the score_board to a pickle file
            save_object(score_board, f_scoreboard)
            pass
        except IOError:
            pass

            # print ""
            # Show your score for each open string, and which note/fret you got right/wrong
            # print "Scores for each open string"
            # print "[String, positive, negative]"
            # for sum_open_string in score_board:
            #    score_pos = sum_open_string[n][1]
            #    score_neg = sum_open_string[n][2]
            #    score = score_pos + score_neg
            #    if score > 0: # no divide by zero error
            #        print sum_open_string[n], "-", "%.2f%%" % (100 * score_pos/(score_pos + score_neg))
            #    else:
            #        print sum_open_string[n]

            # print ""
            # print "Scores for each fret"
            # print "[Fret, positive, negative]"
            # for sum_fret in score_board[m]:
            #    score_pos = sum_fret[1]
            #    score_neg = sum_fret[2]
            #    score = score_pos + score_neg
            #    if score > 0: # no divide by zero error
            #        print sum_fret, "-", "%.2f%%" % (100 * score_pos/(score_pos + score_neg))
            #    else:
            #        print sum_fret


# Returns true if the scale contains sharps or flats
def bool_sharp_scale(scales):
    bool = False
    for scale in scales:
        if len(scale) == 2:
            bool = True
            break
    return bool


def show_all_notes_on_fretboard():
    temp_scale = Settings.string_scale
    Settings.string_scale = 'All'
    print ""
    print "Show All Notes On The Fretboard"
    print ""
    show_fretboard(tuning_dict, notes_sharp, notes_flat, notes_sharp, bool_flat=True, bool_scale=True,
                   bool_interval=False)
    print ""
    show_fretboard(tuning_dict, notes_sharp, notes_flat, notes_flat, bool_flat=False, bool_scale=True,
                   bool_interval=False)
    print ""
    show_fretboard(tuning_dict, notes_sharp, notes_flat, notes_sharp, bool_flat=True, bool_scale=True,
                   bool_interval=True)
    print ""
    Settings.string_scale = temp_scale  # set back to original value for scale


def change_settings():
    # Check your settings
    # False = Don't show intervals on fretboard,  True = Show notes on fretboard
    bool_interval = False

    print " "
    print "Would you like a guitar or a bass?"
    while True:
        Settings.instrument = raw_input().title()
        # instrument = 'Guitar'
        if len(Settings.instrument) == 0:  # If nothing was entered, set the default to guitar"
            Settings.instrument = 'Guitar'
            break
        if Settings.instrument == 'Bass':
            break
        if Settings.instrument == 'Guitar':
            break
        else:
            print "Only guitar and bass are allowed. Your " + Settings.instrument + " is not."
    print "Selection: " + Settings.instrument
    print " "

    # print distinct list of strings the instrument can have
    print "Your string options for " + Settings.instrument + " are:"
    instrument_list = []

    for tuning_i, notes in tuning_dict.iteritems():
        # print "RE", re.findall('\d+', tuning)[0], tuning
        strings_inst = re.findall('\d+', tuning_i)[0]  # creates a list of all the strings that an instrument can have
        if Settings.instrument.lower() in tuning_i.lower():
            if (strings_inst + " String " + Settings.instrument) not in instrument_list:
                instrument_list.append(strings_inst + " String " + Settings.instrument)
    print instrument_list
    print " "

    # find the number of strings the instrument has
    print "How many strings does your " + Settings.instrument.lower() + " have?"
    valid_strings = False
    while not valid_strings:
        Settings.string_no = raw_input().strip()
        # print "STRING NO", string_no
        if bool_int(Settings.string_no):
            if len(Settings.string_no) == 0:
                if Settings.instrument == 'Bass':  # If a bass is selected set default to 4 strings"
                    Settings.string_no = '4'
                    valid_strings = True
                if Settings.instrument == 'Guitar':  # If a guitar is selected set default to 6 strings"
                    Settings.string_no = '6'
                    valid_strings = True
            if int(Settings.string_no) > 0 and int(Settings.string_no) < 8:
                if Settings.instrument == 'Bass' and (
                                int(Settings.string_no) > 3 and int(
                            Settings.string_no) < 7):  # If a bass is selected set default to 4 strings"
                    valid_strings = True
                if Settings.instrument == 'Guitar' and (int(Settings.string_no) >= 5 and int(Settings.string_no) < 8):
                    valid_strings = True
            else:
                print "Not a valid number for " + Settings.instrument.lower()
    print "Selection:", Settings.string_no
    print " "

    # Show possible tuning for the instrument and string number
    print "What tuning does your " + Settings.string_no + " string " + Settings.instrument.lower() + " have?"
    if len(Settings.tuning_short) == 0:
        for tuning_i, notes in tuning_dict.iteritems():
            if str(Settings.instrument.lower() + " " + Settings.string_no) in tuning_i.lower():
                # possible_tuning =  tuning_i.replace(instrument, "").replace(string_no, "")
                possible_tuning = tuning_i.replace(Settings.instrument + " " + Settings.string_no, "")
                print possible_tuning
        print "Please select your tuning from the above list for your " + Settings.string_no + " string "

    # Exit out of this loop if someone enters a bad selection 5 times
    count = 0
    while count <= 5:
        Settings.tuning_short = raw_input().title()
        # tuning = 'Standard'
        # If no tuning is selected set defaults
        # print "TUNING", tuning, "STRING NO", string_no, "INSTRUMENT", instrument
        if len(Settings.tuning_short) == 0:
            if Settings.instrument == 'Guitar':
                Settings.tuning_short = 'Standard'
                print "AAA 1"
            if Settings.instrument == 'Bass':
                if Settings.string_no == '4':
                    print "AAA 2"
                    Settings.tuning_short = 'Standard'
                if Settings.string_no == '5':
                    print "AAA 3"
                    Settings.tuning_short = 'Standard B'
                if Settings.string_no == '6':
                    print "AAA 4"
                    Settings.tuning_short = 'Standard'
            your_tuning = str(Settings.instrument + " " + Settings.string_no + " " + Settings.tuning_short).title()
            count = count + 1
            break
        else:
            your_tuning = str(Settings.instrument + " " + Settings.string_no + " " + Settings.tuning_short).title()
            # print "dict", tuning_dict[your_tuning]
            # print "Strip:", your_tuning.title().strip()
            if your_tuning.title() in tuning_dict.keys():
                your_tuning = str(Settings.instrument + " " + Settings.string_no + " " + Settings.tuning_short).title()
                # print "FOUND", your_tuning, "in tuning_dict"
                break
            else:
                print "Not valid tuning"
                count = count + 1
                break
    print "Selection:", Settings.tuning_short
    print " "
    print "Tuning Instrument:", your_tuning.title()

    # randomly chose either flats or sharp to display on fretboard
    if randint(0, 1) == 0:  # random number 0 or 1
        notes = notes_flat
    else:
        notes = notes_sharp

    Settings.tuning_short = your_tuning

    # print a character map of the fretboard for the instrument with the selected tuning
    print "Tuning:", tuning_dict[Settings.dict_tuning]
    print " "

    # print "Intervals and their half-steps"
    # for chord in steps:
    #    print chord, steps.index(chord)
    # print "---------------------------------------------------------"

    print " "

    # Continue while loop till a vaild note is chosen
    while True:
        print "Enter root note: (eg " + random.choice(notes_flat) + ")"
        # root_note = raw_input().title()   #eg C
        print "Selection:", Settings.root_note
        if len(Settings.root_note) == 0:  # If nothing was entered, set the default to "A"
            Settings.root_note = "A"
            break
        if Settings.root_note in notes_flat:  # If the note contains a flat
            notes = notes_flat
            break
        if Settings.root_note in notes_sharp:  # If the note contains a sharp
            notes = notes_sharp
            break
        else:
            print Settings.root_note, " is an invalid note"

    print " "
    print "---------------------------------------------------------"

    # Show list of possible chords to chose from
    chord_str = ''
    print "Chose your chord from the following list:"
    for chord, chord_short in sorted(chord_dict.items()):
        chord_str = chord_str + chord_short[0] + ', '
    print chord_str[:-2]  # remove the last comma
    print "---------------------------------------------------------"

    # Enter your chosen chord
    valid_chord = False
    # chord_name = ""
    chord_chosen_short = shorten_chord(Settings.chord_name)
    while not (valid_chord):  # Continue the while loop till a valid chord is chosen
        print "Enter chord type: (eg " + random.choice(chord_dict.keys()) + ")"
        # chord_name = raw_input().strip().lower()
        # chord_name = '7#9#5'
        # print len(chord_name), chord_name
        if len(chord_short) == 0:  # If nothing was entered, set the default to "major"
            chord_short = "major"
            valid_chord = True
            break
        if chord_short in chord_dict.keys():  # Find the chord name in the key to the chord dictionary
            valid_chord = True
            break
        else:
            for chord, chord_short in chord_dict.iteritems():
                if chord_chosen_short == chord_short[0] or chord_chosen_short == chord_dict[chord][0]:
                    # print "Chord:", chord_name, chord
                    chord_chosen_short = chord
                    valid_chord = True
                    break
            if valid_chord == True:
                break
            else:
                valid_chord = False
                print Settings.chord_name, " is an invalid chord"
    print "Chord:", chord_chosen_short
    print "---------------------------------------------------------"

    # Print out the interval, note, half-step, and note for the chosen chord
    print "Root note:", Settings.root_note
    print "Chord Dictionary: ", Settings.chord_name, ":", chord_dict[chord_chosen_short]
    print "Interval, steps, note"
    chord_notes = list()
    for chord in range(1, len(chord_dict[chord_chosen_short])):
        interval = chord_dict[chord_chosen_short][chord]
        interval_temp = interval
        step = 0
        step_from_note = 0
        # print "chord", chord, "interval", interval, "steps", steps.index(interval)+step
        b = interval.count('b')  # Count the number of flats in the interval (eg b3)
        h = interval.count('#')  # Count the number of sharps in the interval (eg #5)
        if b > 1 or h >= 1:
            if b > 1:  # flattened more than twice
                step = -b
                interval_temp = interval.replace("b", "")
            if h >= 1:  # sharpened more than once
                step = h
                interval_temp = interval.replace("#", "")

        # find the number of the interval, then add/substract the number of sharps/flats
        step_from_note = (notes.index(Settings.root_note) + steps.index(interval_temp) + step) % 12

        # add valid notes to chord_notes
        chord_notes.append(notes[step_from_note])
        print interval, steps.index(interval_temp) + step, notes[step_from_note]
    print "---------------------------------------------------------"

    # print "Chord notes: ", chord_notes
    # print "---------------------------------------------------------"

    print "Valid notes:", chord_notes
    print " "

    show_fretboard(tuning_dict, notes_sharp, notes_flat, chord_notes, bool_flat=True, bool_scale=False,
                   bool_interval=False)
    print " "
    show_fretboard(tuning_dict, notes_sharp, notes_flat, chord_notes, bool_flat=True, bool_scale=False,
                   bool_interval=True)
    print " "


def chord_all_keys():
    # Print out the fretboard for all root notes
    print " "
    print " "
    print Settings.chord_name.title(), "Chord for 12 keys"
    print "---------------------------------------------------------"
    print " "
    chord_short = shorten_chord(Settings.chord_name)
    for Settings.root_note in notes_flat:
        chord_notes = return_chord_notes(Settings.root_note, chord_short)  # Search for chord in chord dictionary
        print "Chord Name: ", Settings.root_note, Settings.chord_name.title()
        print "Intervals:  ", ', '.join(
            chord_dict[chord_short][1:])  # chord_dict[chord_short][1:]  # chord_dict[chord_name][chord]
        print "Chord Notes:", ', '.join(chord_notes)

        print " "
        show_fretboard(tuning_dict, notes_sharp, notes_flat, chord_notes, bool_flat=True, bool_scale=False,
                       bool_interval=False)
        print " "
        show_fretboard(tuning_dict, notes_sharp, notes_flat, chord_notes, bool_flat=True, bool_scale=False,
                       bool_interval=True)
        print " "

    print "---------------------------------------------------------"

def valid_scale(check_scale):
    # Returns True if check_scale is found in ListScales, otherwise returns False
    valid = False
    for Scale_i in ListScales:  # check through list of scales
        if check_scale in Scale_i["Scale"]:  # pattern match string with list
            if check_scale.lower() == Scale_i["Scale"].lower():
                valid = True
                break
    return valid

def scale_all_keys():
    # Show list of possible scales
    print "What scale from the following list do you want to use?"

    if len(Settings.string_scale) > 0:  # If the scale has already been selected
        print "Selection:", Settings.string_scale
    else:  # If the scale has not yet been selected
        for Scale_i in ListScales:
            if Scale_i["Scale"] in ShortList_Scale:  # Using a short list of scales
                Settings.string_scale = Settings.string_scale + Scale_i["Scale"] + ", "

        print Settings.string_scale[:-2]

        # Keep asking for a scale till a valid one is chosen
        valid_scale = False
        pos_scale = []  # possible scale list of names that fit the string_scale
        while not valid_scale:
            Settings.string_scale = raw_input().title()  # Wait for input from the user
            # string_scale = "Byzantine"
            if len(
                    Settings.string_scale) == 0 or Settings.string_scale == "":  # If nothing was entered, set the default to Major"
                Settings.string_scale = 'Major'
                break
            else:
                for Scale_i in ListScales:  # check through list of scales
                    if Settings.string_scale in Scale_i["Scale"]:  # pattern match string with list
                        pos_scale.append(Scale_i["Scale"])  # save to new possible list if the string is in any scale
                        if Settings.string_scale == Scale_i["Scale"] or Settings.string_scale.lower() == Scale_i[
                            "Scale"]:
                            # print "Valid scale", string_scale, "in ", Scale["Scale"]
                            valid_scale = True
                            break
                if valid_scale:
                    # print "check len", string_scale
                    break
                else:
                    print Settings.string_scale + " is an invalid scale"
                    for possible in pos_scale:
                        print "Try: " + possible
                    del pos_scale[:]  # delete the possible list after completion
                    print " "

    print " "
    print " "
    print Settings.string_scale.title(), "Scale in 12 keys"
    print "---------------------------------------------------------"
    print " "

    # Find the Index of the chosen scale
    scale_interval = ""
    scale_steps = ""
    for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
        # print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
        if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
            scale_steps = Scale["H_Steps"]
            scale_interval = Scale["L_Steps"]  # eg ['1', '3', '5', '7']
            break

    # Print the scales for each of the 12 keys
    for Settings.root_note in notes_flat:
        scale_notes = return_scale_notes(Settings.root_note, scale_interval)

        print "Scale Name: ", Settings.root_note, Settings.string_scale  # eg E Major
        print "Steps:      ", ''.join(scale_steps)
        print "Intervals:  ", ', '.join(scale_interval)
        print "Scale Notes:", ', '.join(scale_notes)
        print " "

        show_fretboard(tuning_dict, notes_sharp, notes_flat, scale_notes, bool_flat=True, bool_scale=True,
                       bool_interval=False)
        print " "
        show_fretboard(tuning_dict, notes_sharp, notes_flat, scale_notes, bool_flat=True, bool_scale=True,
                       bool_interval=True)
        print " "

    print "---------------------------------------------------------"


def change_to_finger(intervals, frets):
    # Returns a list with the fingers used (with the input of the interval and fret position)
    # finger is the finger number (1-4) that you want to add to the list
    # intervals is a list like ['1', '5', '1', '3', '5', '1']
    # frets is a list of the fret positions of the Intervals like [2, 4, 4, 3, 2, 2]

    fingers = ['' for i in range(0, len(frets))]
    l = sorted(frets)
    # s1 = l[-4]  # 1st smallest
    # s2 = l[-3]  # 2nd smallest
    # s3 = l[-2]  # 3rd smallest
    # s4 = l[-1]  # 4th smallest

    from heapq import nsmallest
    l = list(set(l))
    lsort = nsmallest(7, l)
    # print lsort, len(lsort)

    s1 = s2 = s3 = s4 = 0

    if len(lsort) >= 1:
        s1 = lsort[0]  # 1st smallest
    if len(lsort) >= 2:
        s2 = lsort[1]  # 2nd smallest
    if len(lsort) >= 3:
        s3 = lsort[2]  # 3rd smallest
    if len(lsort) >= 4:
        s4 = lsort[3]  # 4th smallest

    # print intervals, len(intervals), frets
    # print l, s1, s2, s3, s4

    # Next finger on next fret
    # The natural finger placement for a given hand position is to place the index finger on the first fret
    # in the position, the long finger on the second fret, the ring finger on the third fret, and the little
    # finger on the fourth fret.

    for i in range(len(frets)):
        # print i, frets[i]
        if frets[i] == s1:  # if the number is the 1st smallest
            fingers[i] = 1
        if frets[i] == s2:
            fingers[i] = 2
        if frets[i] == s3:
            fingers[i] = 3
        if frets[i] == s4:
            fingers[i] = 4

    return fingers


def chord_sequence(chord_sequence):
    # chord_sequence is a string of chords separated by a space eg. "Bm Gb A E G D Em F#"  or  "E EmF FmF#GbG GmG#AbA AmA#BbB BmC CmC#DbD DmD#Eb"
    # Modified this code from here: http://codegolf.stackexchange.com/questions/2975/generating-guitar-tabs/3906#3906

    instrument_details = Settings.string_no.title() + " String " + Settings.instrument.title() + " in " + Settings.tuning_short + " Tuning"
    print ""
    print "CHORD SEQUENCE - " + instrument_details.upper()
    print "---------------------------------------------------------"
    print ""

    chord_string = ' ' * 2
    string_spacing = 4

    if len(chord_sequence) < 1:
        # Chords for Hotel California by Eagles
        # i - V - bVII - IV - bVI - bIII - iv
        default_sequence = 'Bm F# A E G D Em F#'

        print "Please enter the chords you would like tabs for eg. 'Bm F# A E G D Em' for Hotel California"
        chord_sequence = raw_input().strip()
        if len(chord_sequence) < 1:
            chord_sequence = default_sequence

    for chord in chord_sequence.split():
        chord_string = chord_string + chord + " " * (string_spacing - len(chord) + 1)

    print chord_string

    s = [("E EmF FmF#GbG GmG#AbA AmA#BbB BmC CmC#DbD DmD#Eb".find("%-02s" % s[:2]) / 4, s[-1] != 'm') for s in
         chord_sequence.split()]
    compact_o_strings = "".join(tuning_dict[Settings.dict_tuning])  # eg for Guitar: "EADGBE"

    for t in range(len(tuning_dict[Settings.dict_tuning])):
        l = compact_o_strings[t] + ' '
        for (i, M) in s:
            assert isinstance(M, object)
            x = i > 4;
            l += `i - 5 * x + 2 * (2 < t + x < 5) + (M + x) * (t == 2 - x)` + "-" * string_spacing
        print l
    print ""


def shorten_chord(long_chord_name):
    short_chord_name = Settings.chord_name.lower().replace('major', '').replace('minor', 'm')
    short_chord_name = short_chord_name.replace('th', '').replace('nd', '')
    short_chord_name = short_chord_name.replace('flat', 'b').replace('sharp', '#')
    short_chord_name = short_chord_name.replace('augmented ', 'aug')
    short_chord_name = short_chord_name.replace('diminished ', 'dim')
    short_chord_name = short_chord_name.replace('suspended ', 'sus')
    short_chord_name = short_chord_name.replace('added', 'add')
    short_chord_name = short_chord_name.replace('five', '5')
    short_chord_name = short_chord_name.replace('six', '6')
    short_chord_name = short_chord_name.replace('seven', '7')
    short_chord_name = short_chord_name.replace('nine', '9')
    short_chord_name = short_chord_name.replace('eleven', '11')
    short_chord_name = short_chord_name.replace('thirteen', '13')
    short_chord_name = short_chord_name.replace(" ", "")
    return short_chord_name


def chord_chart_all_keys():
    # Print chord diagram for all root notes where fingerings exist
    short_chord = shorten_chord(Settings.chord_name)
    print " "
    print Settings.chord_name.title(), "Chord for 12 keys"
    print "---------------------------------------------------------"
    print " "
    for root_note in notes_flat:
        chord_chart(root_note, short_chord, fret_position="")
        print " "


def chord_chart(tonic, chord_type, fret_position):
    # Draws a Chord Diagram between Settings.start_chord_fret and Settings.end_chord_fret (See Settings.py and settings.txt)
    # For eg A major:  tonic = 'A', chord_type = '', fret_position = '0-0-2-2-2-0'
    import csv
    #global test_file
    test_file = 'Chord Finger Positions.csv'
    #global csv_file
    csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',')
    l_chord_found = False

    strings = int(Settings.string_no)
    chord_frets = [0 for OpenString in range(strings)]
    chord_fingers = [0 for OpenString in range(strings)]
    chord_sorted_interval = ""
    # chord_short = chord_type
    fret_sym = ":"  # unichr(124)

    first_fret = 0  # First fret where the chord begins
    last_fret = 0  # Last fret where the chord ends
    min_fret = 0
    max_fret = 0

    string_spacing = 3  # spacing between two strings eg E - A string
    chart_spacing = 4  # spacing between two charts (eg between the note chart and the interval chart)

    fret_bar = (("-" * string_spacing) * strings)[:-string_spacing + 1]  # Starts with the first fret
    fret_o_bar = (("=" * string_spacing) * strings)[:-string_spacing + 1]  # For the open strings
    interval_bar = ""
    fret_finger = ""
    fret_string_finger = ""
    tuning_bar = ""

    margin_string = " " * string_spacing
    margin_left = " " * (string_spacing - 2)
    margin_chart = " " * chart_spacing

    chord_name = ""
    fret_pos = ""
    finger_pos = ""
    header_finger = ['Fg-E','Fg-A','Fg-D','Fg-G','Fg-B','Fg-e']
    header_fret = ['Ft-E','Ft-A','Ft-D','Ft-G','Ft-B','Ft-e']

    # If fret_position is provided = True, otherwise = False. If true search for that chord.
    if fret_position.strip() == "":
        bool_fret_pos = False
    else:
        bool_fret_pos = True

    # Read in the csv file with the chords and fill in the variables
    # print Settings.instrument.lower(), Settings.root_note + " " +  Settings.chord_name
    print ""
    if Settings.instrument.lower() == "guitar" and strings == 6:
        for line in csv_file:
            chord_name = line['Chord Name']
            if chord_name == tonic + chord_type:
                for i in range(6):
                    chord_frets[i] = line[str(header_fret[i])]      # Frets for each chord
                    chord_fingers[i] = line[str(header_finger[i])]  # Finger's 1-4 for each chord

                fret_num = [int(num) for num in chord_frets if num != 'x']                   # List of all the fret numbers without the 'x'
                finger_num = [int(num) for num in chord_fingers if num != 'x' and num >= 0]  # List of all the finger numbers larger than 0

                min_fret = min(fret_num)
                max_fret = max(fret_num)

                fret_pos = line['Fret Positions']
                finger_pos = line['Finger Positions']
                chord_sorted_interval = line['Sorted Intervals']

                l_chord_found = False
                if max(finger_num) > 0:
                    if bool_fret_pos:   # If fret_position exists, search for the chord with the given fret position
                        if fret_pos == fret_position:
                            l_chord_found = True
                            break
                    else:
                        if Settings.start_chord_fret <= min_fret and Settings.end_chord_fret >= max_fret >= Settings.start_chord_fret and min_fret <= Settings.end_chord_fret:
                            print tonic+chord_type+":", chord_name, " ", fret_pos, " ", finger_pos, " ", chord_sorted_interval, "within range", min_fret, max_fret, ", ", Settings.start_chord_fret, "-", Settings.end_chord_fret
                            l_chord_found = True
                            break
                        #else:
                        #    print chord_name, fret_pos, " ", finger_pos, "out of range", min_fret, max_fret, ", ", Settings.start_chord_fret, "-", Settings.end_chord_fret
                else:
                    print chord_name, " ", fret_pos, " ", finger_pos, "No fingering", "Searched for chord:", tonic + chord_type
    else:
        print "Please be aware that we only have fingerings for 6-string guitars in standard tuning"

    try: # Search for chord in chord dictionary
        chord_notes = return_chord_notes(tonic, chord_type)
        intervals = chord_dict[chord_type][1:]  # Leave out the first element of the list eg ['maj7', '1', '3', '5', '7']
    except: # If cannot be found, use the details in the csv file.
        print "Chord", tonic + chord_type, "chord not found in Chords.py dictionary. Checking csv file."
        chord_notes = line['Notes'].split()  # Make into alist
        intervals = chord_sorted_interval.split()

    print "Chord Name: ", tonic + chord_type
    print "Compact form:", fret_pos, finger_pos
    print "Intervals:  ", ', '.join(intervals), "/", chord_sorted_interval  # chord_sorted_interval is from csv file
    print "Chord Notes:", ', '.join(chord_notes)

    # Check if there are no duplicate notes in the chord and if it is 4-note chord
    if duplicate_note(line['Notes']) == False and len(chord_notes) == 4:
        print "V-System: Fits into Ted Greene's 4-note chord system"

    if not (l_chord_found):
        print "Fingering for", tonic + chord_type, "chord not found"
    print ""

    bool_intervals = True  # Show the intervals in the chord chart
    finalnotes = ''
    finalinterval = ''
    finalfinger = ''
    finalchordinterval = ''
    lfinalnotes = ['' for OpenString in range(strings)]      # store the last valid note for each open string
    lfinalinterval = ['' for OpenString in range(strings)]   # store the last valid interval for each open string
    interval_fingers = [0 for OpenString in range(strings)]  # store the intervals for the strings used in the chord

    # Print open string line
    for open_string in tuning_dict[Settings.dict_tuning]:
        step_from_note = (notes.index(open_string)) % 12
        fret_note = notes[step_from_note]
        tuning_bar = tuning_bar + fret_note + " " * (string_spacing - len(fret_note))

    print margin_left + " " * 6 + "Notes" + " " * (
    len(tuning_bar) - len("Notes")) + margin_chart + "Intervals" + " " * (
    len(tuning_bar) - len("Intervals")) + margin_chart + "Finger Pos" + \
          ' ' * (len(tuning_bar) - len("Finger Positions"))
    print ""
    print margin_left + " " * 6 + tuning_bar + margin_chart + tuning_bar + margin_chart + tuning_bar

    # Print within reasonable, viewable range
    if Settings.end_chord_fret+1 - Settings.start_chord_fret > 6:
        if min_fret> 3:
            first_fret = min_fret  # First fret where the chord begins
        else:
            first_fret = 0  # First fret where the chord begins
        last_fret =  max(max_fret+1,min_fret+5)  # Last fret where the chord ends
    else:
            first_fret = Settings.start_chord_fret   # First fret where the chord begins
            last_fret = Settings.end_chord_fret+1    # Last fret where the chord ends

    # Print fretboard
    for fret in range(first_fret, last_fret):
        fret_string = ""
        interval_bar = ""
        fret_finger = ""
        fret_string_finger = ""
        i = 0  # goes through each string
        for open_string in tuning_dict[Settings.dict_tuning]:
            step_from_note = (notes.index(open_string) + fret) % 12
            fret_note = notes[step_from_note]
            fret_finger = ""

            if fret == 0 and str(chord_frets[i]).lower() == 'x':
                interval = 'x'
                lfinalinterval[i] = 'x'
                interval_fingers[i] = 'x'
                fret_finger = 'x'

            # Show the notes on the string if the fret has a number
            try:
                n = int(chord_frets[i])
                if fret == int(chord_frets[i]):
                    show_specific_chord = True
                else:
                    show_specific_chord = False
            except:
                show_specific_chord = False

            if fret_note in chord_notes and show_specific_chord:  # The note is in the chord
                interval = intervals[chord_notes.index(fret_note)]
                lfinalinterval[i] = interval   # Interval for Interval diagram
                lfinalnotes[i] = fret_note     # Note for diagram

                fret_string = fret_string + fret_note + " " * (string_spacing - len(fret_note))
                interval_bar = interval_bar + interval + " " * (string_spacing - len(interval))

                fret_finger = "+"  # default

                # If the fret is the same as in the chord, assign the finger to the column in the csv file
                if l_chord_found:
                    if str(chord_frets[i]).lower() != 'x':
                        if fret == int(chord_frets[i]):
                            # print "checking", fret, chord_frets[i], i
                            interval_fingers[i] = interval  # Interval for Finger diagram
                            if interval_fingers[i] == 0:
                                interval_fingers[i] = 'x'
                            # print open_string, fret, chord_frets[i], chord_fingers[i]
                            if fret > 0:
                                fret_finger = str(chord_fingers[i])
                            else:
                                fret_finger = 'O'  # Open string
                    else:  # str(chord_frets[i]).lower() == 'x'
                        if str(chord_frets[i]).lower() == 'x':
                            if fret == 0:
                                # interval = 'x'
                                # lfinalinterval[i] = interval  # Still draw the interval in the Interval Diagram
                                interval_fingers[i] = 'x'
                                fret_finger = 'x'
                            else:
                                # fret_finger = 'x'        # leave out this variable to leave the (+) symbol in the diagram
                                interval_fingers[i] = 'x'  # only change the bottom finalchordinterval line
                fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
            else:
                if fret_note in chord_notes and str(chord_frets[i]).lower() == 'x':
                    lfinalnotes[i] = 'x'         # Last row under Interval diagram
                    lfinalinterval[i] = 'x'      # Last row under Note diagram
                    interval_fingers[i] = 'x'    # Last row under Finger diagram
                    if fret == 0:
                        fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
                    else:
                        fret_finger = "+"
                        interval = '+'

                        fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
                        fret_string = fret_string + fret_finger + " " * (string_spacing - len(fret_finger))
                        interval_bar = interval_bar + interval + " " * (string_spacing - len(interval))
                else:
                    # If the note isn't in the chord and it isn't an 'x' print the fret symbol
                    if fret == 0 and str(chord_frets[i]).lower() == 'x':
                        lfinalnotes[i] = 'x'
                        lfinalinterval[i] = 'x'
                        interval_fingers[i] = 'x'  # Last row under Finger diagram
                        # No fret_sym here, as we use an fret_finger='x' if this letter is not part of the chord
                        fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
                    else:
                        # Put a fret symbol if the note is not in the chord
                        fret_string_finger = fret_string_finger + fret_sym + " " * (string_spacing - len(fret_sym))
                    fret_string = fret_string + fret_sym + " " * (string_spacing - len(fret_sym))
                    interval_bar = interval_bar + fret_sym + " " * (string_spacing - len(fret_sym))
            i += 1

        # Indicate the beginning fret on the chart diagram
        if fret == first_fret:   #Settings.start_chord_fret:
            fret_num = str(first_fret) + "fr." + " " * (6 - len(str(fret)) - 3)  # Will always contain 6 characters
        else:
            fret_num = " " * 6  # Will always contain 6 characters

        # After each fret check if we have a full chord
        if set(lfinalinterval) <= set(intervals) and set(intervals) <= set(lfinalinterval):
            print margin_left + fret_num + fret_string + margin_chart + interval_bar + margin_chart + fret_string_finger  # , lfinalinterval, fret_f, f1, "Full Chord"  # line for notes and intervals
        else:
            print margin_left + fret_num + fret_string + margin_chart + interval_bar + margin_chart + fret_string_finger  # , lfinalinterval, fret_f, f1  # line for notes and intervals

        # Print the fret bar
        if fret > 0:  # Just the fret bar without notes or intervals
            print margin_left + " " * 6 + fret_bar + margin_chart + " " * (string_spacing - 1) + fret_bar + " " * (
                string_spacing - 1) + margin_chart + fret_bar
        elif fret == first_fret:
            if fret == 0:  # indicate the open position of the first fret
                print margin_left + " " * 6 + fret_o_bar + margin_chart + " " * (
                    string_spacing - 1) + fret_o_bar + " " * (string_spacing - 1) + margin_chart + fret_o_bar
            else:  # indicate the position of the first fret
                print margin_left + " " * 6 + fret_bar + margin_chart + " " * (string_spacing + 1) + fret_bar + " " * (
                    string_spacing + 1) + margin_chart + fret_bar
        else:  # double line eg === for the open string at the nut
            print margin_left + " " * 6 + fret_o_bar + margin_chart + " " * (string_spacing + 1) + fret_o_bar + " " * (
                string_spacing + 1) + margin_chart + fret_o_bar

    # Print the last line with the last notes in the fret range start_chord_fret - end_chord_fret
    for i in range(len(tuning_dict[Settings.dict_tuning])):
        finalnotes = finalnotes + lfinalnotes[i] + " " * (string_spacing - len(lfinalnotes[i]))              # Last line for Notes Diagram
        finalinterval = finalinterval + lfinalinterval[i] + " " * (string_spacing - len(lfinalinterval[i]))  # Last line for Interval Diagram
        finalchordinterval = finalchordinterval + str(interval_fingers[i]) + " " * (
            string_spacing - len(str(interval_fingers[i])))                                                  # Last line for Finger Pos Diagram
    print ""
    print margin_left + " " * 6 + finalnotes + margin_chart + finalinterval + margin_chart + finalchordinterval
    print ""


def chord_chart2(tonic, chord_type, fret_position):
    # Draws a Chord Diagram between Settings.start_chord_fret and Settings.end_chord_fret (See Settings.py and settings.txt)
    # For eg A major:  tonic = 'A', chord_type = '', fret_position = '0-0-2-2-2-0'
    import csv
    #global test_file
    test_file = 'Chord Finger Positions.csv'
    #global csv_file
    csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',')
    l_chord_found = False

    strings = int(Settings.string_no)
    chord_frets = [0 for OpenString in range(strings)]
    chord_fingers = [0 for OpenString in range(strings)]
    chord_sorted_interval = ""
    # chord_short = chord_type
    fret_sym = ":"  # unichr(124)

    first_fret = 0  # First fret where the chord begins
    last_fret = 0  # Last fret where the chord ends
    min_fret = 0
    max_fret = 0

    string_spacing = 3  # spacing between two strings eg E - A string
    chart_spacing = 4  # spacing between two charts (eg between the note chart and the interval chart)

    fret_bar = (("-" * string_spacing) * strings)[:-string_spacing + 1]  # Starts with the first fret
    fret_o_bar = (("=" * string_spacing) * strings)[:-string_spacing + 1]  # For the open strings
    interval_bar = ""
    fret_finger = ""
    fret_string_finger = ""
    tuning_bar = ""

    margin_string = " " * string_spacing
    margin_left = " " * (string_spacing - 2)
    margin_chart = " " * chart_spacing

    chord_name = ""
    fret_pos = ""
    finger_pos = ""
    header_finger = ['Fg-E','Fg-A','Fg-D','Fg-G','Fg-B','Fg-e']
    header_fret = ['Ft-E','Ft-A','Ft-D','Ft-G','Ft-B','Ft-e']

    # If fret_position is provided = True, otherwise = False. If true search for that chord.
    if fret_position.strip() == "":
        bool_fret_pos = False
    else:
        bool_fret_pos = True

    # Read in the csv file with the chords and fill in the variables
    # print Settings.instrument.lower(), Settings.root_note + " " +  Settings.chord_name
    print ""
    if Settings.instrument.lower() == "guitar" and strings == 6:
        for line in csv_file:
            chord_name = line['Chord Name']
            if chord_name == tonic + chord_type:
                for i in range(6):
                    chord_frets[i] = line[str(header_fret[i])]      # Frets for each chord
                    chord_fingers[i] = line[str(header_finger[i])]  # Finger's 1-4 for each chord

                fret_num = [int(num) for num in chord_frets if num != 'x']                   # List of all the fret numbers without the 'x'
                finger_num = [int(num) for num in chord_fingers if num != 'x' and num >= 0]  # List of all the finger numbers larger than 0

                min_fret = min(fret_num)
                max_fret = max(fret_num)

                fret_pos = line['Fret Positions']
                finger_pos = line['Finger Positions']
                chord_sorted_interval = line['Sorted Intervals']

                l_chord_found = False
                if max(finger_num) > 0:
                    if bool_fret_pos:   # If fret_position exists, search for the chord with the given fret position
                        if fret_pos == fret_position:
                            l_chord_found = True
                            break
                    else:
                        if Settings.start_chord_fret <= min_fret and Settings.end_chord_fret >= max_fret >= Settings.start_chord_fret and min_fret <= Settings.end_chord_fret:
                            print tonic+chord_type+":", chord_name, " ", fret_pos, " ", finger_pos, " ", chord_sorted_interval, "within range", min_fret, max_fret, ", ", Settings.start_chord_fret, "-", Settings.end_chord_fret
                            l_chord_found = True
                            break
                        #else:
                        #    print chord_name, fret_pos, " ", finger_pos, "out of range", min_fret, max_fret, ", ", Settings.start_chord_fret, "-", Settings.end_chord_fret
                else:
                    print chord_name, " ", fret_pos, " ", finger_pos, "No fingering", "Searched for chord:", tonic + chord_type
    else:
        print "Please be aware that we only have fingerings for 6-string guitars in standard tuning"

    try: # Search for chord in chord dictionary
        chord_notes = return_chord_notes(tonic, chord_type)
        intervals = chord_dict[chord_type][1:]  # Leave out the first element of the list eg ['maj7', '1', '3', '5', '7']
    except: # If cannot be found, use the details in the csv file.
        print "Chord", tonic + chord_type, "chord not found in Chords.py dictionary. Checking csv file."
        chord_notes = line['Notes'].split()  # Make into alist
        intervals = chord_sorted_interval.split()

    print "Chord Name: ", tonic + chord_type
    print "Compact form:", fret_pos, finger_pos
    print "Intervals:  ", ', '.join(intervals), "/", chord_sorted_interval  # chord_sorted_interval is from csv file
    print "Chord Notes:", ', '.join(chord_notes)

    # Check if there are no duplicate notes in the chord and if it is 4-note chord
    if duplicate_note(line['Notes']) == False and len(chord_notes) == 4:
        print "V-System: Fits into Ted Greene's 4-note chord system"

    if not (l_chord_found):
        print "Fingering for", tonic + chord_type, "chord not found"
    print ""

    bool_intervals = True  # Show the intervals in the chord chart
    finalnotes = ''
    finalinterval = ''
    finalfinger = ''
    finalchordinterval = ''
    lfinalnotes = ['' for OpenString in range(strings)]      # store the last valid note for each open string
    lfinalinterval = ['' for OpenString in range(strings)]   # store the last valid interval for each open string
    interval_fingers = [0 for OpenString in range(strings)]  # store the intervals for the strings used in the chord

    # Print open string line
    for open_string in tuning_dict[Settings.dict_tuning]:
        step_from_note = (notes.index(open_string)) % 12
        fret_note = notes[step_from_note]
        tuning_bar = tuning_bar + fret_note + " " * (string_spacing - len(fret_note))

    print margin_left + " " * 6 + "Notes" + " " * (
    len(tuning_bar) - len("Notes")) + margin_chart + "Intervals" + " " * (
    len(tuning_bar) - len("Intervals")) + margin_chart + "Finger Pos" + \
          ' ' * (len(tuning_bar) - len("Finger Positions"))
    print ""
    print margin_left + " " * 6 + tuning_bar + margin_chart + tuning_bar + margin_chart + tuning_bar

    # Print within reasonable, viewable range
    if Settings.end_chord_fret+1 - Settings.start_chord_fret > 6:
        if min_fret> 3:
            first_fret = min_fret  # First fret where the chord begins
        else:
            first_fret = 0  # First fret where the chord begins
        last_fret =  max(max_fret+1,min_fret+5)  # Last fret where the chord ends
    else:
            first_fret = Settings.start_chord_fret   # First fret where the chord begins
            last_fret = Settings.end_chord_fret+1    # Last fret where the chord ends

    # Print fretboard
    for fret in range(first_fret, last_fret):
        fret_string = ""
        interval_bar = ""
        fret_finger = ""
        fret_string_finger = ""
        i = 0  # goes through each string
        for open_string in tuning_dict[Settings.dict_tuning]:
            step_from_note = (notes.index(open_string) + fret) % 12
            fret_note = notes[step_from_note]
            fret_finger = ""

            if fret == 0 and str(chord_frets[i]).lower() == 'x':
                interval = 'x'
                lfinalinterval[i] = 'x'
                interval_fingers[i] = 'x'
                fret_finger = 'x'

            if fret_note in chord_notes:  # The note is in the chord
                interval = intervals[chord_notes.index(fret_note)]
                lfinalinterval[i] = interval   # Interval for Interval diagram
                lfinalnotes[i] = fret_note     # Note for diagram

                fret_string = fret_string + fret_note + " " * (string_spacing - len(fret_note))
                interval_bar = interval_bar + interval + " " * (string_spacing - len(interval))

                fret_finger = "+"  # default

                # If the fret is the same as in the chord, assign the finger to the column in the csv file
                if l_chord_found:
                    if str(chord_frets[i]).lower() != 'x':
                        if fret == int(chord_frets[i]):
                            # print "checking", fret, chord_frets[i], i
                            interval_fingers[i] = interval  # Interval for Finger diagram
                            if interval_fingers[i] == 0:
                                interval_fingers[i] = 'x'
                            # print open_string, fret, chord_frets[i], chord_fingers[i]
                            if fret > 0:
                                fret_finger = str(chord_fingers[i])
                            else:
                                fret_finger = 'O'  # Open string
                    else:  # str(chord_frets[i]).lower() == 'x'
                        if str(chord_frets[i]).lower() == 'x':
                            if fret == 0:
                                # interval = 'x'
                                # lfinalinterval[i] = interval  # Still draw the interval in the Interval Diagram
                                interval_fingers[i] = 'x'
                                fret_finger = 'x'
                            else:
                                # fret_finger = 'x'        # leave out this variable to leave the (+) symbol in the diagram
                                interval_fingers[i] = 'x'  # only change the bottom finalchordinterval line
                fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
            else:
                # If the note isn't in the chord and it isn't an 'x' print the fret symbol
                if fret == 0 and str(chord_frets[i]).lower() == 'x':
                    # No fret_sym here, as we use an fret_finger='x' if this letter is not part of the chord
                    fret_string_finger = fret_string_finger + fret_finger + " " * (string_spacing - len(fret_finger))
                else:
                    # Put a fret symbol if the note is not in the chord
                    fret_string_finger = fret_string_finger + fret_sym + " " * (string_spacing - len(fret_sym))
                fret_string = fret_string + fret_sym + " " * (string_spacing - len(fret_sym))
                interval_bar = interval_bar + fret_sym + " " * (string_spacing - len(fret_sym))
            i += 1

        # Indicate the beginning fret on the chart diagram
        if fret == first_fret:   #Settings.start_chord_fret:
            fret_num = str(first_fret) + "fr." + " " * (6 - len(str(fret)) - 3)  # Will always contain 6 characters
        else:
            fret_num = " " * 6  # Will always contain 6 characters

        # After each fret check if we have a full chord
        if set(lfinalinterval) <= set(intervals) and set(intervals) <= set(lfinalinterval):
            print margin_left + fret_num + fret_string + margin_chart + interval_bar + margin_chart + fret_string_finger  # , lfinalinterval, fret_f, f1, "Full Chord"  # line for notes and intervals
        else:
            print margin_left + fret_num + fret_string + margin_chart + interval_bar + margin_chart + fret_string_finger  # , lfinalinterval, fret_f, f1  # line for notes and intervals

        # Print the fret bar
        if fret > 0:  # Just the fret bar without notes or intervals
            print margin_left + " " * 6 + fret_bar + margin_chart + " " * (string_spacing - 1) + fret_bar + " " * (
                string_spacing - 1) + margin_chart + fret_bar
        elif fret == first_fret:
            if fret == 0:  # indicate the open position of the first fret
                print margin_left + " " * 6 + fret_o_bar + margin_chart + " " * (
                    string_spacing - 1) + fret_o_bar + " " * (string_spacing - 1) + margin_chart + fret_o_bar
            else:  # indicate the position of the first fret
                print margin_left + " " * 6 + fret_bar + margin_chart + " " * (string_spacing + 1) + fret_bar + " " * (
                    string_spacing + 1) + margin_chart + fret_bar
        else:  # double line eg === for the open string at the nut
            print margin_left + " " * 6 + fret_o_bar + margin_chart + " " * (string_spacing + 1) + fret_o_bar + " " * (
                string_spacing + 1) + margin_chart + fret_o_bar

    # Print the last line with the last notes in the fret range start_chord_fret - end_chord_fret
    for i in range(len(tuning_dict[Settings.dict_tuning])):
        finalnotes = finalnotes + lfinalnotes[i] + " " * (string_spacing - len(lfinalnotes[i]))              # Last line for Notes Diagram
        finalinterval = finalinterval + lfinalinterval[i] + " " * (string_spacing - len(lfinalinterval[i]))  # Last line for Interval Diagram
        finalchordinterval = finalchordinterval + str(interval_fingers[i]) + " " * (
            string_spacing - len(str(interval_fingers[i])))                                                  # Last line for Finger Pos Diagram
    print ""
    print margin_left + " " * 6 + finalnotes + margin_chart + finalinterval + margin_chart + finalchordinterval
    print ""


def finger_rules():
    ## Rules for fingering
    # You can use 4 fingers for notes, and in rare cases one thumb. Each finger can cover several consquitive strings and take wider intervals if the note further towards the bridge compensate for this.
    # For chords you can only ever reach over the maximum stretch of the hand.
    # You can use 1 finger to play strings next to each other (up to the strings of the instrument)
    # Try to fit each finger per fret if possible. Generally the first finger starts on a fret lower, and the last finger on the highest fret.
    # It is possible to play all 4 fingers on the same fret.
    print "Finger Rules!"


# def return_steps_scale(roman_interval, scale_name):
#
#    for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
#        if Scale["Scale"] == scale_name:  # if the scale matches a scale in ListScales
#            scale_interval = Scale["L_Steps"]
#            break

def chords_from_progression(chord, progression_intervals):
    # chord is a string eg "Gb"
    # interval is where the chord starts eg G chord = I interval
    # progression_intervals is a list eg ['I', 'V', 'vi', 'IV']
    # chord_notes would then be ['G', 'D', 'Ebm', 'C']

    global notes
    global notes_flat
    global notes_sharp

    # Determine the root of the chord
    root = chord
    chord_notes = []

    # determine the root from the chord
    if chord[:2] in accidental_notes:
        root = chord[:2]
    else:
        root = chord[:1]

    print chord
    print progression_intervals

    r1 = root.count('b')
    r2 = root.count('#')
    if r1 > 0:
        notes = notes_flat
    if r2 > 0:
        notes = notes_sharp

    interval_found = False
    roman = 0

    for interval in progression_intervals:
        print "interss", interval
        chord_type = ''
        interval_step = 0
        i1 = interval[:1].count('b')  # only check first character as there might be b5's added for triads
        i2 = interval[:1].count('#')  # only check first character as there might be b5's added for triads
        if i1 <= 0 and i2 <= 0:
            interval_short = interval
        else:
            interval_short = interval[1:]
            if i1 > 0:
                interval_step = - i1
            if i2 > 0:
                interval_step = i2

        if interval_short in roman_pos:
            roman = roman_pos[interval_short]
            interval_found = True
            # print roman

            if interval_short in roman_numeral_major:
                chord_type = ''  # major
            if interval_short in roman_numeral_minor:
                chord_type = 'm'  # minor
            if interval_short in roman_numeral_diminished:
                chord_type = 'dim'  # diminished
            if interval_short in roman_numeral_augmented:
                chord_type = 'aug'  # augmented
            if interval_short in roman_numeral_dimsus:
                chord_type = 'dimsus2'  # diminished sus
                # print "recognised chord", chord_type, "in", progression_intervals
        else:
            chord_type = interval.replace('v', '').replace('V', '').replace('i', '').replace('I', '')
            # print "other chord", chord_type, "in", interval
            print "trying", chord_type
            if chord_type in chord_list:
                temp_interval = interval_short.replace(chord_type, '')
                if temp_interval in roman_pos:
                    roman = roman_pos[temp_interval]
                    interval_found = True
                    print "gotcha", temp_interval, chord_type

        if interval_found:
            step_from_note = (notes.index(root) + roman + interval_step) % 12
            if not (chord_type in ['', 'm', 'min', '7', '(no5)']):  # don't use brackets for these chords
                chord_notes.append(notes[step_from_note] + '(' + chord_type + ')')
            else:
                chord_notes.append(notes[step_from_note] + chord_type)

                # print notes[step_from_note], ( roman + interval_step ) % 12,
    print chord_notes

    # if the progression starts with # or b, extract the rest of the progression
    if progression_intervals[:1] == '#' or progression_intervals[:1] == 'b':
        progression_intervals = progression_intervals[1:]

    # chord_list = list(chord_dict.keys())
    # chord_list in progression_intervals

    print ""
    return chord_notes


def play_chosen_scale():
    print ""
    print "PLAY FREQUENCIES OF NOTES IN SCALE"
    print "---------------------------------------------------------"
    print ""

    note_length = 0.07
    scale_list = ""
    cut_at_col = 80
    last_cut = 0
    new_cut = cut_at_col
    new_lines = 0

    for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
        if len(Scale["L_Steps"]) > 2:  # Don't include scales with less than or equal to two elements (intervals)
            scale_list += Scale["Scale"] + ", "
            new_cut = len(scale_list) % cut_at_col
            if last_cut > new_cut:
                scale_list += '\r\n'  # New line for windows
                new_lines += 1
                # print "new cut", last_cut, ">", new_cut
            # print last_cut, new_cut
            last_cut = new_cut

    print ""
    print "Chose a scale from the following list:"
    print ""
    print scale_list[:-1]  # Leave out the comma at the end
    print ""

    while True:
        scale = raw_input("Please select scale: ").strip()
        if len(scale) == 0:  # If nothing was entered, use the data from settings
            scale = Settings.string_scale
            break
        else:
            if valid_scale(scale):
                break
            else:
                print "You can only choose from the list above."
    print "Selection: " + scale.title()
    print " "

    while True:
        root = raw_input("Please select root note: ").strip()
        if len(root) == 0:  # If nothing was entered, use the data from settings
            root = Settings.root_note
            break
        else:
            if root in notes_sharp or root in notes_flat:
                break
            else:
                print root, " is an invalid note"
    print "Selection: " + root.title()
    print ""

    while True:
        octave = raw_input("Please select an octave: ").strip()
        if len(octave) == 0:  # If nothing was entered use octave = 4
            octave = 4
            break
        else:
            try:
                octave = int(octave)
            except ValueError:
                #Handle the exception
                print 'Please enter an integer'
            if octave >= 0 and octave <= 8:
                break
            else:
                print "The octave must be between 0-8"
    print "Selection: " + str(octave)

    play_scale(root, scale, octave, note_length)
    print ""


def play_scale(root, scale, octave, note_length):
    notes_here = ['B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb']
    interval = return_scale_interval(scale)
    scale_notes = return_scale_notes(root, interval)
    semitones = return_semitones(interval)
    rootsemitones = [(x + notes_here.index(root)) % 12 for x in semitones]
    change_index = rootsemitones.index(max(rootsemitones))  # index for highest note in the same octave

    print ""
    print "Scale Name:", root, scale
    print "Intervals: ", ' '.join(interval)
    print "Notes:     ", ' '.join(scale_notes)
    print "Semitones: ", str(semitones)[1:-1]  # leave out the brackets
    # print "Semitone + root:", rootsemitones
    print ""

    oct = octave
    change = False
    # count = 0

    if root == 'B':
        # where the octave ticks over
        change = True

    for i, note in enumerate(scale_notes):
        if change == True and rootsemitones[i] > 0:
            # only change the octave once in the loop
            oct = oct + 1
            change = False
        if i == change_index:
            change = True
        # print note, "index", i, rootsemitones[i], "change", change, "oct", oct
        play_note(note, oct, note_length)


def play_scale2(root, scale, octave, note_length):
    notes_here = ['B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb']
    nums = [i for i in range(-9, 3, 1)]  # B = 0
    interval = return_scale_interval(scale)
    scale_notes = return_scale_notes(root, interval)
    semitones = return_semitones(interval)

    print ""
    print "Scale Name:", root, scale
    print "Intervals: ", ' '.join(interval)
    print "Notes:     ", ' '.join(scale_notes)
    print "Semitones: ", semitones
    print "Semitone + root:", [(x + notes_here.index(root)) % 12 for x in semitones]
    print ""

    distance = 0
    oct = octave
    change = False
    last_num = 0
    for note in scale_notes:
        distance = notes_here.index(note) - notes_here.index('B')

        if last_num < distance:
            change = False
        else:
            change = True

        last_num = distance

        print note, "index", notes_here.index(note), "B index", notes_here.index('B'), "dis", distance, "oct", oct
        print change, last_num, distance

        if change == True and notes_here.index(note) > notes_here.index('B'):
            oct = oct + 1
            change = False

        play_note(note, oct, note_length)

    print ""


def duplicate_note(str_notes):
    # str_notes is a string eg "Db Gb A  D  Gb Db"
    # Returns True if the string contains duplicates. Returns Flase if no duplicates are found.
    notes_list = str_notes.split()
    seen = set()
    #print notes_list
    for note in notes_list:
        if note in seen: return True
        seen.add(note)
    return False


def return_v_system(my_voice):
    # my_voice is a string eg 'TABS' with any mix of the letters B A T S with an optional '+/-' after a letter  eg TBAS+
    # See TedGreene.py
    v_sys = 'None'
    for s, v in greene_table.iteritems():
        #print s, v, my_voice
        if my_voice in v:
            v_sys = str(s)
            #print "Found in v-system:", v_sys
            break
    return v_sys


def nth_largest(n, iter):
    return heapq.nlargest(n, iter)[-1]


def return_note_names(fret_position):
    # fret_position are the positions of the frets for a particular chord eg ['x', 'x', 15, 4, 13, 12]
    # returns the note names for the strings from left to right eg ['F','A','C','E']
    chord_notes = []
    for i in range(int(Settings.string_no)):
        o_string_note = tuning_dict[Settings.dict_tuning][i]   # open string
        if fret_position[i] != 'x':
            try:
                fret_num = int(fret_position[i])
                step_from_note = (notes.index(o_string_note) + fret_num) % 12
                fret_note = notes[step_from_note]
                chord_notes.append(fret_note)   # add valid notes to chord_notes
            except:
                print "Fret", fret_position, "contains a fret that is not a number."
                break
    return chord_notes


def drop_chord(fret_position, voices_to_drop):
    # eg. tonic = 'A', chord_type = '13sus4', fret_position = [0,0,2,2,2,0], voices_to_drop = [2,4]
    jm_tuning_add = 0  # Joni Mitchel interval
    drop = 0
    indx = 0
    octave_shape1 = [3,2]   # For string 1 and 2    Down 3 strings, right 2 frets
    octave_shape2 = [3,3]   # For string 3          Down 3 strings, right 3 frets
    octave_shape3 = [2,-2]  # For string 4          Down 2 strings, left 2 frets
    octave_shape4 = [1,-8]  # For string 5          Down 1 string, left 8 frets
    unison = [-1,-5]        # Up 1 string, left 5 frets

    chord_notes_before = []
    chord_notes_after = []
    voicing_fret = []  # Order of pitches of the chord notes
    drop_fret_position = list(fret_position)

    print ""
    # Find the lowest sounding note in the chord
    for i in range(6):
        if i >= 1:  # to keep track of octaves
            jm_tuning_add += joni_mitchell_tuning(Settings.dict_tuning)[i]  # For standard tuning the result is ['E',5,5,5,5,4,5] so the addition becomes 0, 5, 10, 15, 19, 24
        if fret_position[i] != 'x':
            fret_num = int(fret_position[i])
            voicing_fret.append(fret_num + jm_tuning_add)   # List of 4 numbers eg [15, 5, 18, 21]

    voicing_string_order = list(voicing_fret)   # Use list() to not reference the same object
    chord_notes_before = return_note_names(fret_position)

    print fret_position
    print chord_notes_before
    print "voicing", voicing_fret

    # Find the nth largest number to drop the given voicing (eg Drop 2, Drop 3)
    for v in voices_to_drop:
        drop = nth_largest(v, voicing_fret)   # Find the nth largest number
        indx = voicing_string_order.index(drop)
        print "Drop", v, "nth num", drop, "index", indx,
        # voicing_string_order[indx] = drop - 12   # Change the nth largest number and reduce by an octave

        j = 0
        for i in range(6):
            if fret_position[i] != 'x':
                # change the bottom strings to the new octave position
                if j == indx:
                    if i == 5 or i==4: # On string 1 and 2
                        print i, i-octave_shape1[0], drop_fret_position[i], octave_shape1[1]
                        drop_fret_position[i-octave_shape1[0]] = drop_fret_position[i] + octave_shape1[1]
                    if i == 3: # On string 3
                        if drop_fret_position[i-octave_shape2[0]] == 'x':
                            print i, i-octave_shape2[0], drop_fret_position[i], octave_shape2[1]
                            drop_fret_position[i-octave_shape2[0]] = drop_fret_position[i] + octave_shape2[1]
                        else:
                            print "Move unison up", drop_fret_position[i-unison[0]],  drop_fret_position[i] + unison[1]+1
                            drop_fret_position[i-unison[0]] = drop_fret_position[i] + unison[1]+1
                            drop_fret_position[i-octave_shape2[0]] = drop_fret_position[i] + octave_shape2[1]
                    if i == 2: # On string 4
                        if drop_fret_position[i-octave_shape3[0]] == 'x':
                            print i, i-octave_shape3[0], drop_fret_position[i], octave_shape3[1]
                            drop_fret_position[i-octave_shape3[0]] = drop_fret_position[i] + octave_shape3[1]
                        else:
                            print "Move unison up", drop_fret_position[i-unison[0]],  drop_fret_position[i] + unison[1]
                            drop_fret_position[i-unison[0]] = drop_fret_position[i] + unison[1]
                            drop_fret_position[i-octave_shape3[0]] = drop_fret_position[i] + octave_shape3[1]
                    if i == 1: # On string 5
                        if drop_fret_position[i-octave_shape4[0]] == 'x':
                            print i, i-octave_shape4[0], drop_fret_position[i], octave_shape4[1]
                            drop_fret_position[i-octave_shape4[0]] = drop_fret_position[i] + octave_shape4[1]
                        else:
                            print "Move unison up", drop_fret_position[i-unison[0]],  drop_fret_position[i] + unison[1]
                            drop_fret_position[i-unison[0]] = drop_fret_position[i] + unison[1]
                            drop_fret_position[i-octave_shape4[0]] = drop_fret_position[i] + octave_shape4[1]
                    drop_fret_position[i] = 'x' # this string is no longer played
                j += 1

    # Check if the notes are the same
    chord_notes_after = return_note_names(drop_fret_position)
    print chord_notes_after

    return drop_fret_position


def drop(fret_close_positions, drops, start_strings, move_to, drop_interval):
    # fret_positions are the fret positions for the chord eg Dbdim7 -> x-x-8-9-8-9 -> ['x', 'x', '8', '9', '8', '9']
    # drop_interval is a numeric list eg [12, 24] for eg. octave = 12, two octaves = 24, or unison = 0
    # drops is a numeric list of which voicings to drop eg Drop 3 = [3], Drop 2 & 4 = [2, 4]
    # strings is a numeric list of where to drop or raise the note in relation to the dropped voicing.
    # eg [2] will mean find the given voice to raise two strings above it.

    # Find the lowest sounding note in the chord
    jm_tuning_add = 0
    drop_positions = [0 for OpenString in range(int(Settings.string_no))]

    voicing_fret = []  # Order of pitches of the chord notes
    for i in range(int(Settings.string_no)):
        if i >= 1:  # to keep track of octaves
            jm_tuning_add += joni_mitchell_tuning(Settings.dict_tuning)[i]  # For standard tuning the result is ['E',5,5,5,5,4,5] so the addition becomes 0, 5, 10, 15, 19, 24
        if fret_close_positions[i] != 'x':
            fret_num = int(fret_close_positions[i])
            voicing_fret.append(fret_num + jm_tuning_add)   # List of 4 numbers eg [15, 5, 18, 21]

    print voicing_fret
    
    chord_chart(tonic = 'C', chord_type='6', fret_position = 'x-x-14-12-10-8')


    return drop_positions  # eg ['x', '10', 'x', '9', '11', '9]

# Testing
# print drop(['x', 'x', '8', '9', '8', '9'], drops=[2,4], start_strings=[2,4], move_to=[3,2], drop_interval=[-12,12])


def show_ted_greene(my_chord):
    # See TedGreene.py
    # ted_greene_method1_text()  # Show the text explaining method 1
    # Find all the four note chords in the database which fit into the V-System according to Ted Greene
    # http://www.tedgreene.com/images/lessons/v_system/03_Method1_HowToRecognize.pdf

    print ""
    print "TED GREENE'S V-SYSTEM FOR FOUR-NOTE CHORDS"
    print "---------------------------------------------------------"
    print "Each four notes of the chord is allocated a voice depending on their sound "
    print "from low - high, from Bass (B), Tenor (T), Alto (A), Soprano (S)."
    print ""
    print "Finding 4-note chords without doubling for", my_chord, "between frets", Settings.start_chord_fret, "and", Settings.end_chord_fret
    print ""

    import csv
    global test_file
    test_file = 'Chord Finger Positions.csv'
    global csv_file
    csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',')

    chord_frets = [0 for OpenString in range(6)]      # Frets from the chord
    chord_fingers = [0 for OpenString in range(6)]    # Finger numbers from the chord (1-4)
    chord_interval = [0 for OpenString in range(6)]   # Intervals from the chord
    chord_interval_copy = list()

    # Order of voices: Bass (lowest), Tenor (second lowest), Alto (second highest), Soprano (highest)
    voices = ['B', 'T', 'A', 'S']
    voices_exclude = []  # 'BSTA','BAST','STAB','ABST','TABS']   # Don't show charts of items with this voicing.
    list_sorted_intervals = list()  # Sorted intervals eg.  [1, b3, 5, b7]

    header_fret = list()
    header_interval = list()
    frets = list()
    chord_notes = list()
    v_chord_tone_path = list()   # The order in which the voices appear using the 'chord tone path'

    intervals = list()           # Intervals from the dictionary
    bad_chords = list()          # Chords that can't be found in the chord dictionary
    interesting_chords = list()
    v_syst = list()
    voicing_fret = list()        # fret_num + jm_tuning_add
    voicing_letters = list()
    voicing_jm_order = list()

    freqs_voice = {}             # Counts the frequency of each voicing
    freqs_sys = {}               # Counts the frequency of system

    count_bad = 0
    count_v_chord = 0  # Count the number of chords that are in the V-System
    jm_tuning_add = 0  # Joni Mitchel interval
    min_v = 0
    min_fret = 0
    max_fret = 0

    tonic = ''
    chord_name = ''
    fret_note = ''
    chord_notes = ''
    grouping = ''
    voice_str = ''
    voice_str_oct = ''
    voice_line = ''
    common_voice = ''.join(voices)  # Most common voice
    v_system = ''
    bool_octave_leap = False
    doubled_note = False

    a_change = 0
    b_change = 0

    header_fret = ['Ft-E','Ft-A','Ft-D','Ft-G','Ft-B','Ft-e']
    header_interval = ['Fi-E','Fi-A','Fi-D','Fi-G','Fi-B','Fi-e']   # The intervals are already converted to the lowest octave. Eg #9 = b3

    if Settings.instrument.lower() == "guitar" and Settings.string_no == '6':
        for line in csv_file:
            # print "Gr", line['Chord Name'], " ", line['Fret Positions'], " ", line['Finger Positions']
            chord_name = line['Chord Name']
            if chord_name.lower()==my_chord.lower() or my_chord.lower()=='all chords':
                if line['Fg-E'] != 0 or line['Fg-A'] != 0 or line['Fg-D'] != 0 or line['Fg-G'] != 0 or \
                                line['Fg-B'] != 0 or line['Fg-e'] != 0:
                    chord_type = line['Chord Type']
                    tonic = chord_name.replace(chord_type,"")  # Take out the chord type from the chord name for the root note
                    fret_pos = line['Fret Positions']
                    finger_pos = line['Finger Positions']
                    chord_notes = line['Notes']
                    chord_sorted_interval = line['Sorted Intervals']
                    grouping = line['Grouping']

                    for i in range(6):
                        chord_frets[i] = line[str(header_fret[i])]           # Frets for each string in the chord
                        chord_interval[i] = line[str(header_interval[i])]    # Intervals for each string in the chord

                    try:  # try to find the notes and intervals of the chord by looking up the chord formula
                        chord_notes = return_chord_notes(tonic, chord_type)  # Search for chord in chord dictionary
                        intervals = chord_dict[chord_type][1:]  # Leave out the first element of the list eg ['maj7', '1', '3', '5', '7']

                    except:  # if the chord cannot be found in the chord dictionary
                        # print line['Chord Name'], line['Fret Positions'], line['Finger Positions'], "  Can't find chord", chord_type
                        count_bad += 1
                        if chord_type not in bad_chords:
                            bad_chords.append(chord_type)

                    # Check if any notes are doubled
                    doubled_note = False
                    chord_notes = []         # empty the list
                    frets = []               # fret numbers for each valid string
                    fret_num = []
                    finger_num = []
                    v_chord_tone_path = []

                    for i in range(6):
                        o_string_note = tuning_dict[Settings.dict_tuning][i]   # open string
                        if chord_frets[i].strip() != 'x':
                            try:
                                fret_num = int(chord_frets[i])
                                frets.append(fret_num)
                                step_from_note = (notes.index(o_string_note) + fret_num) % 12
                                fret_note = notes[step_from_note]
                                if fret_note in chord_notes:
                                    doubled_note = True
                                chord_notes.append(fret_note)   # add valid notes to chord_notes
                            except:
                                print "Fret", chord_frets, "contains a fret that is not a number. See csv file for chord", chord_name, chord_type, fret_pos, finger_pos
                                break

                    #fret_num = [int(num) for num in chord_frets if num != 'x']  # List of all the fret numbers without the 'x'
                    finger_num = [int(num) for num in chord_fingers if num != 'x' and num >= 0]  # List of all the finger numbers larger than 0
                    try:
                        min_fret = min(frets)
                        max_fret = max(frets)
                    except:
                        print frets, "does not have a minimum or maximum"
                        break

                    # Check if the chord is within the viewable fret range
                    if Settings.start_chord_fret <= min_fret and Settings.end_chord_fret >= max_fret >= Settings.start_chord_fret and min_fret <= Settings.end_chord_fret:
                        # Check if the chord has exactly four distinct notes, so it fits into the V-System
                        if len(frets)==4 and not doubled_note:
                            #print "Gr2", frets, " ",  chord_frets[0], chord_frets[1], chord_frets[2], chord_frets[3], chord_frets[4], chord_frets[5], " ", min_fret, max_fret, len(frets)
                     ####       #print chord_name, ", ", fret_pos, ", ", finger_pos, ", ", line['Notes'], ", ", chord_sorted_interval
                                #line['Notes'], ", ", line['Fi-E']+" "+line['Fi-A']+" "+line['Fi-D']+" "+line['Fi-G']+" "+line['Fi-B']+" "+line['Fi-e'], ", ", chord_sorted_interval
                            #########################
                            ###    PRINT CHART    ###
                            #########################
                            #chord_chart(tonic, chord_type, fret_pos)  # prints 3 diagrams of the chord (notes, intervals, finger positions)
                            count_v_chord += 1  # successfully found a chord that fits into the V-System

                            # Find the lowest sounding note in the chord
                            jm_tuning_add = 0
                            voicing_fret = []  # Order of pitches of the chord notes
                            for i in range(6):
                                if i >= 1:  # to keep track of octaves
                                    jm_tuning_add += joni_mitchell_tuning(Settings.dict_tuning)[i]  # For standard tuning the result is ['E',5,5,5,5,4,5] so the addition becomes 0, 5, 10, 15, 19, 24
                                if chord_frets[i] != 'x':
                                    fret_num = int(chord_frets[i])
                                    voicing_fret.append(fret_num + jm_tuning_add)   # List of 4 numbers eg [15, 5, 18, 21]

                            voicing_letters = list(voicing_fret)        # Use list() to not reference the same object
                            voicing_jm_order = list(voicing_fret)
                            voicing_original = list(voicing_fret)       # Original order of the jm tuning
                            #if sorted(voicing_fret) <> voicing_copy:   #Sort the order of pitches and compare with the order as they appear
                            #    print voicing_fret, "DIFFERENT ORDER"

                            # Sort the voicing by the chord's index (by pitch) from lowest sound to highest sound
                            for v in voices:  # replace each voicing_fret with the order of the voicing letter
                                min_v = min(voicing_fret)
                                # print v, min_v, voicing_copy, voicing_fret, voicing_jm_order
                                voicing_letters[voicing_letters.index(min_v)] = v                  # Change the smallest number into B, T, A then S
                                voicing_fret = list(filter(lambda x: x!= min_v, voicing_fret))     # Remove the smallest number
                                # print voicing_letters, voicing_jm_order   # The results will be two lists eg: ['B', 'T', 'A', 'S'] [5, 15, 18, 21]

                            # Change the voicing by Chord Tone Path (start with the lowest interval of the chord)
                            list_sorted_intervals = chord_sorted_interval.split()   # Change the interval string into a list
                            chord_interval_copy = [degree for degree in chord_interval if degree != '' and degree !='x']
                            # print "CHORD ORDER", voicing_copy, "interval short", chord_interval_copy, "sorted", list_sorted_intervals
                            for interval in list_sorted_intervals:                  # There should only be 4 items
                                v_index = chord_interval_copy.index(interval)       # Look for the index for each interval (eg b3, 5, b7)
                                # print interval, v_index, voicing_letters[v_index]
                                v_chord_tone_path.append(voicing_letters[v_index])  # Look up the letter in voicing_letters that comes from the sorted intervals
                            voice_str = ''.join(v_chord_tone_path)                  # Make the voicing_letters list into a string
                            # print "V-SYSTEM:", voice_str

                            if len(list_sorted_intervals)==4 and len(v_chord_tone_path)==4 and len(grouping)==6: # and min_fret>=12:
                                # Check for higher or lower octaves with chords. Compare each of the adjacent voices eg if your voicing is BTAS then compare B - A, A - T, T - S
                                bool_octave_leap = False
                                #print chord_name, " ", fret_pos, " ", chord_sorted_interval, chord_notes
                                for i in range(3):
                                    a = voicing_original[voicing_letters.index(voices[i])]    # voicing_jm_order[v_chord_tone_path.index(voice_str[i])]     # voicing_jm_order[voicing_copy.index(voice_str[i])]
                                    b = voicing_original[voicing_letters.index(voices[i+1])]  # voicing_jm_order[v_chord_tone_path.index(voice_str[i+1])]   # voicing_jm_order[voicing_copy.index(voice_str[i+1])]
                                    va = voicing_letters[i]    # eg. for BTAS:  B
                                    vb = voicing_letters[i+1]  # eg. for BTAS:  T

                                    # print voice_str, va+"-"+vb+":", str(b)+"-"+str(a)+" =", b - a, v_chord_tone_path, voicing_jm_order
                                    if abs(b - a) >= 12:          # Check for octave leap between voicings
                                        bool_octave_leap = True
                                        a_change = a
                                        b_change = b
                                        if a <= b:
                                            voice_str = str(voice_str.replace(va, va + "-"))   # Add a '+' for an octave higher eg B becomes B+
                                            # print "Extra - octave between", vb, "and", va +":", str(b)+"-"+str(a)+" =", b-a
                                        else:
                                            voice_str = str(voice_str.replace(vb, vb + "-"))   # Add a '-' for an octave lower eg B becomes B-
                                            # print "Extra + octave between", vb, "and", va +":", str(a)+"-"+str(b)+" =", a-b
                                        print chord_name, " ", fret_pos, " ", chord_sorted_interval, chord_notes, voicing_jm_order, "V-System:", v_system, "("+voice_str+")"

                                print chord_name, " ", fret_pos, " ", chord_sorted_interval, chord_notes, voicing_jm_order, "V-System:", v_system, "("+voice_str+")"

                                v_system = return_v_system(str(voice_str))                     # eg 'V-4'
                                freqs_voice[voice_str] = freqs_voice.get(voice_str, 0) + 1     # Counter for each voice eg System: V-2 (BSTA), Count: 468
                                freqs_sys[v_system] = freqs_sys.get(v_system, 0) + 1           # Counter for each system eg System: V-4 Count: 395
                                if voice_str not in v_syst:
                                    v_syst.append(voice_str)

                                print grouping
                                chord_chart(tonic, chord_type, fret_pos)
                                if '+' in str(voice_str) or '-' in str(voice_str):             # not in voices_exclude:
                                    #########################
                                    ###    PRINT CHART    ###
                                    #########################
                                    chord_chart(tonic, chord_type, fret_pos)
                                    interesting_chords.append(chord_name+"  "+fret_pos+"  "+chord_sorted_interval+"  "+v_system+" ("+voice_str+")")

                                    voice_line = "VOICES:" + " " * 44
                                    j = 0
                                    for i in range(6):
                                        if chord_frets[i] != 'x' and j < 4:
                                            try:
                                                voice_line += voices[j] + " "*2
                                                j += 1
                                            except:
                                                voice_line += " "*3
                                        else:
                                            voice_line += " "*3
    else:
        print "Please be aware that we only have fingerings for 6-string guitars in standard tuning."
        return   # exits the function

    if my_chord == 'All Chords':
        print ""
        print "Found", count_v_chord, "chords which fit into Ted Greene's V-System"
        print "Frequency of each vocing:"
        print ""

        s = sorted(freqs_voice.items(),key = lambda x :-x[1])  # Reverse sort the table by value (Count)
        for voice, count in s:
            print "System:", return_v_system(voice)+" ("+voice+"),", "Count:", count
        print ""

        s = sorted(freqs_sys.items(),key = lambda x :-x[1])  # Reverse sort the table by value (Count)
        for sys, count in s:
            print "System:", sys, "Count:", count
        print ""

        #print "Interesting chords which are not in voicing", " ".join(voices_exclude)  # Most common voices
        print "Interesting chords which have an octave leap"
        for chord in interesting_chords:
            print chord

        # print "Could't find these chords in the chord dictionary"
        # print bad_chords, "they occured", count_bad, "times"


def show_menu():
    main_menu = {}
    main_menu[1] = "Change Settings"
    main_menu[2] = "All Notes on Fretboard"
    main_menu[3] = "Scale on Fretboard in 12 keys (" + Settings.string_scale.title() + ")"
    main_menu[4] = "Scale Tabs in 12 keys (" + Settings.string_scale.title() + ")"
    main_menu[5] = "Chord Inver. in 12 keys (" + Settings.chord_name.title() + ")"
    main_menu[6] = "Chord Diagram in 12 keys (" + Settings.chord_name.title() + ")"
    main_menu[7] = "Mental Fretboard Trainer"
    main_menu[8] = "Visual Fretboard Trainer"
    main_menu[9] = "Semi-tone Interval Trainer"
    main_menu[10] = "Finger Reach"
    main_menu[11] = "Chord Chart (" + Settings.chord_name.title() + ")"
    main_menu[12] = "Your Chord Sequence (Tabs)"
    main_menu[13] = "Chord Progressions"
    main_menu[14] = "Play Notes of Scales"
    main_menu[15] = "Joni Mitchell Tunings Notation"
    main_menu[16] = "Ted Greene's V-System"
    main_menu[17] = "Testing V-System"
    main_menu[18] = "Exit"

    while True:
        options = main_menu.keys()
        print ""
        instrument_details = Settings.string_no.title() + " String " + Settings.instrument.title() + " in " + Settings.tuning_short + " Tuning"
        print "MAIN MENU - " + instrument_details.upper()
        print "---------------------------------------------------------"
        for entry in options:
            print str(entry) + ".", main_menu[entry]
        print ""
        selection = raw_input("Please Select: ").strip()
        if bool_int(selection):  # if selection is an integer
            selection = int(selection)
            if selection == 1:
                change_settings()
            elif selection == 2:
                show_all_notes_on_fretboard()
            elif selection == 3:
                scale_all_keys()
            elif selection == 4:
                scale_tabs_all_keys()
            elif selection == 5:
                chord_all_keys()
            elif selection == 6:
                chord_chart_all_keys()
            elif selection == 7:
                mental_fretboard_trainer(Settings.no_questions)
            elif selection == 8:
                visual_fretboard_trainer(Settings.no_questions)
            elif selection == 9:
                interval_trainer(Settings.no_questions)
            elif selection == 10:
                show_stretch_distance()
            elif selection == 11:
                chord_chart(Settings.root_note, shorten_chord(Settings.chord_name), fret_position = "")
            elif selection == 12:
                chord_sequence("")
            elif selection == 13:
                chords_from_progression('G', ['viib5', 'vii', 'VII'])
                chords_from_progression('G', ['III', 'bIII', 'i', 'ii(no5)', 'iii', 'iiio', 'III+', 'V5', 'iiiosus2',
                                              'viib5', 'vii', 'VII'])
                chords_from_progression('G', ['I', 'V', 'vi', 'IV'])
                chords_from_progression('G', ['I', 'vi', 'IV', 'V'])
                chords_from_progression('G', ['I', 'V', 'vi', 'iii', 'IV', 'I', 'IV', 'V'])
                chords_from_progression('G', ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'V', 'I', 'I'])
                chords_from_progression('G', ['ii', 'IV', 'V'])
                chords_from_progression('G', ['I', 'IV', 'V', 'IV'])
                chords_from_progression('G', ['V', 'IV', 'I'])
                chords_from_progression('G', ['vi', 'IV', 'I', 'V'])
                chords_from_progression('G', ['vi', 'V', 'IV', 'III'])
                chords_from_progression('G', ['vi', 'V', 'VI', 'V'])
                chords_from_progression('G', ['ii', 'I', 'V', 'bVII', 'VI'])
                chords_from_progression('G', ['ii', 'I', 'vii', 'bVII', 'VI'])
                chords_from_progression('G', ['i', 'V', 'bVII', 'IV', 'bVI', 'bIII', 'iv', 'V'])
                # Caryn example
                chords_from_progression('Bb', ['I', 'ii', 'iii', 'IV', 'V7', 'vi', 'viib5', 'VIII'])
                chords_from_progression('Bb', ['vi', 'viib5', 'I', 'ii', 'iii', 'IV', 'V7'])
            elif selection == 14:
                play_chosen_scale()
                # play_sound(frequency = 3000, length = 0.5)
                # play_chromatic(note_length = 0.1)
                # play_note(note='A', octave=4, note_length=0.2)
            elif selection == 15:
                show_mitchell_tunings()
            elif selection == 16:
                show_ted_greene('All Chords')
                #show_ted_greene('E7#9')
                #show_ted_greene('E7b5(#9)')
                #show_ted_greene('Em9(maj7)')
                #show_ted_greene('Eb7#9')
                #show_ted_greene('F7#9')
                #show_ted_greene('Bm(maj7)')
            elif selection == 17:

                print "C6   x-x-14-12-10-8"
                print drop(fret_close_positions=['x', 'x', '14', '12', '10', '8'], drops=[2,4], start_strings=[2,4], move_to=[3,2], drop_interval=[-12,12])

                #print 'Bb A A# F# Gb C Db', " - ", sharp('Bb A A# F# Gb C Db')
                #print 'Bb A A# F# Gb C Db', " - ", flat('Bb A A# F# Gb C Db')
                #print flat(['A#','A','Bb','Gb','F#','C'])
                #print sharp(['Bb', 'A', 'A#', 'F#', 'Gb', 'C'])
                #convert_note(['A#','A','Bb','Gb','F#','C'])

                #print ""
                #print "D-9 (no root)"
                #print drop_chord(['x','x',15,14,13,12],[2])
                #print drop_chord(['x','x',15,14,13,12],[3])
                #print drop_chord(['x','x',15,14,13,12],[4])
                #print drop_chord(['x','x',15,14,13,12],[2,3])
                #print drop_chord(['x','x',15,14,13,12],[2,4])
                #print drop_chord(['x','x',15,14,13,12],[2,3,4])  #Check when overwriting string with an existing note
                #
                #  print "Db Gb A D Gb Db", duplicate_note("Db Gb A D Gb Db")
                # print return_v_system('TABS')
            elif selection == 18:
                exit()
            else:
                print "Unknown option", selection, "selected!"
        else:
            print "Unknown option", selection, "selected!"


show_menu()
