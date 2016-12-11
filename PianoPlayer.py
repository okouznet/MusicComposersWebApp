from mingus.containers import NoteContainer
from mingus.containers import Note
from mingus.containers import Track
from mingus.containers import Bar
from mingus.containers import Composition
from mingus.containers.instrument import Piano
from mingus.midi import midi_file_out
from mingus.midi import midi_file_in

class PianoPlayer :
    def __init__(self):
        """
        function to initialize PianoPlayer class
        """
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
        """
        function to update track
        :param notes: array of notes to add
        :param duration: how long note should play for
        :return: none
        """
        mingus_notes = []
        for n in notes:
            if isinstance(n, int) == True:
                x = Note().from_int(n)
                mingus_notes.append(x)
            else:
                x = Note(n)
                mingus_notes.append(x)
        self.track.add_notes(mingus_notes, duration=duration)

    def clearTrack(self):
        """
        function to reset track and matrix
        :return: none
        """
        self.track = Track(Piano())
        self.matrix = {}
        for n in self.notes:
            i = int(n)
            self.matrix[i] = [0] * 10

    def saveTrack(self, filename):
        """
        save track in piano class to file
        :param filename: name of file
        :return: none
        """
        track = self.track
        path = "static/library/"
        file = path + filename + ".mid"
        midi_file_out.write_Track(file, track)

    def saveComposition(self, filename, track):
        """
        function to save customized composition to file
        :param filename: name of file
        :param track: Track() object to save
        :return: none
        """
        path = "static/library/"
        file = path + filename + ".mid"
        midi_file_out.write_Track(file, track)

    def buildComposition(self, compose):
        """
        function to parse file into a composition
        :param compose: contents of midi file
        :return: tuple containing composition and length of composition
        """
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
        """
        function to add file to matrix
        :param filename: name if midi file
        :return: matrix and array of beats (each beat is a 16th note)
        """
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
        #count.pop()
        return (matrix, count_total)


    def midi_matrix(self, track, total_count=6):
        """
        build matrix where columns = notes and rows = beats
        - one denotes that a note occured on a particular beat
        :param track: Track() object to be parsed
        :param total_count: array of beats (16th notes)
        :return: matrix
        """
        matrix = {}
        for n in self.notes:
            i = int(n)
            matrix[i] = [0] * total_count
        count = 0
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
        """
        function to get matrix from class
        :return: matrix
        """
        return self.matrix

    def getNotes(self):
        """
        function to get array of notes
        :return: notes
        """
        temp = self.notes
        temp.reverse()
        return temp[0:len(temp) -11 - 1]

    def make_queue(self, filename):
        """
        parse a song into a composition for play along feature
        :param filename: name of midi file
        :return: return an array of notes in file
        """
        file = midi_file_in.MIDI_to_Composition(filename)

        composition = self.buildComposition(file[0])
        result = []
        for track in composition[0]:

            for bar in track:
                for notes in bar:
                    temp = []
                    for n in notes[2]:
                        temp.append(int(n))
                    if len(notes[2]) > 0:
                        result.append(temp)
        return result

    def get_track(self, dict):
        """
        parse track from matrix representation
        :param dict: mapping of beats to notes that occurred on that particular beat
        :param length:
        :return:
        """

        track = Track()
        for key in sorted(dict.iterkeys()):
            notes = dict[key]
            mingus = []
            for chord in notes:
                mingus.append(chord[0])
            track.add_notes(mingus)
        return track

    def get_composition(self, composition, tempo, length):
        """

        :param composition: matrix of midi file to be parsed
        :param tempo: tempo of piece
        :param length: number of beats in piece
        :return: track
        """
        whole = tempo * 4
        half = tempo * 2
        quarter = tempo
        eighth = tempo / 2
        sixteenth = tempo / 4
        duration_dict = {whole: 1, half: 2, quarter: 4, eighth: 8, sixteenth: 16}

        composition_dict = {}

        for track in composition:
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
                    # n.append(str(i))\
            #c.add_track(t)
        track = self.get_track(dict=composition_dict)
        return track


def note_converter(note):
    """
    converts string representation to mingus representation of a note
    :param note: string (e.g. 'C3')
    :return: a Note() object (e.g. 'C-3')
    """
    n = 'C-3'
    if (len(note) == 2):
        n = note[0] + '-' + str(int(note[1]))
    elif (len(note) == 3):
        n = note[0:2] + '-' + str(int(note[2]))
    return Note(n)
