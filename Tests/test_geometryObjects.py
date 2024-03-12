import pytest
import geometryObjects

def test_Pointequal():
    pointA = geometryObjects.Point(0, 0)
    pointB = geometryObjects.Point(1.2, 1.2)
    pointC = geometryObjects.Point(1.2, 1.2)
    assert pointA != pointB
    assert pointB == pointC

def test_Pointrepr():
    pointB = geometryObjects.Point(1.2, 1.2)
    repr = pointB.__str__()
    assert repr == 'Point x=1.2, y=1.2'
