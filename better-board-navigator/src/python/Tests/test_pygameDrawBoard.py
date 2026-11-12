import pytest
from pygameDrawBoard import DrawBoardEngine
import board

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