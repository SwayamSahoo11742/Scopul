from music21 import converter, tempo, note, chord, stream, tempo, meter
from mido import bpm2tempo
from Scopul.scopul_exception import MeasureNotFoundException

# A container class, whose job is to store data nicely
class Tempo:
    def __init__(self, bpm, measure=None) -> None:
        self.music21 = tempo.MetronomeMark(number=bpm)
        self.bpm = bpm
        self.midi_tempo = bpm2tempo(bpm)
        self.measure = measure
