import music21
from Scopul.MusicalElements import Note, Rest, Chord
from Scopul.ChordProgression import ChordProgression
from Scopul.scopul_exception import InvalidMusicElementError, PercussionChordifyError
from Scopul.conversions import note_to_number
from collections.abc import Iterable
from Scopul.helpers import sublist
from Scopul import TimeSignature, Tempo
import re
from copy import deepcopy


class Part:
    """A class representing the a part in a score.
    EX: A flute part
    """

    def __init__(self, part: Iterable | music21.stream.Part) -> None:
        if not isinstance(part, music21.stream.Part):
            part = music21.stream.Part()
            for ele in part:
                if isinstance(ele, Note):
                    part.append(music21.note.Note(ele.name, velocity=ele.velocity, duration=music21.duration.Duration(ele.length)))
                if isinstance(ele, Rest):
                    part.append(music21.note.Rest(ele.length))
                if isinstance(ele, Chord):
                    c = music21.chord.Chord()
                    for nt in ele.notes:
                        c.add(music21.note.Note(nt.name, velocity=nt.velocity, duration=music21.duration.Duration(nt.length)))
                    part.append(c)
           
        self._part = part 
        self.name = part.partName

    @property
    def sequence(self):
        sequence = []
        # Looping through the part
        if isinstance(self._part, music21.stream.Part):
            for element in self._part.recurse():
                # Setting the class and appending depending on the type of symbol
                if isinstance(element, music21.note.Note):
                    sequence.append(Note(element))
                elif isinstance(element, music21.chord.Chord):
                    sequence.append(Chord(element))
                elif isinstance(element, music21.note.Rest):
                    sequence.append(Rest(element))
        return sequence


    # =========================================================================================== METHODS ====================================================================================================================
    def get_chord_progression(self):
        try:
            return ChordProgression(self)
        except AttributeError:
            raise PercussionChordifyError("Cannot get chord progression for Percussion part")
        
    def delete(self, index: int = 0):
        self._part.pop(index)
        
    def insert(self, element, measure_number: int = None, position: int = 0):
        if not isinstance(element, (Note, Rest, Chord, TimeSignature, Tempo)):
            raise ValueError(f"{type(element)} is not a Scopul musical element (Notes, Rests, Chords, Tempo, TimeSignature)")
        
        if not measure_number:
            # If no measure number is provided, add the element to the last measure in the part
            measure_number = self.sequence[-1].measure

        new_part = music21.stream.Stream()

        # copying into new part with modified time
        element_added = False
        for measure in self._part.getElementsByClass("Measure"):

            if measure.number == measure_number and not element_added:
                measure.insert(position, deepcopy(element.music21))
                element_added = True

            new_part.append(measure)

        new_part = new_part.makeMeasures()
        self._part.replace(self._part, new_part)

    # Note list
    def get_notes(self) -> list:
        """Retrieves all the notes in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of note objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        seq = self.sequence
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
    def get_note_count(self) -> int:
        """Retrieves the number of notes"""
        return len(self.get_notes())

    # Note list
    def get_rests(self) -> list:
        """Retrieves all the notes in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of rest objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        seq = self.sequence
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
    def get_rest_count(self) -> int:
        """Retrieves the number of rests"""
        return len(self.get_rests())

        # Note list

    def get_chords(self) -> list:
        """Retrieves all the chords in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of chords objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        seq = self.sequence
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
    def get_chord_count(self) -> int:
        """Retrieves the number of notes"""
        return len(self.get_chords())

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

    def get_highest_note(self):
        """Retrieves all the chords in a given sequence

        Args:
            seq: a list of Scopul musical symbols (Rest, Chord, Note)

        Returns:
            a list of chords objects extracted from the list

        Raises:
            InvalidMusicElementError: if found a type that is not Rest, Note or Chord
        """
        seq = self.sequence
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
    def search_rhythm(self, rhythm: Iterable):
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
                    raise TypeError # Potential idea ("Incorrect note type found. Note types include: 'r' (Rests), 'n' (Notes) or 'c' (Chords)")

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


