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

def test_calculateCenterDimensionsFromArea(shape2):
    shape2.calculateCenterDimensionsFromArea()
    assert shape2.getCoords() == gobj.Point(-1, 0)
    assert shape2.width == 4
    assert shape2.height == 4

def test_translateInPlace(shape1):
    shape1.calculateAreaFromWidthHeightCoords()
    shape1.translateInPlace([-1, 0.5])
    assert shape1.getCoords() == gobj.Point(-1, 0.5)
    assert shape1.getArea() == [gobj.Point(-2, -1.5), gobj.Point(0, 2.5)]

def test_rotateInPlace(shape1):
    shape1.calculateAreaFromWidthHeightCoords()
    shape1.rotateInPlace(gobj.Point(0, 0), 45)
    assert shape1.getCoords() == gobj.Point(0, 0)
    assert shape1.getArea() == [gobj.Point(-0.707, -2.121), gobj.Point(0.707, 2.121)]