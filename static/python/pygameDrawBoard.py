import pygame, math
import boardCanvasWrapper, pin, board
import geometryObjects as gobj
import component as comp

class DrawBoardEngine:
    def __init__(self, width:int, height:int):
        self.boardData = None
        self.drawHandler = {'Line': self.drawLine,
                            'Arc': self.drawArc}
        self.width = width
        self.height = height
        self.boardLayer = self._getEmptySurfce()

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
    
    def drawBoard(self, side:str):
        self.boardLayer = self._getEmptySurfce()
        self.drawOutlines((255, 255, 255))
        self.drawComponents((255, 255, 255), side)
    
    def drawOutlines(self, color:tuple[int, int, int], width:int=1):
        for shape in self.boardData.getOutlines():
            shapeType = shape.getType()
            self.drawHandler[shapeType](color, shape, width)
    
    def drawComponents(self, color:tuple[int, int, int], side:str, width:int=1):
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
                self.drawInstanceAsCirlceOrPolygon(componentInstance, color, width)

            self.drawPins(componentInstance, color, side, width)
    
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

    def blitBoardLayerIntoTarget(self, targetSurface:pygame.Surface, side:str):            
        if side == 'T':  
            self.boardLayer = pygame.transform.flip(self.boardLayer, True, False)
        targetSurface.blit(self.boardLayer, (0, 0))  

    def drawLine(self, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        pygame.draw.line(self.boardLayer, color, startPoint.getXY(), endPoint.getXY())

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

if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    WIDTH, HEIGHT = 1200, 700
    FPS = 60

    sideQueue = ['B', 'T']
    side = 'T'

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
    engine.blitBoardLayerIntoTarget(WIN, side)

    run = True
    while run:
        clock.tick(FPS)

        ## handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:
                pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SEMICOLON:
                    side = sideQueue.pop(0)
                    sideQueue.append(side)
                    engine.drawBoard(side)                    
                    engine.blitBoardLayerIntoTarget(WIN, side)
        ## display image
        
        pygame.display.update()
        #run = False

    pygame.quit()