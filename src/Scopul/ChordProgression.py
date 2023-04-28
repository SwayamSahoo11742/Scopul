from Scopul.MusicalElements import Chord
from Scopul.scopul_exception import InvalidMusicElementError
from music21 import roman, analysis
class ChordProgression:
    """ChordProgression, a class to work with chord progressions for the Scopul class"""
    def __init__(self, part) -> None:
        self.music21 = part._part.chordify().recurse().getElementsByClass('Chord')
        self.roman_chords = []
        self.key = None

        for chord in self.music21:
            self.roman_chords.append(roman.romanNumeralFromChord(chord).figure)
        
        key = analysis.discrete.analyzeStream(self.music21, 'key')
        self.key = f"{key.tonic.name, key.mode}"
        self.chords = [Chord(chord) for chord in self.music21]

    @property
    def length(self):
        return len(self.roman_chords)
    
    def transpose(self, key: str):
        self.music21.transpose(key)
        self.update()
    
    def append(self, chord: Chord):
        if not isinstance(chord, Chord):
            return InvalidMusicElementError(f"type {type(chord)} is not a Scopul musical element")
        self.music21.append(chord.music21)
        self.update()

    def insert(self, index: int, chord: Chord):
        self.music21.insert(index, chord.music21)
        self.update()

    def delete(self, index:int):
        self.music21.remove(index)
        self.update()
    
    def update(self):
        self.roman_chords = []
        self.key = None

        for chord in self.music21:
            self.roman_chords.append(roman.romanNumeralFromChord(chord).figure)
        
        key = analysis.discrete.analyzeStream(self.music21, 'key')
        self.key = f"{key.tonic.name, key.mode}"
        self.chords = [Chord(chord) for chord in self.music21]
    



    
    
    



