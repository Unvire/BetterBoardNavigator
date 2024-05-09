import pygame
import boardCanvasWrapper, component, pin
import geometryObjects as gobj

def drawBoardLayer(targetSurface:pygame.Surface, surfaces:list[pygame.Surface]):
    targetSurface.fill((0, 0, 0))
    for surface in surfaces:
        targetSurface.blit(surface, (0, 0))

def drawLine(surface:pygame.Surface, color:tuple[int, int, int], lineInstance:gobj.Line, width:int=1):
    startPoint, endPoint = lineInstance.getPoints()
    pygame.draw.line(surface, color, startPoint.getXY(), endPoint.getXY())

def drawArc(surface:pygame.Surface, color:tuple[int, int, int], arcInstance:gobj.Arc, width:int=1):
    startPoint, endPoint = arcInstance.getPoints()[:2]
    x0, y0, = startPoint.getXY()
    x1, y1 = endPoint.getXY()
    endAngle, startAngle = arcInstance.getAsCenterRadiusAngles()[-2:] # y axis is mirrored so angles are swapped    
    pygame.draw.arc(surface, color, (x0, y0, x1 - x0, y1 - y0), startAngle, endAngle, width)

def drawCircle(surface:pygame.Surface, color:tuple[int, int, int], circleInstance:gobj.Circle, width:int=1):
    centerPoint, radius = circleInstance.getCenterRadius()
    pygame.draw.circle(surface, color, centerPoint.getXY(), radius, width)

def drawPolygon(surface:pygame.Surface, color:tuple[int, int, int], pointsList:list[gobj.Point], width:int=1):
    pointsXYList = [point.getXY() for point in pointsList]
    pygame.draw.polygon(surface, color, pointsXYList, width)

if __name__ == '__main__':
    WIDTH, HEIGHT = 1200, 700
    FPS = 60

    sideQueue = ['B', 'T']
    side = sideQueue[0]

    boardWrapper = boardCanvasWrapper.BoardCanvasWrapper(WIDTH, HEIGHT)
    boardWrapper.loadAndSetBoardFromFilePath(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\nexyM.GCD')
    boardInstance = boardWrapper.normalizeBoard()

    ## pygame
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    boardLayer = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    lineInstance = gobj.Line(gobj.Point(100, 100), gobj.Point(1000, 630))
    arcInstance = gobj.Arc(gobj.Point(200, 200), gobj.Point(400, 400) ,gobj.Point(400, 200))
    circleInstance = gobj.Circle(gobj.Point(500, 500), 50)
    polygonInstance = [gobj.Point(100, 100), gobj.Point(200, 100), gobj.Point(300, 300)]

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
            
        drawPolygon(boardLayer, (255, 255, 255), polygonInstance)

        ## display image
        drawBoardLayer(WIN, [boardLayer])
        pygame.display.update()
        #run = False

    pygame.quit()