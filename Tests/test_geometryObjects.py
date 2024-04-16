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

@pytest.mark.parametrize('inputData, expected', [((0, 0, 0), gobj.Point(1, 1)), ((0, 0, 90), gobj.Point(-1, 1)), 
                                                 ((2, 2, 90), gobj.Point(3, 1)), ((1, 2, 90), gobj.Point(2, 2))])
def test_PointRotate(inputData, expected):
    xRotation, yRotation, angleDeg = inputData
    rotationPoint = gobj.Point(xRotation, yRotation)

    A = gobj.Point(1, 1)
    A.rotate(rotationPoint, angleDeg)
    assert A == expected

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

def test_PointScaleInPlace():
    pointA = gobj.Point(2, 2)
    pointA.scaleInPlace(0.5)
    assert [pointA.getX(), pointA.getY()] == [1, 1]
 
def test_PointTranslateInPlace():
    gobj.Point.DECIMAL_POINT_PRECISION = 3
    pointA = gobj.Point(2, 2)
    vector = [1.2345, -1.2345]

    pointA.translateInPlace(vector)
    errorX = abs(pointA.getX() - 3.235)
    errorY = abs(pointA.getY() - 0.766)
    decimalPrecision = 10 ** (-gobj.Point.DECIMAL_POINT_PRECISION)
    assert errorX <= decimalPrecision
    assert errorY <= decimalPrecision

def test_PointScale():
    pointA = gobj.Point(2, 2)
    pointB = gobj.Point.scale(pointA, 0.5)
    assert [pointA.getX(), pointA.getY()] == [2, 2]    
    assert [pointB.getX(), pointB.getY()] == [1, 1]

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

def test_RectangleEqual():
    r1 = gobj.Rectangle(gobj.Point(0, 0), gobj.Point(1, 1))
    r2 = gobj.Rectangle(gobj.Point(0, 0), gobj.Point(1.1, 1))
    r3 = gobj.Rectangle(gobj.Point(-1, 0), gobj.Point(1.1, 1))
    r4 = gobj.Rectangle(gobj.Point(-2, -2), gobj.Point(1.1, 11))
    assert r1 == r1
    assert r1 != r2
    assert r1 != r3
    assert r1 != r4

def test_getLineAndAreaFromNumArray():
    valArray = ['1967.441', '2267.244', '2026.496', '3267.244']    
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    shape, bottomLeftPoint, topRightPoint = gobj.getLineAndAreaFromNumArray(valArray, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Line(gobj.Point(1967.441, 2267.244), gobj.Point(2026.496, 3267.244))
    assert bottomLeftPoint == gobj.Point(1967.441, 2267.244)
    assert topRightPoint == gobj.Point(2026.496, 3267.244)

def test_getArcAndAreaFromValArray():
    valArray = ['996.063', '137.795', '956.693', '137.795', '976.378', '147.795']    
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    
    shape, bottomLeftPoint, topRightPoint = gobj.getArcAndAreaFromValArray(valArray, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Arc(gobj.Point(996.063, 137.795), gobj.Point(956.693, 137.795), gobj.Point(976.378, 147.795))
    assert bottomLeftPoint == gobj.Point(956.693, 137.795)
    assert topRightPoint == gobj.Point(996.063, 147.795)

def test_getCircleAndAreaFromValArray():
    valArray = ['-2.8661417', '2.527559', '0.08070866']
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    shape, bottomLeftPoint, topRightPoint = gobj.getCircleAndAreaFromValArray(valArray, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Circle(gobj.Point(-2.8661417, 2.527559), 0.08070866)
    assert bottomLeftPoint == gobj.Point(-2.94685036, 2.44685034)
    assert topRightPoint == gobj.Point(-2.78543304, 2.60826766)

def test_getRectangleAndAreaFromValArray():
    valArray = ['-0.02755896', '-0.03149596', '0.05511801', '0.06299203']
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    shape, bottomLeftPoint, topRightPoint = gobj.getRectangleAndAreaFromValArray(valArray, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Rectangle(gobj.Point(-0.02755896, -0.03149596), gobj.Point(-0.02755896 + 0.05511801, -0.03149596 + 0.06299203))
    assert bottomLeftPoint == gobj.Point(-0.02755896, -0.03149596)
    assert topRightPoint == gobj.Point(-0.02755896 + 0.05511801, -0.03149596 + 0.06299203)

def test_getSquareAndAreaFromValArray():
    valArray = ['-0.025', '-0.025', '0.025']
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    shape, bottomLeftPoint, topRightPoint = gobj.getSquareAndAreaFromValArray(valArray, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Rectangle(gobj.Point(-0.025, -0.025), gobj.Point(0.025, 0.025))
    assert bottomLeftPoint == gobj.Point(-0.025, -0.025)
    assert topRightPoint == gobj.Point(0.025, 0.025)