import pytest
import geometryObjects as gobj

def test_PointEqual():
    pointA = gobj.Point(0, 0)
    pointB = gobj.Point(1.2, 1.2)
    pointC = gobj.Point(1.200, 1.200)
    pointD = gobj.Point(1.201, 1.199)
    pointE = gobj.Point(1.202, 1.198)
    assert pointA != pointB
    assert pointB == pointC
    assert pointC == pointD
    assert pointC != pointE

def test_minXYCoords():
    minPoint = gobj.Point(float('Inf'), float('Inf'))
    point1 = gobj.Point(float(-10), float(23)) 
    minPoint = gobj.Point.minXYCoords(minPoint, point1)
    assert minPoint == gobj.Point(float(-10), float(23))

    point2 = gobj.Point(float(23), float(-10))
    minPoint = gobj.Point.minXYCoords(minPoint, point2)
    assert minPoint == gobj.Point(float(-10), float(-10))

    point3 = gobj.Point(float(2), float(1.79))
    minPoint = gobj.Point.minXYCoords(minPoint, point3)
    assert minPoint == gobj.Point(float(-10), float(-10))

def test_maxXYCoords():
    maxPoint = gobj.Point(float('-Inf'), float('-Inf'))
    point1 = gobj.Point(float(-10), float(23)) 
    maxPoint = gobj.Point.maxXYCoords(maxPoint, point1)
    assert maxPoint == gobj.Point(float(-10), float(23))
    
    point2 = gobj.Point(float(23), float(-9))
    maxPoint = gobj.Point.maxXYCoords(maxPoint, point2)
    assert maxPoint == gobj.Point(float(23), float(23))

    point3 = gobj.Point(float(2.09), float(-11.79))
    maxPoint = gobj.Point.maxXYCoords(maxPoint, point3)
    assert maxPoint == gobj.Point(float(23), float(23))

def test_minXY_maxXYCoords():
    minPoint = gobj.Point(float('Inf'), float('Inf'))
    maxPoint = gobj.Point(float('-Inf'), float('-Inf'))
    point1 = gobj.Point(float(-10), float(23)) 
    minPoint, maxPoint = gobj.Point.minXY_maxXYCoords(minPoint, maxPoint, point1)
    assert minPoint == gobj.Point(float(-10), float(23))
    assert maxPoint == gobj.Point(float(-10), float(23))

    point2 = gobj.Point(float(23), float(-9))
    minPoint, maxPoint = gobj.Point.minXY_maxXYCoords(minPoint, maxPoint, point2)
    assert minPoint == gobj.Point(float(-10), float(-9))
    assert maxPoint == gobj.Point(float(23), float(23))

    point3 = gobj.Point(float(-20), float(24.79))
    minPoint, maxPoint = gobj.Point.minXY_maxXYCoords(minPoint, maxPoint, point3)
    assert minPoint == gobj.Point(float(-20), float(-9))
    assert maxPoint == gobj.Point(float(23), float(24.79))

    point4 = gobj.Point(float(0), float(0))
    minPoint, maxPoint = gobj.Point.minXY_maxXYCoords(minPoint, maxPoint, point4)
    assert minPoint == gobj.Point(float(-20), float(-9))
    assert maxPoint == gobj.Point(float(23), float(24.79))

def test_PointRepr():
    pointB = gobj.Point(1.2, 1.2)
    repr = pointB.__str__()
    assert repr == 'Point x=1.2, y=1.2'
 
def test_LineEqual():
    pointA = gobj.Point(0, 0)
    pointB = gobj.Point(1.2, 1.2)
    pointC = gobj.Point(1, -1)
    line1 = gobj.Line(pointA, pointB)
    line2 = gobj.Line(pointB, pointA)
    line3 = gobj.Line(pointC, pointA)
    assert line1 == line2
    assert line1 != line3

@pytest.mark.parametrize('input, expected', [('1', 1.0), (' ', None),('-1.0', -1.0), ('10.123', 10.123), ('0', 0.0), ('1y9897a', None),])
def test_floatOrNone(input, expected):
    assert gobj.floatOrNone(input) == expected

def test_ArcEqual():
    pointA = gobj.Point(0, 0)
    pointB = gobj.Point(1.2, 1.2)
    pointC = gobj.Point(1, -1)
    arc1 = gobj.Arc(pointA, pointB, pointC)
    arc2 = gobj.Arc(pointB, pointA, pointC)
    arc3 = gobj.Arc(pointA, pointC, pointC)
    arc4 = gobj.Arc(pointC, pointB, pointC)
    arc5 = gobj.Arc(pointA, pointB, pointA)
    assert arc1 == arc1
    assert arc1 != arc2
    assert arc1 != arc3
    assert arc1 != arc4
    assert arc1 != arc5

def test_CircleEqual():
    c1 = gobj.Circle(gobj.Point(0, 0), 1)
    c2 = gobj.Circle(gobj.Point(1, 0), 1)
    c3 = gobj.Circle(gobj.Point(0, 0), 2)
    c4 = gobj.Circle(gobj.Point(1, 0), 2)
    assert c1 == c1
    assert c1 != c2
    assert c1 != c3
    assert c1 != c4