import pygame
import boardCanvasWrapper, component, pin 

def drawBoardLayer(targetSurface:pygame.Surface, surfaces:list[pygame.Surface]):
    targetSurface.fill((0, 0, 0))
    for surface in surfaces:
        targetSurface.blit(surface, (0, 0))

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
        pygame.display.update()
        #run = False

    pygame.quit()