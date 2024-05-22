import pygame, math
import boardCanvasWrapper, pin, board
import geometryObjects as gobj
import component as comp

class DrawBoardEngine:
    MIN_SCALE_FACTOR = 0.2
    STEP_FACTOR = 0.05
    MAX_SURFACE_DIMENSION = 10000

    def __init__(self, width:int, height:int):
        self.boardData = None
        self.drawHandler = {'Line': self.drawLine,
                            'Arc': self.drawArc}
        self.width = width
        self.height = height        
        self.targetSurfaceDimensions = [width, height]
        self.boardLayer = self._getEmptySurfce()
        self.scale = 1
        self.offsetVector = [0, 0]

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
    
    def setScale(self, factor:int|float):
        self.scale = factor
    
    def setOffsetVector(self, vector:tuple[int, int]):
        self.offsetVector = vector
    
    def updateOffsetVector(self, relativeVector:tuple[int, int]):
        xMove, yMove = self.offsetVector
        dx, dy = relativeVector
        self.offsetVector = [xMove + dx, yMove + dy]
    
    def scaleUp(self, zoomingPoint:tuple[int, int]):
        previousScaleFactor = self._getScaleFactorFromSurfaceDimensions()

        screenWidth, screenHeight = self.targetSurfaceDimensions
        isWidthTooBig = previousScaleFactor * screenWidth > DrawBoardEngine.MAX_SURFACE_DIMENSION
        isHeightTooBig = previousScaleFactor * screenHeight > DrawBoardEngine.MAX_SURFACE_DIMENSION
        if isWidthTooBig or isHeightTooBig:
            return

        if self.scale < 1:
            scaleFactor = 1 / self.scale
            self.scale += DrawBoardEngine.STEP_FACTOR
        else:
            self.scale += DrawBoardEngine.STEP_FACTOR
            scaleFactor = self.scale
        
        self._scaleWidthHeightByFactor(scaleFactor)
        newOffset = self._calculateNewAreaOffsetVector(zoomingPoint, previousScaleFactor)
        self.setOffsetVector(newOffset)
        self.boardData.scaleBoard(scaleFactor)

    def scaleDown(self, zoomingPoint:tuple[int, int]):
        previousScaleFactor = self._getScaleFactorFromSurfaceDimensions()

        if self.scale > DrawBoardEngine.MIN_SCALE_FACTOR:
            if self.scale > 1:
                scaleFactor = 1 / self.scale
                self.scale -= DrawBoardEngine.STEP_FACTOR
            else:
                self.scale -= DrawBoardEngine.STEP_FACTOR
                scaleFactor = self.scale
            
            self._scaleWidthHeightByFactor(scaleFactor)
            newOffset = self._calculateNewAreaOffsetVector(zoomingPoint, previousScaleFactor)
            self.setOffsetVector(newOffset)
            self.boardData.scaleBoard(scaleFactor)
    
    def _scaleWidthHeightByFactor(self, factor:int|float):
        self.width *= factor
        self.height *=  factor
    
    def _calculateNewAreaOffsetVector(self, zoomingPoint:tuple[int, int], previousScaleFactor:float):
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

        originSurfaceDimensions = [val * previousScaleFactor for val in self.targetSurfaceDimensions]

        pointMoveReversed = reverseSurfaceLinearTranslation(zoomingPoint, self.offsetVector)
        pointRelativeToSurface = calculatePointCoordsRelativeToSurfaceDimensions(pointMoveReversed, originSurfaceDimensions)
        pointInScaledSurface = calcluatePointInScaledSurface([self.width, self.height], pointRelativeToSurface)
        resultOffset = translateScaledPointToCursorPosition(pointInScaledSurface, zoomingPoint)
        return resultOffset
    
    def getScaleFactor(self) -> int|float:
        return self.scale
    
    def flipSurfaceIfTopSide(self, side:str):   
        if side == 'T':  
            self.boardLayer = pygame.transform.flip(self.boardLayer, True, False)
    
    def drawBoard(self, side:str):
        self.boardLayer = self._getEmptySurfce()
        self.drawOutlines((255, 255, 255), width=3)
        self.drawComponents((43, 194, 48), (252, 186, 3), side)
    
    def drawOutlines(self, color:tuple[int, int, int], width:int=1):
        for shape in self.boardData.getOutlines():
            shapeType = shape.getType()
            self.drawHandler[shapeType](color, shape, width)
    
    def drawComponents(self, componentColor:tuple[int, int, int], pinColor:tuple[int, int, int], side:str, width:int=1):
        componentNames = self.boardData.getSideGroupedComponents()[side]
        for componentName in componentNames:
            componentInstance = self.boardData.getElementByName('components', componentName)
            mountingType = componentInstance.getMountingType()
            componentSide = componentInstance.getSide()
            pinsDict = componentInstance.getPins()

            numOfPins = len(pinsDict)
            isSkipComponentSMT = mountingType == 'SMT' and componentSide == side and numOfPins == 1
            isSkipComponentTH = mountingType == 'TH' and componentSide != side
            isDrawComponent = not (isSkipComponentSMT or isSkipComponentTH)
            if isDrawComponent:
                self.drawInstanceAsCirlceOrPolygon(componentInstance, componentColor, width + 1)

            self.drawPins(componentInstance, pinColor, side, width)
    
    def drawPins(self, componentInstance:comp.Component, color:tuple[int, int, int], side:str, width:int=1):
        pinsDict = componentInstance.getPins()
        for _, pinInstance in pinsDict.items():
            self.drawInstanceAsCirlceOrPolygon(pinInstance, color, width)
    
    def drawInstanceAsCirlceOrPolygon(self, instance: pin.Pin|comp.Component, color:tuple[int, int, int], width:int=1):
        if  instance.getShape() == 'CIRCLE':
            shape = instance.getShapeData()
            self.drawCircle(color, shape, width)
        else:
            pointsList = instance.getShapePoints()
            self.drawPolygon(color, pointsList, width)

    def blitBoardLayerIntoTarget(self, targetSurface:pygame.Surface):    
        targetSurface.fill((0, 0, 0))
        targetSurface.blit(self.boardLayer, self.offsetVector)  

    def drawLine(self, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        pygame.draw.line(self.boardLayer, color, startPoint.getXY(), endPoint.getXY(), width)

    def drawArc(self, color:tuple[int, int, int], arcInstance:gobj.Arc, width:int=1):
        def inversedAxisAngle(angleRad:float):
            return 2 * math.pi - angleRad

        rotationPoint, radius, startAngle, endAngle = arcInstance.getAsCenterRadiusAngles()
        x0, y0 = rotationPoint.getXY()
        x0 -= radius
        y0 -= radius

        endAngle, startAngle = arcInstance.getAsCenterRadiusAngles()[-2:] # y axis is mirrored so angles are substracted from 2*pi 
        startAngle, endAngle = inversedAxisAngle(startAngle), inversedAxisAngle(endAngle)
        pygame.draw.arc(self.boardLayer, color, (x0, y0, 2 * radius, 2 * radius), startAngle, endAngle, width)

    def drawCircle(self, color:tuple[int, int, int], circleInstance:gobj.Circle, width:int=1):
        centerPoint, radius = circleInstance.getCenterRadius()
        pygame.draw.circle(self.boardLayer, color, centerPoint.getXY(), radius, width)

    def drawPolygon(self, color:tuple[int, int, int], pointsList:list[gobj.Point], width:int=1):
        pointsXYList = [point.getXY() for point in pointsList]
        pygame.draw.polygon(self.boardLayer, color, pointsXYList, width)
    
    def _getEmptySurfce(self) -> pygame.Surface:
        return pygame.Surface((self.width, self.height))
    
    def _getScaleFactorFromSurfaceDimensions(self) -> float:
        screenWidth, _ = self.targetSurfaceDimensions
        surfaceWidth = self.width
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

    filePath = openSchematicFile()
    boardWrapper = boardCanvasWrapper.BoardCanvasWrapper(WIDTH, HEIGHT)
    boardWrapper.loadAndSetBoardFromFilePath(filePath)
    boardInstance = boardWrapper.normalizeBoard()

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    
    engine = DrawBoardEngine(WIDTH, HEIGHT)
    engine.setBoardData(boardInstance)
    engine.drawBoard(side)
    engine.blitBoardLayerIntoTarget(WIN)

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
                    print(pygame.mouse.get_pos())
            
            elif event.type == pygame.MOUSEBUTTONUP:
                isMousePressed = False

            elif event.type == pygame.MOUSEMOTION:
                if isMousePressed:
                    dx, dy = pygame.mouse.get_rel()
                    if not isMovingCalledFirstTime:
                        engine.updateOffsetVector((dx, dy))                    
                        engine.blitBoardLayerIntoTarget(WIN)
                    else:
                        isMovingCalledFirstTime = False
            
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    engine.scaleUp(pygame.mouse.get_pos())
                    engine.drawBoard(side)
                    engine.blitBoardLayerIntoTarget(WIN)
                else:
                    engine.scaleDown(pygame.mouse.get_pos())
                    engine.drawBoard(side)                    
                    engine.blitBoardLayerIntoTarget(WIN)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SEMICOLON:
                    side = sideQueue.pop(0)
                    sideQueue.append(side)
                    engine.drawBoard(side)
                    engine.flipSurfaceIfTopSide(side)                    
                    engine.blitBoardLayerIntoTarget(WIN)

        ## display image
        pygame.display.update()
        #run = False

    pygame.quit()