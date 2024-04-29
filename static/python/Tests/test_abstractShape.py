import pytest
from abstractShape import Shape
import geometryObjects as gobj

@pytest.fixture
def shape1():
    exampleShape = Shape('1')
    exampleShape.setCoords((gobj.Point(0, 0)))
    exampleShape.setDimensions(2, 4)
    return exampleShape

@pytest.fixture
def shape2():
    exampleShape = Shape('2')
    exampleShape.setArea(gobj.Point(-3, -2), gobj.Point(1, 2))
    return exampleShape

def test_calculateArea(shape1):
    shape1.calculateAreaFromWidthHeightCoords()
    assert shape1.getArea() == [gobj.Point(-1, -2), gobj.Point(1, 2)]

def test_calculateShapeData(shape2):
    shape2.setShape('RECT')
    shape2.caluclateShapeData()
    assert shape2.shapeData == gobj.Rectangle(gobj.Point(-3, -2), gobj.Point(1, 2))

    shape2.setShape('CIRCLE')
    shape2.caluclateShapeData()
    assert shape2.shapeData == gobj.Circle(gobj.Point(-1, 0), 2)

def test_calculateCenterDimensionsFromArea(shape2):
    shape2.calculateCenterDimensionsFromArea()
    assert shape2.getCoords() == gobj.Point(-1, 0)
    assert shape2.width == 4
    assert shape2.height == 4

def test_translateInPlace(shape1):
    shape1.calculateAreaFromWidthHeightCoords()
    shape1.setShape('RECT')
    shape1.caluclateShapeData()

    shape1.translateInPlace([-1, 0.5])
    assert shape1.getCoords() == gobj.Point(-1, 0.5)
    assert shape1.getArea() == [gobj.Point(-2, -1.5), gobj.Point(0, 2.5)]
    assert shape1.getShapePoints() == [gobj.Point(-2, -1.5), gobj.Point(0, -1.5), gobj.Point(0, 2.5), gobj.Point(-2, 2.5)]

    shape1.setShape('CIRCLE') #verify calculations -> area is not a square
    shape1.caluclateShapeData()
    shape1.translateInPlace([1, -0.5])
    assert shape1.getShapePoints() == [gobj.Point(0, 0)]

def test_rotateInPlace(shape1):
    gobj.Point.DECIMAL_POINT_PRECISION = 3
    shape1.calculateAreaFromWidthHeightCoords()
    shape1.setShape('RECT')
    shape1.caluclateShapeData()
    
    shape1.rotateInPlace(gobj.Point(0, 0), 45)
    assert shape1.getCoords() == gobj.Point(0, 0)
    assert shape1.getArea() == [gobj.Point(-0.707, -2.121), gobj.Point(0.707, 2.121)]
    assert shape1.getShapePoints() == [gobj.Point(0.707, -2.121), gobj.Point(2.121, -0.707), gobj.Point(-0.707, 2.121), gobj.Point(-2.121, 0.707)]

def test_rotateInPlace_normalizeShapePoints(shape1):
    gobj.Point.DECIMAL_POINT_PRECISION = 3
    shape1.calculateAreaFromWidthHeightCoords()
    shape1.setShape('RECT')
    shape1.caluclateShapeData()
    
    shape1.rotateInPlace(gobj.Point(0, 0), 45)
    shape1.normalizeArea(shape1.getArea() + shape1.getShapePoints())
    assert shape1.getCoords() == gobj.Point(0, 0)
    assert shape1.getArea() == [gobj.Point(-2.121, -2.121), gobj.Point(2.121, 2.121)]
    assert shape1.getShapePoints() == [gobj.Point(0.707, -2.121), gobj.Point(2.121, -0.707), gobj.Point(-0.707, 2.121), gobj.Point(-2.121, 0.707)]