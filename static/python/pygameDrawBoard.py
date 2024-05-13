import pygame, math
import boardCanvasWrapper, component, pin, board
import geometryObjects as gobj

class DrawBoardEngine:
    def __init__(self, width:int, height:int):
        self.boardData = None
        self.boardLayer = pygame.Surface((width, height))
        self.drawHandler = {'Line': self.drawLine,
                            'Arc': self.drawArc}
        self.width = width
        self.height = height

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
    
    def drawOutlines(self, side:str, color:tuple[int, int, int], width:int=1):
        # handle side mirroring
        for i, shape in enumerate(self.boardData.getOutlines()):
            shapeType = shape.getType()
            self.drawHandler[shapeType](color, shape, width)

    def blitBoardLayerIntoTarget(self, targetSurface:pygame.Surface):
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

if __name__ == '__main__':
    WIDTH, HEIGHT = 1200, 700
    FPS = 60

    sideQueue = ['B', 'T']
    side = sideQueue[0]

    boardWrapper = boardCanvasWrapper.BoardCanvasWrapper(WIDTH, HEIGHT)
    boardWrapper.loadAndSetBoardFromFilePath(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\nexyM.GCD')
    boardInstance = boardWrapper.normalizeBoard()

    engine = DrawBoardEngine(WIDTH, HEIGHT)
    engine.setBoardData(boardInstance)

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

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
               pass
        
        ## display image
        engine.drawOutlines('B', (255, 255, 255))
        engine.blitBoardLayerIntoTarget(WIN)

        pygame.display.update()
        #run = False

    pygame.quit()