import geometryObjects as gobj
import component as comp
import pin, board
import loaderSelectorFactory

class BoardCanvasWrapper():
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.baseBoard = None
        self.baseScale = 0.0

    def loadAndSetBaseBoard(self, filePath:str):
        boardInstance = self._loadBaseBoard(filePath)
        self._setBaseBoard(boardInstance)
    
    def normalizeBoard(self):
        self._calculateBaseScale(self.baseBoard.getArea())

    def _loadBaseBoard(self, filePath:str) -> board.Board:
        fileExtension  = filePath.split('.')[-1]
        loader = loaderSelectorFactory.LoaderSelectorFactory(fileExtension)
        fileLines = loader.loadFile(filePath)
        return loader.processFileLines(fileLines)

    def _setBaseBoard(self, boardInstace:board.Board):
        self.baseBoard = boardInstace

    def _calculateBaseScale(self, boardArea:tuple[gobj.Point, gobj.Point]):
        bottomLeftPoint, topRightPoint = boardArea
        x0, y0 = bottomLeftPoint.getXY()
        x1, y1 = topRightPoint.getXY()

        areaWidth = abs(x1 - x0)
        areaHeight = abs(y1 - y0)
        
        FITNESS_SCALE_FACTOR = 0.9
        minCanvasDimension = FITNESS_SCALE_FACTOR * min(self.width, self.height)
        maxBoardDimension = max(areaWidth, areaHeight)
        baseScale = minCanvasDimension / maxBoardDimension
        self._setBaseScale(baseScale)
    
    def _setBaseScale(self, baseScale:float):
        self.baseScale = baseScale
        
    def _cacluclateBaseOffset(self):
        pass

if __name__ == '__main__':
    normalizedBoard = BoardCanvasWrapper(1200, 700)
    normalizedBoard.loadAndSetBaseBoard(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\lvm Core.cad')
    normalizedBoard.normalizeBoard()

