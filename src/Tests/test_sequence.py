import os
import sys
import inspect
import pytest
import music21

# Importing from parent Scopul
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Scopul import Scopul, Part, Tempo, TimeSignature, Rest, Note, Chord
from Scopul import InvalidFileFormatError, InvalidMusicElementError

file1 = "testfiles/test1.mid"
file2 = "testfiles/test2.mid"
scop = Scopul(file1)


def test_part():
    assert type(scop.parts) == list
    assert type(scop.parts[0]) == Part
    assert scop.parts[0].name == "Right Hand"

print(f"--------------{type(scop.parts[0].get_measure([1,2]))}")
def test_sequence():
    assert type(scop.parts[0].sequence) == list
    assert type(scop.parts[0].sequence[0]) == Chord
    assert type(scop.parts[0].get_measure([1, 2])) == list


def test_note():

    assert type(scop.parts[0].sequence[1]) == Note
    note = scop.parts[0].sequence[1]
    assert note.length == 3.0
    assert note.measure == 1
    assert note.velocity == 90


def test_rest():

    assert type(scop.parts[0].sequence[412]) == Rest
    rest = scop.parts[0].sequence[412]
    assert rest.length == 0.25
    assert rest.measure == 84


def test_chord():
    assert type(scop.parts[0].sequence[0]) == Chord
    chord = scop.parts[0].sequence[0]
    assert chord.length == 0.5
    assert chord.notes[0].name == "D4"
    assert chord.notes[1].name == "F3"
    assert chord.measure == 1


part = scop.parts[0]


def test_get_notes():
    # Test that get_notes method returns a list of Note objects

    seq = part.sequence
    notes = part.get_notes()
    assert isinstance(notes, list)
    assert all(isinstance(note, Note) for note in notes)


def test_get_note_count():
    # Test that get_note_count returns the correct number of notes in the sequence
    seq = part.sequence
    note_count = part.get_note_count()
    assert isinstance(note_count, int)
    assert note_count == len(part.get_notes())


def test_get_rests():
    # Test that get_rests method returns a list of Rest objects
    seq = part.sequence
    rests = part.get_rests()
    assert isinstance(rests, list)


def test_get_rhythm():
    # Test case 1 - simple rhythm with overlap=False
    part = Scopul("testfiles/test1.mid").parts[0]
    result = part.search_rhythm([0.75, 0.25, 0.5, 0.75, 0.25, 0.5])

    new_result = []
    for sequence in result:
        new_result.append([type(note) for note in sequence])

    expected_type = [
        [Note, Rest, Note, Note, Rest, Note],
        [Note, Rest, Note, Note, Rest, Note],
        [Note, Rest, Note, Note, Rest, Note],
    ]

    assert len(result) == 1

    # Test case 2 - complex rhythm with overlap=False
    part = Scopul("testfiles/test1.mid").parts[0]
    result = part.search_rhythm([["c", 0.75], ["r", 0.25], ["c", 0.75], ["r", 0.25]])

    new_result = []
    for sequence in result:
        new_result.append([type(note) for note in sequence])

    expected = [[Chord, Rest, Chord, Rest]] * 42

    assert new_result == expected
    assert len(result) == 42

def test_Note_object_creation():
    note = Note(name="C4", length=1.5)

    assert note.length == 1.5
    assert note.name == "C4"
    assert note.velocity == None
    assert note.measure == None
    assert isinstance(note.music21, music21.note.Note) == True

def test_Rest_object_creation():
    rest = Rest(length=0.25)

    assert rest.length == 0.25
    assert rest.measure == None
    assert isinstance(rest.music21, music21.note.Rest) == True

def test_Note_object_creation():
    N1 = Note(name="C4", length=1.5)
    N2 = Note(name="B2", length=1.5)
    N3 = Note(name="E5", length=1.5)

    chord = Chord(notes=[N1, N2, N3])

    assert chord.length == 1.5
    assert len(chord.notes) == 3

    for note in chord.notes:
        assert isinstance(note, Note) == True

    assert chord.measure == None
    assert isinstance(chord.music21, music21.chord.Chord) == True

def test_part_insertion():
    N1 = Note(name="E5", length=1.6)
    previous = len(scop.parts[0].sequence)
    scop.parts[0].insert(N1, 7, 4)
    assert len(scop.parts[0].sequence) - previous == 1

def test_part_deletion():
    previous = len(scop.parts[0].sequence)
    scop.parts[0].delete(1)
    assert len(scop.parts[0].sequence) - previous == -6