I am to lazy to write whole doc and I was learning JS  with this project. Below you can find logic of code (without going into details):

# Part 1: Processing cad files
**Modules and classes**
```
loaderSelectorFactory.py -> LoaderSelectorFactory
camcadLoader.py -> CamCadLoader
gencadLoader.py -> GenCadLoader
odbPlusPlusLoader.py -> ODBPlusPlusLoader
visecadLoader.py -> VisecadLoader
```

Currently 3 types of files are fully supported: camcad (.cad), gencad (.gcd) and odb++ (.zip or .tgz). CCZ files are implemented but not working properly.

To load a file user should use the factory:
```python
factory = LoaderSelectorFactory('.cad') #or different file extenstion
fileLines = loader.loadFile(filePath)
boardInstance = loader.processFileLines(fileLines)
```

All of the board processing classes implement common interfaces, that are called by the factory:
```python
fileLines = loaderInstance.loadFile(filePath) # returns list of raw text file lines
boardInstance = loaderInstance.processFileLines(fileLines)
```

# Part 2: Extracting data from cad files
Examples of processing sections of files can be found in the tests.

## CAMCAD
**Modules and classes**
```
camcadLoader.py -> CamCadLoader
```

Processing file lines logic:
```python
def processFileLines(self, fileLines:list[str]) -> board.Board:       
    # save sections start and end line
    self._getSectionsLinesBeginEnd(fileLines)

    # get board dimensions from BOARDINFO or BOARDOUTLINE
    self._getBoardDimensions(fileLines, self.boardData)

    # extract components from PARTLIST
    partNumberToComponents = self._getComponenentsFromPARTLIST(fileLines, self.boardData)

    # extract pad shapes from PAD
    padsDict = self._getPadsFromPAD(fileLines, self.boardData.getWidthHeight())

    # extract nets. Assign pads to components. Assign pads to nets
    matchedComponents = self._getNetsFromNETLIST(fileLines, padsDict, self.boardData)

    # assign shapes to components from PACKAGES. Return list of components without package
    componentWithoutpackages = self._getPackages(fileLines, partNumberToComponents, self.boardData)

    # rotate components. Build rectangular shape that covers pads for components without package
    self._rotateComponents(self.boardData, componentWithoutpackages)

    # remove VIAs and not matched compponents
    self._removeNotMatchedComponents(self.boardData, matchedComponents)

    return self.boardData
```

## GENCAD
**Modules and classes**
```
gencadLoader.py -> GenCadLoader
```

Processing file lines logic:
```python
def processFileLines(self, fileLines:list[str]) -> board.Board:
    # save sections start and end line
    self._getSectionsLinesBeginEnd(fileLines)

    # get board dimensions from BOARD
    self._getBoardDimensions(fileLines, self.boardData)

    # get all needed structures: pads (names -> shape), artwork (name -> shape), components (name -> position, angle, pads)
    padsDict = self._getPadsFromPADS(fileLines)
    artworksDict = self._getArtWorksFromARTWORKS(fileLines) #sometimes pad shape is stored as artwork
    padstackDict = self._getPadstacksFromPADSTACKS(fileLines, padsDict)
    shapeToComponentsDict = self._getComponentsFromCOMPONENTS(fileLines, self.boardData)
    shapesDict = self._getAreaPinsfromSHAPES_ARTWORKS(fileLines, artworksDict)

    # merge all helper structures into compononents
    self._addShapePadDataToComponent(self.boardData, shapeToComponentsDict, shapesDict, padstackDict)

    # get net -> pad assignment
    self._getNetsFromSIGNALS(fileLines, self.boardData)
    return self.boardData
```

## ODB++
**Modules and classes**
```
odbPlusPlusLoader.py -> ODBPlusPlusLoader
unlzw3.py -> unlzw
```

