# All our relationship / music notation junk
from musicstructs import *
from dataclasses import dataclass
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from window import Ui_MainWindow
from midiutil import MIDIFile
from time import sleep
from pygame import mixer
import os
import random
import sys
import logging
import datetime as dt

dt_date = str(dt.datetime.now().date())
dt_sec = str(dt.datetime.now().time().second)
dt_min = str(dt.datetime.now().time().minute)
dt_hr = str(dt.datetime.now().time().hour)
file_name = '{}-{}-{}-{}'.format(dt_date, dt_hr, dt_min, dt_sec)

drum_range_low = 'A1'
drum_range_height = 'F4'

LOGGING = False
if not os.path.exists('./logs'):
    os.mkdir('./logs')

if LOGGING:
    logging.basicConfig(filename='logs/{}.log'.format(file_name), level=logging.DEBUG)

# Init pygame audio mixer
mixer.init()
mixer.set_num_channels(64)

# init MyMidi
MyMIDI = MIDIFile(1)


# Return array that is rotated circular

def rotate(l, n):
    return l[-n:] + l[:-n]


# Compare two floats against an error returns TRUE if both floats are ~=
def floatequal(l, r, precision=.01):
    return abs(l - r) < precision


@dataclass
class MidiNote:
    def __init__(self, track: int = 0, channel: int = 0, pitch: int = 60, time: float = 1, duration: float = 1,
                 volume: int = 100):
        self.track: int = track
        self.channel: int = channel
        self.pitch: int = pitch
        self.time: float = time
        self.duration: float = duration
        self.volume: int = volume


class Song:
    def __init__(self):
        self.name = ''
        self.measures = []

