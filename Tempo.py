from music21 import converter, meter, tempo
from mido import bpm2tempo


class Tempo:
    def __init__(self, midi: str) -> None:
        self._midi = converter.parse(midi)
        self._bpm_list = get_tempos(self._midi)
        self._midi_tempo_list = [
            {"tempo": bpm2tempo(m["tempo"]), "measure": m["measure"]}
            for m in self.bpm_list
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


def get_tempos(midi):
    lst = []
    for i in midi.flat:
        if isinstance(i, tempo.MetronomeMark):
            lst.append({"tempo": i.number, "measure": i.measureNumber})

    return lst
