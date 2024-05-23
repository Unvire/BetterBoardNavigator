import pytest
from boardCanvasWrapper import BoardCanvasWrapper
import geometryObjects as gobj

@pytest.fixture
def scaleAndOffsetCalculationData():
    inputData = [[gobj.Point(0, 0), gobj.Point(10, 10)], 
                [gobj.Point(-10, 0), gobj.Point(0, 10)],
                [gobj.Point(-10, -10), gobj.Point(0, 0)],
                [gobj.Point(0, -10), gobj.Point(10, 0)],
                [gobj.Point(0, 0), gobj.Point(0.1, 0.1)],
                [gobj.Point(-0.1, 0), gobj.Point(0, 0.1)],
                [gobj.Point(-0.1, -0.1), gobj.Point(0, 0)],
                [gobj.Point(0, -0.1), gobj.Point(0.1, 0)], 
                [gobj.Point(0, 0), gobj.Point(10000, 10000)],
                [gobj.Point(-10000, 0), gobj.Point(0, 10000)],
                [gobj.Point(-10000, -10000), gobj.Point(0, 0)],
                [gobj.Point(0, -10000), gobj.Point(10000, 0)],
                [gobj.Point(-10, -10), gobj.Point(10, 10)],
                [gobj.Point(-0.1, -0.1), gobj.Point(0.1, 0.1)],
                [gobj.Point(-10000, -10000), gobj.Point(10000, 10000)]]
    return inputData

def test_calculateAndSetBaseScale(scaleAndOffsetCalculationData):
    expected = [63, 63, 63, 63, 6300, 6300, 6300, 6300, 0.063, 0.063, 0.063, 0.063, 31.5, 3150, 0.0315]
    instance = BoardCanvasWrapper(1200, 700)
    for area, result in zip(scaleAndOffsetCalculationData, expected):
        instance._calculateAndSetBaseScale(area)
        assert round(instance.baseScale - result, 6) == 0