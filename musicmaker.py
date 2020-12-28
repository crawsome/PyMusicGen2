import os
import random
import subprocess
import sys
from time import sleep

from pygame import mixer

mixer.init()

# Return array that is rotated circular
def rotate(l, n):
    return l[-n:] + l[:-n]


# Compare two floats against an error returns TRUE if both floats are ~=
def floatequal(l, r):
    return abs(l - r) < .01


class MusicMaker:
    def __init__(self, key='C', tension='Major', durations=(.5, .25, 0), seed=1, beatspermeasure=8, beatsperminute=80):
        # static
        self.STARTINGPOINT = 24  # starting point on keyboard
        self.NOTERANGE = 16  # of notes we use (2 octaves of key notes)

        # Given
        self.wavs = next(os.walk("wav/"))[2]
        self.key = key
        self.tension = tension
        self.durations = []
        self.seed = []
        self.beatspermeasure = beatspermeasure
        self.beatsperminute = beatsperminute

        # Generated
        self.ourscale = []
        self.thismeasure = []
        self.song = []
        self.filename = ''
        self.wavdir = ''
        self.basicnotelist = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.name_to_int_base12 = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9,
                                   'Bb': 10, 'B': 11}
        self.name_to_int_distance = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': -6, 'G': -5, 'Ab': -4,
                                     'A': -3, 'Bb': -2, 'B': -1}
        self.int_distance = [0, 1, 2, 3, 4, 5, -6, -5, -4, -3, -2, -1]
        self.intref = ["C0", "Db0", "D0", "Eb0", "E0", "F0", "#0", "G0", "Ab0", "A0", "Bb0", "B0", "C1", "Db1", "D1",
                       "Eb1", "E1", "F1", "F#1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2", "Eb2", "E2", "F2",
                       "F#2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3", "Eb3", "E3", "F3", "F#3", "G3", "Ab3",
                       "A3", "Bb3", "B3", "C4", "Db4", "D4", "Eb4", "E4", "F4", "F#4", "G4", "Ab4", "A4", "Bb4", "B4",
                       "C5", "Db5", "D5", "Eb5", "E5", "F5", "F#5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6",
                       "Eb6", "E6", "F6", "F#6", "G6", "Ab6", "A6", "Bb6", "B6", "C7", "Db7", "D7", "Eb7", "E7", "F7",
                       "F#7", "G7", "Ab7", "A7", "Bb7", "B7", "C8"]
        self.toneref = {"C0": 0, "Db0": 1, "D0": 2, "Eb0": 3, "E0": 4, "F0": 5, "F#0": 6, "G0": 7, "Ab0": 8, "A0": 9,
                        "Bb0": 10, "B0": 11, "C1": 12, "Db1": 13, "D1": 14, "Eb1": 15, "E1": 16, "F1": 17, "F#1": 18,
                        "G1": 19, "Ab1": 20, "A1": 21, "Bb1": 22, "B1": 23, "C2": 24, "Db2": 25, "D2": 26, "Eb2": 27,
                        "E2": 28, "F2": 29, "F#2": 30, "G2": 31, "Ab2": 32, "A2": 33, "Bb2": 34, "B2": 35, "C3": 36,
                        "Db3": 37, "D3": 38, "Eb3": 39, "E3": 40, "F3": 41, "F#3": 42, "G3": 43, "Ab3": 44, "A3": 45,
                        "Bb3": 46, "B3": 47, "C4": 48, "Db4": 49, "D4": 50, "Eb4": 51, "E4": 52, "F4": 53, "F#4": 54,
                        "G4": 55, "Ab4": 56, "A4": 57, "Bb4": 58, "B4": 59, "C5": 60, "Db5": 61, "D5": 62, "Eb5": 63,
                        "E5": 64, "F5": 65, "F#5": 66, "G5": 67, "Ab5": 68, "A5": 69, "Bb5": 70, "B5": 71, "C6": 72,
                        "Db6": 73, "D6": 74, "Eb6": 75, "E6": 76, "F6": 77, "F#6": 78, "G6": 79, "Ab6": 80, "A6": 81,
                        "Bb6": 82, "B6": 83, "C7": 84, "Db7": 85, "D7": 86, "Eb7": 87, "E7": 88, "F7": 89, "F#7": 90,
                        "G7": 91, "Ab7": 92, "A7": 93, "Bb7": 94, "B7": 95, "C8": 96}

    # get range difference between two notes
    def getrangecount(self, a, b):
        return abs(self.toneref[a] - self.toneref[b])

    # returns a scale of 16 notes, from the key tonic + 24
    def makescale(self):
        ouroffset = self.name_to_int_distance[self.key]
        keywheel = []
        if 'Major' == self.tension:
            keywheel = [0, 2, 2, 1, 2, 2, 2, 1]
        if 'Natural Minor ' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 1, 2, 2]
        if 'Harmonic Minor' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 1, 3, 1]
        if 'Melodic' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 2, 2, 2]
        if 'Dorian' == self.tension:
            keywheel = [0, 2, 1, 2, 2, 2, 1, 2]
        if 'Mixolydian' == self.tension:
            keywheel = [0, 2, 2, 1, 2, 2, 1, 2]
        if 'Phrygian' == self.tension:
            keywheel = [0, 1, 3, 1, 2, 1, 2, 2]
        if 'Minor Pentatonic' == self.tension:
            keywheel = [0, 3, 2, 2, 3, 2]
        if 'Pentatonic' == self.tension:
            keywheel = [0, 2, 2, 3, 2, 3]
        filler = 0
        for note in range(self.NOTERANGE):
            filler += keywheel[note % len(keywheel)]
            self.ourscale.append(filler + ouroffset + self.STARTINGPOINT)

    # Makes a random quantity of rests to fill in a measure.
    # Results may vary, and the end of the measure is more likely to have
    # a higher amount of notes.
    def makedurations(self):
        times = [0.0, 0.0, .25, .25, .5, .5, 1.0, 1.0]
        while abs(sum(self.durations) - float(self.beatspermeasure)) > .001:
            nexttime = random.choice(times)
            self.durations.append(nexttime)
            if abs(nexttime - self.durations[-1]) < .01:
                del self.durations[-1]
                nexttime = random.choice(times)
                self.durations.append(nexttime)
            if sum(self.durations) - float(self.beatspermeasure) > .2:
                del self.durations[-1]
                continue
            if sum(self.durations) - float(self.beatspermeasure) < .1:
                continue

    # Fills an n=#sleeps array with notes from that scale that hopefully travel well.
    def makemeasure(self):
        for sleeps in self.durations:
            success = True
            while not success:
                # add something to it if it's empty
                if not self.thismeasure:
                    self.thismeasure.append(random.choice(self.ourscale))

                # This step adds the root note to the end of the measure.
                lastnote = self.thismeasure[-1]

                # randomly choose a note from our scale
                nextjump = random.choice(self.ourscale)
                absjump = abs(nextjump - lastnote)

                # no jump higher than 10, no minor 5th"
                # not a minor second or second away in a chord
                # not the same exact note twice together in a chord
                if (absjump >= 10 or absjump == 6) or \
                        ((absjump == 2 or absjump == 1) and sleeps < 0.01) or \
                        (abs(absjump - lastnote == lastnote) and sleeps < 0.01):
                    success = False

                if success:
                    print("success with %s" % (nextjump))
                    self.thismeasure.append(nextjump)
                    print(self.thismeasure)
                    break

    def playmeasure(self):

        for notes, sleeps in zip(self.thismeasure):
            print("note: %s" % (self.intref[notes]))
            print("sleep time: %f seconds\n" % sleeps)
            self.playnote(notes, sleeps)
        keep = str(input("keep this measure? y/n? \n"))

    # plays a single note by integer value
    def playnote(self, noteint, sleeptime):
        # make a list of all files in the directory
        if sys.platform in ('posix', 'linux', 'linux2'):
            subprocess.Popen(['aplay', '-q', 'wav/' + str(self.thismeasure[noteint])])
        if sys.platform in ('win32', 'win64', 'windows'):
            s = mixer.Sound(("wav/" + str(self.thismeasure[noteint])))
            s.play()
        sleep(sleeptime)

    # plays a single note by filename
    def playnotefile(self, filename, sleeptime):
        subprocess.Popen(['aplay', '-q', 'wav/' + filename])
        sleep(sleeptime)

    # plays a song file
    def playsongfile(self, keyinfodict, oursong):
        ourseeds = keyinfodict["ourseeds"]
        for seed, measure in zip(ourseeds, oursong):
            print("seed: %d" % seed)
            print(*measure)
            for notes, times in zip(*measure):
                self.playnote(notes, times)
