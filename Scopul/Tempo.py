from music21 import converter, tempo, note, chord, stream, tempo, meter
from mido import bpm2tempo
from Scopul.scopul_exception import MeasureNotFoundException

# from Scopul.Sequence import Part


class Tempo:
    def __init__(self, bpm, measure) -> None:
        self._music21 = tempo.MetronomeMark(number=bpm)
        self.bpm = bpm
        self.midi_tempo = bpm2tempo(bpm)
        self.measure = measure
