# Frequency
# #http://askubuntu.com/questions/202355/how-to-play-a-fixed-frequency-sound-using-python

from __future__ import division  # Avoid division problems in Python 2
import math
#import pyaudio


def play_sound(frequency, length):
    # frequency = 261.63  #Hz, waves per second, 261.63 = C4 note
    # length = 1.5  # seconds to play sound

    # sudo apt-get install python-pyaudio
    PyAudio = pyaudio.PyAudio

    # See http://en.wikipedia.org/wiki/Bit_rate#Audio
    bitrate = 16000  # number of frames per second/frameset.

    # See http://www.phy.mtu.edu/~suits/notefreqs.html

    numberofframes = int(bitrate * length)
    RESTFRAMES = numberofframes % bitrate
    wavedata = ''

    for x in xrange(numberofframes):
        wavedata = wavedata + chr(int(math.sin(x / ((bitrate / frequency) / (2 * math.pi))) * 127 + 128))

    # fill remainder of frameset with silence
    for x in xrange(RESTFRAMES):
        wavedata = wavedata + chr(128)

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=bitrate,
                    output=True)
    stream.write(wavedata)
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_chromatic(note_length):
    A4 = 440  # A4 (fourth octave of A) is 440 Hz
    for n in range(-21, 27, 2):  # n = -21, 19 ...27
        frequency = A4 * 2 ** (n / 12)
        print n, round(frequency, 2)
        play_sound(frequency, note_length)


def play_note(note, octave, note_length):
    A4 = 440  # A4 (fourth octave of A) is 440 Hz

    notes_order_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    notes_order_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_index = [i for i in range(-9, 3, 1)]  # A = 0

    col = 0
    if note in notes_order_flat:
        col = notes_order_flat.index(note)
    if note in notes_order_sharp:
        col = notes_order_sharp.index(note)

    index = note_index[col]
    # print "col", col, "index", index, len(note_index), note_index

    numerator = A4 * 2 ** (index / 12)
    divisor = 2 ** (4 - octave)
    frequency = numerator / divisor

    print note+",", "octave " + str(octave) + ",", "freq.", round(frequency, 2), "Hz"
    #play_sound(frequency, note_length)
