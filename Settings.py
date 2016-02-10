# Settings
# Opens the settings.txt file and loads the variables for all of the available settings.
try:
    # Open the file for reading the fretboard settings
    with open('settings.txt', 'r') as infile:
        data = infile.read()  # Read the contents of the file into memory.
        pass
except IOError as e:
    print "Unable to open settings file" #Does not exist OR no read permissions
    pass

# Return a list of the lines, breaking at line boundaries.
settings = data.splitlines()
#print "Settings:", settings

instrument = str(settings[0]).replace("Instrument:", "").strip(" ")           # eg Guitar or Bass
string_no = str(settings[1]).replace("Strings:", "").strip(" ")               # Number of strings the guitar or bass has eg. 4, 5, 6, 7
tuning_short = str(settings[2]).replace("Tuning:", "").strip(" ").title()     # eg Standard or Drop D
root_note = str(settings[3]).replace("Root Note:", "").strip(" ").title()     # eg A, G, F# etc
chord_name = str(settings[4]).replace("Chord Name:", "").strip(" ").lower()   # eg 7#9#5
string_scale = str(settings[5]).replace("Scale:", "").strip(" ").title()      # eg Major, Mixolydian
dict_tuning = str(instrument + " " + string_no + " " + tuning_short).title()  # eg Guitar 6 Standard

# Fretboard Trainer
# These are the parameters for fretboard memorization.
# The open string, and minimum and maxium fret number you want to be trained on. You will be asked to guess 10 notes.
#
# If you leave he O_string_train parameter blank, it will randomly pick any open string for you.
# If you specify one string, it will train you on that string between fret_train_min and fret_train_max.

o_string_train = str(settings[6]).replace("Training String:", "").strip(" ")       # The string that you chose to memorize eg. E
fret_train_min = int(settings[7].replace("Start Training Fret:", "").strip(" "))   # eg The min fret from which the random note will be chosen eg 1
fret_train_max = int(settings[8].replace("End Training Fret:", "").strip(" "))     # eg The max fret from which the random note will be chosen eg 5
no_questions =  int(settings[9].replace("Number of Questions:", "").strip(" "))    # The number of notes you will guess in a fretboard quiz eg 10
load_and_save = str(settings[10]).replace("Load And Save Score:", "").strip(" ")

# Chord Diagrams
start_chord_fret = int(settings[11].replace("Start Chord Fret:", "").strip(" "))   # The starting fret for the chord diagram eg 0
end_chord_fret = int(settings[12].replace("End Chord Fret:", "").strip(" "))       # The last fret for the chord diagram eg 4

print_log = str(settings[13]).replace("Print Log:", "").strip(" ")
exercise = str(settings[14]).replace("Exercise:", "").strip(" ")                   # Exercise scale patterns. See Exercises.py for valid choices