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
 
def test_LineEqual():
    pointA = geometryObjects.Point(0, 0)
    pointB = geometryObjects.Point(1.2, 1.2)
    pointC = geometryObjects.Point(1, -1)
    line1 = geometryObjects.Line(pointA, pointB)
    line2 = geometryObjects.Line(pointB, pointA)
    line3 = geometryObjects.Line(pointC, pointA)
    assert line1 == line2
    assert line1 != line3
