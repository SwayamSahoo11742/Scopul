import os
import sys
import inspect
import pytest

# Importing from parent Scopul
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Scopul import Scopul, midi_tempo2bpm, bpm2midi_tempo
from Scopul import Tempo

file1 = "testfiles/test1.mid"
file2 = "testfiles/test2.mid"
scop = Scopul(file2)
print(scop.tempo_list)

def test_tempo_list():
    scop.audio = file2
    expected_tempos = [Tempo(389610, 1)]
    assert scop.tempo_list[0].midi_tempo == 389610
    assert scop.tempo_list[0].bpm == round(midi_tempo2bpm(389610))
    assert scop.tempo_list[0].measure == 1

    
def test_tempo2bpm():
    scop.audio = file1
    assert midi_tempo2bpm(1000000) == 60.0


def test_bpm2tempo():
    assert bpm2midi_tempo(69) == 869565
