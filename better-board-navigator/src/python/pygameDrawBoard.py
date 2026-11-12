import pygame, math, copy, re, itertools
import pin, board
from boardWrapper import BoardWrapper
import geometryObjects as gobj
from abstractShape import Shape
import component as comp

class DrawBoardEngine:
    CHUNK_SIZE_PX = 512
    COMPONENT_AREA_BONUS_BUFFER_PX = 30
    BONUS_SCALE_FACTOR = 1.05
    SCALE_BASE = 1.23
    STEP_MAX = 17
    STEP_MIN = -3
    DELTA_ROTATION_ANGLE_DEG = 5
    MIN_FONT_SIZE = 10
    MAX_FONT_SIZE = 26

    def __init__(self, width:int, height:int):
        pygame.font.init()

        self.boardData = None
        self.boardDataBackup = None
        self.drawHandler = {
            'Line': self._drawLine,
            'Arc': self._drawArc
        }
        
        self.colorsDict = {           
            'background': (0, 0, 0), 
            'outlines': (255, 255, 255),
            'components': (8, 212, 15),
            'TH pins': (21, 103, 235),
            'SMT pins': (240, 187, 12),
            'selected component marker': (255, 0, 0),
            'selected net marker': (171, 24, 149),
            'selection rectangle': (158, 158, 158)
        }
        
        self.boardBaseRectangle = None
        self.screenDimensions = [width, height]

        self.boardLayer = None
        self.commonTypeComponentsSurface = None
        self.selectedComponentsSurface = None
        self.selectedNetSurface = None
        self.fontSurface = None

        self.selectedComponentsSet = set()
        self.allSelectedNetComponentsSet = set()
        self.selectedNetComponentSet = set()
        self.selectedCommonTypePrefix = ''
        self.selectedNet = dict()

        self.fontCache = {}

        self.areaCache = {}
        self.surfaceChunks = {}

        self.scaleStep = 0
        self.offsetVector = []
        self.sidesForFlipX = {}
        self.isShowOutlines = True
        self.isShowComponentNames = False
        self.isDebug = False

    # === public methods ===
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
        return componentInstance.getSide() if componentInstance else ''
    
    def getComponentPinout(self, componentName:str) -> dict:
        componentInstance = self.boardData.getElementByName('components', componentName)
        pins = componentInstance.getPins()
        pinoutDict = {pinName:pinInstance.getNet() for pinName, pinInstance in pins.items()}
        return dict(sorted(pinoutDict.items(), key=lambda pinData: self._pinStringValue(pinData[0])))
        
    def getSelectedComponents(self) -> list[str]:
        return list(self.selectedComponentsSet)
    
    def getSelectedNetComponent(self) -> str:
        if self.selectedNetComponentSet:
            return list(self.selectedNetComponentSet)[0]
        return ''

    def checkIfPrefixExists(self, prefix:str) -> bool:
        return prefix in self.boardData.getCommonTypeGroupedComponents()['T'] or prefix in self.boardData.getCommonTypeGroupedComponents()['B']
    
    def getMostCommonPrefix(self) -> str:
        return self.boardData.getMostCommonPrefix()

    def findComponentByClick(self, cursorXY:list[int, int], side:str) -> list[str]:
        x, y = cursorXY
        xOffset, yOffset = self.offsetVector

        if side in self.sidesForFlipX:
            x = self._xForMirroredSurface(x + xOffset)
        else:
            x = x - xOffset
        y = y - yOffset
        
        clickedPoint = gobj.Point(x, y)
        return self.boardData.findComponentByCoords(clickedPoint, side)


    # === setting board data + helper methods ===
    def setBoardData(self, boardData:board.Board, isMakeBackup:bool=True):
        self._resetSelectionCollections()
        self._resetSurfaceVariables()
        
        self.boardData = boardData
        if isMakeBackup:
            self.boardDataBackup = copy.deepcopy(boardData)

        self._buildAreaCache()
        self._centerBoard()
        
    def _resetSelectionCollections(self):
        self.selectedComponentsSet = set()
        self.allSelectedNetComponentsSet = set()
        self.selectedCommonTypePrefix = ''
        self.selectedNet = dict()
        self.selectedNetComponentSet = set()
    
    def _resetSurfaceVariables(self):
        self.scaleStep = 0
        self.offsetVector = [0, 0]
        self.sidesForFlipX = {'T'}
        self.boardBaseRectangle = None
        self.fontCache = {}
        self.isShowComponentNames = False

    def _buildAreaCache(self):
        self.areaCache = {}
        self.areaCache['outlines'] = self.boardData.getOutlines()

        sideComponentsDict = self.boardData.getSideGroupedComponents()
        for side, sideComponentsList in sideComponentsDict.items():
            self.areaCache[side] = {}
            for componentName in sideComponentsList:
                componentInstance = self.boardData.getElementByName('components', componentName)
                self.areaCache[side][componentName] = componentInstance.getArea()
    
    def _centerBoard(self):
        screenWidth, screenHeight = self.screenDimensions
        boardWidth, boardHeight = self.boardData.getWidthHeight()

        xBoardOffset = (screenWidth - boardWidth) / 2
        yBoardOffset = (screenHeight - boardHeight) / 2
        self.offsetVector = [xBoardOffset, yBoardOffset]
    

    # === public interfaces for frame generation ===
    def moveBoardInterface(self, targetSurface:pygame.Surface, relativeXY:list[int, int], side:str) -> pygame.Surface:
        self._updateOffsetVector(relativeXY, side)                    
        return self._blitVisibleChunksIntoScreen(targetSurface, side)
    
    def scaleUpDownInterface(self, targetSurface:pygame.Surface, isScaleUp:bool, pointXY:list[int, int], side:str) -> pygame.Surface:
        if side in self.sidesForFlipX:
            x, y = pointXY
            x = self._xForMirroredSurface(x)
            pointXY = x, y

        if isScaleUp:
            isBlit = self._scaleUp(pointXY)
        else:
            isBlit = self._scaleDown(pointXY)

        if isBlit:
            targetSurface = self.drawChunksAndBlitInterface(targetSurface, side)
        return targetSurface
    
    def changeSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def rotateBoardInterface(self, targetSurface:pygame.Surface,  isClockwise:bool, side:str, angleDeg:float=None) -> pygame.Surface:
        self._rotate(isClockwise, angleDeg)   
        self._buildAreaCache() # each area is normalized after rotation, so references must be updated
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def findComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        self._findComponentByName(componentName)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def componentInScreenCenterInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        componentInstance = self.boardData.getElementByName('components', componentName)
        if not componentInstance:
            return targetSurface
        
        componentSide  = componentInstance.getSide()
        if componentSide == side:
            self._setComponentInScreenCenter(componentInstance, side)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def clearFindComponentByNameInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectComponents()
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def selectNetByNameInterface(self, targetSurface:pygame.Surface, netName:str, side:str) -> pygame.Surface:
        if netName:
            self._selectNet(netName)
        else:
            self._unselectNet()
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def selectNetComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface:
        self._selectNetComponentByName(componentName)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def unselectNetInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectNet()
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def showCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, prefix:str, side:str) -> pygame.Surface:
        self._selectCommonTypeComponents(side, prefix)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def clearCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._unselectCommonTypeComponents()
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def flipUnflipCurrentSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._flipUnflipCurrentSide(side)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def useComponentAreaInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        BoardWrapper.useAreaFromComponentsInPlace(self.boardData)
        boardDataNormalized = self._getNormalizedBoard(self.screenDimensions, self.boardData)
        self.setBoardData(boardDataNormalized, isMakeBackup=False)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def resetToDefaultViewInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self.boardData = copy.deepcopy(self.boardDataBackup)
        self.setBoardData(self.boardData)
        return self.drawChunksAndBlitInterface(targetSurface, side)

    def showHideOutlinesInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._showHideOutlines()
        return self.drawChunksAndBlitInterface(targetSurface, side)

    def showHideComponentNamesInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._showHideComponentNames()
        return self.drawChunksAndBlitInterface(targetSurface, side)

    def changeScreenDimensionsInterface(self, targetSurface:pygame.Surface, dimensions:tuple[int, int], side:str) -> pygame.Surface:
        self.screenDimensions = dimensions[:]
        boardDataNormalized = self._getNormalizedBoard(dimensions, self.boardData)
        self.setBoardData(boardDataNormalized, isMakeBackup=True)
        return self.drawChunksAndBlitInterface(targetSurface, side)
    
    def toggleDebugModeInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._toggleDebugMode()
        self.drawChunksAndBlitInterface(targetSurface, side)

    def drawChunksAndBlitInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        self._chunkifyBoard(side)
        return self._blitVisibleChunksIntoScreen(targetSurface, side)
    

    ## === private helper methods for interfces ===
    def _getNormalizedBoard(self, surfaceDimensions:tuple[int, int], boardInstance:board.Board) -> board.Board:
        width, height = surfaceDimensions
        wrapper = BoardWrapper(width, height)
        wrapper.setBoard(boardInstance)
        return wrapper.normalizeBoard()
    
    def _updateOffsetVector(self, relativeVector:tuple[int, int], side:str):
        xMove, yMove = self.offsetVector
        dx, dy = relativeVector

        if side in self.sidesForFlipX:
            dx *= -1

        self.offsetVector = [xMove + dx, yMove + dy]
    
    def _rotate(self, isClockwise:bool, angleDeg:float=None):
        if not angleDeg:
            angleDeg = self.DELTA_ROTATION_ANGLE_DEG

        if isClockwise:
            angleDeg *= -1

        # board is moved to 0,0 in this operation, width, height can be used to calculated center of rotation
        originWidth, originHeight = self.boardData.getWidthHeight()
        BoardWrapper.rotateBoardInPlaceAroundAreaCenter(self.boardData, angleDeg) 
        rotatedWidth, rotatedHeight = self.boardData.getWidthHeight()
        
        # we are rotating around center so each point moves exactly 1/2 * (originXY - rotatedXY)
        xOffset, yOffset = self.offsetVector
        dx = (originWidth - rotatedWidth) / 2
        dy = (originHeight - rotatedHeight) / 2

        self.offsetVector = [xOffset + dx, yOffset + dy]     
    
    def _scaleUp(self, zoomingPoint:tuple[int, int]) -> bool:
        if self.scaleStep + 1 > self.STEP_MAX:
            return False

        previousStep = self.scaleStep
        self.scaleStep += 1
        self._commonScalingOperations(zoomingPoint, previousStep)
        return True

    def _scaleDown(self, zoomingPoint:tuple[int, int]):
        if self.scaleStep - 1 < self.STEP_MIN:
            return False
        
        previousStep = self.scaleStep
        self.scaleStep -= 1
        self._commonScalingOperations(zoomingPoint, previousStep)
        return True
    
    def _commonScalingOperations(self, zoomingPoint:tuple[int, int], previousStepValue:int):
        originBoardWidthHeight = self.boardData.getWidthHeight()

        # board is scaled by multiplication by a relative factor (self.SCALE_BASE or 1/self.SCALE_BASE)
        relativeScaleFactor = self.SCALE_BASE if (self.scaleStep - previousStepValue) > 0 else 1 / self.SCALE_BASE
        BoardWrapper.scaleBoardInPlace(self.boardData, relativeScaleFactor)
        scaledBoardWidthHeight = self.boardData.getWidthHeight()

        self._updateOffsetVectorForScaledSurface(zoomingPoint, originBoardWidthHeight, scaledBoardWidthHeight)
    
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
        if componentName in self.selectedNetComponentSet:
            self.selectedNetComponentSet = set()

        elif componentName in self.allSelectedNetComponentsSet:
            self.selectedNetComponentSet = {componentName}
    
    def _setComponentInScreenCenter(self, componentInstance:comp.Component, side:str):
        coords = componentInstance.getCoords()
        xComp, yComp = coords.getXY()
        xScreen, yScreen = self.screenDimensions

        
        if side in self.sidesForFlipX:
            xComp = self._xForMirroredSurface(xComp)

        y = yScreen / 2 - yComp
        x = xScreen / 2 - xComp

        if side in self.sidesForFlipX:
            x *= -1
            
        self.offsetVector = [x, y]
    
    def _selectNet(self, netName:str):
        net = self.boardData.getElementByName('nets', netName)
        if not net:
            return
        
        self.allSelectedNetComponentsSet = set(net)
        for componentName, parameters in net.items():
            self.selectedNet[componentName] = parameters['pins']
    
    def _unselectComponents(self):
        self.selectedComponentsSet = set()
    
    def _unselectNet(self):        
        self.allSelectedNetComponentsSet = set()
        self.selectedNetComponentSet = set()
        self.selectedNet = dict()
    
    def _selectCommonTypeComponents(self, side:str, prefix:str):
        prefix = prefix.upper()
        if prefix in self.boardData.getCommonTypeGroupedComponents()[side]:
            self.selectedCommonTypePrefix = prefix
    
    def _unselectCommonTypeComponents(self):
        self.selectedCommonTypePrefix = ''
    
    def _flipUnflipCurrentSide(self, side:str):
        if side in self.sidesForFlipX:
            self.sidesForFlipX.remove(side)
        else:
           self.sidesForFlipX.add(side) 
    
    def _showHideOutlines(self):
        self.isShowOutlines = not self.isShowOutlines
    
    def _showHideComponentNames(self):
        self.isShowComponentNames = not self.isShowComponentNames
    
    def _toggleDebugMode(self):
        self.isDebug = not self.isDebug
    
    def _updateOffsetVectorForScaledSurface(self, zoomingPoint:tuple[int, int], originSurfaceDimensions:tuple[int|float, int|float], 
                scaledSurfaceDimensions:tuple[int|float, int|float]):
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
        ####################################

        pointMoveReversed = reverseSurfaceLinearTranslation(zoomingPoint, self.offsetVector)
        pointRelativeToSurface = calculatePointCoordsRelativeToSurfaceDimensions(pointMoveReversed, originSurfaceDimensions)
        pointInScaledSurface = calcluatePointInScaledSurface(scaledSurfaceDimensions, pointRelativeToSurface)
        xOffset, yOffset = translateScaledPointToCursorPosition(pointInScaledSurface, zoomingPoint)

        self.offsetVector = [xOffset, yOffset]
        
    
    # === private chunk generation logic ===
    def _chunkifyBoard(self, side:str):
        self.surfaceChunks = {}

        width, height = self.boardData.getWidthHeight()
        rows = math.ceil(width / self.CHUNK_SIZE_PX)
        cols = math.ceil(height / self.CHUNK_SIZE_PX)
        
        iRange, jRange = range(rows), range(cols)
        for i, j in itertools.product(iRange, jRange):
            chunkCoordsPx = [i * self.CHUNK_SIZE_PX, j * self.CHUNK_SIZE_PX]

            self.surfaceChunks[(i, j)] = {
                'chunkOffsetXY': chunkCoordsPx,
                'outlinesInChunk': self._findOutlinesInChunk(chunkCoordsPx),
                'componentsInChunk': []
            }

        # map component to each chunk that overlap with its area
        sideComponentsCached =  self.areaCache[side].items()
        for componentName, componentArea in sideComponentsCached:
            instanceAreaXYXY = Shape.getAreaAsXYXY(componentArea)
            self._updateChunksComponentsThatOverlapAreaInPlace(instanceAreaXYXY, componentName)
    
    def _updateChunksComponentsThatOverlapAreaInPlace(self, instanceAreaXYXY:tuple[float, float, float, float], componentName:str):
        xMin, yMin, xMax, yMax = instanceAreaXYXY
        xMin -= self.COMPONENT_AREA_BONUS_BUFFER_PX
        yMin -= self.COMPONENT_AREA_BONUS_BUFFER_PX
        xMax += self.COMPONENT_AREA_BONUS_BUFFER_PX
        yMax += self.COMPONENT_AREA_BONUS_BUFFER_PX

        # x is responsible for columns and y is responsible for rows. Chunks are indexed as (row, col)
        startCol = int(xMin // self.CHUNK_SIZE_PX)
        endCol = int(xMax // self.CHUNK_SIZE_PX)
        startRow = int(yMin // self.CHUNK_SIZE_PX)
        endRow = int(yMax // self.CHUNK_SIZE_PX)

        rangeRows = range(startRow, endRow + 1)
        rangeCols = range(startCol, endCol + 1)

        for col, row in itertools.product(rangeCols, rangeRows):
            key = col, row
            if key not in self.surfaceChunks:
                continue

            self.surfaceChunks[key]['componentsInChunk'].append(componentName)    

    def _blitVisibleChunksIntoScreen(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface:
        color = self.colorsDict['background']
        targetSurface.fill(color)
        
        rowRange, colRange = self._calculateVisibleChunkRowAndColRanges(self.screenDimensions, self.offsetVector)
        for chunkKey in itertools.product(rowRange, colRange):      
            if chunkKey not in self.surfaceChunks:
                continue

            surfaceDataDict = self.surfaceChunks[chunkKey]
            if 'chunkSurface' in surfaceDataDict:
                chunkSurface = surfaceDataDict['chunkSurface']
            else:
                chunkSurface = self._drawChunkSurface(surfaceDataDict, side)
                surfaceDataDict['chunkSurface'] = chunkSurface

            chunkSurface = self._blitDebugData(chunkSurface, chunkKey)
            
            chunkSurface.set_colorkey(color)
            xDraw, yDraw = self._calculateChunkDrawingOffset(chunkKey, side)
            targetSurface.blit(chunkSurface, [xDraw, yDraw])
        return targetSurface        

    def _calculateVisibleChunkRowAndColRanges(self, screenDimensions:tuple[int, int], currentOffset:tuple[int, int]) -> tuple[range, range]:
        screenWidth, screenHeight = screenDimensions
        xOffset, yOffset = currentOffset

        screenLeft = -xOffset
        screenTop = -yOffset
        screenRight = screenLeft + screenWidth
        screenBottom = screenTop + screenHeight

        iStart, iEnd = math.floor(screenLeft / self.CHUNK_SIZE_PX), math.ceil(screenRight / self.CHUNK_SIZE_PX)
        rowRange = range(iStart, iEnd)

        jStart, jEnd = math.floor(screenTop / self.CHUNK_SIZE_PX), math.ceil(screenBottom / self.CHUNK_SIZE_PX)
        colRange = range(jStart, jEnd)
        return rowRange, colRange

    def _drawChunkSurface(self, chunkData:dict, side:str) -> pygame.Surface:
        chunkSurface = self._getEmptySurfce()
        chunkOffsetXY = chunkData['chunkOffsetXY']
        chunkComponentsSet = set(chunkData['componentsInChunk'])

        # draw outlines
        self._drawOutlinesInChunkInPlace(chunkSurface=chunkSurface, chunkOffsetXY=chunkOffsetXY, 
            shapesList = chunkData['outlinesInChunk'] if self.isShowOutlines else []
        )

        # draw all components
        self._drawComponentsInPlace(surface=chunkSurface, side=side, chunkOffsetXY=chunkOffsetXY, 
            width = 1,
            componentNamesList = chunkData['componentsInChunk']
        )

        # draw common type components
        commonTypeComponents = self._getCommonPrefixComponents(side, self.selectedCommonTypePrefix)
        componentNamesSet = chunkComponentsSet & set(commonTypeComponents)
        self._drawComponentsInPlace(surface=chunkSurface, side=side, chunkOffsetXY=chunkOffsetXY, 
            width = 0,
            componentNamesList = list(componentNamesSet), 
        )

        # draw red arrow markers
        componentNamesSet = chunkComponentsSet & self.selectedComponentsSet
        self._drawMarkersInPlace(surface=chunkSurface, side=side, chunkOffsetXY=chunkOffsetXY,
            componentNamesList = list(componentNamesSet), 
            color = self.colorsDict['selected component marker']
        )
        
        # draw pads that belong to selected net
        componentNamesSet = (chunkComponentsSet & set(self.selectedNet)) if self.selectedNet else set()
        self._drawSelectedPinsInPlace(surface=chunkSurface, side=side, chunkOffsetXY=chunkOffsetXY,
            componentNamesSet = componentNamesSet
        )

        # draw selected net components
        componentNamesSet = chunkComponentsSet & self.selectedNetComponentSet
        self._drawMarkersInPlace(surface=chunkSurface, side=side, chunkOffsetXY=chunkOffsetXY,
            componentNamesList = list(componentNamesSet), 
            color = self.colorsDict['selected net marker']
        )

        # apply mirroring in X-Axis
        if side in self.sidesForFlipX:
           chunkSurface = pygame.transform.flip(chunkSurface, True, False)
        
        # add component names (text must be unflipped)
        self._renderComponentNamesInPlace(surface=chunkSurface, chunkOffsetXY=chunkOffsetXY, side=side,
            sideComponents = chunkData['componentsInChunk'] if self.isShowComponentNames else []
        )

        return chunkSurface
    
    def _blitDebugData(self, chunkSurface:pygame.Surface, chunkCoords:tuple[int, int]) -> pygame.Surface:
        if not self.isDebug:
            return chunkSurface
        
        pygame.draw.rect(chunkSurface, (255, 0, 0), (0, 0, self.CHUNK_SIZE_PX, self.CHUNK_SIZE_PX), width=2)
        #pygame.image.save(chunkSurface, f'chunk {chunkCoords}.png')

        i, j = chunkCoords
        chunkIdText = f'[{i}, {j}]'

        debugFont = pygame.font.SysFont('Arial', 24)
        textSurface = debugFont.render(chunkIdText, True, (255, 0, 0))
        textBackground = pygame.Surface(textSurface.get_size(), pygame.SRCALPHA)
        textBackground.fill((0, 0, 0, 150))
        textBackground.blit(textSurface, (0, 0))
        chunkSurface.blit(textBackground, (5, 5))
        return chunkSurface
    
    def _calculateChunkDrawingOffset(self, chunkCoords:tuple[int, int], side:str) -> tuple[float, float]:
        i, j = chunkCoords
        xOffset, yOffset = self.offsetVector

        xDraw = (i * self.CHUNK_SIZE_PX) + xOffset
        yDraw = (j * self.CHUNK_SIZE_PX) + yOffset
        if side in self.sidesForFlipX:
            xDraw = self._xForMirroredSurface(xDraw)
            xDraw -= self.CHUNK_SIZE_PX

        return xDraw, yDraw
    
    def _findOutlinesInChunk(self, coordsPx:tuple[int, int]) -> list[gobj.Line|gobj.Arc]:
        result = []
        chunkCornersXYXY = self._calculateChunkBoundariesXYXY(coordsPx)
        for shape in self.areaCache['outlines']:
            areaCornersXYXY = Shape.getAreaAsXYXY(shape.getArea())
            if self._is2AreasOverlap(chunkCornersXYXY, areaCornersXYXY):
                result.append(shape)

        return result

    def _drawOutlinesInChunkInPlace(self, chunkSurface:pygame.Surface, chunkOffsetXY:tuple[int, int], shapesList:list[gobj.Line|gobj.Point]):
        for shape in shapesList:
            shapeType = shape.getType()
            color = self.colorsDict['outlines']
            self.drawHandler[shapeType](chunkSurface, color, shape, chunkOffsetXY=chunkOffsetXY, width=1)

    def _calculateChunkBoundariesXYXY(self, chunkCoords:tuple[int, int]) -> tuple[int, int, int, int]:
        x0, y0 = chunkCoords
        return x0, y0, x0 + self.CHUNK_SIZE_PX, y0 + self.CHUNK_SIZE_PX

    def _is2AreasOverlap(self, chunkCorners:tuple[int, int, int, int], areaCorners:tuple[int, int, int, int]) -> bool:
        xC_Min, yC_Min, xC_Max, yC_Max = chunkCorners
        xA_Min, yA_Min, xA_Max, yA_Max = areaCorners

        overlapX = (xA_Min <= xC_Max) and (xA_Max >= xC_Min)
        overlapY = (yA_Min <= yC_Max) and (yA_Max >= yC_Min)
        return overlapX and overlapY

    def _getEmptySurfce(self) -> pygame.Surface:
        color = self.colorsDict['background']
        dimensions = [self.CHUNK_SIZE_PX, self.CHUNK_SIZE_PX]
        surface = pygame.Surface(dimensions)
        surface.fill(color)
        return surface
        
    def _getCommonPrefixComponents(self, side:str, prefix:str) -> list[str]:
        commonTypeSideComponents = self.boardData.getCommonTypeGroupedComponents()[side]
        commonPrefixSideComponentNames = commonTypeSideComponents.get(prefix, [])
        return commonPrefixSideComponentNames

    

    # === draw complex shapes logic (components, pads, outlines ...) ===    
    def _drawComponentsInPlace(self, surface:pygame.Surface, componentNamesList:list[str], side:str, chunkOffsetXY:tuple[int, int], width:int=1):
        componentColor = self.colorsDict['components']
        pinColorDict = {
            'SMT': self.colorsDict['SMT pins'], 
            'SMD': self.colorsDict['SMT pins'], 
            'TH':self.colorsDict['TH pins']
        }
        
        componentColor = self.colorsDict['components']
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
                self._drawInstanceAsCirlceOrPolygon(surface, componentInstance, componentColor, chunkOffsetXY, width)

            pinsColor = pinColorDict[componentInstance.getMountingType()]
            self._drawPins(surface, componentInstance, pinsColor, chunkOffsetXY, width)
    
    def _drawMarkersInPlace(self, surface:pygame.Surface, componentNamesList:list[str], color:tuple[int, int, int], side:str, chunkOffsetXY:tuple[int, int]):
        for componentName in componentNamesList:
            componentInstance = self.boardData.getElementByName('components', componentName)
            if componentInstance.getMountingType() == 'TH' or componentInstance.getSide() == side:
                centerPoint = componentInstance.getCoords()
                self._drawMarkerArrow(surface, centerPoint.getXY(), color, chunkOffsetXY)
    
    def _drawSelectedPinsInPlace(self, surface:pygame.Surface, componentNamesSet:set, side:str, chunkOffsetXY:tuple[int, int]):
        color = self.colorsDict['selected net marker']
        for componentName, pinsList in self.selectedNet.items():
            if componentName not in componentNamesSet:
                continue

            componentInstance = self.boardData.getElementByName('components', componentName)
            pinsInstancesList = [componentInstance.getPinByName(pinName) for pinName in pinsList if componentInstance]
            for pinInstance in pinsInstancesList:
                if componentInstance.getMountingType() == 'TH' or componentInstance.getSide() == side:
                    self._drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, chunkOffsetXY, width=0)

    def _drawPins(self, surface:pygame.Surface, componentInstance:comp.Component, color:tuple[int, int, int], chunkOffsetXY:tuple[int, int], width:int=1):
        pinsDict = componentInstance.getPins()
        for _, pinInstance in pinsDict.items():
            self._drawInstanceAsCirlceOrPolygon(surface, pinInstance, color, chunkOffsetXY, width)
    
    def _renderComponentNamesInPlace(self, surface:pygame.Surface, sideComponents:list[str], chunkOffsetXY:tuple[int, int], side:str):
        MIN_COMPONENT_SIZE_PX = 10
        EXAMPLE_FONT_SIZE = 10

        color = self.colorsDict['outlines']
        for componentName in sideComponents:
            componentInstance = self.boardData.getElementByName('components', componentName)
            area = componentInstance.getArea()
            width, height = Shape.getAreaWidthHeight(area)

            if max(width, height) < MIN_COMPONENT_SIZE_PX:
                continue

            textWidth, textHeight = self._getFontWidthHeight(EXAMPLE_FONT_SIZE, componentName)
            targetFontSize = self._calculateFontSize(width, height, textWidth, textHeight, EXAMPLE_FONT_SIZE)

            font = self._getFont(targetFontSize)
            renderedText = font.render(componentName, True, color)

            centerPoint = componentInstance.getCoords()
            x, y = centerPoint.getXY()
            xOffset, yOffset = chunkOffsetXY

            x -= xOffset
            y -= yOffset
            if side in self.sidesForFlipX:
                x = self.CHUNK_SIZE_PX - x
            textRect = renderedText.get_rect(center=(x, y))
            surface.blit(renderedText, textRect)
    
    def _drawInstanceAsCirlceOrPolygon(self, surface:pygame.Surface, instance: pin.Pin|comp.Component, color:tuple[int, int, int], 
                                            chunkOffsetXY:tuple[int, int], width:int=1):
        if  instance.getShape() == 'CIRCLE':
            shape = instance.getShapeData()
            self._drawCircle(surface, color, shape, chunkOffsetXY, width)
        else:
            pointsList = instance.getShapePoints()
            self._drawPolygon(surface, color, pointsList, chunkOffsetXY, width)    


    # === draw most basic shapes (lines, arcs, rectangles, arrows) ===
    def _drawLine(self, surface:pygame.Surface, color:tuple[int, int, int], lineInstance:gobj.Line, chunkOffsetXY:tuple[int, int], width:int=1):
        startPoint, endPoint = lineInstance.getPoints()
        xOffset, yOffset = chunkOffsetXY
        x0, y0 = startPoint.getXY()
        x1, y1 = endPoint.getXY()

        startXY = x0 - xOffset, y0 - yOffset
        endXY = x1 - xOffset, y1 - yOffset
        pygame.draw.line(surface, color, startXY, endXY, width)

    def _drawArc(self, surface:pygame.Surface, color:tuple[int, int, int], arcInstance:gobj.Arc, chunkOffsetXY:tuple[int, int], width:int=1):
        def inversedAxisAngle(angleRad:float):
            return 2 * math.pi - angleRad

        rotationPoint, radius, startAngle, endAngle = arcInstance.getAsCenterRadiusAngles()
        x0, y0 = rotationPoint.getXY()
        xOffset, yOffset = chunkOffsetXY

        xStart = x0 - radius - xOffset
        yStart = y0 - radius - yOffset

        startAngle, endAngle = inversedAxisAngle(endAngle), inversedAxisAngle(startAngle)
        pygame.draw.arc(surface, color, (xStart, yStart, 2 * radius, 2 * radius), startAngle, endAngle, width)

    def _drawCircle(self, surface:pygame.Surface, color:tuple[int, int, int], circleInstance:gobj.Circle, chunkOffsetXY:tuple[int, int], width:int=1):
        centerPoint, radius = circleInstance.getCenterRadius()
        x, y = centerPoint.getXY()
        xOffset, yOffset = chunkOffsetXY

        x -= xOffset
        y -= yOffset
        pygame.draw.circle(surface, color, (x, y), radius, width)

    def _drawPolygon(self, surface:pygame.Surface, color:tuple[int, int, int], pointsList:list[gobj.Point], chunkOffsetXY:tuple[int, int], width:int=1):
        def applyOffset(pointXY:tuple[float, float], offsetXY:tuple[int, int]) -> tuple[float, float]:
            x0, y0 = pointXY
            xOffset, yOffset = offsetXY
            return x0 - xOffset, y0 - yOffset
            
        pointsXYList = [applyOffset(point.getXY(), chunkOffsetXY) for point in pointsList]
        pygame.draw.polygon(surface, color, pointsXYList, width)
    
    def _drawMarkerArrow(self, surface:pygame.Surface, coordsXY:list[int, int], color:tuple[int, int, int], chunkOffsetXY:tuple[int, int]):
        x, y = coordsXY
        xOffset, yOffset = chunkOffsetXY

        x -= xOffset
        y -= yOffset
        k = self.SCALE_BASE ** self.scaleStep
        markerCoords = [
            (x, y), 
            (x - (5 * k), y - (12 * k)), 
            (x - (2 * k), y - (12 * k)), 
            (x - (2 * k), y - (60 * k)), 
            (x + (2 * k), y - (60 * k)), 
            (x + (2 * k), y - (12 * k)), 
            (x + (5 * k), y - (12 * k))
        ]
        pygame.draw.polygon(surface, color, markerCoords, width=0)
    

    # === font generation helpers === 
    def _getFontWidthHeight(self, fontSize:int, textToRender:str) -> tuple[int, int]:
        font = self._getFont(fontSize)
        textWidth, textHeight = font.size(textToRender)
        return textWidth, textHeight
    
    def _calculateFontSize(self, width:int, height:int, exampleTextWidth:int, exampleTextHeight:int, exampleFontSize:int) -> int:
        sizeByWidth = (width / exampleTextWidth) * exampleFontSize
        sizeByHeight = (height / exampleTextHeight) * exampleFontSize

        fontSize = int(min(sizeByWidth, sizeByHeight))
        fontSize = max(self.MIN_FONT_SIZE, min(fontSize, self.MAX_FONT_SIZE))
        return fontSize
    
    def _getFont(self, fontSize:int) -> pygame.font.Font:
        size = max(1, int(fontSize))
        if size not in self.fontCache:
            self.fontCache[size] = pygame.font.Font(None, size)
        return self.fontCache[size]
    

    # === multi use helpers ===
    def _xForMirroredSurface(self, x:float) -> float:
        surfaceWidth = self.screenDimensions[0]
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
            if not componentNumber.isnumeric():
                componentNumber = 0
        except ValueError:
            componentType = componentName
            componentNumber = 0
        return stringValue(componentType) + int(componentNumber)
        


if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    WIDTH, HEIGHT = 1485, 841
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
    print('Components: ', engine.getComponents())
    print('Nets: ', engine.getNets())

    engine.drawChunksAndBlitInterface(WIN, side)
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
    print('Highlight common type components - a')
    print('Clear common type components - s')
    print('Change screen surface dimensions - g')
    print('Set component in screen center - h')
    print('Select component on net (net must be drawn before) - j')
    print('Show/hide component names - k')
    print('Toggle/untoggle debug mode - l')
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
                        engine.moveBoardInterface(WIN, [dx, dy], side)
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
                
                elif event.key == pygame.K_a:
                    prefix = input('Common type prefix: ')
                    engine.showCommonTypeComponentsInterface(WIN, prefix, side)
                
                elif event.key == pygame.K_s:
                    engine.clearCommonTypeComponentsInterface(WIN, side)
                
                elif event.key == pygame.K_m:
                    engine.flipUnflipCurrentSideInterface(WIN, side)
                
                elif event.key == pygame.K_d:
                    engine.useComponentAreaInterface(WIN, side)
                
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
                
                elif event.key == pygame.K_k:
                    engine.showHideComponentNamesInterface(WIN, side)
                
                elif event.key == pygame.K_l:
                    engine.toggleDebugModeInterface(WIN, side)

        
        ## display image
        pygame.display.update()
        #run = False

    pygame.quit()