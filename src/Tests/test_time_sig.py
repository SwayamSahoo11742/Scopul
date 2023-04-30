import os
import sys
import inspect
import pytest

# Importing from parent Scopul
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Scopul import Scopul


# Setting files and declaring a Scop
file1 = "testfiles/test1.mid"
file2 = "testfiles/test2.mid"
scop = Scopul(file1)


# Tetsing time ratio
def test_time_ratio():
    # Testing Ratios
    assert scop.time_sig_list[0].ratio == "6/8"
    # Testing setter error


# Test Fractional parts, (Numerator/Denominators)
def test_fraction():

    # Tetsing values
    scop.path = file1
    assert scop.time_sig_list[0].denominator == 8
    assert scop.time_sig_list[0].numerator == 6





# Test time signature list
def test_list():
    scop.audio = file1
    # Tetsing values
    assert scop.time_sig_list[0].ratio == "6/8"
    assert scop.time_sig_list[0].measure == 1

