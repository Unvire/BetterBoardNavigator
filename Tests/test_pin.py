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

def test_translateInPlace(pin1):
    pin1.calculateArea()
    pin1.translateInPlace([-1, 0.5])
    assert pin1.getCoords() == gobj.Point(-1, 0.5)
    assert pin1.getPinArea() == [gobj.Point(-2, -1.5), gobj.Point(0, 2.5)]

def test_rotateInPlace(pin1):
    pin1.calculateArea()    
    print(pin1.getPinArea()[0], pin1.getPinArea()[1])
    pin1.rotateInPlace(gobj.Point(0, 0), 45)
    print(pin1.getPinArea()[0], pin1.getPinArea()[1])
    assert pin1.getCoords() == gobj.Point(0, 0)
    assert pin1.getPinArea() == [gobj.Point(-0.707, -2.121), gobj.Point(0.707, 2.121)]
