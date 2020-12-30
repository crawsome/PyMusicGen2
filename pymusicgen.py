import os
import pickle
import random
import sys
import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from window import Ui_MainWindow
from midiutil import MIDIFile
import subprocess
from collections import namedtuple
from time import sleep
from pygame import mixer

# Init pygame audio mixer

mixer.init()
mixer.set_num_channels(64)

# init MyMidi
MyMIDI = MIDIFile(1)

note = namedtuple('Note', ['track', 'channel', 'pitch', 'time', 'duration', 'volume'])
basicnotelist = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
name_to_int_base12 = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9,
                      'Bb': 10, 'B': 11}
name_to_int_distance = {'C': 0, 'C#/Db': 1, 'D': 2, 'D#/Eb': 3, 'E': 4, 'F': 5, 'F#/Gb': -6,
                        'G': -5, 'G#/Ab': -4, 'A': -3, 'A#/Bb': -2, 'B': -1}
int_distance = [0, 1, 2, 3, 4, 5, -6, -5, -4, -3, -2, -1]
intref = ["C1", "Db1", "D1", "Eb1", "E1", "F1", "#1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
          "Eb2", "E2", "F2", "F#2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3", "Eb3", "E3", "F3",
          "F#3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4", "Eb4", "E4", "F4", "F#4", "G4", "Ab4",
          "A4", "Bb4", "B4", "C5", "Db5", "D5", "Eb5", "E5", "F5", "F#5", "G5", "Ab5", "A5", "Bb5", "B5",
          "C6", "Db6", "D6", "Eb6", "E6", "F6", "F#6", "G6", "Ab6", "A6", "Bb6", "B6", "C7", "Db7", "D7",
          "Eb7", "E7", "F7", "F#7", "G7", "Ab7", "A7", "Bb7", "B7", "C8"]
toneref = {'C1': 24, 'Db1': 25, 'D1': 26, 'Eb1': 27, 'E1': 28, 'F1': 29, 'F#1': 30, 'G1': 31, 'Ab1': 32, 'A1': 33,
           'Bb1': 34, 'B1': 35, 'C2': 36, 'Db2': 37, 'D2': 38, 'Eb2': 39, 'E2': 40, 'F2': 41, 'F#2': 42, 'G2': 43,
           'Ab2': 44, 'A2': 45, 'Bb2': 46, 'B2': 47, 'C3': 48, 'Db3': 49, 'D3': 50, 'Eb3': 51, 'E3': 52, 'F3': 53,
           'F#3': 54, 'G3': 55, 'Ab3': 56, 'A3': 57, 'Bb3': 58, 'B3': 59, 'C4': 60, 'Db4': 61, 'D4': 62, 'Eb4': 63,
           'E4': 64, 'F4': 65, 'F#4': 66, 'G4': 67, 'Ab4': 68, 'A4': 69, 'Bb4': 70, 'B4': 71, 'C5': 72, 'Db5': 73,
           'D5': 74, 'Eb5': 75, 'E5': 76, 'F5': 77, 'F#5': 78, 'G5': 79, 'Ab5': 80, 'A5': 81, 'Bb5': 82, 'B5': 83,
           'C6': 84, 'Db6': 85, 'D6': 86, 'Eb6': 87, 'E6': 88, 'F6': 89, 'F#6': 90, 'G6': 91, 'Ab6': 92, 'A6': 93,
           'Bb6': 94, 'B6': 95, 'C7': 96, 'Db7': 97, 'D7': 98, 'Eb7': 99, 'E7': 100, 'F7': 101, 'F#7': 102, 'G7': 103,
           'Ab7': 104, 'A7': 105, 'Bb7': 106, 'B7': 107, 'C8': 108}


# Return array that is rotated circular
def rotate(l, n):
    return l[-n:] + l[:-n]


# Compare two floats against an error returns TRUE if both floats are ~=
def floatequal(l, r):
    return abs(l - r) < .01


