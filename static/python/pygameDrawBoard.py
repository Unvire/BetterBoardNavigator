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
        self.drawHandler = {'Line': self.drawLine,
                            'Arc': self.drawArc}
        self.surfaceDimensions = [width, height]
        self.screenDimensions = [width, height]
        self.boardLayer = self._getEmptySurfce()
        self.commonTypeComponentsSurface = self._getEmptySurfce()
        self.selectedComponentsSurface = self._getEmptySurfce()
        self.selectedNetSurface = self._getEmptySurfce()
        self.selectedComponentsSet = set()
        self.selectedNetComponentsSet = set()
        self.selectedNet = dict()
        self.scale = 1
        self.offsetVector = [0, 0]
        self.sidesForFlipX = {'T'}

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
        self.boardDataBackup = copy.deepcopy(boardData)
        self._adjustBoardDimensionsForRotating()
        self.selectedComponentsSurface = self._getEmptySurfce()
        self.selectedNetSurface = self._getEmptySurfce()
        
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
    
    def setOffsetVector(self, vector:tuple[int, int]):
        self.offsetVector = vector
    
    def updateOffsetVector(self, relativeVector:tuple[int, int]):
        xMove, yMove = self.offsetVector
        dx, dy = relativeVector
        self.offsetVector = [xMove + dx, yMove + dy]
    
    def rotate(self, rotationXY:tuple[int, int], isClockwise:bool):
        angle = DrawBoardEngine.DELTA_ROTATION_ANGLE_DEG * (-1) ** int(isClockwise)
        xRot, yRot = rotationXY
        rotationPoint = gobj.Point(xRot, yRot)
        BoardCanvasWrapper.rotateBoardInPlace(self.boardData, rotationPoint, angle)
    
    def scaleUp(self, zoomingPoint:tuple[int, int]):
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
        self.setOffsetVector(newOffset)
        BoardCanvasWrapper.scaleBoardInPlace(self.boardData, scaleFactor)

    def scaleDown(self, zoomingPoint:tuple[int, int]):        
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
        self.setOffsetVector(newOffset)
        BoardCanvasWrapper.scaleBoardInPlace(self.boardData, scaleFactor)
    
    def findComponentByClick(self, cursorXY:list[int, int], side:str):
        x, y = cursorXY
        if side in self.sidesForFlipX:
            screenWidth, _ = self.screenDimensions
            x = screenWidth - x
        xOffset, yOffset = self.offsetVector
        clickedPoint = gobj.Point(x - xOffset, y - yOffset)
        return self.boardData.findComponentByCoords(clickedPoint, side)
    
    def findComponentByName(self, componentName:str):
        componentInstance = self.boardData.getElementByName('components', componentName)
        if not componentInstance:
            return
        
        if componentInstance.name in self.selectedComponentsSet:
            self.selectedComponentsSet.remove(componentInstance.name)
        else:
            self.selectedComponentsSet.add(componentInstance.name)
    
    def selectNet(self, netName:str):
        net = self.boardData.getElementByName('nets', netName)
        self.selectedNetComponentsSet = set(net)
        for componentName, parameters in net.items():
            self.selectedNet[componentName] = parameters['pins']
    
    def unselectComponents(self):
        self.selectedComponentsSet = set()
    
    def unselectNet(self):        
        self.selectedNetComponentsSet = set()
        self.selectedNet = dict()
    
    def unselectComponentsOnNet(self):
        self.selectedNetComponentsSet = set()
    
    def _scaleSurfaceDimensionsByFactor(self, factor:int|float):
        self.surfaceDimensions = [val * factor for val in self.surfaceDimensions]
    
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
    
    def drawBoard(self, side:str):
        WHITE = 255, 255, 255
        GREEN = 8, 212, 15
        BLUE = 21, 103, 235
        YELLOW = 240, 187, 12
        RED = 255, 0, 0
        VIOLET = 171, 24, 149

        def drawBoardLayer(side:str):
            self.boardLayer = self._getEmptySurfce()
            componentNames = self.boardData.getSideGroupedComponents()[side]
            self.drawOutlines(surface=self.boardLayer, color=WHITE, width=3)
            self.drawComponents(surface=self.boardLayer, componentNamesList=componentNames, componentColor=GREEN, smtPinColor=YELLOW, 
                                thPinColor=BLUE, side=side)
        
        def drawSelectedComponents(side:str):
            self.selectedComponentsSurface = self._getEmptySurfce()
            componentNames = list(self.selectedComponentsSet)
            self.drawMarkers(surface=self.selectedComponentsSurface, componentNamesList=componentNames, color=RED, side=side)
        
        def drawSelectedNets(side:str):
            self.selectedNetSurface = self._getEmptySurfce()
            componentNames = list(self.selectedNetComponentsSet)
            self.drawMarkers(surface=self.selectedNetSurface, componentNamesList=componentNames, color=VIOLET, side=side)
            self.drawSelectedPins(surface=self.selectedNetSurface, color=VIOLET, side=side)
        
        drawBoardLayer(side)
        drawSelectedComponents(side)
        drawSelectedNets(side)
        self._flipSurfaceXAxis(side)     
    
    def drawOutlines(self, surface:pygame.Surface, color:tuple[int, int, int], width:int=1):
        for shape in self.boardData.getOutlines():
            shapeType = shape.getType()
            self.drawHandler[shapeType](surface, color, shape, width)
    
    def drawComponents(self, surface:pygame.Surface, componentNamesList:list[str], componentColor:tuple[int, int, int], smtPinColor:tuple[int, int, int], thPinColor:tuple[int, int, int], side:str, width:int=1):
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
                self.drawInstanceAsCirlceOrPolygon(surface, componentInstance, componentColor, width + 1)

            pinsColor = pinColorDict[componentInstance.getMountingType()]
            self.drawPins(surface, componentInstance, pinsColor, width)
    
    def drawMarkers(self, surface:pygame.Surface, componentNamesList:list[str], color:tuple[int, int, int], side:str):
        for componentName in componentNamesList:
            componentInstance = self.boardData.getElementByName('components', componentName)
            componentSide = componentInstance.getSide()
            if componentSide != side:
                continue
            centerPoint = componentInstance.getCoords()
            self._drawMarker(surface, centerPoint.getXY(), color)
    
    def drawSelectedPins(self, surface:pygame.Surface, color:tuple[int, int, int], side:str):
        for componentName, pinsList in self.selectedNet.items():
            componentInstance = self.boardData.getElementByName('components', componentName)
            pinsInstancesList = [componentInstance.getPinByName(pinName) for pinName in pinsList]
            for pinInstance in pinsInstancesList:
                if componentInstance.getMountingType() == 'TH' or componentInstance.getSide() == side:
                    self.drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, width=0)

    def drawPins(self, surface:pygame.Surface, componentInstance:comp.Component, color:tuple[int, int, int], width:int=1):
        pinsDict = componentInstance.getPins()
        for _, pinInstance in pinsDict.items():
            self.drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, width)
    
    def _flipSurfaceXAxis(self, side:str):   
        if side in self.sidesForFlipX:  
            self.boardLayer = pygame.transform.flip(self.boardLayer, True, False)
            self.selectedComponentsSurface = pygame.transform.flip(self.selectedComponentsSurface, True, False)
            self.selectedNetSurface = pygame.transform.flip(self.selectedNetSurface, True, False)
            self.commonTypeComponentsSurface = pygame.transform.flip(self.commonTypeComponentsSurface, True, False)
    
    def drawInstanceAsCirlceOrPolygon(self, surface:pygame.Surface, instance: pin.Pin|comp.Component, color:tuple[int, int, int], width:int=1):
        if  instance.getShape() == 'CIRCLE':
            shape = instance.getShapeData()
            self.drawCircle(surface, color, shape, width)
        else:
            pointsList = instance.getShapePoints()
            self.drawPolygon(surface, color, pointsList, width)
        
    def blitBoardSurfacesIntoTarget(self, targetSurface:pygame.Surface):    
        targetSurface.fill((0, 0, 0))
        targetSurface.blit(self.boardLayer, self.offsetVector)

        self.commonTypeComponentsSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.commonTypeComponentsSurface, self.offsetVector)

        self.selectedComponentsSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.selectedComponentsSurface, self.offsetVector)

        self.selectedNetSurface.set_colorkey((0, 0, 0))
        targetSurface.blit(self.selectedNetSurface, self.offsetVector)

    def drawLine(self, surface:pygame.Surface, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        pygame.draw.line(surface, color, startPoint.getXY(), endPoint.getXY(), width)

    def drawArc(self, surface:pygame.Surface, color:tuple[int, int, int], arcInstance:gobj.Arc, width:int=1):
        def inversedAxisAngle(angleRad:float):
            return 2 * math.pi - angleRad

        rotationPoint, radius, startAngle, endAngle = arcInstance.getAsCenterRadiusAngles()
        x0, y0 = rotationPoint.getXY()
        x0 -= radius
        y0 -= radius

        startAngle, endAngle = inversedAxisAngle(endAngle), inversedAxisAngle(startAngle)
        pygame.draw.arc(surface, color, (x0, y0, 2 * radius, 2 * radius), startAngle, endAngle, width)

    def drawCircle(self, surface:pygame.Surface, color:tuple[int, int, int], circleInstance:gobj.Circle, width:int=1):
        centerPoint, radius = circleInstance.getCenterRadius()
        pygame.draw.circle(surface, color, centerPoint.getXY(), radius, width)

    def drawPolygon(self, surface:pygame.Surface, color:tuple[int, int, int], pointsList:list[gobj.Point], width:int=1):
        pointsXYList = [point.getXY() for point in pointsList]
        pygame.draw.polygon(surface, color, pointsXYList, width)
    
    def _drawMarker(self, surface:pygame.Surface, coordsXY:list[int, int], color:tuple[int, int, int]):
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

    filePath = openSchematicFile()
    boardWrapper = BoardCanvasWrapper(WIDTH, HEIGHT)
    boardWrapper.loadAndSetBoardFromFilePath(filePath)
    boardInstance = boardWrapper.normalizeBoard()
    print(boardInstance.getCommonTypeGroupedComponents())

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption(filePath)

    engine = DrawBoardEngine(WIDTH, HEIGHT)
    engine.setBoardData(boardInstance)
    engine.drawBoard(side)
    engine.blitBoardSurfacesIntoTarget(WIN)

    print('====================================')
    print('Pygame draw PCB engine')
    print('Move - mouse dragging')
    print('Zoom - scroll wheel')    
    print('Change side - ;')
    print('Rotate - , .')
    print('Select component by click mode - z')
    print('Find component by name - x')
    print('Clear arrow markers - c')
    print('Find net by name - v')
    print('Clear selected net - b')
    print('Clear arrow markers of selected net - n')   
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
                        engine.updateOffsetVector((dx, dy))                    
                        engine.blitBoardSurfacesIntoTarget(WIN)
                    else:
                        isMovingCalledFirstTime = False
            
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    engine.scaleUp(pygame.mouse.get_pos())
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                else:
                    engine.scaleDown(pygame.mouse.get_pos())
                    engine.drawBoard(side)                    
                    engine.blitBoardSurfacesIntoTarget(WIN)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SEMICOLON:
                    side = sideQueue.pop(0)
                    sideQueue.append(side)
                    engine.drawBoard(side)           
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_PERIOD:
                    rotationXY = [val / 2 for val in engine.surfaceDimensions]
                    engine.rotate(rotationXY, isClockwise=True)     
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_COMMA:
                    rotationXY = [val / 2 for val in engine.surfaceDimensions]
                    engine.rotate(rotationXY, isClockwise=False)     
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_z:
                    isFindComponentByClickActive = not isFindComponentByClickActive
                    print(f'Find component using clck mode active: {isFindComponentByClickActive}')
                
                elif event.key == pygame.K_x:
                    componentName = input('Component name: ')
                    engine.findComponentByName(componentName)
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_c:
                    engine.unselectComponents()
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_v:
                    netName = input('Net name: ')
                    engine.selectNet(netName)
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_b:
                    engine.unselectNet()
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                
                elif event.key == pygame.K_n:
                    engine.unselectComponentsOnNet()
                    engine.drawBoard(side)
                    engine.blitBoardSurfacesIntoTarget(WIN)
                

        ## display image
        pygame.display.update()
        #run = False

    pygame.quit()