# TODO: Split into two objects. Music / GUI stuff.
class PyMusicGen(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyMusicGen, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Music Generator, 2020 Colin Burke')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # Directory where piano note wav files are stored
        self.wavdir = 'wav/'

        # piano settings
        self.starting_point = 60  # Default: 60 (middle C)
        self.note_range = 24  # Default: 16 (2 octaves of travel room)
        self.c1 = 24  # Used for relative calculation to MIDI integer range

        # from the "Open" menu
        self.save_file_name = ''

        # From GUI Selections
        self.key = None
        self.tension = None
        self.durations = []

        # seed for random (Set to something for testing)
        self.seed = None
        self.random_seed()

        self.beatspermeasure = None
        self.beatsperminute = None

        # Generated using methods below
        self.ourscale = []

        self.thismeasure_notes = []  # filled with note int objects
        self.thismeasure_times = []  # filled with sleep float objects
        self.song_index = 0

        self.thismeasure = {'notes': self.thismeasure_notes, 'times': self.thismeasure_times}

        self.song = Song()  # filed with measures

        # Inserting and moving by-measure in the song
        self.selected_measure = None  # used for iteration in the song
        self.measure_index = 0  # used for iteration in the song

        # Connect functions with gui elements
        self.generatebutton.clicked.connect(self.new_measure)
        self.randomseedbutton.clicked.connect(self.random_seed)
        self.resetsettingsbutton.clicked.connect(self.reset_fields)
        self.randomsettingsbutton.clicked.connect(self.random_fields)

        # Song Control
        self.forwardbutton.clicked.connect(self.forward_measure)
        self.backbutton.clicked.connect(self.back_measure)
        self.deletebutton.clicked.connect(self.delete_measure)
        self.insertbutton.clicked.connect(self.insert_new_measure)
        self.playbutton.clicked.connect(self.play_song)
        self.playmeasurebutton.clicked.connect(self.play_current_measure)

        # Menu Options
        self.actionNew_Song.triggered.connect(self.new_song)
        self.actionSave_Song.triggered.connect(self.save_song)
        self.actionAbout.triggered.connect(self.about_menu_window)
        self.actionExport_to_MIDI.triggered.connect(self.export_to_midi)
        self.actionQuit.triggered.connect(self.quit)

    """Output Methods"""

    # Display the measure to the output label (WIP)
    def show_measure(self, blank=False):
        self.outputlabel.setText('')
        self.outputlabel.setAlignment(QtCore.Qt.AlignLeft)
        measure_note_str = 'Position: {} / Length: {}\n\n'.format(self.song_index + 1, len(self.song.measures))
        if blank:
            self.outputlabel.setText(measure_note_str)
            return

        try:
            measure_note_str += '\t'.join([str(intref[i - self.c1]) for i in self.thismeasure_notes])
        except Exception as e:
            logging.exception('measure_note_str failed ' + str(e))
            logging.exception(self.thismeasure_notes)

        try:
            measure_duration_str = '\t'.join([timeref[i] for i in self.thismeasure_times])
        except Exception as e:
            logging.exception('measure_duration_str failed ' + str(e))

        try:
            self.outputlabel.setText(measure_note_str + '\n' + measure_duration_str)
        except Exception as e:
            logging.exception('outputlabel.setText failed ' + str(e))

    # saves song to file
    def save_song(self):
        filename = ''
        try:
            # create our save file dialog
            qf = QtWidgets.QFileDialog(self)

            # Show user file dialog, Make the file save as a .midi
            filename = qf.getSaveFileName(None, 'Save Song as Midi', '', 'Midi Files (*.mid)')[0]

            if not filename:  # if they hit cancel
                return
        except Exception as e:
            logging.exception('save GUI failed: ' + str(e))

        try:
            MyMIDI.addTempo(track=0, time=0, tempo=self.beatsperminute)
            running_time = 0.0
            for measure in self.song.measures:
                for note, note_length in zip(*measure):
                    MyMIDI.addNote(track=0, channel=0, pitch=note, time=running_time, duration=note_length,
                                   volume=100)
                    running_time += note_length
        except Exception as e:
            logging.exception('failed to parse midi metadata: ' + str(e))

        try:
            with open(filename, 'wb') as output_file:
                MyMIDI.writeFile(output_file)
        except Exception as e:
            logging.exception('failed to save file: ' + str(e))
        return

    # saves song to pdf
    def export_to_pdf(self):  # TODO
        pass

    # saves song to wav
    def export_to_wav(self):  # TODO
        pass

    # saves song to file
    def export_to_midi(self):  # TODO
        pass

    """Play Methods"""

    # plays a song file
    def playsongfile(self):  # TODO
        for measure in self.song.measures:
            self.playmeasure(measure)

    # Plays a measure of notes
    def play_current_measure(self):  # TODO
        try:
            for note, duration in zip(self.thismeasure_notes, self.thismeasure_times):
                self.playnote(note, duration)
        except Exception as e:
            logging.exception(e)

    # plays a single note by integer value
    def playnote(self, noteint, sleeptime):
        # make a list of all files in the directory
        if sys.platform in ('posix', 'linux', 'linux2'):
            # subprocess.Popen(['aplay', '-q', 'wav/' + str(self.thismeasure_notes[noteint])])
            s = mixer.Sound(("wav/" + str(noteint) + '.wav'))
            s.play()
        if sys.platform in ('win32', 'win64', 'windows'):
            s = mixer.Sound(("wav/" + str(noteint) + '.wav'))
            s.play()
        sleep(sleeptime)

    """GUI Action Methods"""

    # get all the note hold durations from user's selections
    def get_durations(self):
        _chord = [.0 for x in range(self.spinbox_chord.value())] if self.notebox_chord.isChecked() else []  # chord
        _32nd = [.125 for x in range(self.spinbox_32.value())] if self.notebox_32.isChecked() else []  # 32nd
        _16th = [.25 for x in range(self.spinbox_16.value())] if self.notebox_16.isChecked() else []  # 16th
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
        random.seed(self.seed)
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

        self.spinbox_bpmeasure.setValue(random.choice([3, 4, 6, 8]))

        # BPM not implemented yet.
        self.spinbox_bpminute.setValue(
            random.choice([60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220]))

    # Menu popup for the About menu
    def about_menu_window(self):  # TODO GET IMAGE + TEXT WORKING
        gl = QtWidgets.QGridLayout()
        gb = QtWidgets.QGroupBox()

        imagelabel = QtWidgets.QLabel
        pixmap = QtGui.QPixmap('about.bmp')
        imagelabel.setPixmap(pixmap)
        gl.addItem(imagelabel)
        # self.imagelabel.show()

    # Generic popup info window
    def popup_window(self, msg='You didn\'t provide a message!', title='INFO'):
        qm = QtWidgets.QMessageBox()
        qm.setFixedSize(500, 200)
        qm.setWindowTitle(title)
        qm.setText(msg)
        qm.exec()
        return

    # Reusable y/n window that returns a bool
    def yesno_window(self, msg='Confirm?', title='INFO'):
        qm = QtWidgets.QMessageBox()
        qm.setWindowTitle(title)
        prompt = msg
        ret = qm.question(self, '', prompt, qm.Yes | qm.No)
        if ret == qm.Yes:
            return True
        else:
            return False

    # Quit the program
    def quit(self):
        sys.exit(self)

    """GUI Data Verification Methods
    These will return an error message to user if they are not checked.
    They are named literally and need no extra comments. 
    """

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

    # runs all the above at once
    def check_fields(self):
        msg = self.check_key_field() + self.check_tension_field() + self.check_checkboxes() + \
              self.check_spinboxes() + self.check_seedbox_field() + self.check_bpmeasure_field() + \
              self.check_bpminute_field()
        return msg

    # Music Theory

    # Song Control

    """Song Control Methods
    These methods are invoked by the user by pressing GUI buttons
    """

    # Move the iterator next by one, return the result to the display
    def forward_measure(self):  # TODO
        if self.song_index < len(self.song.measures) - 1:
            self.song_index += 1
            self.thismeasure = self.song.measures[self.song_index]
            self.thismeasure_notes, self.thismeasure_times = self.song.measures[self.song_index]
            self.show_measure()

    # Move the iterator back by one, return the result to the display
    def back_measure(self):  # TODO
        if self.song_index > 0:
            self.song_index -= 1
            self.thismeasure = self.song.measures[self.song_index]
            self.thismeasure_notes, self.thismeasure_times = self.song.measures[self.song_index]
            self.show_measure()

    # Play the song. (MIDI would be better but it's more complicated than WAVs for now)
    def play_song(self):  # TODO
        try:
            for measure in self.song.measures:
                self.thismeasure = measure
                self.thismeasure_notes = self.thismeasure[0]
                self.thismeasure_times = self.thismeasure[1]
                self.play_current_measure()
        except Exception as e:
            logging.exception(e)

    # Remove the measure at the iterator's position
    def delete_measure(self):  # TODO
        try:
            if self.yesno_window('Delete measure? Are you sure?'):
                if len(self.song.measures) > 0:
                    del self.song.measures[self.song_index]
                    if self.song_index > 0:
                        self.song_index -= 1
                    if len(self.song.measures) == 0:
                        self.show_measure(blank=True)
                        self.thismeasure_notes, self.thismeasure_times = [], []
                        return
                    logging.exception('reassigning vars')
                    self.thismeasure = self.song.measures[self.song_index]
                    self.thismeasure_notes, self.thismeasure_times = self.song.measures[self.song_index]
                self.show_measure()
        except Exception as e:
            logging.exception(self.song_index)
            logging.exception(e)

    # Adds the last generated measure to the song at the iterator's position
    def insert_new_measure(self):  # TODO
        try:
            if self.thismeasure_times == []:
                self.popup_window('Your measure is empty')
                return
            self.song.measures.insert(self.song_index, (self.thismeasure_notes, self.thismeasure_times))
            self.popup_window('Measure successfully inserted. Song is {} measures long'.format(len(self.song.measures)))
            self.show_measure()
        except Exception as e:
            logging.exception(e)

    """Song Creation Methods
    These methods are used during the measure creation process. 
    """

    # reinitialize the whole song object, basically start the program from scratch
    def new_song(self):  # TODO
        if self.yesno_window(title='Save your song?', msg='Save your song before making a new song?'):
            self.save_song()
        else:
            self.song = Song()
            self.show_measure(blank=True)
        pass

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

    # Fills an n=#sleeps array with notes from that scale that hopefully travel well.
    def make_measure(self):
        self.thismeasure_times = []
        while float(sum(self.thismeasure_times)) < float(self.beatspermeasure):
            nexttime = random.choice(self.durations)
            self.thismeasure_times.append(nexttime)
            if sum(self.thismeasure_times) > float(self.beatspermeasure):
                del (self.thismeasure_times[-1])
                continue
            if sum(self.thismeasure_times) - float(self.beatspermeasure) > .001:
                break
        random.shuffle(self.thismeasure_times)
        self.thismeasure_notes = []
        i = len(self.thismeasure_times)
        while i > 0:
            # add something to it if it's empty
            if len(self.thismeasure_notes) == 0:
                self.thismeasure_notes.append(self.ourscale[0])
                i -= 1
            lastnoteused = self.thismeasure_notes[-1]

            # randomly choose a note from our scale
            nextjump = random.choice(self.ourscale)

            # get the absolute value of the last note, and the next proposed note.
            absjump = abs(nextjump - lastnoteused)

            # Note selection rules:

            # not the same exact note twice together in a chord
            if (absjump >= 10 or absjump == 6):  # no jump higher than 10, no minor 5th"
                # logging.debug('Prevented jump more than >10, or =6')
                continue
            elif (absjump == 2 or absjump == 1) and self.thismeasure_times[i] < 0.01:  # no finger mashed chords
                # logging.debug('Prevented mashed next to each other')
                continue
            elif abs(absjump - lastnoteused) == lastnoteused and self.thismeasure_times[i] < 0.01:
                # logging.debug('Prevented layered note')
                continue
            else:
                self.thismeasure_notes.append(nextjump)
                i -= 1
        self.thismeasure = {'notes': self.thismeasure_notes, 'times': self.thismeasure_times}

    # sets a random seed for user
    def random_seed(self):
        self.seed = random.randint(0, sys.maxsize)
        random.seed(self.seed)
        self.seedtextbox.setText(str(self.seed))

    # Make a measure with the given data
    def new_measure(self):
        # Check the data and pass error to the user
        msg = None
        try:
            msg = self.check_fields()
        except Exception as e:
            logging.exception('check_fields() failed: ' + str(e))

        if msg:
            self.popup_window(msg)
            return

        # Update the fields on-generate
        try:
            self.get_fields()
        except Exception as e:
            logging.exception('get_fields() failed: ' + str(e))

        # Create our scale
        try:
            self.makescale()
        except Exception as e:
            logging.exception('makescale() failed: ' + str(e))

        # Create our note times from the durations
        try:
            self.make_measure()
        except Exception as e:
            logging.exception('make_notetimes() failed: ' + str(e))

        # Display the measure on the screen
        try:
            self.show_measure()
        except Exception as e:
            logging.exception('{} {}'.format(self.thismeasure_notes, len(self.thismeasure_notes)))
            logging.exception('{} {} \n{}'.format(self.thismeasure_times, len(self.thismeasure_times),
                                                  (str(sum(self.thismeasure_times)) + 'should equal' + str(
                                                      self.beatspermeasure))))
            logging.exception('show measure failed ' + str(e))

    # get range difference between two notes
    def getrangecount(self, a, b):
        return abs(self.toneref[a] - self.toneref[b])


def main():
    app = QApplication(sys.argv)
    form = PyMusicGen()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
