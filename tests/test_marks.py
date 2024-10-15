from pytest import mark
import time


@mark.smoke
def test_1():
    time.sleep(1)
    assert True

@mark.smoke
def test_2():
    time.sleep(2)
    assert True

@mark.smoke
def test_3():
    assert False

@mark.smoke
def test_4():
    assert False