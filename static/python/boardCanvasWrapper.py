import geometryObjects as gobj
import component as comp
import pin, board
import loaderSelectorFactory

class BoardCanvasWrapper():
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.baseBoard = None

    def setBaseBoard(self, boardInstace:board.Board):
        self.baseBoard = boardInstace

    def normalizeBoard(self):
        pass

    def _calculateBaseScale(self):
        pass

    def _cacluclateBaseOffset(self):
        pass

