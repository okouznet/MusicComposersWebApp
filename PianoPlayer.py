from __future__ import division
from mingus.containers import NoteContainer
from mingus.containers import Note
from mingus.containers import Bar

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

    def saveComposition(self, filename, composition):
        path = "static/library/"
        file = path + filename + ".mid"
        print file
        midi_file_out.write_Composition(file, composition)

    def buildComposition(self, compose, save):
        c = Composition()
        count = 0
        #get components
        for track in compose:
            t = ''
            if (save == 0):
                t = self.track
            else:
                t = Track()
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
        count = 0
        i = 0
        print "composition"
        print file
        for track in file[0]:
            for bar in track:
                print "bar"
                for info in bar:
                    print "add_file"
                    print info
                    if(info[0] == 0):
                        info[0] = info[0] + 1
                    count = count + 1

        #normalize count array
        count_total = []
        for i in range(0, count*4):
            count_total.append(0.0625 * i)
        matrix = self.midi_matrix(composition=file[0], total_count=count_total)
        #count.pop()
        return (matrix, count_total)


    def midi_matrix(self, composition, total_count):
        matrix = {}
        print len(total_count)
        for n in self.notes:
            i = int(n)
            matrix[i] = [0] * len(total_count)
        count = 0
        for track in composition:
            for bar in track:
                for info in bar:


                    for n in info[2]:

                        i = int(n) + 12
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

    def make_queue(self, filename, save):
        file = midi_file_in.MIDI_to_Composition(filename)
        composition = self.buildComposition(file[0], save)
        result = []
        for track in composition[0]:

            for bar in track:
                for notes in bar:
                    temp = []
                    for n in notes[2]:
                        temp.append(int(n))
                    if len(notes[2]) > 0:
                        result.append(temp)
        return result, composition[0]


    def get_track(self, dict, length):
        beats = dict.keys()
        notes = dict.values()

        track = Track()
        bar = Bar()
        for i in range(0, length):
            beat = i / 16
            if (beat in dict):
                note = dict[beat][0]
                if (bar.place_notes(note[0], note[1]) == False):
                    track.add_bar(bar)
                    bar = Bar()
                    bar.place_notes(note[0], note[1])

                # 0.0: [('E-3', 4), ('C-3', 2)],
            else:

                if (bar.place_rest(16) == False):
                    track.add_bar(bar)
                    bar = Bar()
                    bar.place_rest(16)
        print "track"
        print track
        return track

    def get_composition(self, composition, tempo, length):
        """

        :param composition:
        :param tempo:
        :param length:
        :return:
        """
        whole = tempo * 4
        half = tempo * 2
        quarter = tempo
        eighth = tempo / 2
        sixteenth = tempo / 4
        duration_dict = {whole: 1, half: 2, quarter: 4, eighth: 8, sixteenth: 16}

        c = Composition()

        for track in composition:
            composition_dict = {}
            for bar in track:
                n = note_converter(str(bar['key']))
                dur = duration_dict[int(bar['duration'])]
                count = ((float(bar['clock'])) - 32) / (128 * 4)
                if count not in composition_dict:
                    temp = []
                    temp.append((Note(n), dur))
                    composition_dict[count] = temp
                else:
                    x = composition_dict[count]
                    x.append((Note(n), dur))
                    composition_dict[count] = x
                    # extract note
                    # n.append(str(i))
            t = self.get_track(dict=composition_dict, length=length)
            c.add_track(t)
        return c


def note_converter(note):
    """

    :param note:
    :return:
    """
    n = 'C-3'
    if (len(note) == 2):
        n = note[0] + '-' + note[1]
    elif (len(note) == 3):
        n = note[0:2] + '-' + note[2]
    return Note(n)

if __name__ == "__main__":
    p = PianoPlayer()
    file = "/Users/alefevre/Documents/Courses/EECS481/MusicComposersWebApp/static/library/stress.mid"
    composition = p.make_queue(file, 0)
    file2 = "/Users/alefevre/Documents/Courses/EECS481/MusicComposersWebApp/static/library/miditoComposition.mid"
    print composition[1]
    #p.saveComposition(file2, composition[1])