import re
import music21

# A container class, whose job is to store data nicely
class Note:
    """A Class for all the notes"""

    def __init__(self, m21=None, name=None, length=None, velocity=None, measure=None) -> None:
        """
        A class representing a music note.

        Args:
            note: A music21 note object (optional).
            name: A string representing the name of the note in 'note octave' format (optional).
            length: A float or int representing the length of the note (optional).

        Raises:
            ValueError: If name is provided but is not in 'note octave' format.
            TypeError: If length is provided but is not a float or int.
        """

        if m21 is not None:
            self.music21 = m21
            self._measure = m21.measureNumber
            self._velocity = m21.volume.velocity
        else:
            self.music21 = music21.note.Note(name, quarterLength=length)
            self._measure = velocity
            self._velocity = measure

        if name and not re.search(r"[a-zA-z][1-9]", name):
            raise ValueError(
                "name expects a note name in 'note octave' format, ex: 'A1' 'C4'"
            )
        self._name = name if name else self.music21.pitch.nameWithOctave

        if length and not isinstance(length, (int, float)):
            raise TypeError("length only accepts ints and floats")
        self._length = length if length else self.music21.duration.quarterLength

    @property
    def name(self):
        """Returns the note in 'letter-name octave' format.

        Example:
            C4
            D5
            B-4
        """
        return self._name

    @property
    def measure(self):
        """Returns an int representing the measure"""
        return self._measure

    @property
    def velocity(self):
        """Returns an int representing velocity of the note"""
        return self._velocity

    @property
    def length(self):
        """Returns a str representing the length of the note

        Example:
            "quarter"

        """
        return self._length

# A container class, whose job is to store data nicely
class Rest:
    """A Class for all the rests"""

    def __init__(self, m21=None, length=None, measure=None) -> None:

        if length and isinstance(length, (int, float)):
            self._length = length
        else:
            self._length = m21.duration.quarterLength

        if m21 is not None:
            self.music21 = m21
            self._measure = m21.measureNumber
        else:
            self._measure = measure
            self.music21 = music21.note.Rest(quarterlength=length)

    @property
    def length(self):
        """Returns a str, indicating the length of the rest

        Example:
            "whole"
        """
        return self._length

    @property
    def measure(self):
        """Returns an int, representing the measure number"""
        return self._measure

# A container class, whose job is to store data nicely
class Chord:
    """A Class to represent a chord (multiple notes at once)"""

    def __init__(self, m21=None, notes: list = None, measure=None) -> None:
        if isinstance(m21, music21.chord.Chord):
            self.music21 = m21
            self._notes = [Note(note) for note in list(m21.notes)]
            self._measure = m21.measureNumber
            self._length = m21.duration.quarterLength
        # if chord is not a music21 chord object
        else:
            notes = [note.music21 for note in notes]
            self.music21 = music21.chord.Chord(notes)
            self._notes = [Note(note) for note in notes]
            self._measure = measure
            self._length = notes[0].duration.quarterLength

    @property
    def length(self):
        """Returns a str, representing the length of the chord

        Example:
            "eighth"
        """
        return self._length

    @property
    def measure(self):
        """Returns an int, representing the measure number"""
        return self._measure

    @property
    def notes(self):
        """Retrieves a list of notes in a chord

        Returns;
            A list, consisting of Note objects. For example:

            [Note Object, Note Object]
        """
        return self._notes
