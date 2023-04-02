from filter import filter_string
import pytest


def test_1():
    assert(filter_string("Hello, my name is Mr O'Toole.") == ",'.")
def test_value():
    with pytest.raises(ValueError):
        filter_string("123123")
def test_2():
    assert(filter_string("a!??,bc")== "!??,")
def test_3():
    assert(filter_string("F:ad.i")== ":.")

