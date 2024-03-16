import pytest
import component
import geometryObjects

@pytest.mark.parametrize('input, expected', [((None, None), False), ((2, 3), True), ((None, 2), False)])
def test_isCoordsValid(input, expected):
    x, y = input
    point = geometryObjects.Point(x, y)
    testedComponent = component.Component('1')
    testedComponent.setCoords(point)
    assert testedComponent.isCoordsValid() == expected

def test_calculateCenterFromPins():
    testedComponent = component.Component('1')
    testedComponent.addPin('1', geometryObjects.Point(-1, -1), 'net1')
    testedComponent.addPin('2', geometryObjects.Point(3, 2), 'net1')
    testedComponent.addPin('3', geometryObjects.Point(-1, 1), 'net1')
    testedComponent.addPin('4', geometryObjects.Point(2, 0), 'net1')
    testedComponent.calculateCenterFromPins()
    assert testedComponent.coords.x == 1 and testedComponent.coords.y == 0.5