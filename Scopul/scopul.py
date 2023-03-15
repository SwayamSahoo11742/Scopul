from music21 import converter, environment, stream, note, tempo, chord, meter
import os
import pathlib
from collections.abc import Iterable
from Scopul.scopul_exception import (
    InvalidFileFormatError,
    InvalidMusicElementError,
    NoMusePathError,
    MeasureNotFoundException,
)
from mido import bpm2tempo, tempo2bpm, MidiFile

# Setting up music21 with MuseScore
from Scopul.TimeSignature import TimeSignature
from Scopul.Tempo import Tempo
from Scopul.Sequence import Part, Rest, Chord, Note
from Scopul.helpers import get_tempos


class Scopul:
    def __init__(self, audio):
        self.construct(audio)

    # Time Signature (time_sig)
    @property
    def time_sig_list(self) -> TimeSignature:
        """Fetches every occurrence of a time signature.

        Retrieves all the occurrences of time signatures, with an optional ability to get unique signatures only.

        Returns:
            A list or set object with time signatures in it.


        """
        # List of signatures
        sig_list = []

        for meta_message in self.midi.flat:
            if isinstance(meta_message, meter.TimeSignature):
                sig_list.append(
                    TimeSignature(
                        value=meta_message.ratioString,
                        measure=meta_message.measureNumber,
                    )
                )

        return sig_list

    # Midi File (midi)
    @property
    def audio(self):
        """Retrieves your midi file."""
        return self._audio

    @property
    def midi(self):
        """Retrieves midi file"""
        return self._midi

    @property
    def parts(self) -> list:
        """Retrieves a list of Part objects

        Example:
            [Part Object 1, Part Object 2]
        """
        return self._parts

    # Midi File setter
    @audio.setter
    def audio(self, audio) -> None:
        """Allows to reconstruct the object to change accordingly to a new midi"""
        self.construct(audio)

    def get_audio_length(self) -> int:
        """Returns the audio length"""
        return MidiFile(self._audio).length

    @property
    def tempo_list(self):
        """Fetches the tempo list in bpm format

        Fetches the time signatures in bpm with both measure numbers and the tempo

        Returns:
            A list of dict objects with 2 keys: "tempo" and "measure". For example:

            [{"tempo":36, "measure": 1},{"tempo":5, "measure": 56}]

        """
        return get_tempos(self._midi)

    # ================================== METHODS=============================================
    # Generate a pdf
    def generate_pdf(
        self,
        output: str,
        fp: str = "",
        overwrite: bool = False,
        remove_defects: bool = False,
    ) -> None:
        """Generates a pdf of the midi

        Creates a pdf by turning it into musicxml then to pdf

        Args:
            output: a str that represents the name of the file
            fp: a str that represents the file path as to where to save the pdf. Default is '', which will save to the current working directory
            overwrite: a boolean, indicates whether to overwrite files or not
            remove_defects: a boolean, indicates whether to remove defective parts or not

        Returns:
            None, just generates a pdf in the path specified with the name specified

        Raises:
            FileExistsError: if overwrite is False and there is a file at the same path
        """

        # Looking for muse score path
        try:
            env = environment.Environment()
            env["musicxmlPath"] = os.environ["MUSESCORE_PATH"]
            env["musescoreDirectPNGPath"] = os.environ["MUSESCORE_PATH"]
        except:
            raise NoMusePathError(
                "Path to musescore not set. please set using config_musescore()"
            )

        # checking for existence of the path
        if not pathlib.Path(os.environ["MUSESCORE_PATH"]).exists():
            raise FileNotFoundError(
                f"MuseScore path at {os.environ['MUSESCORE_PATH']} not found. Please check to see if it exists"
            )

        # Check for correct file format
        ext = pathlib.Path(output).suffix
        if ext != ".pdf":
            raise InvalidFileFormatError(f"Expected .pdf, got {ext}")

        midi = self.midi.makeMeasures()

        if remove_defects:
            for part in midi.parts:
                try:
                    part.write("musicxml.pdf")
                except:
                    midi.remove(part)

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp + output).exists():
                os.remove(fp + output)
        # If not overwrite
        else:
            if pathlib.Path(fp + output).exists():
                raise FileExistsError(
                    f"{fp + output} already exists. To overwrite, set overwrite=True"
                )

        # Creates the pdf and deletes the musicxml file
        midi.metadata.title = output.split(".")[0]
        midi.write("musicxml.pdf", fp=fp)
        os.rename(fp + ".musicxml.pdf", fp + output)
        os.remove(fp + ".musicxml.musicxml")

    def generate_musicxml(
        self,
        output: str,
        fp: str = "",
        overwrite: bool = False,
        remove_defects: bool = False,
    ) -> None:
        """Generates a musicxml of the midi

        Args:
            output: a str that represents the name of the file
            fp: a str that represents the file path as to where to save the pdf. Default is '', which will save to the current working directory
            overwrite: a boolean, indicates whether to overwrite files or not
            remove_defects: a boolean, indicates whether to remove defective parts or not

        Returns:
            None, just generates a pdf in the path specified with the name specified

        Raises:
            FileExistsError: if overwrite is False and there is a file at the same path
        """

        # Looking for muse score path
        try:
            env = environment.Environment()
            env["musicxmlPath"] = os.environ["MUSESCORE_PATH"]
            env["musescoreDirectPNGPath"] = os.environ["MUSESCORE_PATH"]
        except:
            raise NoMusePathError(
                "Path to musescore not set. please set using config_musescore()"
            )

        # Checking for existence of the path
        if not pathlib.Path(os.environ["MUSESCORE_PATH"]):
            raise FileNotFoundError(
                f"MuseScore path at {os.environ['MUSESCORE_PATH']} not found. Please check to see if it exists"
            )

        # Check for correct file format
        ext = pathlib.Path(output).suffix
        if ext != ".xml":
            raise InvalidFileFormatError(f"Expected .xml, got {ext}")

        midi = self.midi

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp + output).exists():
                os.remove(fp + output)

        # If not overwrite
        else:
            if pathlib.Path(fp + output).exists():
                raise FileExistsError(
                    f"{fp + output} already exists. To overwrite, set overwrite=True"
                )

        if remove_defects:
            for part in midi.parts:
                try:
                    part.write("musicxml.pdf")
                except:
                    midi.remove(part)

        # Creates the pdf and deletes the musicxml file
        self.midi.write("musicxml.xml", fp=fp)
        os.rename(fp + ".musicxml.musicxml", fp + output)

    # (Re)constructor
    def construct(self, audio) -> None:
        """Constructor function to reconstruct the object

        Can also be called with a setter to the midi property. For example:

        testmidi.midi = "test.mid"

        """

        self._audio = audio
        self._midi = converter.parse(audio).makeMeasures()
        self._parts = []
        for part in self.midi.parts:
            self._parts.append(Part(part))

    def save_midi(self, output, fp="", overwrite=False):
        # Check for correct file format
        ext = pathlib.Path(output).suffix
        if ext != ".mid":
            raise InvalidFileFormatError(f"Expected .mid, got {ext}")

        midi = self.midi

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp + output).exists():
                os.remove(fp + output)

        # If not overwrite
        else:
            if pathlib.Path(fp + output).exists():
                raise FileExistsError(
                    f"{fp + output} already exists. To overwrite, set overwrite=True"
                )

        midi.write("midi", fp=fp + output)

    def add_tempo(self, bpm_tempo: int, part, measure_number: int = 1):
        """
        Adds a metronome mark at the specified measure in a part object.

        Args:
            part: A Scopul Part object representing a musical part.
            measure_number: An integer specifying the measure number where the
                metronome mark should be added.
            tempo: A floating point number representing the tempo in beats per
                minute (BPM) for the metronome mark.

        Returns:
            None.

        Raises:
            TypeError: If part is not a Scopul part object
            ValueError: If measure_number is not a positive integer
            ValueError: If tempo is not a positive number.
            MeasureNotFoundError: If given measure does not exist

        If a metronome mark already exists at the specified location, its tempo
        will be updated to the new tempo value
        """
        # Checking if part is a scopul part
        if not isinstance(part, Part):
            raise TypeError("Provided part is not a Scopul Part object")

        part = part._part

        # Checking if measure is a number
        if not isinstance(measure_number, (int, float)):
            raise ValueError("measure must be a positive number")

        # Checking if measure exists
        if measure_number <= 0 or measure_number > len(part):
            raise MeasureNotFoundException(f"measure {measure_number} does not exist")

        #  Checking if tempo in valid
        if not isinstance(bpm_tempo, (int, float)) or bpm_tempo <= 0:
            raise ValueError("Tempo must be a positive number")

        # Find the measure at the specified measure_number

        new_part = stream.Stream()

        # copying into new part with modified time
        mark_added = False
        for element in part.flat:

            if element.measureNumber == measure_number and not mark_added:
                new_part.append(tempo.MetronomeMark(number=bpm_tempo))
                mark_added = True

            if isinstance(
                element,
                (
                    note.Note,
                    note.Rest,
                    chord.Chord,
                    tempo.MetronomeMark,
                    meter.TimeSignature,
                ),
            ):
                new_part.append(element)

        new_part = new_part.makeMeasures()
        self.midi.replace(part, new_part)

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
        midi_file = self.midi
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

            if isinstance(
                element,
                (
                    note.Note,
                    note.Rest,
                    chord.Chord,
                    meter.TimeSignature,
                    tempo.MetronomeMark,
                ),
            ):
                new_part.append(element)

        new_part = new_part.makeMeasures()
        midi_file.replace(part, new_part)

    def add_note(self, element, part, measure_number=None, position=0):
        """Add a musical element (Note, Rest, or Chord) to a measure in the given part.

        Args:
            element: A Scopul musical element (Note, Rest, or Chord) to add to the measure.
            part: A music21 Part object representing the part to add the element to.
            measure_number (optional): An integer specifying the measure number to add the element to.
                If not provided, the element will be added to the last measure in the part.
            position (optional): An integer specifying the position within the measure to add the element.
                Defaults to 0 (the beginning of the measure).

        Raises:
            ValueError: If the given element is not a Scopul musical element (Note, Rest, or Chord),
                or if no measure is found with the given measure number.

        Returns:
            None
        """
        if not isinstance(element, (Note, Rest, Chord)):
            raise ValueError("Not a Scopul musical element (Notes, Rests, Chords)")
        
        if not measure_number:
            # If no measure number is provided, add the element to the last measure in the part
            measure_number = part.sequence[-1].measure

        new_part = stream.Stream()

        # copying into new part with modified time
        element_added = False
        for measure in part._part.getElementsByClass("Measure"):

            if measure.number == measure_number and not element_added:
                measure.insert(position, element._music21)
                element_added = True

            new_part.append(measure)

        new_part = new_part.makeMeasures()
        self.midi.replace(part, new_part)

        
        



