import pytest
import geometryObjects

def test_PointRqual():
    pointA = geometryObjects.Point(0, 0)
    pointB = geometryObjects.Point(1.2, 1.2)
    pointC = geometryObjects.Point(1.2, 1.2)
    assert pointA != pointB
    assert pointB == pointC

def test__minXY():
    minPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    point1 = geometryObjects.Point(float(-10), float(23)) 
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point1)
    print(minPoint)
    assert minPoint == geometryObjects.Point(float(-10), float(23))

    point2 = geometryObjects.Point(float(23), float(-10))
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point2)
    assert minPoint == geometryObjects.Point(float(-10), float(-10))

    point3 = geometryObjects.Point(float(2), float(1.79))
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point3)
    assert minPoint == geometryObjects.Point(float(-10), float(-10))

def test_PointRepr():
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
