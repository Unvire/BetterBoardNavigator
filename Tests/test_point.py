import pytest
import point

def test_equal():
    pointA = point.Point(0, 0)
    pointB = point.Point(1.2, 1.2)
    pointC = point.Point(1.2, 1.2)
    assert pointA != pointB
    assert pointB == pointC

def test_repr():
    pointB = point.Point(1.2, 1.2)
    repr = pointB.__str__()
    assert repr == 'Point x=1.2, y=1.2'
