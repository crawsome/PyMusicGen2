import random
import sys
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
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


class TwoWayIterator: # TODO make simpler / write tests
    def __init__(self, ourlist: list):
        self.index = 0
        self.element = None
        self.ourlist = ourlist

    def insert(self, element):
        self.ourlist.insert(self.index, element)

    def remove(self):
        if len(self.ourlist) > 1:
            del (self.ourlist[self.index])
            self.index -= 1

    def next(self):
        if self.index + 1 < len(self.ourlist):
            self.index += 1
        self.element = self.ourlist[self.index]
        return self.element

    def prev(self):
        if self.index - 1 > 0:
            self.index -= 1
        self.element = self.ourlist[self.index]
        return self.element

    def get_element(self):
        return self.element

class PyMusicGen(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyMusicGen, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Music Generator, 2020 Colin Burke')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # Directory where piano note wav files are stored
        self.wavdir = 'wav/'

        # piano settings
        self.starting_point = 60  # (middle C)
        self.note_range = 16  # 2 octaves of travel room
        self.c1 = 24

        # from the "Open" menu
        self.save_file_name = ''

        # From GUI Selections
        self.key = None
        self.tension = None
        # list of note lengths
        self.durations = []
        # list of this measure's note lengths
        self.thisnote_times = []

        self.seed = None
        self.random_seed()
        self.beatspermeasure = None
        self.beatsperminute = None  # Not implemented yet, or maybe not ever (MIDI ideal replacement)

        # Generated using methods below
        self.ourscale = []
        self.thismeasure = []  # filled with note objects
        self.song = []  # filed with measures
        self.song_iterator = TwoWayIterator(self.song)  # For CRUD operations

        self.imagelabel = QtWidgets.QLabel

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
        self.actionSave_Song.triggered.connect(self.save_song)
        self.actionAbout.triggered.connect(self.about_menu_window)
        self.actionExport_to_MIDI.triggered.connect(self.export_to_midi)
        self.actionQuit.triggered.connect(self.quit)

    def quit(self):
        sys.exit(self)

    def aboutmenu(self):
        self.popup_window()

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

    def check_measureintegrity(self):
        lm = len(self.thismeasure)
        lt = len(self.thisnote_times)
        if lt != lm:
            print('{} {} measure lengths not equal!'.format(lt, lm))

        if lt + lm == 0:
            print('{} {} both measures are empty!'.format(lt, lm))

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
        _8th = [.5 for x in range(self.spinbox_8.value())] if self.notebox_8.isChecked() else []  # eighth
        _4s = [1 for x in range(self.spinbox_4.value())] if self.notebox_4.isChecked() else []  # quarter
        _2s = [2 for x in range(self.spinbox_2.value())] if self.notebox_2.isChecked() else []  # half
        _1s = [4 for x in range(self.spinbox_1.value())] if self.notebox_1.isChecked() else []  # whole
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

        # prevents none from being checked
        nonechecked = True

        # Nifty way of only setting a random it if the checkbox is checked.
        self.notebox_chord.setChecked(bool(random.getrandbits(1)))
        if self.notebox_chord.isChecked():
            self.spinbox_chord.setValue(random.randint(1, 4))
            nonechecked = False
        else:
            self.spinbox_chord.setValue(0)

        self.notebox_32.setChecked(bool(random.getrandbits(1)))
        if self.notebox_32.isChecked():
            self.spinbox_32.setValue(random.randint(1, 4))
            nonechecked = False
        else:
            self.spinbox_32.setValue(0)

        self.notebox_16.setChecked(bool(random.getrandbits(1)))
        if self.notebox_16.isChecked():
            self.spinbox_16.setValue(random.randint(1, 8))
            nonechecked = False
        else:
            self.spinbox_16.setValue(0)

        self.notebox_8.setChecked(bool(random.getrandbits(1)))
        if self.notebox_8.isChecked():
            self.spinbox_8.setValue(random.randint(1, 8))
            nonechecked = False
        else:
            self.spinbox_8.setValue(0)

        self.notebox_4.setChecked(bool(random.getrandbits(1)))
        if self.notebox_4.isChecked():
            self.spinbox_4.setValue(random.randint(1, 8))
            nonechecked = False
        else:
            self.spinbox_4.setValue(0)

        self.notebox_2.setChecked(bool(random.getrandbits(1)))
        if self.notebox_2.isChecked():
            self.spinbox_2.setValue(random.randint(1, 3))
            nonechecked = False
        else:
            self.spinbox_2.setValue(0)

        self.notebox_1.setChecked(bool(random.getrandbits(1)))
        if self.notebox_1.isChecked():
            self.spinbox_1.setValue(random.randint(1, 2))
            nonechecked = False
        else:
            self.spinbox_1.setValue(0)

        if nonechecked:
            self.random_fields()

        self.random_seed()

        self.spinbox_bpmeasure.setValue(random.choice([3, 4, 6, 8, 12, 16]))

        # BPM not implemented yet.
        self.spinbox_bpminute.setValue(
            random.choice([60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220]))

    # Menu popup for the About menu
    def about_menu_window(self):
        gl = QtWidgets.QGridLayout()
        gb = QtWidgets.QGroupBox()

        self.imagelabel = QtWidgets.QLabel
        pixmap = QtGui.QPixmap('about.bmp')
        self.imagelabel.setPixmap(pixmap)
        gl.addItem(self.imagelabel)
        #self.imagelabel.show()

    # Generic popup info window
    def popup_window(self, msg: str, title='INFO'):
        w1 = QtWidgets.QMessageBox()
        w1.setFixedSize(500, 200)
        w1.setWindowTitle('Error')
        w1.setText(msg)
        w1.exec()
        return

    # Reusable y/n window that returns a bool
    def yesno_window(self,txt='Confirm?'):
        qm = QtWidgets.QMessageBox
        prompt = txt
        ret = qm.question(self, '', prompt, qm.Yes | qm.No)
        if ret == qm.Yes:
            return True
        else:
            return False
    # Make a measure with the given data
    def new_measure(self):
        # Check the data and pass error to the user
        msg = None
        try:
            msg = self.check_fields()
        except Exception as e:
            print('check_fields() failed ' + str(e))

        if msg:
            self.popup_window(msg)
            return

        # Update the fields on-generate
        try:
            self.get_fields()
        except Exception as e:
            print('get_fields() failed ' + str(e))

        # Create our scale
        try:
            self.makescale()
        except Exception as e:
            print('makescale() failed ' + str(e))

        # Create our note times from the durations
        try:
            self.make_notetimes()
        except Exception as e:
            print('make_notetimes() failed ' + str(e))

        # Prevents similar stacked note durations at either end of measure
        random.shuffle(self.thisnote_times)

        try:
            # Make our measure!
            self.make_measurenotes()
        except Exception as e:
            print('make_measurenotes() failed ' + str(e))

        self.check_measureintegrity()

        # Display the measure on the screen
        try:
            self.show_measure()
        except Exception as e:
            print('{} {}'.format(self.thismeasure, len(self.thismeasure)))
            print('{} {} \n{}'.format(self.thisnote_times, len(self.thisnote_times),
                                      (str(sum(self.thisnote_times)) + 'should equal' + str(self.beatspermeasure))))
            print('show measure failed ' + str(e))

    # Remove the measure at the iterator's position
    def delete_measure(self):  # TODO
        if self.yesno_window('Delete? Are you sure?'):
            self.song_iterator.remove()
        self.show_measure()

    # Adds the last generated measure to the song at the iterator's position
    def insert_new_measure(self):  # TODO
        print('Before: {}'.format(self.song))
        self.song_iterator.insert([self.thismeasure, self.thisnote_times])
        self.popup_window('Measure successfully inserted. Song is {} measures long'.format(len(self.song)))
        print('After: {}'.format(self.song))

    # Display the measure to the output label (WIP)
    def show_measure(self):
        self.outputlabel.setText('')
        self.outputlabel.setAlignment(QtCore.Qt.AlignLeft)
        try:
            measure_note_str = '\t'.join([str(intref[i - self.c1]) for i in self.thismeasure])
        except Exception as e:
            print(self.thismeasure)
            print('measure_note_str failed ' + str(e))

        try:
            measure_duration_str = '\t'.join([str(i) for i in self.thisnote_times])
        except Exception as e:
            print('measure_duration_str failed ' + str(e))

        try:
            self.outputlabel.setText(measure_note_str + '\n' + measure_duration_str)
        except Exception as e:
            print('outputlabel.setText failed ' + str(e))

    # Move the iterator next by one, return the result to the display
    def forward_measure(self):  # TODO
        if self.thismeasure == self.song_iterator.get_element():
            print('its ok, no need to check for save')
        else:
            if self.yesno_window('Insert your measure before moving?'):
                self.insert_new_measure()
        self.song_iterator.next()
        self.show_measure()

    # Move the iterator back by one, return the result to the display
    def back_measure(self):  # TODO
        if self.yesno_window('Insert your measure before moving?'):
            self.insert_new_measure()
        self.song_iterator.prev()
        self.show_measure()

    # Play the song. (MIDI would be better but it's more complicated than WAVs for now)
    def play_song(self):  # TODO
        pass

    # saves song to file
    def save_song(self):
        filename = ''
        try:
            qf = QtWidgets.QFileDialog(self)
            # Make the file save as a .midi
            filename = qf.getSaveFileName(None, 'Save Song as Midi', '', 'Midi Files (*.mid)')[0]

            # filename = qf.getSaveFileName()[0].replace('.mid', '')  # Just in case the user writes in .mid manually
        except Exception as e:
            print('save GUI failed ' + str(e))
            quit()
        running_time = 0.0
        try:
            MyMIDI.addTempo(track=0, time=0, tempo=self.beatsperminute)
            for measure in self.song:
                for note, note_length in zip(*measure):
                    MyMIDI.addNote(track=0, channel=0, pitch=note, time=running_time, duration=note_length, volume=100)
                    running_time += note_length
        except Exception as e:
            print('failed to parse midi metadata' + str(e))

        try:
            with open(filename, 'wb') as output_file:
                MyMIDI.writeFile(output_file)
        except Exception as e:
            print('failed to save file' + str(e))
        return

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
        self.thisnote_times = []
        while float(sum(self.thisnote_times)) < float(self.beatspermeasure):

            nexttime = random.choice(self.durations)
            self.thisnote_times.append(nexttime)
            if sum(self.thisnote_times) > float(self.beatspermeasure):
                del (self.thisnote_times[-1])
                continue
            if sum(self.thisnote_times) - float(self.beatspermeasure) > .001:
                return

    # Fills an n=#sleeps array with notes from that scale that hopefully travel well.
    def make_measurenotes(self):
        self.thismeasure = []
        i = len(self.thisnote_times)
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
                    ((absjump == 2 or absjump == 1) and self.thisnote_times[i] < 0.01) or \
                    (abs(absjump - lastnoteused == lastnoteused) and self.thisnote_times[i] < 0.01):
                continue
            else:
                self.thismeasure.append(nextjump)
                i -= 1

        # print('{} {}'.format(len(self.thismeasure), len(self.thisnote_times)))

    # plays a song file
    def playsongfile(self):
        for measure in self.song:
            self.playmeasure()

    def playmeasure(self):  # TODO
        print()
        try:
            for note, sleep in zip(self.thismeasure, self.thisnote_times):
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




def main():
    app = QApplication(sys.argv)
    form = PyMusicGen()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
