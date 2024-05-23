import copy
import geometryObjects as gobj
import component as comp
import board, loaderSelectorFactory
from abstractShape import Shape

class NormalizingError(Exception):
    pass

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
        self._resetGroupsToDefault()

    def loadAndSetBoardFromFilePath(self, filePath:str):
        boardInstance = self._loadBaseBoard(filePath)
        self.setBoard(boardInstance)
    
    def loadAndSetBoardFromFileLines(self, fileName:str, fileLines:list[str]):
        loader = loaderSelectorFactory.LoaderSelectorFactory(fileName)
        boardInstace = loader.processFileLines(fileLines)
        self.setBoard(boardInstace)
    
    def normalizeBoard(self):
        self._calculateAndSetBaseScale(self.board.getArea())
        self._calculateAndSetBaseOffsetXY(self.board.getArea())
        try:
            self._normalizeAreaComponentsShapes()
        except NormalizingError:
            self.board = copy.deepcopy(self.boardBackup)
            bottomLeftPoint, topRightPoint = self.board.calculateAreaFromComponents()
            self.board.setArea(bottomLeftPoint, topRightPoint)
            self._resetGroupsToDefault()

            self._calculateAndSetBaseScale(self.board.getArea())
            self._calculateAndSetBaseOffsetXY(self.board.getArea())
            self._normalizeAreaComponentsShapes()
        
        self.board.setGroups(self.sideComponents, self.commonTypeComponents)
        return self.board

    def _normalizeAreaComponentsShapes(self):
        self._scaleAndMoveAreaPoints(self.board.getArea())
        self._recalculateAndGroupComponents(self.board.getComponents())
        self._resizeAndMoveShapes(self.board.getOutlines())
    
    def getSideComponents(self) -> dict:
        return self.sideComponents
    
    def getCommonTypeComponents(self) -> dict:
        return self.commonTypeComponents
        
    def _loadBaseBoard(self, filePath:str) -> board.Board:
        fileExtension  = filePath.split('.')[-1]
        loader = loaderSelectorFactory.LoaderSelectorFactory(fileExtension)
        fileLines = loader.loadFile(filePath)
        return loader.processFileLines(fileLines)

    def setBoard(self, boardInstace:board.Board):
        self.board = boardInstace
        self.boardBackup = copy.deepcopy(self.board)        

    def _calculateAndSetBaseScale(self, boardArea:tuple[gobj.Point, gobj.Point]):
        areaWidth, areaHeight = Shape.getAreaWidthHeight(boardArea)
        
        FITNESS_SCALE_FACTOR = 0.9
        scaleX = self.width / areaWidth
        scaleY = self.height / areaHeight
        baseScale = min(scaleX, scaleY) * FITNESS_SCALE_FACTOR 
        self._setBaseScale(baseScale)
    
    def _setBaseScale(self, baseScale:float):
        self.baseScale = baseScale
        
    def _calculateAndSetBaseOffsetXY(self, boardArea:tuple[gobj.Point, gobj.Point]):
        x0, y0, x1, y1 = Shape.getAreaAsXYXY(boardArea)
        
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
    
    def _scaleAndMoveAreaPoints(self, pointList:list[gobj.Point]):
        for point in pointList:
            point.scaleInPlace(self.baseScale)
            point.translateInPlace(self.baseMoveOffsetXY)

    def _resizeAndMoveShapes(self, shapesList:list):
        for shape in shapesList:
            shape.scaleInPlace(self.baseScale)   
            shape.translateInPlace(self.baseMoveOffsetXY)
    
    def _recalculateAndGroupComponents(self, componentsDict:dict):
        for _, componentInstance in componentsDict.items():
            self._recalculateComponent(componentInstance)
            self._checkIfComponentCoordsArePositive(componentInstance)
            self._addComponentToSideComponents(componentInstance)
            self._addComponentToCommonTypeComponents(componentInstance)
    

    def _recalculateComponent(self, componentInstance:comp.Component):
        componentInstance.scaleInPlace(self.baseScale)
        componentInstance.translateInPlace(self.baseMoveOffsetXY)

    def _checkIfComponentCoordsArePositive(self, componentInstance:comp.Component):
        for point in componentInstance.getArea():
            x, y  = point.getXY()
            keyX, keyY = int(x / 100),  int(y / 100)
            if keyX < 0 or keyY < 0:
                raise NormalizingError    

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
    
    def _resetGroupsToDefault(self):
        self.sideComponents = {'B':[], 'T':[]}
        self.commonTypeComponents = {'B':{}, 'T':{}}
    
    @staticmethod
    def scaleBoardInPlace(board:board.Board, scaleFactor:float):
        board.scaleBoard(scaleFactor)
    
    @staticmethod
    def rotateBoardInPlace(board:board.Board, rotationPoint:gobj.Point, angle:float):
        board.rotateBoard(rotationPoint, angle)
    

if __name__ == '__main__':
    normalizedBoard = BoardCanvasWrapper(1200, 700)
    normalizedBoard.loadAndSetBoardFromFilePath(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\nexyM.gcd')
    normalizedBoard.normalizeBoard()