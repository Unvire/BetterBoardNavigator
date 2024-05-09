import pygame
import boardCanvasWrapper, component, pin, board
import geometryObjects as gobj

class DrawBoardEngine:
    def __init__(self, width:int, height:int):
        self.boardData = None
        self.boardLayer = pygame.Surface((width, height))

    def setBoardData(self, boardData:board.Board):
        self.boardData = boardData
    
    def drawOutlines(self, side):
        shapesList = self.boardData.getOutlines()
        print(str(type(shapesList)))

    def blitBoardLayerIntoTarget(self, targetSurface:pygame.Surface):
        targetSurface.blit(self.boardLayer, (0, 0))

    def drawBoardOutlines(self, boardInstace:board.Board, side:str):
        outlines = boardInstace.getOutlines()
        for shape in outlines:
            print(type(shape))

    def drawLine(self, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        pygame.draw.line(self.boardLayer, color, startPoint.getXY(), endPoint.getXY())

    def drawArc(self, color:tuple[int, int, int], arcInstance:gobj.Arc, width:int=1):
        startPoint, endPoint = arcInstance.getPoints()[:2]
        x0, y0, = startPoint.getXY()
        x1, y1 = endPoint.getXY()
        endAngle, startAngle = arcInstance.getAsCenterRadiusAngles()[-2:] # y axis is mirrored so angles are swapped    
        pygame.draw.arc(self.boardLayer, color, (x0, y0, x1 - x0, y1 - y0), startAngle, endAngle, width)

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

    engine = DrawBoardEngine()
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
                pass

            elif event.type == pygame.MOUSEBUTTONUP:
                pass

            elif event.type == pygame.KEYDOWN:
               pass

        ## display image
        engine.drawBoardLayer(WIN, [boardLayer])
        pygame.display.update()
        #run = False

    pygame.quit()