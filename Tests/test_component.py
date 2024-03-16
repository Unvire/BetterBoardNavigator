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