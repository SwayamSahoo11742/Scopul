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
        """Changes the chords to the specified interval/key
            - Args:
                - interval: an int or a str, depending on your needs
            - Returns:
                - None
        """
        self.music21 = self.music21.transpose(key)
        self._update()
    
    def append(self, chord: Chord):
        if not isinstance(chord, Chord):
            return InvalidMusicElementError(f"type {type(chord)} is not a Scopul musical element")
        self.music21.append(chord.music21)
        self._update()

    def insert(self, index: int, chord: Chord):
        self.music21.insert(index, chord.music21)
        self._update()

    def delete(self, index:int):
        self.music21.remove(index)
        self._update()
    
    def _update(self):
        self.roman_chords = []
        self.key = None

        for chord in self.music21:
            self.roman_chords.append(roman.romanNumeralFromChord(chord).figure)
        
        key = analysis.discrete.analyzeStream(self.music21, 'key')
        self.key = f"{key.tonic.name, key.mode}"
        self.chords = [Chord(chord) for chord in self.music21]
    



    
    
    



