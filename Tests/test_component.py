import pytest
import pin
import component as comp
import geometryObjects as gobj

@pytest.fixture
def componentForPinsCalculation():
    testedComponent = comp.Component('1')
    pad1 = pin.Pin('1') 
    pad2 = pin.Pin('2')
    pad3 = pin.Pin('3')
    pad4 = pin.Pin('4')

    pad1.setCoords(gobj.Point(-1, -1))
    pad2.setCoords(gobj.Point(3, 2))
    pad3.setCoords(gobj.Point(-1, 1))
    pad4.setCoords(gobj.Point(2, 0))

    testedComponent.addPin('1', pad1)
    testedComponent.addPin('2', pad2)
    testedComponent.addPin('3', pad3)
    testedComponent.addPin('4', pad4)
    return testedComponent

@pytest.fixture
def componentForRotateTranslate():
    testedComponent = comp.Component('test')
    testedComponent.setCoords(gobj.Point(0, 0))
    testedComponent.setComponentArea(gobj.Point(-4, -2), gobj.Point(4, 2))

    pad1 = pin.Pin('1')
    pad1.setCoords(gobj.Point(-2, -1)) 
    pad1.setDimensions(1, 1)
    pad1.calculateArea()

    pad2 = pin.Pin('2')
    pad2.setCoords(gobj.Point(2, 1))
    pad2.setDimensions(1, 1)
    pad2.calculateArea()

    testedComponent.addPin('1', pad1)
    testedComponent.addPin('2', pad2)
    return testedComponent

@pytest.mark.parametrize('input, expected', [((None, None), False), ((2, 3), True), ((None, 2), False)])
def test_isCoordsValid(input, expected):
    x, y = input
    point = gobj.Point(x, y)
    testedComponent = comp.Component('1')
    testedComponent.setCoords(point)
    assert testedComponent.isCoordsValid() == expected

def test_calculateHitBoxFromPins(componentForPinsCalculation):
    point1, point2 = componentForPinsCalculation.calculateHitBoxFromPins()
    assert point1 == gobj.Point(-1, -1)
    assert point2 == gobj.Point(3, 2)

def test_calculateCenterFromPins(componentForPinsCalculation):    
    componentForPinsCalculation.calculateCenterFromPins()
    assert componentForPinsCalculation.coords.x == 1 and componentForPinsCalculation.coords.y == 0.5

def test_calculatePackageFromPins(componentForPinsCalculation):
    componentForPinsCalculation.calculatePackageFromPins()
    point1, point2 = componentForPinsCalculation.componentArea
    assert point1 == gobj.Point(-0.95, -0.95)
    assert point2 == gobj.Point(2.85, 1.9)

def test_translateInPlace(componentForRotateTranslate):
    componentForRotateTranslate.translateInPlace([10, 10])
    
    assert componentForRotateTranslate.getCoords() == gobj.Point(10, 10)
    assert componentForRotateTranslate.getComponentArea() == [gobj.Point(6, 8), gobj.Point(14, 12)]

    pin1 = componentForRotateTranslate.getPinByName('1')
    assert pin1.getCoords() == gobj.Point(8, 9)
    assert pin1.getPinArea() == [gobj.Point(7.5, 8.5), gobj.Point(8.5, 9.5)] # before translation: (-2.5, -1.5), (-1.5, 0.5)

    pin2 = componentForRotateTranslate.getPinByName('2')
    assert pin2.getCoords() == gobj.Point(12, 11)
    assert pin2.getPinArea() == [gobj.Point(11.5, 10.5), gobj.Point(12.5, 11.5)] # before translation: (1.5, 0.5), (2.5, 1.5)