import pytest
import point

def test_equal():
    pointA = point.Point(0, 0)
    pointB = point.Point(1.2, 1.2)
    pointC = point.Point(1.2, 1.2)
    assert pointA != pointB
    assert pointB == pointC