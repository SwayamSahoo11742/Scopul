from music21 import converter, tempo, note, chord, stream, tempo
from mido import bpm2tempo
from Scopul.scopul_exception import MeasureNotFoundException
from Scopul.Sequence import Part


class Tempo:
    def __init__(self, scopul) -> None:
        self._scopul = scopul
        self._midi = self._scopul._midi
        self._bpm_list = get_tempos(self._midi)
        self._midi_tempo_list = [
            {"tempo": bpm2tempo(tempo["tempo"]), "measure": tempo["measure"]}
            for tempo in self.bpm_list
        ]

    @property
    def bpm_list(self):
        """Fetches the tempo list in bpm format

        Fetches the time signatures in bpm with both measure numbers and the tempo

        Returns:
            A list of dict objects with 2 keys: "tempo" and "measure". For example:

            [{"tempo":36, "measure": 1},{"tempo":5, "measure": 56}]

        """
        return self._bpm_list

    @property
    def midi_tempo_list(self) -> list:
        """Fetches the tempo list in midi tempo format

        Fetches the time signatures in midi tempo with both measure numbers and the tempo

        Returns:
            A list of dict objects with 2 keys: "tempo" and "measure". For example:

            [{"tempo":100000, "measure": 1},{"tempo":10000, "measure": 65}]

        """
        return self._midi_tempo_list

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
        measure = part.measure(measure_number)

        # Check if there is already a MetronomeMark in the measure
        existing_tempo = None
        for element in measure.elements:
            if isinstance(element, tempo.MetronomeMark):
                existing_tempo = element
                break

        # If an existing MetronomeMark is found, update its tempo
        if existing_tempo is not None:
            existing_tempo.number = bpm_tempo
        else:
            # Create a new MetronomeMark object with the specified tempo
            new_tempo = tempo.MetronomeMark(number=bpm_tempo)

            # Insert the MetronomeMark object at the beginning of the measure
            measure.insert(0, new_tempo)


def get_tempos(midi):
    lst = []
    for meta_message in midi.flat:
        if isinstance(meta_message, tempo.MetronomeMark):
            lst.append(
                {"tempo": meta_message.number, "measure": meta_message.measureNumber}
            )

    return lst
