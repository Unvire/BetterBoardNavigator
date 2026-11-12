import copy
import geometryObjects as gobj
import component as comp
import board, loaderSelectorFactory
from abstractShape import Shape

class NormalizingError(Exception):
    pass

class BoardWrapper():
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
    
    def getMostCommonPrefix(self) -> str:
        return self.board.getMostCommonPrefix()
        
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
        
        self.baseScale = baseScale
        
    def _calculateAndSetBaseOffsetXY(self, boardArea:tuple[gobj.Point, gobj.Point]):
        x0, y0, *_ = Shape.getAreaAsXYXY(boardArea)

        xMove = x0 * self.baseScale
        yMove = y0 * self.baseScale
        self.baseMoveOffsetXY = [-xMove, -yMove]
    
    def _scaleAndMoveAreaPoints(self, pointList:list[gobj.Point]):
        for point in pointList:
            point.scaleInPlace(self.baseScale)
            point.translateInPlace(self.baseMoveOffsetXY)

        bottomLeftPoint, topRightPoint = pointList
        self.board.setArea(bottomLeftPoint, topRightPoint)

    def _resizeAndMoveShapes(self, shapesList:list):
        for shape in shapesList:
            shape.scaleInPlace(self.baseScale)   
            shape.translateInPlace(self.baseMoveOffsetXY)
    
    def _recalculateAndGroupComponents(self, componentsDict:dict):
        for componentInstance in componentsDict.values():
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
        mountingType = componentInstance.getMountingType()
        if 'SM' == mountingType[:2]:
            self.commonTypeComponents[side][prefix].append(componentInstance.name)
        else:
            self.commonTypeComponents['B'][prefix].append(componentInstance.name)
            self.commonTypeComponents['T'][prefix].append(componentInstance.name)
    
    def _resetGroupsToDefault(self):
        self.sideComponents = {'B':[], 'T':[]}
        self.commonTypeComponents = {'B':{}, 'T':{}}
    
    @staticmethod
    def scaleBoardInPlace(board:board.Board, scaleFactor:float):
        board.translateRotateScaleBoard('scaleInPlace', scaleFactor)
        BoardWrapper.translateBoardBottomLeftAreaPointTo00(board)
    
    @staticmethod
    def rotateBoardInPlace(board:board.Board, rotationPoint:gobj.Point, angle:float):
        board.translateRotateScaleBoard('rotateInPlace', rotationPoint, angle)
    
    @staticmethod
    def rotateBoardInPlaceAroundAreaCenter(board:board.Board, angle:float):
        boardArea = board.getArea()
        xRot, yRot = Shape.calculateAreaCenterXY(boardArea)
        
        rotationPoint = gobj.Point(xRot, yRot)
        board.translateRotateScaleBoard('rotateInPlace', rotationPoint, angle)
        BoardWrapper.translateBoardBottomLeftAreaPointTo00(board)
    
    @staticmethod
    def translateBoardInPlace(board:board.Board, moveVector:list[float|int, float|int]):
        board.translateRotateScaleBoard('translateInPlace', moveVector)
    
    @staticmethod
    def useAreaFromComponentsInPlace(board:board.Board):
        bottomLeftPoint, topRightPoint = board.calculateAreaFromComponents()
        board.setArea(bottomLeftPoint, topRightPoint)
    
    @staticmethod
    def setAreaManually(board:board.Board, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        board.setArea(bottomLeftPoint, topRightPoint)
    
    @staticmethod
    def translateBoardBottomLeftAreaPointTo00(board:board.Board):
        bottomLeftPoint = board.getArea()[0]
        x, y = bottomLeftPoint.getXY()
        board.translateRotateScaleBoard('translateInPlace', [-x, -y])  
    

if __name__ == '__main__':    
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    filePath = openSchematicFile()
    normalizedBoard = BoardWrapper(1200, 700)

    normalizedBoard.loadAndSetBoardFromFilePath(filePath)
    normalizedBoard.normalizeBoard()
    print(normalizedBoard.board.getArea())