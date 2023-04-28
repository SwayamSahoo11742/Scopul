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
import subprocess


class Scopul:
    def __init__(self, audio):
        self.construct(audio)

    # Time Signature (time_sig)
    @property
    def time_sig_list(self) -> TimeSignature:
        """Fetches every occurrence of a time signature.


        Returns:
            A list of TimeSignature objects


        """
        # List of signatures
        sig_list = []

        for meta_message in self.music21.flat:
            if isinstance(meta_message, meter.TimeSignature):
                sig_list.append(
                    TimeSignature(
                        value=meta_message.ratioString,
                        measure=meta_message.measureNumber,
                    )
                )

        return sig_list
    
    @property
    def key(self):
        s = stream.Stream()
        for part in self.music21.parts:
            try:
                part.analyze('key')
            except AttributeError:
                continue

            s.insert(part)
        key_sig = s.analyze('key')
        # print the key signature
        return f"{key_sig.tonic.name} {key_sig.mode}"

    # Midi File (midi)
    @property
    def path(self):
        """Retrieves your midi file."""
        return self._path

    @property
    def parts(self) -> list:
        """Retrieves a list of Part objects

        Example:
            [Part Object 1, Part Object 2]
        """
        return self._parts

    # Midi File setter
    @path.setter
    def path(self, path) -> None:
        """Allows to reconstruct the object to change accordingly to a new midi"""
        self.construct(path)

    @property
    def tempo_list(self):
        """Fetches the tempo list in bpm format

        Fetches the time signatures in bpm with both measure numbers and the tempo

        Returns:
            A list of Tempo objects
        """
        return get_tempos(self.music21)

    # ================================== METHODS=============================================
    def get_audio_length(self) -> int:
        """Returns the audio length"""
        return MidiFile(self._audio).length
    
    # Generate a pdf
    def generate_pdf(
        self,
        fp: str = "",
        title: str = "Scop",
        overwrite: bool = False,
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
            mspath = os.environ["MUSESCORE_PATH"]
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
        ext = pathlib.Path(fp).suffix
        if ext != ".pdf":
            raise InvalidFileFormatError(f"Expected .pdf, got {ext}")

        midi = self.music21

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp).exists():
                os.remove(fp)
        # If not overwrite
        else:
            if pathlib.Path(fp).exists():
                raise FileExistsError(
                    f"{fp} already exists. To overwrite, set overwrite=True"
                )

        # Creates the pdf and deletes the musicxml file
        subprocess.run(f'"{mspath}" -o "{fp}" "{self.path}" -T "{title}" 0')

    def generate_musicxml(
        self,
        fp: str = "",
        overwrite: bool = False,
        title = 'scop',
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
            mspath = os.environ["MUSESCORE_PATH"]
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
        ext = pathlib.Path(fp).suffix
        if ext != ".xml":
            raise InvalidFileFormatError(f"Expected .xml, got {ext}")

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp).exists():
                os.remove(fp)

        # If not overwrite
        else:
            if pathlib.Path(fp).exists():
                raise FileExistsError(
                    f"{fp} already exists. To overwrite, set overwrite=True"
                )


        # Creates the pdf and deletes the musicxml file
        subprocess.run(f'"{mspath}" -o "{fp}" "{self.path}" -T {title} 0')

    # (Re)constructor
    def construct(self, path) -> None:
        """Constructor function to reconstruct the object

        Can also be called with a setter to the midi property. For example:

        testmidi.music21 = "test.mid"

        """

        self._path = path
        self.music21 = converter.parse(path).makeMeasures()
        self._parts = []
        for part in self.music21.parts:
            self._parts.append(Part(part))

    def save_midi(self, fp=None, overwrite=True):
        """
        Save the MIDI file to the specified output file path.

        Args:
            self: A reference to the current object.
            output (str): The name of the MIDI output file.
            fp (str, optional): The path to the directory where the output file will be saved. Defaults to the current directory.
            overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.

        Raises:
            InvalidFileFormatError: If the output file has an invalid file extension.
            FileExistsError: If the output file already exists and overwrite is set to False.

        Returns:
            None
        """

        if not fp:
            fp = self.path
        # Check for correct file format
        ext = pathlib.Path(fp).suffix
        if ext != ".mid":
            raise InvalidFileFormatError(f"Expected .mid, got {ext}")

        midi = self.music21

        # Check for overwrite
        if overwrite:
            if pathlib.Path(fp).exists():
                os.remove(fp)

        # If not overwrite
        else:
            if pathlib.Path(fp).exists():
                raise FileExistsError(
                    f"{fp} already exists. To overwrite, set overwrite=True"
                )


        midi.write("midi", fp=fp)



        
        