class TwoWayIterator:
    def __init__(self, ourlist: list):
        self.index = 0
        self.element = None
        self.ourlist = ourlist

    def insert(self, element):
        self.ourlist.insert(self.index, element)

    def remove(self):
        if len(self.ourlist) > 0:
            del (self.ourlist[self.index])
            self.index -= 1

    def next(self):
        if self.index + 1 < len(self.ourlist):
            self.index += 1
        self.element = self.ourlist[self.index]
        return self.element

    def prev(self):
        if self.index - 1 >= 0:
            self.index -= 1
        self.element = self.ourlist[self.index]
        return self.element


class PyMusicGen(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyMusicGen, self).__init__(parent)
        self.setupUi(self)

        # Directory where piano note wav files are stored
        self.wavdir = 'wav/'

        # piano settings
        self.starting_point = 60
        self.note_range = 16

        # from the "Open" menu TODO
        self.save_file_name = ''

        # From GUI Selections
        self.key = None
        self.tension = None
        self.durations = []
        self.note_times = []
        self.seed = None
        self.random_seed()
        self.beatspermeasure = None
        self.beatsperminute = None  # Not implemented yet, or maybe not ever (MIDI ideal replacement)

        # Generated using methods below TODO
        self.ourscale = []
        self.thismeasure = []  # filled with note objects
        self.song = []  # filed with measures
        self.song_iterator = TwoWayIterator(self.song)  # For CRUD operations

        # Connect functions with gui elements
        self.generatebutton.clicked.connect(self.new_measure)
        self.randomseedbutton.clicked.connect(self.random_seed)
        self.resetsettingsbutton.clicked.connect(self.reset_fields)
        self.randomsettingsbutton.clicked.connect(self.random_fields)

        self.forwardbutton.clicked.connect(self.forward_measure)
        self.backbutton.clicked.connect(self.back_measure)
        self.deletebutton.clicked.connect(self.delete_measure)
        self.insertbutton.clicked.connect(self.insert_new_measure)
        self.playbutton.clicked.connect(self.play_song)
        self.playmeasurebutton.clicked.connect(self.playmeasure)

        self.actionNew_Song.triggered.connect(self.newsong)
        self.actionSave_Song.triggered.connect(self.savesong)
        self.actionAbout.triggered.connect(self.aboutmenu)
        self.actionExport_to_MIDI.triggered.connect(self.export_to_midi)
        self.actionQuit.triggered.connect(self.quit)

    def quit(self):
        pass

    def aboutmenu(self):
        pass

    def export_to_midi(self):
        pass

    def newsong(self):
        pass

    # sets a random seed for user
    def random_seed(self):
        self.seed = random.randint(0, sys.maxsize)
        random.seed(self.seed)
        self.seedtextbox.setText(str(self.seed))

    def check_key_field(self):
        msg = ''
        try:
            test = self.keywidget.selectedItems()[0].text()
        except Exception as e:
            msg = 'Please select a Key\n'
        return msg

    def check_tension_field(self):
        msg = ''
        try:
            test = self.tensionwidget.selectedItems()[0].text()
        except Exception as e:
            msg = 'Please select a Tension\n'
        return msg

    def check_checkboxes(self):
        msg = ''
        test = self.notebox_32.isChecked() or self.notebox_16.isChecked() or self.notebox_8.isChecked() or \
               self.notebox_4.isChecked() or self.notebox_2.isChecked() or self.notebox_1.isChecked()

        if not test:
            msg = 'Please check some note boxes\n'
        if self.notebox_chord.isChecked() and not test:
            msg = 'Please check other boxes along with "Chord"'
        return msg

    def check_spinboxes(self):
        msg = ''
        test = self.spinbox_chord.value()
        test += self.spinbox_32.value()
        test += self.spinbox_16.value()
        test += self.spinbox_8.value()
        test += self.spinbox_4.value()
        test += self.spinbox_2.value()
        test += self.spinbox_1.value()
        if test == 0:
            msg = 'Please fill in some note occurrences (positive numbers)\n'
        return msg

    def check_seedbox_field(self):
        msg = ''
        if self.seedtextbox.text() == '':
            msg = 'Please fill in a Seed (A positive #)\n'
        return msg

    def check_bpmeasure_field(self):
        msg = ''
        try:
            test = self.spinbox_bpmeasure.value()
        except Exception as e:
            msg = 'Please fill in "Beats Per Measure" (A positive #)\n'
        return msg

    def check_bpminute_field(self):
        msg = ''
        try:
            test = self.spinbox_bpminute.value()
        except Exception as e:
            msg = 'Please fill in "Beats Per Minute" (A positive #)\n'
        return msg

    # verify all fields have data, or show user
    def check_fields(self):
        msg = self.check_key_field() + self.check_tension_field() + self.check_checkboxes() + \
              self.check_spinboxes() + self.check_seedbox_field() + self.check_bpmeasure_field() + \
              self.check_bpminute_field()
        return msg

    # get all the note hold durations from user's selections
    def get_durations(self):
        _chord = [.0 for x in range(self.spinbox_chord.value())] if self.notebox_chord.isChecked() else []
        _32nd = [.125 for x in range(self.spinbox_32.value())] if self.notebox_32.isChecked() else []
        _16th = [.25 for x in range(self.spinbox_16.value())] if self.notebox_16.isChecked() else []
        _8th = [.5 for x in range(self.spinbox_8.value())] if self.notebox_8.isChecked() else []  # eighth notes
        _4s = [1 for x in range(self.spinbox_4.value())] if self.notebox_4.isChecked() else []  # quarter notes
        _2s = [2 for x in range(self.spinbox_2.value())] if self.notebox_2.isChecked() else []  # half notes
        _1s = [4 for x in range(self.spinbox_1.value())] if self.notebox_1.isChecked() else []  # whole notes
        ret = _chord + _32nd + _16th + _8th + _4s + _2s + _1s
        return ret

    # Assign all user fields
    def get_fields(self):
        self.key = self.keywidget.selectedItems()[0].text()
        self.tension = self.tensionwidget.selectedItems()[0].text()
        self.durations = self.get_durations()
        self.seed = self.seedtextbox.text()
        self.beatspermeasure = self.spinbox_bpmeasure.value()
        self.beatsperminute = self.spinbox_bpminute.value()

    # Reset all user fields
    def reset_fields(self):
        self.keywidget.clearSelection()
        self.tensionwidget.clearSelection()
        self.notebox_chord.setChecked(False)
        self.notebox_32.setChecked(False)
        self.notebox_16.setChecked(False)
        self.notebox_8.setChecked(False)
        self.notebox_4.setChecked(False)
        self.notebox_2.setChecked(False)
        self.notebox_1.setChecked(False)
        self.spinbox_chord.setValue(0)
        self.spinbox_32.setValue(0)
        self.spinbox_16.setValue(0)
        self.spinbox_8.setValue(0)
        self.spinbox_4.setValue(0)
        self.spinbox_2.setValue(0)
        self.spinbox_1.setValue(0)
        self.seedtextbox.setText('')

    # Randomize all user fields
    def random_fields(self):
        # Randomize a listwidget's selection. This was hard to figure out!
        self.keywidget.setCurrentRow(random.randint(0, self.keywidget.count() - 1))
        self.tensionwidget.setCurrentRow(random.randint(0, self.tensionwidget.count() - 1))

        # Nifty way of only setting a random it if the checkbox is checked.
        self.notebox_chord.setChecked(bool(random.getrandbits(1)))
        if self.notebox_chord.isChecked():
            self.spinbox_chord.setValue(random.randint(1, 8))
        else:
            self.spinbox_chord.setValue(0)

        self.notebox_32.setChecked(bool(random.getrandbits(1)))
        if self.notebox_32.isChecked():
            self.spinbox_32.setValue(random.randint(1, 8))
        else:
            self.spinbox_32.setValue(0)

        self.notebox_16.setChecked(bool(random.getrandbits(1)))
        if self.notebox_16.isChecked():
            self.spinbox_16.setValue(random.randint(1, 8))
        else:
            self.spinbox_16.setValue(0)

        self.notebox_8.setChecked(bool(random.getrandbits(1)))
        if self.notebox_8.isChecked():
            self.spinbox_8.setValue(random.randint(1, 8))
        else:
            self.spinbox_8.setValue(0)

        self.notebox_4.setChecked(bool(random.getrandbits(1)))
        if self.notebox_4.isChecked():
            self.spinbox_4.setValue(random.randint(1, 8))
        else:
            self.spinbox_4.setValue(0)

        self.notebox_2.setChecked(bool(random.getrandbits(1)))
        if self.notebox_2.isChecked():
            self.spinbox_2.setValue(random.randint(1, 8))
        else:
            self.spinbox_2.setValue(0)

        self.notebox_1.setChecked(bool(random.getrandbits(1)))
        if self.notebox_1.isChecked():
            self.spinbox_1.setValue(random.randint(1, 8))
        else:
            self.spinbox_1.setValue(0)

        self.random_seed()

        self.spinbox_bpmeasure.setValue(random.choice([2, 3, 4, 6, 8, 12, 16]))

        # BPM not implemented yet.
        self.spinbox_bpminute.setValue(
            random.choice([60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220]))

    # Make a measure with the given data
    def new_measure(self):
        # Check the data and pass error to the user
        msg = self.check_fields()
        if msg:
            w1 = QtWidgets.QMessageBox()
            w1.setFixedSize(500, 200)
            w1.setWindowTitle('Error')
            w1.setText(msg)
            w1.exec()
            return
        # Update the fields on-generate
        self.get_fields()

        # Create our scale
        self.makescale()

        # Create our note times from the durations
        self.make_notetimes()

        # Prevents similar stacked note durations at either end of measure
        random.shuffle(self.note_times)

        # Make our measure!
        self.makemeasure()

        # Display the measure on the screen
        self.show_measure()

    # Remove the measure at the iterator's position
    def delete_measure(self):  # TODO
        self.song_iterator.remove()
        self.show_measure()

    # Adds the last generated measure to the song at the iterator's position
    def insert_new_measure(self):  # TODO
        self.song_iterator.insert((self.thismeasure, self.note_times))

    # Display the measure to the output label (WIP)
    def show_measure(self):
        self.outputlabel.setText('')
        self.outputlabel.setAlignment(QtCore.Qt.AlignLeft)
        measure_note_str = '\t'.join([str(intref[i]) for i in self.thismeasure])
        measure_duration_str = '\t'.join([str(i) for i in self.note_times])
        self.outputlabel.setText(measure_note_str + '\n' + measure_duration_str)

    # Move the iterator next by one, return the result to the display
    def forward_measure(self):  # TODO
        self.song_iterator.next()
        self.show_measure()

    # Move the iterator back by one, return the result to the display
    def back_measure(self):  # TODO
        self.song_iterator.prev()
        self.show_measure()

    # Play the song. (MIDI would be better but it's more complicated than WAVs for now)
    def play_song(self):  # TODO
        pass

    # saves song to file
    def savesong(self):  # TODO
        try:

            qf = QtWidgets.QFileDialog(self)
            qf.setDefaultSuffix('.txt')
            qf.selectNameFilter("Midi files (*.mid)")
            filename = ''.join(qf.getSaveFileName())
            print(filename)
            savefolder = "./songs/"
            filepath = savefolder + filename
            running_time = 0.0
            for note, note_length in zip(self.song):
                running_time += note_length
                MyMIDI.addTempo(track=0, time=0, tempo=self.beatsperminute)
                MyMIDI.addNote(track=0, channel=0, time=running_time, duration=note_length, volume=100)
            if not os.path.isdir(savefolder):
                os.makedirs(savefolder)
            with open(filepath + '.mid', 'wb') as output_file:
                MyMIDI.writeFile(output_file)
            return
        except Exception as e:
            print(e)

    # get range difference between two notes
    def getrangecount(self, a, b):
        return abs(self.toneref[a] - self.toneref[b])

    # returns a scale of 16 notes, from the key tonic + 24
    def makescale(self):
        self.ourscale = []
        ouroffset = name_to_int_distance[self.key]

        keywheel = []
        if 'Major' == self.tension:
            keywheel = [0, 2, 2, 1, 2, 2, 2, 1]
        if 'Natural Minor' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 1, 2, 2]
        if 'Harmonic Minor' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 1, 3, 1]
        if 'Melodic Minor' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 2, 2, 2]
        if 'Dorian Mode' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 2, 1, 2]
        if 'Mixolydian Mode' == self.tension:
            keywheel = [0, 2, 2, 1, 2, 2, 1, 2]
        if 'Phrygian' == self.tension:
            keywheel = [0, 1, 3, 1, 2, 1, 2, 2]
        if 'Pentatonic' == self.tension:
            keywheel = [0, 2, 2, 3, 2, 3]
        if 'Minor Pentatonic' == self.tension:
            keywheel = [0, 3, 2, 2, 3, 2]
        filler = 0
        for note in range(self.note_range):
            filler += keywheel[note % len(keywheel)]
            self.ourscale.append(filler + ouroffset + self.starting_point)

    # Add random note lengths to an array until it equals beats per measure
    def make_notetimes(self):
        self.note_times = []
        while sum(self.note_times) < float(self.beatspermeasure):
            nexttime = random.choice(self.durations)
            self.note_times.append(nexttime)
            if sum(self.note_times) > float(self.beatspermeasure):
                del (self.note_times[-1])
                continue
            if sum(self.note_times) - float(self.beatspermeasure) > .001:
                return

    # Fills an n=#sleeps array with notes from that scale that hopefully travel well.
    def makemeasure(self):  # TODO
        self.thismeasure = []
        i = len(self.note_times)
        try:
            while i > 0:
                # add something to it if it's empty
                if len(self.thismeasure) == 0:
                    self.thismeasure.append(self.ourscale[0])
                    i -= 1
                lastnoteused = self.thismeasure[-1]

                # randomly choose a note from our scale
                nextjump = random.choice(self.ourscale)
                absjump = abs(nextjump - lastnoteused)

                # no jump higher than 10, no minor 5th"
                # not a minor second or second away in a chord
                # not the same exact note twice together in a chord
                if (absjump >= 10 or absjump == 6) or \
                        ((absjump == 2 or absjump == 1) and self.note_times[i] < 0.01) or \
                        (abs(absjump - lastnoteused == lastnoteused) and self.note_times[i] < 0.01):
                    continue
                else:
                    self.thismeasure.append(nextjump)
                    i -= 1
        except Exception as e:
            print(e)

        # print('{} {}'.format(len(self.thismeasure), len(self.note_times)))

    def playmeasure(self):  # TODO
        print()
        try:
            for note, sleep in zip(self.thismeasure, self.note_times):
                self.playnote(note, sleep)
        except Exception as e:
            print(e)

    # plays a single note by integer value
    def playnote(self, noteint, sleeptime):
        # make a list of all files in the directory
        if sys.platform in ('posix', 'linux', 'linux2'):
            subprocess.Popen(['aplay', '-q', 'wav/' + str(self.thismeasure[noteint])])
        if sys.platform in ('win32', 'win64', 'windows'):
            s = mixer.Sound(("wav/" + str(noteint) + '.wav'))
            s.play()
        sleep(sleeptime)

    # plays a song file
    def playsongfile(self):  # TODO
        for measure in self.song:
            self.playmeasure()


def main():
    app = QApplication(sys.argv)
    form = PyMusicGen()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
