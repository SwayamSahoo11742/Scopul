import music21
from Scopul.scopul_exception import InvalidMusicElementError
from Scopul.conversions import note_to_number
from collections.abc import Iterable
from Scopul.helpers import sublist
import re


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
            if isinstance(element, music21.note.Note):
                self.sequence.append(Note(element))
            elif isinstance(element, music21.chord.Chord):
                self.sequence.append(Chord(element))
            elif isinstance(element, music21.note.Rest):
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
            ValueError: if inputted negative number, or a list with not length of 2
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

    # rhythm -> List of rhythm
    # gets a list of all the occurrences of a rhythm in the current part
    def get_rhythm(self, rhythm: Iterable):
        """gets a list of all the occurrences of a rhythm in the current part

        Args:
            rhythm: a list where each element represents a rhythm
                the elements in the list must be the note's quarter length (For example, 1 would be quarter note, 0.5 will be eight note)
                For example:
                    [1, 1, 0.5, 0.5, 2]
                    this will be a rhythm of quarter, quarter, eighth, eighth, half

                Can specify note type using the following format:
                    [[type, quarterlength], [type, quarterlength] ...]

                    For Example:
                    [["c", 0.75], ["r", 0.25]]
                    This will search for rhythms with dotted-eight chords followed by 16th rest

                    Types:
                        r: Rest
                        c: Chord
                        n: Note

            overlap: Boolean, will determine whether or not to retrieve overlapping cases

            Returns:
                a list of lists, with each list containing the Scopul musical element objects that satisfy the rhythm:
                For Example:
                    get_rhythm([1, 1, 2])

                    >>> [[Scopul.Note, Scopul.Note, Scopul.Rest], [Scopul.Rest, Scopul.Rest, Scopul.Chord]] # Sample output
        """

        # Creating the note type list
        type_list = []

        for note in rhythm:
            try:
                if note[0] not in ["r", "c", "n"]:
                    raise TypeError

                type_list.append(note[0])

            except TypeError:
                type_list.append(None)

        # Create rhythm type regex
        type_regex = [re.escape(x) if x is not None else "." for x in type_list]
        type_regex = "^" + "".join(type_regex) + "$"

        # Creating rhythm list
        rhythm_list = []

        for note in rhythm:
            try:
                rhythm_list.append(note[-1])

            except TypeError:
                rhythm_list.append(note)

        # Filtering part by rhythm

        seq_element_list = [element for element in self.sequence]
        seq_ql_list = [element.music21.quarterLength for element in self.sequence]

        # Use the sublist function to find all occurrences of the given rhythm in the sequence
        rhythm_indices = sublist(seq_ql_list, rhythm_list, overlap=False)

        # Extract the sublists of elements that correspond to the found rhythmic patterns
        rhythm_list = [seq_element_list[i[0] : i[-1] + 1] for i in rhythm_indices]

        # Filter part by note types
        final_list = []
        for sequence in rhythm_list:
            # Comparing rhythm type regex to sequence note types
            match = re.match(
                type_regex,
                "".join(
                    [
                        "c"
                        if type(element) == Chord
                        else "r"
                        if type(element) == Rest
                        else "n"
                        for element in sequence
                    ]
                ),
            )
            if match:
                final_list.append(sequence)

        # Return the list of rhythmic patterns
        return final_list


class Note:
    """A Class for all the notes"""

    def __init__(self, note=None, name=None, length=None) -> None:
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

        if note is not None:
            self.music21 = note
            self._measure = note.measureNumber
            self._velocity = note.volume.velocity
        else:
            self.music21 = music21.note.Note(name, quarterLength=length)
            self._measure = None
            self._velocity = None

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


class Rest:
    """A Class for all the rests"""

    def __init__(self, rest=None, length=None) -> None:

        if length and isinstance(length, (int, float)):
            self._length = length
        else:
            self._length = rest.duration.quarterLength

        if rest is not None:
            self.music21 = rest
            self._measure = rest.measureNumber
        else:
            self._measure = None
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


class Chord:
    """A Class to represent a chord (multiple notes at once)"""

    def __init__(self, chord=None, notes: list = None) -> None:
        if isinstance(chord, music21.chord.Chord):
            self.music21 = chord
            self._notes = [Note(note) for note in list(chord.notes)]
            self._measure = chord.measureNumber
            self._length = chord.duration.quarterLength
        # if chord is not a music21 chord object
        else:
            notes = [note.music21 for note in notes]
            self.music21 = music21.chord.Chord(notes)
            self._notes = [Note(note) for note in notes]
            self._measure = None
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
