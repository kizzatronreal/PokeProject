import pytest
import main

def test_break_down_tuples():
    testlist = [[(1,), (0.5,), (1,)], [(0,), (1,), (0.5,)]]
    newlist = main.break_down_tuples(testlist)
    assert isinstance(newlist[0], list)
    assert isinstance(newlist[0][0], tuple) == False
    assert isinstance(newlist[1], list)
    assert isinstance(newlist[1][0], tuple) == False

