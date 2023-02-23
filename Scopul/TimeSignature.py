from music21 import meter, converter, stream, note, chord, midi
from Scopul.scopul_exception import MeasureNotFoundException
import re


class TimeSignature:
    def __init__(self, scopul):
        """Time Signature object for Scopul

        Args:
            scopul: A Scopul Object
        """
        self._scopul = scopul
        self.midi = self._scopul._midi
        self._ratio = f"{self.midi[meter.TimeSignature][0].numerator}/{self.midi[meter.TimeSignature][0].denominator}"
        self._numerator = int(self.ratio.split("/")[0])
        self._denominator = int(self.ratio.split("/")[1])

    # Signature denominator (denominator)
    @property
    def denominator(self) -> int:
        """Denominator part of the time signature"""
        return self._denominator

    # Signature numerator (numerator)
    @property
    def numerator(self) -> int:
        """Numerator part of the fraction time signature"""
        return self._numerator

    # Signature Ratio (ratio)
    @property
    def ratio(self) -> str:
        """Ratio / fractional representation of the time signature

        Example:
            3/4
            4/4
            2/2
        """
        return self._ratio

    # Time Signature appearance count (count)
    @property
    def count(self) -> int:
        """Get the count of the number of time signatures.

        Returns:
            An Integer representing the count of time signature appearances
            Example:

            test_midi.count = 2

        """
        # initiate counter
        count = 0

        for meta_message in self.midi.flat:
            if isinstance(meta_message, meter.TimeSignature):
                count += 1

        return count

    # Time Signature appearances list (list)
    def list(self, unique: bool = False) -> list:
        """Fetches every occurance of a time signature.

        Retrieves all the occurances of time signatures, with an optional ability to get unique signatures only.

        Args:
            unique: Optional boolean value to indicate whether to return unique time changes or to repeat

        Returns:
            A list or set object with time signatures in it.


        """
        # List of signatures
        sig_list = []

        for meta_message in self.midi.flat:
            if isinstance(meta_message, meter.TimeSignature):
                sig_list.append(
                    {
                        "ratio": meta_message.ratioString,
                        "measure": meta_message.measureNumber,
                    }
                )

        # If asked for no repeats
        if unique:
            # Loop through list
            for idx, signatures in enumerate(sig_list):
                try:
                    if sig_list[idx - 1]["ratio"] == signatures["ratio"]:
                        sig_list.pop(idx)
                except:
                    pass

        return sig_list

    def add_TimeSignature(self, time_sig: str, part, measure: int = 1) -> None:
        """A method to add a timesignature to a piece

        Args:
            time_sig: a str object representing the int. For example - "3/4"
            part: the Part object you want to modify
            measure: an int, representing the measure number you want to add this time signature. Default is one

        Returns:
            None, only modifies the midi

        """
        # Getting the Music21 converter object and the Muic21 part object
        midi_file = self._scopul.midi
        part = part._part

        # Looking for measure
        if part[-1].measureNumber < measure:
            raise MeasureNotFoundException(
                f"Measure {measure} was not found in this part"
            )

        new_part = stream.Stream()

        # copying into new part with modified time
        time_added = False
        for element in part.flat:

            if element.measureNumber == measure and not time_added:
                new_part.append(meter.TimeSignature(time_sig))
                time_added = True

            if isinstance(element, (note.Note, note.Rest, chord.Chord)):
                new_part.append(element)

        new_part = new_part.makeMeasures()
        midi_file.replace(part, new_part)
