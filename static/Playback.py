from mingus.containers import NoteContainer
from mingus.containers import Note
from mingus.containers import Track
from mingus.midi import fluidsynth
from mingus.containers.instrument import Piano
from PianoPlayer import *

class Playback:
    def __init__(self, piece):
        self.piano = PianoPlayer()
        if piece == 'a':
            self.piece = "Beethoven"

    def buildPiece(self):
        return True
