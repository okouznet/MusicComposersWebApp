from mingus.containers import NoteContainer
from mingus.containers import Note
from mingus.containers import Track
from mingus.containers import Composition
from mingus.containers.instrument import Piano
from mingus.midi import midi_file_out
from mingus.midi import midi_file_in

class PianoPlayer :
    def __init__(self):
        self.track = Track(Piano())

        self.notes = []
        #initialize keys
        for i in range(21, 109):
            self.notes.append(i)
        self.matrix = {}
        for n in self.notes:
            i = int(n)
            self.matrix[i] = [0] * 10

    def addTrack(self, notes, duration=None):
        mingus_notes = []
        for n in notes:
            if isinstance(n, int) == True:
                x = Note().from_int(n)
                mingus_notes.append(x)
            else:
                x = Note(n)
                mingus_notes.append(x)
        self.track.add_notes(mingus_notes, duration=duration)

    def addComposition(self):
        c = Composition()

        return

    def playTrack(self, notes, duration=None):
        t = Track(Piano())
        for n in notes:
            t.add_notes(n, duration=duration)

    def clearTrack(self):
        self.track = Track(Piano())
        self.matrix = {}
        for n in self.notes:
            i = int(n)
            self.matrix[i] = [0] * 10

    def saveTrack(self, filename):
        t = self.track
        path = "static/library/"
        file = path + filename + ".mid"
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

        #get total count
        count = []
        i = -1
        for bar in file[0][0]:
            for info in bar:
                if(info[0] == 0):
                    i = i + 1
                count.append(info[0] + i)
        #normalize count array
        count_total = []
        for i in range(0, len(count)*4):
            count_total.append(0.0625 * i)
        matrix = self.midi_matrix(track=file[0][0], total_count=len(count_total))
        count.pop()
        return (matrix, count_total)


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

                    x[count*4] = 1
                    matrix[i] = x
                count = count + 1
        return matrix

    def getMatrix(self):
        return self.matrix

    def getNotes(self):
        temp = self.notes
        temp.reverse()
        return temp[0:len(temp) -11 - 1]

    def make_queue(self, filename):
        file = midi_file_in.MIDI_to_Composition(filename)

        composition = self.buildComposition(file[0])
        result = []
        for track in composition[0]:

            for bar in track:
                for notes in bar:
                    temp = []
                    for n in notes[2]:
                        temp.append(int(n))
                    print notes
                    if len(notes[2]) > 0:
                        result.append(temp)
        return result

if __name__ == "__main__":
    p = PianoPlayer()
    notes = p.getNotes()
    print notes