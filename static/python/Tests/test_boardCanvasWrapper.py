import pytest
from boardCanvasWrapper import BoardCanvasWrapper
import geometryObjects as gobj

@pytest.mark.parametrize('inputData, expected', [([gobj.Point(0, 0), gobj.Point(10, 10)], 63), ([gobj.Point(-10, 0), gobj.Point(0, 10)], 63),
                                                ([gobj.Point(-10, -10), gobj.Point(0, 0)], 63), ([gobj.Point(0, -10), gobj.Point(10, 0)], 63),
                                                ([gobj.Point(0, 0), gobj.Point(0.1, 0.1)], 6300), ([gobj.Point(-0.1, 0), gobj.Point(0, 0.1)], 6300),
                                                ([gobj.Point(-0.1, -0.1), gobj.Point(0, 0)], 6300),([gobj.Point(0, -0.1), gobj.Point(0.1, 0)], 6300),
                                                ([gobj.Point(0, 0), gobj.Point(10000, 10000)], 0.063), ([gobj.Point(-10000, 0), gobj.Point(0, 10000)], 0.063),
                                                ([gobj.Point(-10000, -10000), gobj.Point(0, 0)], 0.063), ([gobj.Point(0, -10000), gobj.Point(10000, 0)], 0.063),
                                                ([gobj.Point(-10, -10), gobj.Point(10, 10)], 31.5), 
                                                ([gobj.Point(-0.1, -0.1), gobj.Point(0.1, 0.1)], 3150),
                                                ([gobj.Point(-10000, -10000), gobj.Point(10000, 10000)], 0.0315)
                                                ])
def test_calculateAndSetBaseScale(inputData, expected):
    instance = BoardCanvasWrapper(1200, 700)
    instance._calculateAndSetBaseScale(inputData)
    assert instance.baseScale == expected