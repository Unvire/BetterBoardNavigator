import pytest
import component
import geometryObjects

@pytest.fixture
def componentForPinsCalculation():
    testedComponent = component.Component('1')
    testedComponent.addPin('1', geometryObjects.Point(-1, -1), 'net1')
    testedComponent.addPin('2', geometryObjects.Point(3, 2), 'net1')
    testedComponent.addPin('3', geometryObjects.Point(-1, 1), 'net1')
    testedComponent.addPin('4', geometryObjects.Point(2, 0), 'net1')
    return testedComponent

@pytest.mark.parametrize('input, expected', [((None, None), False), ((2, 3), True), ((None, 2), False)])
def test_isCoordsValid(input, expected):
    x, y = input
    point = geometryObjects.Point(x, y)
    testedComponent = component.Component('1')
    testedComponent.setCoords(point)
    assert testedComponent.isCoordsValid() == expected

def test_calculateHitBoxFromPins(componentForPinsCalculation):
    point1, point2 = componentForPinsCalculation.calculateHitBoxFromPins()
    assert point1 == geometryObjects.Point(-1, -1)
    assert point2 == geometryObjects.Point(3, 2)

def test_calculateCenterFromPins(componentForPinsCalculation):    
    componentForPinsCalculation.calculateCenterFromPins()
    assert componentForPinsCalculation.coords.x == 1 and componentForPinsCalculation.coords.y == 0.5

def test_calculatePackageFromPins(componentForPinsCalculation):
    componentForPinsCalculation.calculatePackageFromPins()
    point1, point2 = componentForPinsCalculation.package
    assert point1 == geometryObjects.Point(-0.95, -0.95)
    assert point2 == geometryObjects.Point(2.85, 1.9)