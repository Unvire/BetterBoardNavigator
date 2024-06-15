import pygame, math, copy, re
import pin, board
from boardWrapper import BoardWrapper
import geometryObjects as gobj
import component as comp

class DrawBoardEngine:
    MIN_SURFACE_DIMENSION = 100
    STEP_FACTOR = 0.05
    MAX_SURFACE_DIMENSION = 11000
    DELTA_ROTATION_ANGLE_DEG = 5

    def __init__(self, width:int, height:int):
        self.boardData = None
        self.boardDataBackup = None
        self.drawHandler = {'Line': self._drawLine,
                            'Arc': self._drawArc}
        
        self.colorsDict = {           
            'background': (0, 0, 0), 
            'outlines': (255, 255, 255),
            'components': (8, 212, 15),
            'TH pins': (21, 103, 235),
            'SMT pins': (240, 187, 12),
            'selected component marker': (255, 0, 0),
            'selected net marker': (171, 24, 149)
        }
        
        self.surfaceDimensions = [width, height]
        self.screenDimensions = [width, height]

        self.boardLayer = self._getEmptySurfce()
        self.commonTypeComponentsSurface = self._getEmptySurfce()
        self.selectedComponentsSurface = self._getEmptySurfce()
        self.selectedNetSurface = self._getEmptySurfce()

        self.selectedComponentsSet = set()
        self.allSelectedNetComponentsSet = set()
        self.selectedNetComponentsSet = set()
        self.selectedCommonTypePrefix = ''
        self.selectedNet = dict()
        self.isHideSelectedNetComponents = False

        self.scale = 1
        self.offsetVector = []
        self.sidesForFlipX = {}
        self.isShowOutlines = True
    
    def getColor(self, key:str) -> tuple[int, int, int]:
        return self.colorsDict.get(key, None)

    def getComponents(self) -> list[str]:
        componentsList = list(self.boardData.getComponents().keys())
        return sorted(componentsList, key=self._componentStringValue)
    
    def getNets(self) -> dict:
        nets = {}
        for netName, componentOnNetSubDict in self.boardData.getNets().items():
            nets[netName] = {}
            componentsOnNetDict = {}
            for componentName in componentOnNetSubDict:
                pinsList = sorted(componentOnNetSubDict[componentName]['pins'], key=self._pinStringValue)
                pinsString = ', '.join(pinsList)
                componentsOnNetDict[componentName] = pinsString
            nets[netName] = dict(sorted(componentsOnNetDict.items(), key=lambda componentPinoutData: self._componentStringValue(componentPinoutData[0])))

        sortedNetNamesList = sorted(nets.keys()) 
        return {netName:nets[netName] for netName in sortedNetNamesList}
    
    def getSideOfComponent(self, componentName:str) -> str:
        componentInstance = self.boardData.getElementByName('components', componentName)
        return componentInstance.getSide()
    
    def getComponentPinout(self, componentName:str) -> dict:
        componentInstance = self.boardData.getElementByName('components', componentName)
        pins = componentInstance.getPins()
        pinoutDict = {pinName:pinInstance.getNet() for pinName, pinInstance in pins.items()}
        return dict(sorted(pinoutDict.items(), key=lambda pinData: self._pinStringValue(pinData[0])))
        
    def getSelectedComponents(self) -> list[str]:
        return list(self.selectedComponentsSet)
    
    def changeColor(self, key:str, RGB:tuple[int, int, int]):
        if key in self.colorsDict:
            self.colorsDict[key] = RGB

    def setBoardData(self, boardData:board.Board, isMakeBackup:bool=True):
        def resetVariablesAndSurfaces():
            self._resetSelectionCollections()
            self._resetSurfaceVariables()
            self._resetSurfaceDimensions()
            self.selectedComponentsSurface = self._getEmptySurfce()
            self.selectedNetSurface = self._getEmptySurfce()
            self.selectedNetSurface = self._getEmptySurfce()
        
        resetVariablesAndSurfaces()
        self.boardData = boardData
        if isMakeBackup:
            self.boardDataBackup = copy.deepcopy(boardData)
        self._adjustBoardDimensionsForRotating()
    
    def _resetSelectionCollections(self):
        self.selectedComponentsSet = set()
        self.allSelectedNetComponentsSet = set()
        self.selectedCommonTypePrefix = ''
        self.selectedNet = dict()
        self.isHideSelectedNetComponents = False
    
    def _resetSurfaceVariables(self):
        self.scale = 1
        self.offsetVector = [0, 0]
        self.sidesForFlipX = {'T'}
    
    def _resetSurfaceDimensions(self):
        screenWidth, screenHeight = self.screenDimensions
        self.surfaceDimensions = [screenWidth, screenHeight]
    
    def moveBoardInterface(self, targetSurface:pygame.Surface, relativeXY:list[int, int]) -> pygame.Surface:
        self._updateOffsetVector(relativeXY)                    
        return self._blitBoardSurfacesIntoTarget(targetSurface)
    
    def scaleUpDownInterface(self, targetSurface:pygame.Surface, isScaleUp:bool, pointXY:list[int, int], side:str) -> pygame.Surface:
        if isScaleUp:
            self._scaleUp(pointXY)
        else:
            self._scaleDown(pointXY)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def changeSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        return self.drawAndBlitInterface(targetSurface, side)
    
    def rotateBoardInterface(self, targetSurface:pygame.Surface,  isClockwise:bool, side:str, angleDeg:float=None) -> pygame.Surface:
        rotationXY = [val / 2 for val in self.surfaceDimensions]
        self._rotate(rotationXY, isClockwise, angleDeg)     
        return self.drawAndBlitInterface(targetSurface, side)
    
    def findComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        self._findComponentByName(componentName)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def componentInScreenCenterInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        componentInstance = self.boardData.getElementByName('components', componentName)
        componentSide  = componentInstance.getSide()
        if componentSide == side:
            self._setComponentInScreenCenter(componentInstance, side)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def clearFindComponentByNameInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectComponents()
        return self.drawAndBlitInterface(targetSurface, side)
    
    def selectNetByNameInterface(self, targetSurface:pygame.Surface, netName:str, side:str) -> pygame.Surface:
        if netName:
            self._selectNet(netName)
        else:
            self._unselectNet()
        return self.drawAndBlitInterface(targetSurface, side)
    
    def selectNetComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        self._selectNetComponentByName(componentName)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def unselectNetInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectNet()
        return self.drawAndBlitInterface(targetSurface, side)
    
    def showHideMarkersForSelectedNetByNameInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._showHideNetComponents()
        return self.drawAndBlitInterface(targetSurface, side)
    
    def showCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, prefix:str, side:str) -> pygame.Surface:
        self._selectCommonTypeComponents(side, prefix)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def clearCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectCommonTypeComponents()
        return self.drawAndBlitInterface(targetSurface, side)
    
    def flipUnflipCurrentSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._flipUnflipCurrentSide(side)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def changeAreaInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        BoardWrapper.useAreaFromComponentsInPlace(self.boardData)
        boardDataNormalized = self._getNormalizedBoard(self.screenDimensions, self.boardData)
        self.setBoardData(boardDataNormalized, isMakeBackup=False)
        return self.drawAndBlitInterface(targetSurface, side)
    
    def resetToDefaultViewInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self.boardData = copy.deepcopy(self.boardDataBackup)
        self.setBoardData(self.boardData)
        return self.drawAndBlitInterface(targetSurface, side)

    def showHideOutlinesInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._showHideOutlines()
        return self.drawAndBlitInterface(targetSurface, side)

    def changeScreenDimensionsInterface(self, targetSurface:pygame.Surface, dimensions:tuple[int, int], side:str) -> pygame.Surface:
        self.screenDimensions = dimensions[:]
        boardDataNormalized = self._getNormalizedBoard(dimensions, self.boardData)
        self.setBoardData(boardDataNormalized, isMakeBackup=True)
        return self.drawAndBlitInterface(targetSurface, side)

    def drawAndBlitInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._drawBoard(side)
        return self._blitBoardSurfacesIntoTarget(targetSurface)

    def _getNormalizedBoard(self, surfaceDimensions:tuple[int, int], boardInstance:board.Board) -> board.Board:
        width, height = surfaceDimensions
        wrapper = BoardWrapper(width, height)
        wrapper.setBoard(boardInstance)
        return wrapper.normalizeBoard()

    def _adjustBoardDimensionsForRotating(self):
        def calculateDiagonal(dimensions:list[int|float]) -> float:
            width, height = dimensions
            return math.sqrt(width ** 2 + height ** 2)
        
        def calculateScalingFactor(boardAreaDiagonal:float) -> float:
            SCALE_FACTOR = 1.05
            scaleFactor = 1
            for dimension in self.surfaceDimensions:
                if boardAreaDiagonal / dimension > 1:
                    scaleFactor = max(scaleFactor, boardAreaDiagonal / dimension * SCALE_FACTOR)
            return scaleFactor
        
        boardAreaDiagonal = calculateDiagonal(self.boardData.getWidthHeight())
        scaleFactor = calculateScalingFactor(boardAreaDiagonal)
        self._scaleSurfaceDimensionsByFactor(scaleFactor)
        self._centerBoardInAdjustedSurface()
    
    def _setOffsetVector(self, vector:tuple[int, int]):
        self.offsetVector = vector
    
    def _updateOffsetVector(self, relativeVector:tuple[int, int]):
        xMove, yMove = self.offsetVector
        dx, dy = relativeVector
        self.offsetVector = [xMove + dx, yMove + dy]
    
    def _rotate(self, rotationXY:tuple[int, int], isClockwise:bool, angleDeg:float=None):
        if not angleDeg:
            angleDeg = DrawBoardEngine.DELTA_ROTATION_ANGLE_DEG
        angleDeg *= (-1) ** int(isClockwise) 
        xRot, yRot = rotationXY
        rotationPoint = gobj.Point(xRot, yRot)
        BoardWrapper.rotateBoardInPlace(self.boardData, rotationPoint, angleDeg)
    
    def _scaleUp(self, zoomingPoint:tuple[int, int]):
        surfaceWidth, surfaceHeight = self.surfaceDimensions
        isWidthTooBig = surfaceWidth > DrawBoardEngine.MAX_SURFACE_DIMENSION
        isHeightTooBig = surfaceHeight > DrawBoardEngine.MAX_SURFACE_DIMENSION
        if isWidthTooBig or isHeightTooBig:
            return
        
        previousScaleFactor = self._getScaleFactorFromSurfaceDimensions()
        if self.scale < 1:
            scaleFactor = 1 / self.scale
            self.scale += DrawBoardEngine.STEP_FACTOR
        else:
            self.scale += DrawBoardEngine.STEP_FACTOR
            scaleFactor = self.scale
        
        self._scaleSurfaceDimensionsByFactor(scaleFactor)
        newOffset = self._calculateOffsetVectorForScaledSurface(zoomingPoint, previousScaleFactor)
        self._setOffsetVector(newOffset)
        BoardWrapper.scaleBoardInPlace(self.boardData, scaleFactor)

    def _scaleDown(self, zoomingPoint:tuple[int, int]):        
        surfaceWidth, surfaceHeight = self.surfaceDimensions
        isWidthTooSmall = surfaceWidth < DrawBoardEngine.MIN_SURFACE_DIMENSION
        isHeightTooSmall = surfaceHeight < DrawBoardEngine.MIN_SURFACE_DIMENSION
        if isWidthTooSmall or isHeightTooSmall:
            return

        previousScaleFactor = self._getScaleFactorFromSurfaceDimensions()
        if self.scale > 1:
            scaleFactor = 1 / self.scale
            self.scale -= DrawBoardEngine.STEP_FACTOR
        else:
            self.scale -= DrawBoardEngine.STEP_FACTOR
            scaleFactor = self.scale
        
        self._scaleSurfaceDimensionsByFactor(scaleFactor)
        newOffset = self._calculateOffsetVectorForScaledSurface(zoomingPoint, previousScaleFactor)
        self._setOffsetVector(newOffset)
        BoardWrapper.scaleBoardInPlace(self.boardData, scaleFactor)
    
    def findComponentByClick(self, cursorXY:list[int, int], side:str) -> list[str]:
        x, y = cursorXY
        xOffset, yOffset = self.offsetVector

        x = x - xOffset
        y = y - yOffset
        if side in self.sidesForFlipX:
            x = self._xForMirroredSurface(x)
            
        clickedPoint = gobj.Point(x, y)
        return self.boardData.findComponentByCoords(clickedPoint, side)
    
    def _findComponentByName(self, componentName:str) -> comp.Component|None:
        componentInstance = self.boardData.getElementByName('components', componentName)
        if not componentInstance:
            return
        
        if componentInstance.name in self.selectedComponentsSet:
            self.selectedComponentsSet.remove(componentInstance.name)
            return
        else:
            self.selectedComponentsSet.add(componentInstance.name)
            return componentInstance
    
    def _selectNetComponentByName(self, componentName:str):
        if componentName in self.selectedNetComponentsSet:
            self.selectedNetComponentsSet = set()
        elif componentName in self.allSelectedNetComponentsSet:
            self.selectedNetComponentsSet = set()
            self.selectedNetComponentsSet.add(componentName)
    
    def _setComponentInScreenCenter(self, componentInstance:comp.Component, side:str):
        coords = componentInstance.getCoords()
        xComp, yComp = coords.getXY()
        xScreen, yScreen = self.screenDimensions

        if side in self.sidesForFlipX:
            xComp = self._xForMirroredSurface(xComp)
        x = xScreen / 2 - xComp
        y = yScreen / 2 - yComp

        self._setOffsetVector([x, y])
    
    def _selectNet(self, netName:str):
        net = self.boardData.getElementByName('nets', netName)
        self.allSelectedNetComponentsSet = set(net)
        for componentName, parameters in net.items():
            self.selectedNet[componentName] = parameters['pins']
        self.isHideSelectedNetComponents = False
    
    def _unselectComponents(self):
        self.selectedComponentsSet = set()
    
    def _unselectNet(self):        
        self.allSelectedNetComponentsSet = set()
        self.selectedNetComponentsSet = set()
        self.selectedNet = dict()
    
    def _showHideNetComponents(self):
        self.isHideSelectedNetComponents = not self.isHideSelectedNetComponents
    
    def _selectCommonTypeComponents(self, side:str, prefix:str):
        prefix = prefix.upper()
        if prefix in self.boardData.getCommonTypeGroupedComponents()[side]:
            self.selectedCommonTypePrefix = prefix
    
    def _unselectCommonTypeComponents(self):
        self.selectedCommonTypePrefix = ''
    
    def _scaleSurfaceDimensionsByFactor(self, factor:int|float):
        self.surfaceDimensions = [val * factor for val in self.surfaceDimensions]
    
    def _flipUnflipCurrentSide(self, side:str):
        if side in self.sidesForFlipX:
            self.sidesForFlipX.remove(side)
        else:
           self.sidesForFlipX.add(side) 
    
    def _showHideOutlines(self):
        self.isShowOutlines = not self.isShowOutlines
    
    def _centerBoardInAdjustedSurface(self):
        surfaceWidth, surfaceHeight = self.surfaceDimensions
        screenWidth, screenHeight = self.screenDimensions

        xOffset = (screenWidth - surfaceWidth) / 2
        yOffset = (screenHeight - surfaceHeight) / 2
        self.offsetVector = [xOffset, yOffset]
        BoardWrapper.translateBoardInPlace(self.boardData, [-xOffset, -yOffset]) #'-' because board must be moved away from its center 
    
    def _calculateOffsetVectorForScaledSurface(self, zoomingPoint:tuple[int, int], previousScaleFactor:float):
        def reverseSurfaceLinearTranslation(screenCoords:list[int, int], offset:list[int, int]) -> tuple[int, int]:
            xScreen, yScreen = screenCoords
            xMove, yMove = offset
            return xScreen - xMove, yScreen - yMove

        def calculatePointCoordsRelativeToSurfaceDimensions(point:tuple[int, int], surfaceDimensions:tuple[int, int]) -> tuple[float, float]:
            x, y = point
            width, height = surfaceDimensions
            return x / width, y / height
        
        def calcluatePointInScaledSurface(surfaceDimensions:tuple[int, int], relativePosition:tuple[float, float]) -> tuple[int, int]:
            width, height = surfaceDimensions
            xRel, yRel = relativePosition
            return round(width * xRel), round(height * yRel)
        
        def translateScaledPointToCursorPosition(point:tuple[int, int], cursorPosition:tuple[float, float]) -> tuple[int, int]:
            x, y = point
            xCursor, yCursor = cursorPosition
            return xCursor - x, yCursor - y

        originSurfaceDimensions = [val * previousScaleFactor for val in self.screenDimensions]

        pointMoveReversed = reverseSurfaceLinearTranslation(zoomingPoint, self.offsetVector)
        pointRelativeToSurface = calculatePointCoordsRelativeToSurfaceDimensions(pointMoveReversed, originSurfaceDimensions)
        pointInScaledSurface = calcluatePointInScaledSurface(self.surfaceDimensions, pointRelativeToSurface)
        resultOffset = translateScaledPointToCursorPosition(pointInScaledSurface, zoomingPoint)
        return resultOffset
    
    def _drawBoard(self, side:str):
        def resetSurfaces():            
            self.boardLayer = self._getEmptySurfce()
            self.commonTypeComponentsSurface = self._getEmptySurfce()
            self.selectedComponentsSurface = self._getEmptySurfce()
            self.selectedNetSurface = self._getEmptySurfce()

        def drawBoardLayer(side:str):
            componentNames = self.boardData.getSideGroupedComponents()[side]
            if self.isShowOutlines:
                drawOutlines()
            drawComponents(componentNamesList=componentNames, width=1, side=side)

        def drawCommonTypeComponents(side:str):
            prefix = self.selectedCommonTypePrefix
            if prefix in self.boardData.getCommonTypeGroupedComponents()[side]:
                componentNames = self.boardData.getCommonTypeGroupedComponents()[side][prefix]
                drawComponents(componentNamesList=componentNames, width=0, side=side)
        
        def drawOutlines():
            color = self.colorsDict['outlines']
            self._drawOutlines(surface=self.boardLayer, color=color, width=3)

        def drawComponents(componentNamesList:list[str], width:int, side:str):
            componentColor = self.colorsDict['components']
            smtPinColor = self.colorsDict['SMT pins']
            thPinColor = self.colorsDict['TH pins']
            self._drawComponents(surface=self.boardLayer, componentNamesList=componentNamesList, componentColor=componentColor, 
                                 smtPinColor=smtPinColor, thPinColor=thPinColor, side=side, width=width)
        
        def drawSelectedComponents(side:str):
            color = self.colorsDict['selected component marker']
            componentNames = list(self.selectedComponentsSet)
            self._drawMarkers(surface=self.selectedComponentsSurface, componentNamesList=componentNames, color=color, side=side)
        
        def drawSelectedNets(side:str):
            componentNames = list(self.selectedNetComponentsSet)
            color = self.colorsDict['selected net marker']
            if not self.isHideSelectedNetComponents:
                self._drawMarkers(surface=self.selectedNetSurface, componentNamesList=componentNames, color=color, side=side)
            self._drawSelectedPins(surface=self.selectedNetSurface, color=color, side=side)
        
        resetSurfaces()
        drawBoardLayer(side)
        drawCommonTypeComponents(side)
        drawSelectedComponents(side)
        drawSelectedNets(side)
        self._flipSurfaceXAxis(side)     
    
    def _drawOutlines(self, surface:pygame.Surface, color:tuple[int, int, int], width:int=1):
        for shape in self.boardData.getOutlines():
            shapeType = shape.getType()
            self.drawHandler[shapeType](surface, color, shape, width)
    
    def _drawComponents(self, surface:pygame.Surface, componentNamesList:list[str], componentColor:tuple[int, int, int], smtPinColor:tuple[int, int, int], thPinColor:tuple[int, int, int], side:str, width:int=1):
        pinColorDict = {'SMT':smtPinColor, 'SMD':smtPinColor, 'TH':thPinColor}
        
        for componentName in componentNamesList:
            componentInstance = self.boardData.getElementByName('components', componentName)
            mountingType = componentInstance.getMountingType()
            componentSide = componentInstance.getSide()
            pinsDict = componentInstance.getPins()

            numOfPins = len(pinsDict)
            isSkipComponentSMT = mountingType == 'SMT' and componentSide == side and numOfPins == 1
            isSkipComponentTH = mountingType == 'TH' and componentSide != side
            isDrawComponent = not (isSkipComponentSMT or isSkipComponentTH)
            if isDrawComponent:
                self._drawInstanceAsCirlceOrPolygon(surface, componentInstance, componentColor, width)

            pinsColor = pinColorDict[componentInstance.getMountingType()]
            self._drawPins(surface, componentInstance, pinsColor, width)
    
    def _drawMarkers(self, surface:pygame.Surface, componentNamesList:list[str], color:tuple[int, int, int], side:str):
        for componentName in componentNamesList:
            componentInstance = self.boardData.getElementByName('components', componentName)
            if componentInstance.getMountingType() == 'TH' or componentInstance.getSide() == side:
                centerPoint = componentInstance.getCoords()
                self._drawMarkerArrow(surface, centerPoint.getXY(), color)
    
    def _drawSelectedPins(self, surface:pygame.Surface, color:tuple[int, int, int], side:str):
        for componentName, pinsList in self.selectedNet.items():
            componentInstance = self.boardData.getElementByName('components', componentName)
            pinsInstancesList = [componentInstance.getPinByName(pinName) for pinName in pinsList]
            for pinInstance in pinsInstancesList:
                if componentInstance.getMountingType() == 'TH' or componentInstance.getSide() == side:
                    self._drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, width=0)

    def _drawPins(self, surface:pygame.Surface, componentInstance:comp.Component, color:tuple[int, int, int], width:int=1):
        pinsDict = componentInstance.getPins()
        for _, pinInstance in pinsDict.items():
            self._drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, width)
    
    def _flipSurfaceXAxis(self, side:str):   
        if side in self.sidesForFlipX:  
            self.boardLayer = pygame.transform.flip(self.boardLayer, True, False)
            self.selectedComponentsSurface = pygame.transform.flip(self.selectedComponentsSurface, True, False)
            self.selectedNetSurface = pygame.transform.flip(self.selectedNetSurface, True, False)
            self.commonTypeComponentsSurface = pygame.transform.flip(self.commonTypeComponentsSurface, True, False)
    
    def _drawInstanceAsCirlceOrPolygon(self, surface:pygame.Surface, instance: pin.Pin|comp.Component, color:tuple[int, int, int], width:int=1):
        if  instance.getShape() == 'CIRCLE':
            shape = instance.getShapeData()
            self._drawCircle(surface, color, shape, width)
        else:
            pointsList = instance.getShapePoints()
            self._drawPolygon(surface, color, pointsList, width)
        
    def _blitBoardSurfacesIntoTarget(self, targetSurface:pygame.Surface) -> pygame.Surface:    
        color = self.colorsDict['background']
        targetSurface.fill(color)
        targetSurface.blit(self.boardLayer, self.offsetVector)

        self.commonTypeComponentsSurface.set_colorkey(color)
        targetSurface.blit(self.commonTypeComponentsSurface, self.offsetVector)

        self.selectedComponentsSurface.set_colorkey(color)
        targetSurface.blit(self.selectedComponentsSurface, self.offsetVector)

        self.selectedNetSurface.set_colorkey(color)
        targetSurface.blit(self.selectedNetSurface, self.offsetVector)
        return targetSurface

    def _drawLine(self, surface:pygame.Surface, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        pygame.draw.line(surface, color, startPoint.getXY(), endPoint.getXY(), width)

    def _drawArc(self, surface:pygame.Surface, color:tuple[int, int, int], arcInstance:gobj.Arc, width:int=1):
        def inversedAxisAngle(angleRad:float):
            return 2 * math.pi - angleRad

        rotationPoint, radius, startAngle, endAngle = arcInstance.getAsCenterRadiusAngles()
        x0, y0 = rotationPoint.getXY()
        x0 -= radius
        y0 -= radius

        startAngle, endAngle = inversedAxisAngle(endAngle), inversedAxisAngle(startAngle)
        pygame.draw.arc(surface, color, (x0, y0, 2 * radius, 2 * radius), startAngle, endAngle, width)

    def _drawCircle(self, surface:pygame.Surface, color:tuple[int, int, int], circleInstance:gobj.Circle, width:int=1):
        centerPoint, radius = circleInstance.getCenterRadius()
        pygame.draw.circle(surface, color, centerPoint.getXY(), radius, width)

    def _drawPolygon(self, surface:pygame.Surface, color:tuple[int, int, int], pointsList:list[gobj.Point], width:int=1):
        pointsXYList = [point.getXY() for point in pointsList]
        pygame.draw.polygon(surface, color, pointsXYList, width)
    
    def _drawMarkerArrow(self, surface:pygame.Surface, coordsXY:list[int, int], color:tuple[int, int, int]):
        x, y = coordsXY
        k = self._getScaleFactorFromSurfaceDimensions()
        markerCoords = [(x, y), (x - (4 * k), y - (6 * k)), (x - (2 * k), y - (6 * k)), (x - (2 * k), y - (40 * k)), 
                        (x + (2 * k), y - (40 * k)), (x + (2 * k), y - (6 * k)), (x + (4 * k), y - (6 * k))]
        pygame.draw.polygon(surface, color, markerCoords, width=0)
    
    def _getEmptySurfce(self) -> pygame.Surface:
        color = self.colorsDict['background']
        surface = pygame.Surface(self.surfaceDimensions)
        surface.fill(color)
        return surface
    
    def _getScaleFactorFromSurfaceDimensions(self) -> float:
        screenWidth, _ = self.screenDimensions
        surfaceWidth, _ = self.surfaceDimensions
        return surfaceWidth / screenWidth
    
    def _xForMirroredSurface(self, x:float) -> float:
        surfaceWidth, _ = self.surfaceDimensions
        return surfaceWidth - x
    
    def _pinStringValue(self, pinName:str) -> int:
        if pinName.isnumeric():
            return int(pinName)
        else:
            return sum([ord(char) for char in pinName])
    
    def _componentStringValue(self, componentName:str):
        ## split component name into letters and digits. Calculate value as [ord(char1) + ord(char2) + ...] * 1000 + componentNumber
        stringValue = lambda componentType: sum([ord(char) for char in componentType]) * 1000

        try:
            componentType, componentNumber, *_ = list(filter(None, re.split(r'(\d+)', componentName)))
        except ValueError:
            componentType = componentName
            componentNumber = 0
        return stringValue(componentType) + int(componentNumber)

if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    WIDTH, HEIGHT = 1200, 700
    FPS = 60

    sideQueue = ['B', 'T']
    side = 'T'
    isMousePressed = False
    isMovingCalledFirstTime = True
    isFindComponentByClickActive = False

    filePath = openSchematicFile()
    wrapper = BoardWrapper(WIDTH, HEIGHT)
    wrapper.loadAndSetBoardFromFilePath(filePath)
    boardInstance = wrapper.normalizeBoard()

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption(filePath)

    engine = DrawBoardEngine(WIDTH, HEIGHT)
    engine.setBoardData(boardInstance)
    engine.drawAndBlitInterface(WIN, side)    
    print('Components: ', engine.getComponents())
    print('Nets: ', engine.getNets())

    print('====================================')
    print('Pygame draw PCB engine')
    print('Move - mouse dragging')
    print('Zoom - scroll wheel')    
    print('Change side - ;')
    print('Rotate - , .')    
    print('Reset to default view - r')
    print('Use components for area calculation - d')
    print('Show/hide outlines - f')
    print('Flip unflip current side - m')
    print('Select component by click mode - z')
    print('Find component by name - x')
    print('Clear arrow markers - c')
    print('Find net by name - v')
    print('Clear selected net - b')
    print('Show/hide selected net components - n')
    print('Highlight common type components - a')
    print('Clear common type components - s')
    print('Change screen surface dimensions - g')
    print('Set component in screen center - h')
    print('Select component on net (net must be drawn before) - j')
    print('====================================')

    run = True
    while run:
        clock.tick(FPS)

        ## handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    isMousePressed = True
                    isMovingCalledFirstTime = True    
                    if isFindComponentByClickActive:
                        foundComponents = engine.findComponentByClick(pygame.mouse.get_pos(), side)
                        print(f'clicked component: {foundComponents}')

            elif event.type == pygame.MOUSEBUTTONUP:
                isMousePressed = False

            elif event.type == pygame.MOUSEMOTION:
                if isMousePressed:
                    dx, dy = pygame.mouse.get_rel()
                    if not isMovingCalledFirstTime:
                        engine.moveBoardInterface(WIN, [dx, dy])
                    else:
                        isMovingCalledFirstTime = False
            
            elif event.type == pygame.MOUSEWHEEL:
                pointXY = pygame.mouse.get_pos()
                if event.y > 0:
                    engine.scaleUpDownInterface(WIN, isScaleUp=True, pointXY=pointXY, side=side)
                else:
                    engine.scaleUpDownInterface(WIN, isScaleUp=False, pointXY=pointXY, side=side)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SEMICOLON:
                    side = sideQueue.pop(0)
                    sideQueue.append(side)
                    engine.changeSideInterface(WIN, side)
                
                elif event.key == pygame.K_PERIOD:
                    engine.rotateBoardInterface(WIN, isClockwise=True, side=side)
                
                elif event.key == pygame.K_COMMA:
                    engine.rotateBoardInterface(WIN,  isClockwise=False, side=side)
                
                elif event.key == pygame.K_z:
                    isFindComponentByClickActive = not isFindComponentByClickActive
                    print(f'Find component using clck mode active: {isFindComponentByClickActive}')
                
                elif event.key == pygame.K_x:
                    componentName = input('Component name: ')
                    engine.findComponentByNameInterface(WIN, componentName, side)
                    print(engine.getComponentPinout(componentName))
                
                elif event.key == pygame.K_c:
                    engine.clearFindComponentByNameInterface(WIN, side)
                
                elif event.key == pygame.K_v:
                    netName = input('Net name: ')
                    engine.selectNetByNameInterface(WIN, netName, side)
                
                elif event.key == pygame.K_b:
                    engine.unselectNetInterface(WIN, side)
                
                elif event.key == pygame.K_n:
                    engine.showHideMarkersForSelectedNetByNameInterface(WIN, side)
                
                elif event.key == pygame.K_a:
                    prefix = input('Common type prefix: ')
                    engine.showCommonTypeComponentsInterface(WIN, prefix, side)
                
                elif event.key == pygame.K_s:
                    engine.clearCommonTypeComponentsInterface(WIN, side)
                
                elif event.key == pygame.K_m:
                    engine.flipUnflipCurrentSideInterface(WIN, side)
                
                elif event.key == pygame.K_d:
                    engine.changeAreaInterface(WIN, side)
                
                elif event.key == pygame.K_r:
                    engine.resetToDefaultViewInterface(WIN, side)
                
                elif event.key == pygame.K_f:
                    engine.showHideOutlinesInterface(WIN, side)

                elif event.key == pygame.K_g:
                    width = int(input("New width: "))
                    height = int(input("New height: "))
                    WIN = pygame.display.set_mode((width, height))
                    engine.changeScreenDimensionsInterface(WIN, [width, height], side)

                elif event.key == pygame.K_h:
                    componentName = input('Component name: ')
                    engine.componentInScreenCenterInterface(WIN, componentName, side)
                
                elif event.key == pygame.K_j:
                    componentName = input('Net component name: ')
                    engine.selectNetComponentByNameInterface(WIN, componentName, side)

        
        ## display image
        pygame.display.update()
        #run = False

    pygame.quit()