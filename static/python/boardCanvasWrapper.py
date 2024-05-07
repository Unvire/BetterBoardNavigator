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

    def _calculateBaseScale(self, boardArea:tuple[gobj.Point, gobj.Point]):
        bottomLeftPoint, topRightPoint = boardArea
        x0, y0 = bottomLeftPoint.getXY()
        x1, y1 = topRightPoint.getXY()

        areaWidth = abs(x1 - x0)
        areaHeight = abs(y1 - y0)
        print(areaWidth, areaHeight)

    def _cacluclateBaseOffset(self):
        pass

