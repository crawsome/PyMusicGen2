# MusicGenerator
Music generator made in Python and QT. 

## Quickstart
1. Click "Randomize"
2. Click "Generate"
3. Click "Play measure"
4. More directions to come as I develop the rest of the GUI

## Manual Use
### Select a Key
Select a Key in the **Key** list. 

### Select a Tension
Select a Tension in the **Tension** list. 

### Select Note Occurences. 
(This process will be improved over time.)
When you check a checkbox and enter a number. This will be the **chance of occurence** in the song of that note type. 
So if you choose 2 on Quarter notes, and 2 on Half notes, there will be a 50/50 chance of each appearing in the song.
It fills up an array of sleep values that correspond to your selections, and the song will use those sleep values as the song's rhythm.

#### Chords Checkbox
**NOTE:** If you include "Chords", you must combine it with other notes. Reason being, chords area played with the last note, at a sleep value of 0.0, and 0s cannot fill a measure of times. 

### Enter a Seed
This determines the "random" number generators deterministic pattern in Python. 

### Define the Beats Per Measure
This determines how many notes can fit in your measure

## Define the Beats Per Minute (Midi Only)
When you outout to MIDI, this value will be the tempo of the song. 
[Contribute](https://colinburke.com/contribute), so I can dedicate more time to projects like this.
