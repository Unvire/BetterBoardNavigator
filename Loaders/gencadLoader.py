import sys, os, copy 
sys.path.append(os.getcwd())
import geometryObjects as gobj
import component as comp
import board, pin

class GenCadLoader:
    def __init__(self):
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARD':[], 'PADS':[], 'SHAPES':[], 'COMPONENTS':[], 'SIGNALS':[], 'ROUTES':[], 'MECH':[], 'PADSTACKS':[]}
        self.handleShape = {'LINE':self._getLineFromLINE, 'ARC': self._getArcFromARC, 'CIRCLE':self._getCircleFromCIRCLE, 'RECTANGLE':self._getRectFromRECTANGLE}
    
    def loadFile(self, filePath:str):
        self._setFilePath(filePath)
        fileLines = self._getFileLines()        
        self._getSectionsLinesBeginEnd(fileLines)
        padsDict = self._getPadsFromPADS(fileLines)
        padstackDict = self._getPadstacksFromPADSTACKS(fileLines, padsDict)
        shapeToComponentsDict = self._getComponentsFromCOMPONENTS(fileLines, self.boardData)
        shapesDict = self._getAreaPinsfromSHAPES(fileLines)
        self._addShapePadDataToComponent(self.boardData, shapeToComponentsDict, shapesDict, padstackDict)

        return self.boardData
    
    def _setFilePath(self, filePath:str):
        self.filePath = filePath
    
    def _getFileLines(self) -> list[str]:
        with open(self.filePath, 'r') as file:
            fileLines = file.readlines()
        return fileLines
    
    def _getSectionsLinesBeginEnd(self, fileLines:list[str]):
        for i, line in enumerate(fileLines):
            sectionName = line[1:-1]
            if sectionName in self.sectionsLineNumbers or (sectionName:=sectionName[3:]) in self.sectionsLineNumbers:
                self.sectionsLineNumbers[sectionName].append(i)
    
    def _getBoardDimensions(self, fileLines:list[str], boardInstance:board.Board):
        boardOutlineRange = self._calculateRange('BOARD')
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        shapes = []

        for i in boardOutlineRange:
            if ' ' in fileLines[i]:
                keyWord, *line  = fileLines[i].replace('\n', '').split(' ')
                if keyWord == 'ARTWORK':
                    break
                shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](line, bottomLeftPoint, topRightPoint)
                shapes.append(shape)
        
        boardInstance.setOutlines(shapes)
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
    
    def _getPadsFromPADS(self, fileLines:list[str]) -> dict:
        i, iEnd = self.sectionsLineNumbers['PADS']
        padsDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'PAD' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, padName, *_  = self._splitButNotBetweenCharacter(line)                  
                bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
                
                while 'PAD' not in fileLines[i + 1]:
                    i += 1
                    keyWord, *line  = fileLines[i].replace('\n', '').split(' ')
                    _, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](line, bottomLeftPoint, topRightPoint)
                
                keyWord = 'RECT' if keyWord != 'CIRCLE' else keyWord
                newPad = self._createPin(padName, keyWord, bottomLeftPoint, topRightPoint)                    
                padsDict[padName] = newPad
            i += 1
        return padsDict
    
    def _getPadstacksFromPADSTACKS(self, fileLines:list[str], padsDict:dict) -> dict:
        i, iEnd = self.sectionsLineNumbers['PADSTACKS']
        padstackDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'PADSTACK' in fileLines[i]:
                padstackLine = fileLines[i].replace('\n', '')
                _, padstackName, *_ = self._splitButNotBetweenCharacter(padstackLine)
                
                padLine = fileLines[i + 1].replace('\n', '')
                _, padName, *_ = self._splitButNotBetweenCharacter(padLine)

                padstackDict[padstackName] = padsDict[padName]
            i += 1
        return padstackDict
    
    def _getComponentsFromCOMPONENTS(self, fileLines:list[str], boardInstance:board.Board) -> dict:
        i, iEnd = self.sectionsLineNumbers['COMPONENTS']
        shapeDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'COMPONENT' in fileLines[i][:9]:
                componentParameters = {}
                isEndOfComponentSection = False
                while not isEndOfComponentSection:
                    line = fileLines[i].replace('\n', '')
                    keyWord, *parameters = self._splitButNotBetweenCharacter(line)
                    componentParameters[keyWord] = parameters
                    i += 1
                    isEndOfComponentSection = 'COMPONENT' == fileLines[i][:9] or i >= iEnd
                newComponent = self._createComponent(componentParameters)
                componentName = componentParameters['COMPONENT'][0] 
                boardInstance.addComponent(componentName, newComponent)

                shapeName = componentParameters['SHAPE'][0]
                if not shapeName in shapeDict:
                    shapeDict[shapeName] = []
                shapeDict[shapeName].append(componentName)
                continue
            i += 1
        return shapeDict
    
    def _getAreaPinsfromSHAPES(self, fileLines:list[str]) -> dict:
        i, iEnd = self.sectionsLineNumbers['SHAPES']

        shapesDict = {}
        while i <= iEnd:
            if ' ' in fileLines[i] and 'SHAPE' in fileLines[i][:5]:
                shapeParameters = {}                
                isEndOfShapeSection = False                
                while not isEndOfShapeSection:
                    line = fileLines[i].replace('\n', '')
                    keyWord, *parameters = self._splitButNotBetweenCharacter(line)
                    if not keyWord in shapeParameters:
                        shapeParameters[keyWord] = []
                    shapeParameters[keyWord].append(parameters)
                    i += 1
                    isEndOfShapeSection = 'SHAPE' == fileLines[i][:5] or i >= iEnd
                shapeName = shapeParameters['SHAPE'][0][0]
                self._calculateShapeAreaInPlace(shapeParameters)
                shapesDict[shapeName] = shapeParameters
                continue
            i += 1
        return shapesDict
    
    def _addShapePadDataToComponent(self, boardInstance:board.Board, shapesToComponents:dict, shapesDict:dict, padstackDict:dict):
        components = boardInstance.getComponents()
        for shapeName, componentsList in shapesToComponents.items():
            for componentName in componentsList:
                componentInstance = components[componentName]
                pins = shapesDict[shapeName]['PIN']
                packageType = shapesDict[shapeName]['INSERT'][0][0]
                componentArea = shapesDict[shapeName]['AREA']
                componentAreaType = shapesDict[shapeName]['AREA_NAME']
                
                for pinNumber, padstackName, pinX, pinY, _, pinAngle, _ in pins:
                    pinInstance = copy.deepcopy(padstackDict[padstackName])
                    self._caclulatePinToBasePosition(pinInstance, float(pinAngle), [float(pinX), float(pinY)])
                    self._calculatePinToComponentPosition(pinInstance, pinNumber, componentInstance)
                
                self._addAreaAndMountingData(componentInstance, componentAreaType, componentArea, packageType)
                componentInstance.rotateInPlaceAroundCoords(componentInstance.getAngle())

    def _createPin(self, name:str, shape:str, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> pin.Pin:
        newPin = pin.Pin(name)
        newPin.setShape(shape)
        newPin.setPinArea(bottomLeftPoint, topRightPoint)
        newPin.calculateCenterDimensionsFromArea()
        return newPin

    def _createComponent(self, componentParameters:dict) -> comp.Component:
        ## [0], because every value is nested in a list
        name = componentParameters['COMPONENT'][0]
        x, y = [gobj.floatOrNone(val) for val in componentParameters['PLACE']]
        side = componentParameters['LAYER'][0][0]
        angle = gobj.floatOrNone(componentParameters['ROTATION'][0])

        newComponent = comp.Component(name)
        newComponent.setCoords(gobj.Point(x, y))
        newComponent.setSide(side)
        newComponent.setAngle(angle)
        return newComponent
    
    def _addAreaAndMountingData(self, componentInstance:comp.Component, componentAreaType:str, componentArea:list[gobj.Point, gobj.Point], componentMountingType:str):
        componentAreaX, componentAreaY = componentArea
        componentInstance.setComponentAreaType(componentAreaType)
        componentInstance.setMountingType(componentMountingType)

        moveVector = componentInstance.getCoordsAsTranslationVector()
        componentAreaX.translateInPlace(moveVector)
        componentAreaY.translateInPlace(moveVector)
        componentInstance.setComponentArea(componentAreaX, componentAreaY)
    
    def _caclulatePinToBasePosition(self, pinInstance:pin.Pin, angle:float|int, translationVector:list[float|int, float|int]):
        pinInstance.rotateInPlace(pinInstance.getCoords(), angle)
        pinInstance.translateInPlace(translationVector)
    
    def _calculatePinToComponentPosition(self, pinInstance:pin.Pin, pinName:str, componentInstance:comp.Component):
        moveVector = componentInstance.getCoordsAsTranslationVector()
        pinInstance.translateInPlace(moveVector)
        componentInstance.addPin(pinName, pinInstance)
    
    def _calculateShapeAreaInPlace(self, shapeParameters:dict) -> tuple[str, gobj.Point, gobj.Point]:        
        circle = self._unnestCoordsList(shapeParameters.get('CIRCLE', []))

        if circle:
            shape = 'CIRCLE'
            bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
            _, bottomLeftPoint, topRightPoint = self._getCircleFromCIRCLE(circle[:3], bottomLeftPoint, topRightPoint) # extract only first circle
        else:
            shape = 'RECT'
            rectangles = self._unnestRectanglesList(shapeParameters.get('RECTANGLE', []))
            lines = self._unnestCoordsList(shapeParameters.get('LINE', []))
            arcs = self._unnestCoordsList(shapeParameters.get('ARC', []))
            bottomLeftPoint, topRightPoint = self._coordsListToBottomLeftTopRightPoint(rectangles + arcs + lines)
        
        shapeParameters['AREA_NAME'] = shape
        shapeParameters['AREA'] = [bottomLeftPoint, topRightPoint]
    
    def _getLineFromLINE(self, fileLine:list[str], bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Line, gobj.Point, gobj.Point]:
        xStart, yStart, xEnd, yEnd = [gobj.floatOrNone(val) for val in fileLine]
        startPoint = gobj.Point(xStart, yStart)
        endPoint = gobj.Point(xEnd, yEnd)

        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], [startPoint, endPoint])
        
        lineInstance = gobj.Line(startPoint, endPoint)
        return lineInstance, bottomLeftPoint, topRightPoint
    
    def _getArcFromARC(self, fileLine:list[str], bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Arc, gobj.Point, gobj.Point]:
        xStart, yStart, xEnd, yEnd, xCenter, yCenter = [gobj.floatOrNone(val) for val in fileLine]
        startPoint = gobj.Point(xStart, yStart)
        endPoint = gobj.Point(xEnd, yEnd)
        rotationPoint = gobj.Point(xCenter, yCenter)

        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], [startPoint, endPoint, rotationPoint])

        arcInstance = gobj.Arc(startPoint, endPoint, rotationPoint)
        return arcInstance, bottomLeftPoint, topRightPoint

    def _getCircleFromCIRCLE(self, fileLine:list[str], bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Circle, gobj.Point, gobj.Point]:
        xCenter, yCenter, radius = [gobj.floatOrNone(val) for val in fileLine]
        centerPoint = gobj.Point(xCenter, yCenter)

        checkedPoints = [gobj.Point.translate(centerPoint, [-radius, -radius]), gobj.Point.translate(centerPoint, [radius, radius])]
        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)
         
        circleInstance = gobj.Circle(centerPoint, radius)
        return circleInstance, bottomLeftPoint, topRightPoint

    def _getRectFromRECTANGLE(self, fileLine:list[str], bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Rectangle, gobj.Point, gobj.Point]:
        x0, y0, width, height = [gobj.floatOrNone(val) for val in fileLine]
        point0 = gobj.Point(x0, y0)
        point1 = gobj.Point(x0 + width, y0 + height)

        checkedPoints = [point0, point1]
        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)
         
        rectangleInstance = gobj.Rectangle(point0, point1)
        return rectangleInstance, bottomLeftPoint, topRightPoint
    
    def _coordsListToBottomLeftTopRightPoint(self, coordsList:list[str|float]) -> tuple[str, gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

        while coordsList:
            x = gobj.floatOrNone(coordsList.pop(0))
            y = gobj.floatOrNone(coordsList.pop(0))
            point = gobj.Point(x, y)
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint

    def _splitButNotBetweenCharacter(self, line:str, splitCharacter:str=' ', ignoreCharacter:str='"') -> list[str]:
        initialSplit = line.split(splitCharacter)
        result = []

        while initialSplit:
            current = initialSplit.pop(0)
            if current[0] == ignoreCharacter:
                concatenated = current
                while current[-1] != ignoreCharacter:
                    current = initialSplit.pop(0)
                    concatenated += f'{splitCharacter}{current}'
                current = concatenated.replace(ignoreCharacter, '')
            result.append(current)
        return result

    def _updatebottomLeftTopRightPoints(self, bottomLeftTopRightPoints:tuple[gobj.Point, gobj.Point],  checkedPoints:list[gobj.Point]) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = bottomLeftTopRightPoints
        for point in checkedPoints:
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint
    
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    
    def _unnestRectanglesList(self, rectanglesNestedList: list[list[float]]) -> list:
        result = []
        for rect in rectanglesNestedList:
                bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
                _, bottomLeftPoint, topRightPoint = self._getRectFromRECTANGLE(rect, bottomLeftPoint, topRightPoint)
                newRectLine = [bottomLeftPoint.getX(), bottomLeftPoint.getY(), topRightPoint.getX(), topRightPoint.getY()]
                result += newRectLine
        return result

    def _unnestCoordsList(self, nestedCoordsList:list[list[str|float]]) -> list[str|float]:
        result = []
        for array in nestedCoordsList:
            result += array
        return result
    
    
if __name__ == '__main__':
    loader = GenCadLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\wallbox main rev5.GCD')