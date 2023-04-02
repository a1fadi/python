from praccy import praccy

def test_praccy_1():
    assert praccy(1) == 1

def test_praccy_3():
    assert praccy(3) == 6

def test_praccy_string():
    assert praccy("a") == 0

def test_praccy_1213():
    assert praccy(1213) == 736291
