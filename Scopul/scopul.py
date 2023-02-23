from music21 import converter, environment
import os
import pathlib
from collections.abc import Iterable
from Scopul.scopul_exception import (
    InvalidFileFormatError,
    InvalidMusicElementError,
    NoMusePathError,
)
from mido import bpm2tempo, tempo2bpm, MidiFile

# Setting up music21 with MuseScore
from Scopul.TimeSignature import TimeSignature
from Scopul.Tempo import Tempo
from Scopul.Sequence import Part, Rest, Chord, Note


class Scopul:
    def __init__(self, audio):
        self.construct(audio)

    # Tempo (tempo)
    @property
    def tempo(self) -> Tempo:
        """Fetches Tempo object"""
        return self._tempo

    # Time Signature (time_sig)
    @property
    def time_sig(self) -> TimeSignature:
        """Fetches the Time Signature object"""
        return self._time_sig

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

    def get_audio_lenght(self) -> int:
        """Returns the audio lenght"""
        return MidiFile(self._audio).length

    # Generate a pdf
    def generate_pdf(self, output: str, fp: str = "", overwrite: bool = False) -> None:
        """Generates a pdf of the midi

        Creates a pdf by turning it into musicxml then to pdf

        Args:
            output: a str that represents the name of the file
            fp: a str that represents the file path as to where to save the pdf. Default is '', which will save to the current working directory
            overwrite: a boolean, indicates whether to overwrite files or not

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

        # checking for existance of the path
        if not pathlib.Path(os.environ["MUSESCORE_PATH"]).exists():
            raise FileNotFoundError(
                f"MuseScore path at {os.environ['MUSESCORE_PATH']} not found. Please check to see if it exists"
            )

        # Check for correct file format
        ext = pathlib.Path(output).suffix
        if ext != ".pdf":
            raise InvalidFileFormatError(f"Expected .pdf, got {ext}")

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
        self.midi.metadata.title = output.split(".")[0]
        self.midi.write("musicxml.pdf", fp=fp)
        os.rename(fp + ".musicxml.pdf", fp + output)
        os.remove(fp + ".musicxml.musicxml")

    def generate_musicxml(
        self, output: str, fp: str = "", overwrite: bool = False
    ) -> None:
        """Generates a musicxml of the midi

        Args:
            output: a str that represents the name of the file
            fp: a str that represents the file path as to where to save the pdf. Default is '', which will save to the current working directory
            overwrite: a boolean, indicates whether to overwrite files or not

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

        # Checking for existance of the path
        if not pathlib.Path(os.environ["MUSESCORE_PATH"]):
            raise FileNotFoundError(
                f"MuseScore path at {os.environ['MUSESCORE_PATH']} not found. Please check to see if it exists"
            )

        # Check for correct file format
        ext = pathlib.Path(output).suffix
        if ext != ".xml":
            raise InvalidFileFormatError(f"Expected .xml, got {ext}")

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
        self.midi.write("musicxml.xml", fp=fp)
        os.rename(fp + ".musicxml.musicxml", fp + output)

    # (Re)constructor
    def construct(self, audio) -> None:
        """Constructor function to reconstruct the object

        Can also be called with a setter to the midi property. For example:

        testmidi.midi = "test.mid"

        """

        self._audio = audio
        self._midi = converter.parse(audio)
        self._time_sig = TimeSignature(self)
        self._tempo = Tempo(self)
        self._parts = []
        for part in self.midi.parts:
            self._parts.append(Part(part))


def midi_tempo2bpm(tempo: int | Iterable) -> float | list:
    """Converts a midi tempo value to bpm

    Args:
        tempo: an int

    Returns:
        A list or an int, depending on the input.

        EX (int input):
            65
        OR (list input):
            [125,50,65]
    """
    try:
        if isinstance(tempo, int):
            return tempo2bpm(tempo)
        elif isinstance(tempo, Iterable):
            return [tempo2bpm(temp) for temp in tempo]
    except TypeError:
        raise TypeError("midi_tempo2bpm only accepts str or iterable objects")


def bpm2midi_tempo(tempo: int | list) -> float | list:
    """Converts a bpm value to midi tempo

    Args:
        tempo: an int

    Returns:
        List or Str object, depending on the input

        EX (int input):
            10000
        OR (list input):
            [10000,896534,23334]
    """
    try:
        if isinstance(tempo, int):
            return bpm2tempo(tempo)
        elif isinstance(tempo, Iterable):
            return [bpm2tempo(temp) for temp in tempo]
    except TypeError:
        raise TypeError("bpm2midi_tempo only accepts str or iterable objects")
