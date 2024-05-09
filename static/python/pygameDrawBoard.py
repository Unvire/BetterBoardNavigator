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
            
        drawLine(boardLayer, (255, 255, 255), lineInstance)

        ## display image
        drawBoardLayer(WIN, [boardLayer])
        pygame.display.update()
        #run = False

    pygame.quit()