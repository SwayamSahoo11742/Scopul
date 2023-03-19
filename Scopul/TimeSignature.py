from music21 import meter, converter, stream, note, chord, midi, tempo
from Scopul.scopul_exception import MeasureNotFoundException
import re

# A container class, whose job is to store data nicely
class TimeSignature:
    def __init__(self, value, measure=None):
        """Time Signature object for Scopul

        Args:
            scopul: A Scopul Object
        """
        self.music21 = meter.TimeSignature(value=value)
        self.ratio = f"{self.music21.numerator}/{self.music21.denominator}"
        self.numerator = int(self.ratio.split("/")[0])
        self.denominator = int(self.ratio.split("/")[1])
        self.measure = measure
