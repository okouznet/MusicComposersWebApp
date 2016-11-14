import wave
from mingus.containers import NoteContainer
from mingus.containers import Note
from mingus.containers import Track
from mingus.containers import Composition
from mingus.containers.instrument import Piano
from mingus.midi import midi_file_out
from mingus.midi import midi_file_in
#from mingus.midi import fluidsynth
import math

#keys = ["'C-4'", "'C#-4'", "'D-4'", "'D#-4'", "'E-4'", "'F-4'", "'F#-4'", "'G-4'", "'G#-4'", "'A-4'", "'A#-4'", "'B-4'"]
class PianoPlayer :
    #sound_file = "static/soundfront.SF2"

    def __init__(self):
        self.track = Track(Piano())
        #self.player = fluidsynth
        #self.player.init(self.sound_file)
        self.notes = []
        #initialize keys
        for i in range(48, 60):
            self.notes.append(i)
        self.matrix = {}
        for n in self.notes:
            i = int(n)
            self.matrix[i] = [0] * 10

    def addTrack(self, notes, duration=None):
        mingus_notes = []
        for n in notes:
            x = Note().from_int(n)
            print x
            mingus_notes.append(x)
        self.track.add_notes(mingus_notes, duration=duration)

    def playTrack(self, notes, duration=None):
        t = Track(Piano())
        for n in notes:
            t.add_notes(n, duration=duration)
        #self.player.play_Track(t);

    def clearTrack(self):
        self.track = Track(Piano())

    def saveTrack(self, filename):
        t = self.track
        path = "static/library/"
        file = path + filename + ".mid"
        #self.player.play_Track(t)
        midi_file_out.write_Track(file, t)


    def buildComposition(self, compose):
        c = Composition()
        count = 0
        #get components
        for track in compose:
            t = self.track
            for bar in track:
                for info in bar:
                    #get note information and duration
                    t.add_notes(info[2], duration=info[1])
                    count = round(count + info[0], 2)
            c.add_track(t)

        return c, count

    def add_file(self, filename):
        file = midi_file_in.MIDI_to_Composition(filename)
        #composition = self.buildComposition(file[0])

        #get total count
        count = []
        i = -1
        for bar in file[0][0]:
            for info in bar:
                if(info[0] == 0):
                    i = i + 1
                print str(i) + " " + str(info[0] + i)
                count.append(info[0] + i)
        print count
        matrix = self.midi_matrix(track=file[0][0], total_count=len(count))
        count.pop()
        return (matrix, count)

    def midi_matrix(self, track, total_count=6):
        matrix = {}
        for n in self.notes:
            i = int(n)
            matrix[i] = [0] * total_count
        count = 0
        for bar in track:
            for info in bar:
                for n in info[2]:
                    i = int(n)
                    x = matrix[i]
                    x[count] = 1
                    matrix[i] = x
                count = count + 1
        return matrix

    def getMatrix(self):
        return self.matrix

    def getNotes(self):
        return self.notes