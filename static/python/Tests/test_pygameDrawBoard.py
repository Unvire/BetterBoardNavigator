import pytest
from pygameDrawBoard import DrawBoardEngine
import board

def test__calculateOffsetVectorForScaledSurface():
    engine = DrawBoardEngine(1200, 700)
    engine.offsetVector = [-50, -50]
    zoomingPoint = [300, 300]
    
    ## scale up -> 1 * 1.3
    engine._scaleSurfaceDimensionsByFactor(1.3)
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1)
    assert newOffset == (-155, -155)

    ## scale up -> 1 * 1.3 * 1.3
    engine._scaleSurfaceDimensionsByFactor(1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1.3)
    assert newOffset == (-292, -292)

    ## scale down -> 1 * 1.3
    engine._scaleSurfaceDimensionsByFactor(1 / 1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1.3 * 1.3)
    assert newOffset == (-155, -155)

    ## scale down -> 1
    engine._scaleSurfaceDimensionsByFactor(1 / 1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1.3)
    assert newOffset == (-50, -50)

    ## scale down -> 1 * 0.7
    engine._scaleSurfaceDimensionsByFactor(1 / 1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1)
    assert newOffset == (31, 31)

    ## scale down -> 1 * 0.7 * 0.4
    engine._scaleSurfaceDimensionsByFactor(1 / 1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1 / 1.3)
    assert newOffset == (93, 93)

    ## scale up -> 1 * 0.7
    engine._scaleSurfaceDimensionsByFactor(1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1 / 1.3 / 1.3)
    assert newOffset == (31, 31)

    ## scale up -> 1
    engine._scaleSurfaceDimensionsByFactor(1.3)
    engine.offsetVector = newOffset
    newOffset = engine._calculateOffsetVectorForScaledSurface(zoomingPoint, 1 / 1.3)
    assert newOffset == (-50, -50)

def test_getComponents():
    boardInstance = board.Board()
    boardInstance.components = {'HOLE': '', 
                                'C10': '',
                                'C11': '',
                                'C13': '',
                                'C2': '',
                                'C20': '',
                                'R7': '',
                                'R19': '',
                                'R1': '',
                                'P2_U7_COMP':'',
                                '2D-CODE':''}
    engine = DrawBoardEngine(1200, 700)
    engine.boardData = boardInstance

    print(engine.getComponents())
    expected = ['2D-CODE', 'C2', 'C10', 'C11', 'C13', 'C20', 'P2_U7_COMP', 'R1', 'R7', 'R19', 'HOLE']
    assert engine.getComponents() == expected