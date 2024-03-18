import pytest
import pin
import geometryObjects

@pytest.fixture
def pin1():
    examplePin = pin.Pin('1')
    examplePin.setCoords((geometryObjects.Point(0, 0)))
    examplePin.setDimensions(2, 4)
    return examplePin

def test_calculateArea(pin1):
    pin1.calculateArea()
    assert pin1.pinArea == [geometryObjects.Point(-1, -2), geometryObjects.Point(1, 2)]