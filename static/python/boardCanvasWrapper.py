import copy
import geometryObjects as gobj
import component as comp
import pin, board
import loaderSelectorFactory

class BoardCanvasWrapper():
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.board = None
        self.boardBackup = None
        self.baseScale = 0.0
        self.baseMoveOffsetXY = [0.0, 0.0]
        self.sideComponents = {}
        self.commonTypeComponents = {}
        self.hitMap = {}
        self._resetGroupsToDefault()

    def loadAndSetBoardFromFilePath(self, filePath:str):
        boardInstance = self._loadBaseBoard(filePath)
        self._setBoard(boardInstance)
    
    def loadAndSetBoardFromFileLines(self, fileName:str, fileLines:list[str]):
        loader = loaderSelectorFactory.LoaderSelectorFactory(fileName)
        boardInstace = loader.processFileLines(fileLines)
        self._setBoard(boardInstace)
    
    def normalizeBoard(self):
        self._calculateAndSetBaseScale(self.board.getArea())
        self._calculateAndSetBaseOffsetXY(self.board.getArea())
        try:
            self._recalculateAndGroupComponents(self.board.getComponents())
            self._resizeAndMoveShapes(self.board.getOutlines())
            self._resizeAndMoveTracks(self.board.getTracks())
        except KeyError:
            print('again')
            self.board = copy.deepcopy(self.boardBackup)
            self.board.calculateAreaFromComponents()
            self._resetGroupsToDefault()
            self.normalizeBoard()
        
    def _loadBaseBoard(self, filePath:str) -> board.Board:
        fileExtension  = filePath.split('.')[-1]
        loader = loaderSelectorFactory.LoaderSelectorFactory(fileExtension)
        fileLines = loader.loadFile(filePath)
        return loader.processFileLines(fileLines)

    def _setBoard(self, boardInstace:board.Board):
        self.board = boardInstace
        self.boardBackup = copy.deepcopy(self.board)        

    def _calculateAndSetBaseScale(self, boardArea:tuple[gobj.Point, gobj.Point]):
        x0, y0, x1, y1 = self._getBoardAreaCoordsAsXYXY(boardArea)
        areaWidth = abs(x1 - x0)
        areaHeight = abs(y1 - y0)
        
        FITNESS_SCALE_FACTOR = 0.9
        scaleX = self.width / areaWidth
        scaleY = self.height / areaHeight
        baseScale = min(scaleX, scaleY) * FITNESS_SCALE_FACTOR 
        self._setBaseScale(baseScale)
    
    def _setBaseScale(self, baseScale:float):
        self.baseScale = baseScale
        
    def _calculateAndSetBaseOffsetXY(self, boardArea:tuple[gobj.Point, gobj.Point]):
        x0, y0, x1, y1 = self._getBoardAreaCoordsAsXYXY(boardArea)
        
        xMidScaled = (x1 + x0) / 2 * self.baseScale
        yMidScaled = (y1 + y0) / 2 * self.baseScale
        xTarget = self.width // 2
        yTarget = self.height // 2

        xMove, yMove = xTarget - xMidScaled, yTarget - yMidScaled
        self._setBaseMoveOffsetXY(xMove, yMove)

    def _setBaseMoveOffsetXY(self, x:float, y:float):
        self.baseMoveOffsetXY = [x, y]    
    
    def _resizeAndMoveTracks(self, tracksDict:dict):
        for _, sidesDict in tracksDict.items():
            for _, shapesList in sidesDict.items():
                self._resizeAndMoveShapes(shapesList)

    def _resizeAndMoveShapes(self, shapesList:list):
        for shape in shapesList:
            pointList = shape.getPoints()
            for point in pointList:
                point.scaleInPlace(self.baseScale)   
                point.translateInPlace(self.baseMoveOffsetXY)
            if isinstance(shape, gobj.Arc):
                shape.calculateAngleRadRepresentation
    
    def _recalculateAndGroupComponents(self, componentsDict:dict):
        for _, componentInstance in componentsDict.items():
            self._recalculateComponent(componentInstance)
            self._addComponentToHitMap(componentInstance)
            self._addComponentToSideComponents(componentInstance)
            self._addComponentToCommonTypeComponents(componentInstance)
    

    def _recalculateComponent(self, componentInstance:comp.Component):
        componentInstance.scaleInPlace(self.baseScale)
        componentInstance.translateInPlace(self.baseMoveOffsetXY)

    def _addComponentToHitMap(self, componentInstance:comp.Component):
        for point in componentInstance.getArea():
            x, y  = point.getXY()
            keyX, keyY = int(x / 100),  int(y / 100)
            side = componentInstance.getSide()
            self.hitMap[side][keyX][keyY].append(componentInstance.name)        

    def _addComponentToSideComponents(self, componentInstance:comp.Component):
        side = componentInstance.getSide()
        mountType = componentInstance.getMountingType()
        if mountType == 'TH':
            self.sideComponents['B'].append(componentInstance.name)
            self.sideComponents['T'].append(componentInstance.name)
        else:
            self.sideComponents[side].append(componentInstance.name)

    def _addComponentToCommonTypeComponents(self, componentInstance:comp.Component):
        def findNonNumericPrefix(s:str) -> str:
            result = ''
            for char in s:
                if char.isnumeric():
                    return result
                result += char
            
        prefix = findNonNumericPrefix(componentInstance.name)
        self.commonTypeComponents['B'].setdefault(prefix, [])
        self.commonTypeComponents['T'].setdefault(prefix, [])

        side = componentInstance.getSide()
        self.commonTypeComponents[side][prefix].append(componentInstance.name)

    def _getBoardAreaCoordsAsXYXY(self, boardArea:tuple[gobj.Point, gobj.Point]) -> tuple[float, float, float, float]:
        bottomLeftPoint, topRightPoint = boardArea
        xBL, yBL = bottomLeftPoint.getXY()
        xTR, yTR = topRightPoint.getXY()
        return xBL, yBL, xTR, yTR
    
    def _resetGroupsToDefault(self):
        self.sideComponents = {'B':[], 'T':[]}
        self.commonTypeComponents = {'B':{}, 'T':{}}
        self.hitMap = {'B':{}, 'T':{}}
        self._initHitmap()
    
    def _initHitmap(self):
        rangeWidth = range(int(self.width / 100))
        rangeHeight = range(int(self.height / 100))
        for side in ['T', 'B']:
            self.hitMap[side] = {}
            for w in rangeWidth:
                self.hitMap[side][w] = {}
                for h in rangeHeight:
                    self.hitMap[side][w][h] = []
    

if __name__ == '__main__':
    normalizedBoard = BoardCanvasWrapper(1200, 700)
    normalizedBoard.loadAndSetBoardFromFilePath(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\lvm core.cad')
    normalizedBoard.normalizeBoard()