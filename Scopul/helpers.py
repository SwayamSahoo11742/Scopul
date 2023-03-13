from music21 import tempo
from collections.abc import Iterable
from mido import tempo2bpm, bpm2tempo

def sublist(lst, sublist, overlap=False):
    """
    Finds all occurrences of a sublist in a list and returns a list of nested lists containing the indices of each occurrence.

    Parameters:
    lst (list): The list to search for sublists.
    sublist (list): The sublist to search for in the list.
    overlap (bool, optional): Whether to include overlapping sublist occurrences. Defaults to False.

    Returns:
    list: A list of nested lists containing the indices of each occurrence of the sublist in the list. If overlap is False, non-overlapping sublist occurrences are returned. If overlap is True, all sublist occurrences (including overlapping ones) are returned.
    """

    # Create an empty list to store the sublists that are found
    sublists = []

    # Initialize a counter variable
    i = 0

    # Loop through the list
    while i < len(lst) - len(sublist) + 1:

        # Check if the sublist is found at this position
        if lst[i : i + len(sublist)] == sublist:

            # If it is found, save the start and end indices of the sublist
            start = i
            end = i + len(sublist) - 1

            # If overlap is True, check for additional occurrences of the sublist that overlap with this one
            if overlap:
                i += 1
                while (
                    i < len(lst) - len(sublist) + 1
                    and lst[i : i + len(sublist)] == sublist
                ):
                    end += len(sublist)
                    i += len(sublist)

            # Add the indices of this sublist to the list of sublists
            sublists.append(list(range(start, end + 1)))

            # Move the counter to the next position after the sublist
            i = end + 1

        # If the sublist is not found at this position, move the counter to the next position
        else:
            i += 1

    # Return the list of sublists
    return sublists


def get_tempos(midi):
    lst = []
    for meta_message in midi.flat:
        if isinstance(meta_message, tempo.MetronomeMark):
            lst.append(
                {"tempo": meta_message.number, "measure": meta_message.measureNumber}
            )

    return lst

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