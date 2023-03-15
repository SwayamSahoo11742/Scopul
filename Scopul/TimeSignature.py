from music21 import meter, converter, stream, note, chord, midi, tempo
from Scopul.scopul_exception import MeasureNotFoundException
import re


class TimeSignature:
    def __init__(self, value, measure):
        """Time Signature object for Scopul

        Args:
            scopul: A Scopul Object
        """
        self._music21 = meter.TimeSignature(value=value)
        self.ratio = f"{self._music21.numerator}/{self._music21.denominator}"
        self.numerator = int(self.ratio.split("/")[0])
        self.denominator = int(self.ratio.split("/")[1])
        self.measure = measure
