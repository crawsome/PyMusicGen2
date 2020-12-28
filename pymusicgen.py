import os
import pickle
import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from window import Ui_MainWindow


class TwoWayIterator:
    def __init__(self, ourlist):
        self.index = 0
        self.element = None
        self.ourlist = ourlist

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

class Note:
    def __init__(self):
        self.tone_int = 0
        self.duration = 0
        self.

class PyMusicGen(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyMusicGen, self).__init__(parent)
        self.setupUi(self)
        self.key = None
        self.tension = None
        self.occurences = []
        self.seed = None
        self.random_seed()
        self.beatspermeasure = None
        self.beatsperminute = None  # Not implemented yet, or maybe not ever (MIDI ideal replacement)
        self.measure = [] # filled with note objects
        self.song = [] #filed with measures
        self.generatebutton.clicked.connect(self.generate_measure)
        self.randomseedbutton.clicked.connect(self.random_seed)
        self.resetsettingsbutton.clicked.connect(self.reset_fields)
        self.randomsettingsbutton.clicked.connect(self.random_fields)

    def get_occurences(self):
        _chord = [0 for x in self._chord] if self.notebox_chord.isChecked() else None  # played with last note
        _32nd = [.125 for x in self._32nds] if self.notebox_32.isChecked() else None  # thirty-second notes
        _16th = [.25 for x in self._16ths] if self.notebox_16.isChecked() else None  # sixteenth notes
        _8th = [.5 for x in self._8ths] if self.notebox_8.isChecked() else None  # eighth notes
        _4s = [1 for x in self._4s] if self.notebox_4.isChecked() else None  # quarter notes
        _2s = [2 for x in self._2s] if self.notebox_2.isChecked() else None  # half notes
        _1s = [4 for x in self._1s] if self.notebox_1.isChecked() else None  # whole notes
        return {'_chords': _chord, '_32nds': _32nd, '_16ths': _16th, '_8ths': _8th, '_4s': _4s, '_2s': _2s,
                '_1s': _1s}

    def random_seed(self):
        self.seed = random.randint(0, sys.maxsize)
        self.seedtextbox.setText(str(self.seed))

    def check_fields(self):
        check = True
        msg = ''
        try:
            if not self.keywidget.selectedItems()[0].text():
                msg += 'Please select a Key\n'
                check = False
            if not self.keywidget.selectedItems()[0].text():
                msg += 'Please select a Tension\n'
                check = False
            if not (self.notebox_chord.isChecked() or self.notebox_16.isChecked() or self.notebox_8.isChecked() or self.notebox_4.isChecked() or self.notebox_2.isChecked() or self.notebox_1.isChecked()):
                msg += 'Please check some note boxes, and enter values\n'
                check = False
            if not (self.spinbox_chord.value() or self.spinbox_16.value() or self.spinbox_8.value() or self.spinbox_4.value() or self.spinbox_2.value() or self.spinbox_1.value()):
                msg += 'Please fill in a note occurrence (A positive #)\n'
                check = False
            if not self.seedtextbox.text():
                msg += 'Please fill in a Seed (A positive #)\n'
                check = False
            if not self.spinbox_bpmeasure.value():
                msg += 'Please fill in "Beats Per Measure" (A positive #)\n'
                check = False
            if not self.spinbox_bpminute.value():
                msg += 'Please fill in "Beats Per Minute" (A positive #)\n'
                check = False

        except Exception as e:
            check = False
            print(e)
        print(check)
        return check, msg

    #TODO
    def get_fields(self):
        self.key = self.keywidget.selectedItems()[0].text() if self.keywidget.selectedItems()[0].text() else None
        self.tension = self.tensionwidget.selectedItems()[0].text() if self.tensionwidget.selectedItems()[
            0].text() else None
        self.tension = self.get_occurences()
        # self.seed = self.seedtextbox.text()
        # self.beatspermeasure = self.spinbox_bpmeasure.value()
        # self.beatsperminute = self.spinbox_bpminute.value()
        # measuredata = {'key': self.key, 'tension': self.tension, 'occurences': self.occurences, 'seed': self.seed, 'beatspermeasure': self.beatspermeasure, 'beatsperminute': self.beatsperminute}

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

    def random_fields(self):
        # These two were hard to figure out!
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

    # Remove the measure at the iterator's position
    def delete_measure(self):
        pass

    # Adds the last generated measure to the song at the iterator's position
    def insert_new_measure(self):
        pass

    # Move the iterator next by one, return the result to the display
    def forward_measure(self):
        pass

    # Move the iterator back by one, return the result to the display
    def back_measure(self):
        pass

    # Use the algorithm to make a measure with the given data
    def generate_measure(self):
        if not self.check_fields():
            w1 = QtWidgets.QLabel()
            w1.text = "Please fill in all fields before generating a measure."
            w1.show()

        # self.get_fields()  # Update the data first
        # self.measure_iterator = OmniIter(self.measure)
        # self.measure_iterator.surroundings()

    # Play the song. (MIDI would be better but it's more complicated than WAVs for now)
    def play_song(self):
        pass

    # saves song to file
    def savesong(self, keyinfodict, oursong):
        filename = str(input("save as:"))
        savefolder = "./songs/"
        filepath = savefolder + filename
        if not os.path.isdir(savefolder):
            os.makedirs(savefolder)
        with open(filepath, 'wb') as f:
            pickle.dump([keyinfodict, oursong], f, -1)
        return


class MusicMaker:
    def __init__(self):
        self.ourscale = None
        self.key = None
        self.keywheel = []
        self.measures = []


def main():
    app = QApplication(sys.argv)
    form = PyMusicGen()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