Processing file lines logic:
```python

# odb++ is zipped folder structure, so it raw file lines must be extracted
def loadFile(self, filePath:str) -> list[str]:
    self._setFilePath(filePath)
    fileLines = self._getFileLinesFromArchive()
    return fileLines

# important data is stored in 4 files. Paths for them are validated with the patterns below. Files can be additionaly zipped (.Z extension).
# For that case unlzw3 function is used

commonPattern = r'^[\w+\s\-]+\/steps\/[\w+\s\-]+\/'
botComponentsFilePattern = commonPattern + r'layers\/comp_\+_bot\/components(.(z|Z))?$' # matches comp_+_bot files both zipped and uzipped
topComponentsFilePattern = commonPattern + r'layers\/comp_\+_top\/components(.(z|Z))?$' # matches comp_+_top files both zipped and uzipped
edaFilePattern = commonPattern + r'eda\/data(.(z|Z))?$' # matches eda path both zipped and unzipped
profileFilePattern = commonPattern + r'profile(.(z|Z))?$'  # matches profile path both zipped and unzipped

# raw text is then extracted from these files and send as `return fileLines` for processing function



def processFileLines(self, fileLines:list[str]) -> board.Board:
    # save sections start and end line (sections are build by loadFile method)
    self._getSectionsFromFileLines(fileLines)

    self._getBoardOutlineFromProfileFile(self.fileLines['profile'], self.boardData)
    packageIDToComponentNameDict, componentIDToNameDict = self._getComponentsFromCompBotTopFiles(self.fileLines['comp_+_bot'], self.fileLines['comp_+_top'], self.boardData)
    packagesDict = self._getPackagesFromEda(self.fileLines['eda'])
    netsDict = self._getNetsFromEda(self.fileLines['eda'])
    self._assignPackagesToComponents(packageIDToComponentNameDict, packagesDict, self.boardData)
    self._assignNetsAndPins(componentIDToNameDict, netsDict, self.boardData)

    # for some reason components must be rotated twice the value in file lines
    self._fixRotationOfComponents(self.boardData)

    # rescale components relative to board size
    self._fixComponentsAreaScale(self.boardData)
    return self.boardData
```

# Part 3: Board instance and BoardWrapper
Classes and modules:
```
board.py -> Board
boardWrapper.py -> BoardWrapper
```

## Board
This is a dataclass for extracted data from cad file.
properties:
```python
# area is given as 2 points: bottomLeftPoint and topRightPoint
self.area = [] 

# list of shapes: lines and arcs
self.outlines = []

# collection of components given as: {component name: componentInstance}
self.components = {}

# collection of components given as {netName: {'componentInstance': reference to component in self.components, 'pins': [list of pins]}}
self.nets = {}

# components grouped by their side and prefixes
self.sideGroupedComponents = {}
self.commonTypeGroupedComponents = {}

# most common prefix. It is assumed that this is a testpoint
self.mostCommonPrefix = ''
```


```python
# returns widest area:[bottomLeftPoint and topRightPoint] that all components can be inserted into
def calculateAreaFromComponents(self) -> tuple[gobj.Point, gobj.Point]: pass
    
# returns area:[bottomLeftPoint and topRightPoint] that all shapes can be inserted into
def calculateAreaFromOutlines(self) -> tuple[gobj.Point, gobj.Point]: pass
    
def translateRotateScaleBoard(self, functionName:str, *args):
    '''
    Calls translateInPlace, rotateInPlace or scaleInPlace on area, shapes and components.
    functionName must be: translateInPlace, rotateInPlace or scaleInPlace
    Arguments for functions:
        translateInPlace -> moveVector:list[int|float, int|float]
        rotateInPlace -> rotationPoint:geometryObjects.Point, angleDeg:int|float
        scaleInPlace -> factor:int|float
    '''
    pass

# returns [bottomLeftPoint and topRightPoint] from rotated shape
def normalizeArea(self, area:list[gobj.Point, gobj.Point]) -> list[gobj.Point, gobj.Point]: pass
    
# checks if clickedPoint is inside any of the components shape. Returns list of component names that clicked.
def findComponentByCoords(self, clickedPoint:gobj.Point, side:str) -> list[str]: pass
```


## BoardWrapper
This class is used as man in the middle between DrawBoardEngine and Board.

properties:
```python
# width and height of canvas in px
self.width = width
self.height = height

# board instance references. Board backup is a deepcopy of board for "reset to default" operation
self.board = None
self.boardBackup = None

# scaling and offset of canvas
self.baseScale = 0.0
self.baseMoveOffsetXY = [0.0, 0.0]

# groups for faster drawing - components grouped by side and prefix
self.sideComponents = {}
self.commonTypeComponents = {}


self.isCheckForPositiveCoordsActive = True
```

