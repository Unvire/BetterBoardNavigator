import pygame, math, copy
import pin, board
from boardCanvasWrapper import BoardCanvasWrapper
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
        
        self.surfaceDimensions = [width, height]
        self.screenDimensions = [width, height]

        self.boardLayer = self._getEmptySurfce()
        self.commonTypeComponentsSurface = self._getEmptySurfce()
        self.selectedComponentsSurface = self._getEmptySurfce()
        self.selectedNetSurface = self._getEmptySurfce()

        self.selectedComponentsSet = set()
        self.selectedNetComponentsSet = set()
        self.selectedCommonTypePrefix = ''
        self.selectedNet = dict()
        self.isHideSelectedNetComponents = False

        self.scale = 1
        self.offsetVector = [0, 0]
        self.sidesForFlipX = {'T'}

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
        self.boardDataBackup = copy.deepcopy(boardData)
        self._adjustBoardDimensionsForRotating()
        self.selectedComponentsSurface = self._getEmptySurfce()
        self.selectedNetSurface = self._getEmptySurfce()
    
    def moveBoardInterface(self, targetSurface:pygame.Surface, relativeXY:list[int, int]):
        self._updateOffsetVector(relativeXY)                    
        self._blitBoardSurfacesIntoTarget(targetSurface)
    
    def scaleUpDownInterface(self, targetSurface:pygame.Surface, isScaleUp:bool, pointXY:list[int, int], side:str):
        if isScaleUp:
            self._scaleUp(pointXY)
        else:
            self._scaleDown(pointXY)
        self._drawAndBlit(targetSurface, side)
    
    def changeSideInterface(self, targetSurface:pygame.Surface, side:str):
        self._drawAndBlit(targetSurface, side)
    
    def rotateBoardInterface(self, targetSurface:pygame.Surface, rotationXY:list[int, int], isClockwise:bool, side:str):
        self._rotate(rotationXY, isClockwise)     
        self._drawAndBlit(targetSurface, side)
    
    def findComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str):
        self._findComponentByName(componentName)
        self._drawAndBlit(targetSurface, side)
    
    def clearFindComponentByNameInterface(self, targetSurface:pygame.Surface, side:str):
        self._unselectComponents()
        self._drawAndBlit(targetSurface, side)
    
    def selectNetByNameInterface(self, targetSurface:pygame.Surface, netName:str, side:str):
        self._selectNet(netName)
        self._drawAndBlit(targetSurface, side)
    
    def unselectNetByNameInterface(self, targetSurface:pygame.Surface, side:str):
        self._unselectNet()
        self._drawAndBlit(targetSurface, side)
    
    def showHideMarkersForSelectedNetByNameInterface(self, targetSurface:pygame.Surface, side:str):
        self._showHideNetComponents()
        self._drawAndBlit(targetSurface, side)
    
    def showCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, prefix:str, side:str):
        self._selectCommonTypeComponents(side, prefix)
        self._drawAndBlit(targetSurface, side)
    
    def clearCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, side:str):
        self._unselectCommonTypeComponents()
        self._drawAndBlit(targetSurface, side)
    
    def flipUnflipCurrentSideInterface(self, targetSurface:pygame.Surface, side:str):
        self._flipUnflipCurrentSide(side)
        self._drawAndBlit(targetSurface, side)
    
    def changeAreaInterface(self, targetSurface:pygame.Surface, rectangleXYXY:list[tuple[int, int], tuple[int, int]], side:str):
        BoardCanvasWrapper.changeAreaInPlace(self.boardData, rectangleXYXY)
        
        screenWidth, screenHeight = self.screenDimensions
        wrapper = BoardCanvasWrapper(screenWidth, screenHeight)
        wrapper.setBoard(self.boardData)
        boardData = wrapper.normalizeBoard()

        self.setBoardData(boardData)
        self._drawAndBlit(targetSurface, side)
    
    def _drawAndBlit(self, targetSurface:pygame.Surface, side:str):
        self._drawBoard(side)
        self._blitBoardSurfacesIntoTarget(targetSurface)

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
    
    def setScale(self, factor:int|float):
        self.scale = factor
    
    def _setOffsetVector(self, vector:tuple[int, int]):
        self.offsetVector = vector
    
    def _updateOffsetVector(self, relativeVector:tuple[int, int]):
        xMove, yMove = self.offsetVector
        dx, dy = relativeVector
        self.offsetVector = [xMove + dx, yMove + dy]
    
    def _rotate(self, rotationXY:tuple[int, int], isClockwise:bool):
        angle = DrawBoardEngine.DELTA_ROTATION_ANGLE_DEG * (-1) ** int(isClockwise)
        xRot, yRot = rotationXY
        rotationPoint = gobj.Point(xRot, yRot)
        BoardCanvasWrapper.rotateBoardInPlace(self.boardData, rotationPoint, angle)
    
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
        BoardCanvasWrapper.scaleBoardInPlace(self.boardData, scaleFactor)

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
        BoardCanvasWrapper.scaleBoardInPlace(self.boardData, scaleFactor)
    
    def findComponentByClick(self, cursorXY:list[int, int], side:str):
        x, y = cursorXY
        if side in self.sidesForFlipX:
            screenWidth, _ = self.screenDimensions
            x = screenWidth - x
        xOffset, yOffset = self.offsetVector
        clickedPoint = gobj.Point(x - xOffset, y - yOffset)
        return self.boardData.findComponentByCoords(clickedPoint, side)
    
    def _findComponentByName(self, componentName:str):
        componentInstance = self.boardData.getElementByName('components', componentName)
        if not componentInstance:
            return
        
        if componentInstance.name in self.selectedComponentsSet:
            self.selectedComponentsSet.remove(componentInstance.name)
        else:
            self.selectedComponentsSet.add(componentInstance.name)
    
    def _selectNet(self, netName:str):
        net = self.boardData.getElementByName('nets', netName)
        self.selectedNetComponentsSet = set(net)
        for componentName, parameters in net.items():
            self.selectedNet[componentName] = parameters['pins']
        self.isHideSelectedNetComponents = False
    
    def _unselectComponents(self):
        self.selectedComponentsSet = set()
    
    def _unselectNet(self):        
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
    
    def _centerBoardInAdjustedSurface(self):
        surfaceWidth, surfaceHeight = self.surfaceDimensions
        screenWidth, screenHeight = self.screenDimensions

        xOffset = (screenWidth - surfaceWidth) / 2
        yOffset = (screenHeight - surfaceHeight) / 2
        self.offsetVector = [xOffset, yOffset]
        BoardCanvasWrapper.translateBoardInPlace(self.boardData, [-xOffset, -yOffset]) #'-' because board must be moved away from its center 
    
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
    
    def getScaleFactor(self) -> int|float:
        return self.scale
    
    def _drawBoard(self, side:str):
        WHITE = 255, 255, 255
        GREEN = 8, 212, 15
        BLUE = 21, 103, 235
        YELLOW = 240, 187, 12
        RED = 255, 0, 0
        VIOLET = 171, 24, 149

        def drawBoardLayer(side:str):
            self.boardLayer = self._getEmptySurfce()
            componentNames = self.boardData.getSideGroupedComponents()[side]
            self._drawOutlines(surface=self.boardLayer, color=WHITE, width=3)
            self._drawComponents(surface=self.boardLayer, componentNamesList=componentNames, componentColor=GREEN, smtPinColor=YELLOW, 
                                thPinColor=BLUE, side=side)
        
        def drawCommonTypeComponents(side:str):
            self.commonTypeComponentsSurface = self._getEmptySurfce()
            prefix = self.selectedCommonTypePrefix
            if prefix in self.boardData.getCommonTypeGroupedComponents()[side]:
                componentNames = self.boardData.getCommonTypeGroupedComponents()[side][prefix]
                self._drawComponents(surface=self.commonTypeComponentsSurface, componentNamesList=componentNames, componentColor=GREEN, 
                                    smtPinColor=YELLOW, thPinColor=BLUE, side=side, width=0)
        
        def drawSelectedComponents(side:str):
            self.selectedComponentsSurface = self._getEmptySurfce()
            componentNames = list(self.selectedComponentsSet)
            self._drawMarkers(surface=self.selectedComponentsSurface, componentNamesList=componentNames, color=RED, side=side)
        
        def drawSelectedNets(side:str):
            self.selectedNetSurface = self._getEmptySurfce()
            componentNames = list(self.selectedNetComponentsSet)
            if not self.isHideSelectedNetComponents:
                self._drawMarkers(surface=self.selectedNetSurface, componentNamesList=componentNames, color=VIOLET, side=side)
            self._drawSelectedPins(surface=self.selectedNetSurface, color=VIOLET, side=side)
        
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
        
    def _blitBoardSurfacesIntoTarget(self, targetSurface:pygame.Surface):    
        targetSurface.fill((0, 0, 0))
        targetSurface.blit(self.boardLayer, self.offsetVector)

        self.commonTypeComponentsSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.commonTypeComponentsSurface, self.offsetVector)

        self.selectedComponentsSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.selectedComponentsSurface, self.offsetVector)

        self.selectedNetSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.selectedNetSurface, self.offsetVector)

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
        return pygame.Surface(self.surfaceDimensions)
    
    def _getScaleFactorFromSurfaceDimensions(self) -> float:
        screenWidth, _ = self.screenDimensions
        surfaceWidth, _ = self.surfaceDimensions
        return surfaceWidth / screenWidth

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
    isNewArea = False
    newArea = []

    filePath = openSchematicFile()
    boardWrapper = BoardCanvasWrapper(WIDTH, HEIGHT)
    boardWrapper.loadAndSetBoardFromFilePath(filePath)
    boardInstance = boardWrapper.normalizeBoard()

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption(filePath)

    engine = DrawBoardEngine(WIDTH, HEIGHT)
    engine.setBoardData(boardInstance)
    engine._drawBoard(side)
    engine._blitBoardSurfacesIntoTarget(WIN)

    print('====================================')
    print('Pygame draw PCB engine')
    print('Move - mouse dragging')
    print('Zoom - scroll wheel')    
    print('Change side - ;')
    print('Rotate - , .')
    print('Flip unflip current side - m')
    print('Select component by click mode - z')
    print('Find component by name - x')
    print('Clear arrow markers - c')
    print('Find net by name - v')
    print('Clear selected net - b')
    print('Show/hide selected net components - n')
    print('Highlight common type components - a')
    print('Clear common type components - s')
    print('Select area for cropping out - d')
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
                    if isNewArea:
                        newArea.append(pygame.mouse.get_pos())
                        print(newArea)
                        if len(newArea) == 2:
                            isNewArea = False
                            engine.changeAreaInterface(WIN, newArea, side)

            
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
                    rotationXY = [val / 2 for val in engine.surfaceDimensions]
                    engine.rotateBoardInterface(WIN, rotationXY, isClockwise=True, side=side)
                
                elif event.key == pygame.K_COMMA:
                    rotationXY = [val / 2 for val in engine.surfaceDimensions]
                    engine.rotateBoardInterface(WIN, rotationXY, isClockwise=False, side=side)
                
                elif event.key == pygame.K_z:
                    isFindComponentByClickActive = not isFindComponentByClickActive
                    print(f'Find component using clck mode active: {isFindComponentByClickActive}')
                
                elif event.key == pygame.K_x:
                    componentName = input('Component name: ')
                    engine.findComponentByNameInterface(WIN, componentName, side)
                
                elif event.key == pygame.K_c:
                    engine.clearFindComponentByNameInterface(WIN, side)
                
                elif event.key == pygame.K_v:
                    netName = input('Net name: ')
                    engine.selectNetByNameInterface(WIN, netName, side)
                
                elif event.key == pygame.K_b:
                    engine.unselectNetByNameInterface(WIN, side)
                
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
                    isNewArea = True
                    print(f'Select new area:')
                

        ## display image
        pygame.display.update()
        #run = False

    pygame.quit()