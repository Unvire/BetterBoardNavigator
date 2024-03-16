import pytest
import geometryObjects

def test_PointEqual():
    pointA = geometryObjects.Point(0, 0)
    pointB = geometryObjects.Point(1.2, 1.2)
    pointC = geometryObjects.Point(1.200, 1.200)
    pointD = geometryObjects.Point(1.201, 1.199)
    pointE = geometryObjects.Point(1.202, 1.198)
    assert pointA != pointB
    assert pointB == pointC
    assert pointC == pointD
    assert pointC != pointE

def test_minXYCoords():
    minPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    point1 = geometryObjects.Point(float(-10), float(23)) 
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point1)
    assert minPoint == geometryObjects.Point(float(-10), float(23))

    point2 = geometryObjects.Point(float(23), float(-10))
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point2)
    assert minPoint == geometryObjects.Point(float(-10), float(-10))

    point3 = geometryObjects.Point(float(2), float(1.79))
    minPoint = geometryObjects.Point.minXYCoords(minPoint, point3)
    assert minPoint == geometryObjects.Point(float(-10), float(-10))

def test_maxXYCoords():
    maxPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
    point1 = geometryObjects.Point(float(-10), float(23)) 
    maxPoint = geometryObjects.Point.maxXYCoords(maxPoint, point1)
    assert maxPoint == geometryObjects.Point(float(-10), float(23))
    
    point2 = geometryObjects.Point(float(23), float(-9))
    maxPoint = geometryObjects.Point.maxXYCoords(maxPoint, point2)
    assert maxPoint == geometryObjects.Point(float(23), float(23))

    point3 = geometryObjects.Point(float(2.09), float(-11.79))
    maxPoint = geometryObjects.Point.maxXYCoords(maxPoint, point3)
    assert maxPoint == geometryObjects.Point(float(23), float(23))

def test_minXY_maxXYCoords():
    minPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    maxPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
    point1 = geometryObjects.Point(float(-10), float(23)) 
    minPoint, maxPoint = geometryObjects.Point.minXY_maxXYCoords(minPoint, maxPoint, point1)
    assert minPoint == geometryObjects.Point(float(-10), float(23))
    assert maxPoint == geometryObjects.Point(float(-10), float(23))

    point2 = geometryObjects.Point(float(23), float(-9))
    minPoint, maxPoint = geometryObjects.Point.minXY_maxXYCoords(minPoint, maxPoint, point2)
    assert minPoint == geometryObjects.Point(float(-10), float(-9))
    assert maxPoint == geometryObjects.Point(float(23), float(23))

    point3 = geometryObjects.Point(float(-20), float(24.79))
    minPoint, maxPoint = geometryObjects.Point.minXY_maxXYCoords(minPoint, maxPoint, point3)
    assert minPoint == geometryObjects.Point(float(-20), float(-9))
    assert maxPoint == geometryObjects.Point(float(23), float(24.79))

    point4 = geometryObjects.Point(float(0), float(0))
    minPoint, maxPoint = geometryObjects.Point.minXY_maxXYCoords(minPoint, maxPoint, point4)
    assert minPoint == geometryObjects.Point(float(-20), float(-9))
    assert maxPoint == geometryObjects.Point(float(23), float(24.79))

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