methods:
```python
# creates and sets Board instance
def loadAndSetBoardFromFilePath(self, filePath:str): pass
def loadAndSetBoardFromFileLines(self, fileName:str, fileLines:list[str]): pass

# recalculates all board elements (shapes, pads, components) so that they fit in area given earlier (self.width, self.height)
def normalizeBoard(self) -> board.Board: pass

# static method for in place operations
@staticmethod
def scaleBoardInPlace(board:board.Board, scaleFactor:float):
    board.translateRotateScaleBoard('scaleInPlace', scaleFactor)

@staticmethod
def rotateBoardInPlace(board:board.Board, rotationPoint:gobj.Point, angle:float):
    board.translateRotateScaleBoard('rotateInPlace', rotationPoint, angle)

@staticmethod
def translateBoardInPlace(board:board.Board, moveVector:list[float|int, float|int]):
    board.translateRotateScaleBoard('translateInPlace', moveVector)

@staticmethod
def useAreaFromComponentsInPlace(board:board.Board):
    bottomLeftPoint, topRightPoint = board.calculateAreaFromComponents()
    board.setArea(bottomLeftPoint, topRightPoint)

@staticmethod
def setAreaManually(board:board.Board, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
    board.setArea(bottomLeftPoint, topRightPoint)
```


# Part 4: Drawing the board
**Classes and modules:**
```
pygameDrawBoard.py -> DrawBoardEngine
```

This class is responsible for generating frame with the board on demand. It means that there is no pygame main loop and pygame is used as an image generator.
Colors and their meaning:
- black -> background
- white -> bord outlines
- green -> components
- yellow -> SMD pads
- blue -> TH pads
- violet -> selected net
- red arrow -> selected component by name

Displaying cad file:
```python
# get BoardWrapper and normalize the wrapped Board instance
wrapper = BoardWrapper(canvas.width, canvas.height)
wrapper.loadAndSetBoardFromFilePath(cadFileName)
boardInstance = wrapper.normalizeBoard()

# init and configure pygame
pygame.init()
pygame.display.set_caption('Better Board Navigator')
SURFACE = pygame.display.set_mode((canvas.width, canvas.height))

# set canvas dimensions and pass BoardWrapper to the engine
engine = DrawBoardEngine(canvas.width, canvas.height)
engine.setBoardData(boardInstance)

# generate frame and display it
side = 'T' # 'T' or 'B'
engine.drawAndBlitInterface(SURFACE, side)
```

Public methods and possible operations:
```python
# getters
def getComponents(self) -> list[str]: pass
def getNets(self) -> dict: pass
def getSideOfComponent(self, componentName:str) -> str: pass # returns side of component or '' 
def getComponentPinout(self, componentName:str) -> dict: pass # returns {componentPin: netName}
def getSelectedComponents(self) -> list[str]: # list of selected components
def getSelectedNetComponent(self) -> str: # component of selected NET
def getMostCommonPrefixInterface(self) -> str: pass 


def checkIfPrefixExists(self, prefix:str) -> bool: # for example prefix C exists for C101, C200, C32..

def setBoardData(self, boardData:board.Board, isMakeBackup:bool=True): pass #setter for board wrapper instance
##########################################

# interfaces to interact with the canvas
# move image from source to destination given as relative distance from origin 
def moveBoardInterface(self, targetSurface:pygame.Surface, relativeXY:list[int, int]) -> pygame.Surface: pass 

# scale up or down. Whole canvas is scaled so there is a hardcoded max size of canvas.
def scaleUpDownInterface(self, targetSurface:pygame.Surface, isScaleUp:bool, pointXY:list[int, int], side:str) -> pygame.Surface: pass

# generate other side of the board
def changeSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# rotate board by given angle
def rotateBoardInterface(self, targetSurface:pygame.Surface,  isClockwise:bool, side:str, angleDeg:float=None) -> pygame.Surface: pass

# pass a name to find a component and mark it with red arrow. Pass the name second time to unselect it
def findComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface: pass

# set component in the center of the canvas
def componentInScreenCenterInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface: pass

# clear all selected components (red arrows)
def clearFindComponentByNameInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# select net by name and mark pads with violet color
def selectNetByNameInterface(self, targetSurface:pygame.Surface, netName:str, side:str) -> pygame.Surface: pass

# pass a name to find a component and mark it with violet arrow. Pass the name second time to unselect it
def selectNetComponentByNameInterface(self, targetSurface:pygame.Surface, componentName:str, side:str) -> pygame.Surface: pass

# unselect selected net and net component
def unselectNetInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# show/hide net component arrow
def showHideMarkersForSelectedNetByNameInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# fulfill components with common prefix
def showCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, prefix:str, side:str) -> pygame.Surface: pass

# clear compoments with common prefix
def clearCommonTypeComponentsInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# mirror current side in Y Axis
def flipUnflipCurrentSideInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# normalize board using all components as a reference
def useComponentAreaInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# self explanatory
def resetToDefaultViewInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass
def showHideOutlinesInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass

# set canvas dimensions
def changeScreenDimensionsInterface(self, targetSurface:pygame.Surface, dimensions:tuple[int, int], side:str) -> pygame.Surface: pass

# generate frame and display it
def drawAndBlitInterface(self, targetSurface:pygame.Surface, side:str) -> pygame.Surface: pass
```

