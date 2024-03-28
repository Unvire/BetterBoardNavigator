import pytest
import pin
import geometryObjects as gobj

@pytest.fixture
def pin1():
    examplePin = pin.Pin('1')
    examplePin.setCoords((gobj.Point(0, 0)))
    examplePin.setDimensions(2, 4)
    return examplePin

@pytest.fixture
def pin2():
    examplePin = pin.Pin('1')
    examplePin.setPinArea(gobj.Point(-3, -2), gobj.Point(1, 2))
    return examplePin

def test_calculateArea(pin1):
    pin1.calculateArea()
    assert pin1.pinArea == [gobj.Point(-1, -2), gobj.Point(1, 2)]

def test_calculateCenterDimensionsFromArea(pin2):
    pin2.calculateCenterDimensionsFromArea()
    assert pin2.coords == gobj.Point(-1, 0)
    assert pin2.width == 4
    assert pin2.height == 4