from music21 import note, chord
from Scopul.scopul_exception import InvalidMusicElementError
from Scopul.conversions import note_to_number
from collections.abc import Iterable


class Part:
    """A class representing the a part in a score.
    EX: A flute part
    """

    def __init__(self, part) -> None:
        self._part = part
        self.name = part.partName
        self.sequence = []
        # Looping through the part
        for element in part.recurse():
            # Setting the class and appending depending on the type of symbol
            if isinstance(element, note.Note):
                self.sequence.append(Note(element))
            elif isinstance(element, chord.Chord):
                self.sequence.append(Chord(element))
            elif isinstance(element, note.Rest):
                self.sequence.append(Rest(element))

    # Note list
    def get_notes(self, seq: list) -> list:
        """Retrieves all the notes in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of note objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        # Notes list
        notes = []

        # If not a iterable, raise error
        if not isinstance(seq, Iterable):
            raise TypeError(
                "Not an iterable. Include a iterable object of Scopul Rests, Chords or Note"
            )

        # loop through the sequence
        for idx, element in enumerate(seq):
            # If its not a scopul sequence, raise error
            if not isinstance(element, (Chord, Rest, Note)):
                raise InvalidMusicElementError(
                    f"Please include a valid Scopul Sequence that contains Chord, Rest or Note objects. Invalid type found : {type(element)} at index {idx}"
                )
            # Append to list
            if isinstance(element, Note):
                notes.append(element)

        return notes

    # Gets a count of notes
    def get_note_count(self, seq: list) -> int:
        """Retrieves the number of notes"""
        return len(self.get_notes(seq))

    # Note list
    def get_rests(self, seq: list) -> list:
        """Retrieves all the notes in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of rest objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        # rests list
        rests = []

        # If not a iterable, raise error
        if not isinstance(seq, Iterable):
            raise TypeError(
                "Not an iterable. Include a iterable object of Scopul Rests, Chords or Note"
            )

        # loop through the sequence
        for idx, element in enumerate(seq):
            # If its not a scopul sequence, raise error
            if not isinstance(element, (Chord, Rest, Note)):
                raise InvalidMusicElementError(
                    f"Please include a valid Scopul Sequence that contains Chord, Rest or Note objects. Invalid type found : {type(element)} at index {idx}"
                )
            # Append to list
            if isinstance(element, Note):
                rests.append(element)

        return rests

    # Gets a count of rests
    def get_rest_count(self, seq: list) -> int:
        """Retrieves the number of rests"""
        return len(self.get_rests(seq))

        # Note list

    def get_chords(self, seq: list) -> list:
        """Retrieves all the chords in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of chords objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        # chords list
        chords = []

        # If not a iterable, raise error
        if not isinstance(seq, Iterable):
            raise TypeError(
                "Not an iterable. Include a iterable object of Scopul Rests, Chords or Note"
            )

        # loop through the sequence
        for idx, element in enumerate(seq):
            # If its not a scopul sequence, raise error
            if not isinstance(element, (Chord, Rest, Note)):
                raise InvalidMusicElementError(
                    f"Please include a valid Scopul Sequence that contains Chord, Rest or Note objects. Invalid type found : {type(element)} at index {idx}"
                )
            # Append to list
            if isinstance(element, Note):
                chords.append(element)

        return chords

    # Gets a count of notes
    def get_chord_count(self, seq: list) -> int:
        """Retrieves the number of notes"""
        return len(self.get_chords(seq))

    def get_measure(self, measures: int | list):
        """Fetches the contents of a measure.

        Retrieves about chords, notes and rest objects in the sequence

        Args:
            m: an int, representing the measure or a list [start, end], representing a range of measures

        Returns:
            A list with all the contents in the measure(s) requested

        Raises:
            ValueError: if inputted negative number, or a list with not lenght of 2
            TypeError: if input is not a list of int
        """
        # If integer
        if isinstance(measures, int):

            # if invalid integer
            if measures <= 0:
                raise ValueError("get_measure only allows positive integers")

            seq = []
            for element in self.sequence:
                if element.measure == measures:
                    seq.append(element)
            return seq

        # If list
        elif isinstance(measures, Iterable):

            # Check for positive int
            for measure in measures:
                if measure <= 0:
                    raise ValueError("get_measure only allows positive integers")

            # check for only start and end values
            if len(measures) != 2:
                raise ValueError("usage: get_measure([start, end])")

            seq = []
            for element in self.sequence:
                if element.measure in range(measures[0], measures[1] + 1):
                    seq.append(element)
            return seq

        # Incorrect type
        else:
            raise TypeError(
                f"get_measure only accepts int or iterable, instead got {type(measures)}"
            )

    def get_highest_note(self, seq: list):
        """Retrieves all the chords in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of chords objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        # highest note
        highest = 0

        # If not a list, raise error
        if not isinstance(seq, Iterable):
            raise TypeError(
                "Not a list. Include a list of Scopul Rests, Chords or Note"
            )

        # loop through the sequence
        for idx, element in enumerate(seq):
            if not isinstance(element, (Chord, Rest, Note)):
                raise InvalidMusicElementError(
                    f"Please include a valid Scopul Sequence that contains Chord, Rest or Note objects. Invalid type found : {type(element)} at index {idx}"
                )
            # Append to list
            if isinstance(element, Note):
                if highest == 0:
                    highest = element
                else:
                    note_val = note_to_number(element.name[0], int(element.name[1]))
                    if note_val > note_to_number(highest.name[0], int(highest.name[1])):
                        highest = element

        return highest


class Note:
    """A Class for all the notes"""

    def __init__(self, note) -> None:
        self._name = note.pitch.nameWithOctave
        self._measure = note.measureNumber
        self._velocity = note.volume.velocity
        self._lenght = note.duration.type

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
        """Returns an int, representing velocity of the note"""
        self._velocity

    @property
    def lenght(self):
        """Returns a str representing the lenght of the note

        Example:
            "quarter"

        """
        return self._lenght


class Rest:
    """A Class for all the rests"""

    def __init__(self, rest) -> None:
        self._measure = rest.measureNumber
        self._lenght = rest.duration.type

    @property
    def lenght(self):
        """Returns a str, indicating the lenght of the rest

        Example:
            "whole"
        """
        return self._lenght

    @property
    def measure(self):
        """Returns an int, representing the measure number"""
        return self._measure


class Chord:
    """A Class to represent a chord (multiple notes at once)"""

    def __init__(self, chord) -> None:
        # Converting to notes
        self._notes = [Note(note) for note in list(chord.notes)]
        self._measure = chord.measureNumber
        self._lenght = chord.duration.type

    @property
    def lenght(self):
        """Returns a str, representing the lenght of the chord

        Example:
            "eighth"
        """
        return self._lenght

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