# Part 5: Basic shapes
**Classes and modules:**
```
geometryObjects.py -> Point, AbstractBaseShape, Line, Arc, Circle, Rectangle
```

## Point
Point stores carthesian coordinates and provide static methods for point operations:
```python
# getters and setters
def setX(self, x:float): pass
def setY(self, y:float): pass
def getX(self) -> float: pass
def getY(self) -> float: pass
def getXY(self) -> tuple[float, float]: pass
def getType(self) -> str: pass

# method that modify instance in place
def rotateInPlace(self, rotationPoint:'Point', angleDeg:float): pass    # rotates around given point by given angle
def scaleInPlace(self, coefficient:float): pass     #scale coordinates by given factor
def translateInPlace(self, vector:list[int|float, int|float]): pass # linear translation by given vector

# static methods for list of points:
## use this method in loop to find BottomLeft and TopRight points (points with minXY coords and maxXY coords)
def minXY_maxXYCoords(currentMinPoint:'Point', currentMaxPoint:'Point', checkedPoint:'Point') -> tuple['Point', 'Point']:
    return Point.minXYCoords(currentMinPoint, checkedPoint), Point.maxXYCoords(currentMaxPoint, checkedPoint)

@staticmethod
def minXYCoords(currentMinPoint:'Point', checkedPoint:'Point') -> 'Point': pass
@staticmethod
def maxXYCoords(currentMaxPoint:'Point', checkedPoint:'Point') -> 'Point':pass

# static method for Point: (same as above)
@staticmethod
def translate(point:'Point', vector:list[float]) -> 'Point': pass

@staticmethod
def scale(point:'Point', coefficient:float) -> 'Point': pass
```

## Line
This class descibes line as start and endpoint
methods:
```python
def getType(self) -> str:
def getPoints(self) -> tuple[Point, Point]:
def getPointsAsXYTuple(self) -> tuple['int|float', 'int|float', 'int|float', 'int|float']:
```

## Arc
This class describes arc. Supported representations are: 
- StartPoint, EndPoint, RotationPoint 
- CenterPoint, Radius, Angle

```python
def __init__(self, startPoint:Point, endPoint:Point, rotationPoint:Point):
def getType(self) -> str: pass
def calculateAngleRadRepresentation(self): pass

def getAsCenterRadiusAngles(self) -> tuple[Point, float, float, float]:
    return self.rotationPoint, self.radius, self.startAngle, self.endAngle

def getPoints(self) -> tuple[Point, Point, Point]:
    return self.startPoint, self.endPoint, self.rotationPoint

def scaleInPlace(self, factor: float | int): pass
def rotateInPlace(self, rotationPoint: Point, angleDeg: float): pass
```

## Circle
This class describes circle as centerPoint, Radius


```python
def __init__(self, centerPoint:Point, radius:float):
    
def setRadius(self, radius:float): pass
def getRadius(self) -> float: pass    
def getType(self) -> str: pass
def getPoints(self) -> list[Point]:
    ''' [centerPoint] ''' 
    return [self.centerPoint]

def getCenterRadius(self) -> tuple[Point, float]: pass
def scaleInPlace(self, factor: float | int): pass

def checkIfPointInside(self, point:Point) -> bool: pass
def calculateArea(self) -> tuple[Point, Point]: # returns bottomLeft and topRight points
```

## Rectangle
This class represents rectangle as bottomLeft and topRight Points

```python
def __init__(self, bottomLeftPoint:Point, topRightPoint:Point):
def getPoints(self) -> list[Point, Point, Point, Point]:
    ''' [bottomLeftPoint, bottomRightPoint, topRightPoint, topLeftPoint] '''
    return [self.bottomLeftPoint, self.bottomRightPoint, self.topRightPoint, self.topLeftPoint]

def checkIfPointInside(self, pointP:Point) -> bool: pass
def calculateArea(self) -> tuple[Point, Point]: pass
```