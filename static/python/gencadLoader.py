import copy
import geometryObjects as gobj
import component as comp
import board, pin
from abstractShape import Shape

class GenCadLoader:
    def __init__(self):        
        self.filePath = None
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARD':[], 'PADS':[], 'SHAPES':[], 'COMPONENTS':[], 'SIGNALS':[], 'ROUTES':[], 'MECH':[], 'PADSTACKS':[], 'ARTWORKS':[]}
        self.handleShape = {'LINE':gobj.getLineAndAreaFromNumArray, 'ARC':gobj.getArcAndAreaFromValArray, 
                            'CIRCLE':gobj.getCircleAndAreaFromValArray, 'RECTANGLE':gobj.getRectangleAndAreaFromValArray}
    
    def loadFile(self, filePath:str) -> list[str]:
        self._setFilePath(filePath)
        fileLines = self._getFileLines()
        return fileLines
    
    def processFileLines(self, fileLines:list[str]) -> board.Board:
        self._getSectionsLinesBeginEnd(fileLines)
        self._getBoardDimensions(fileLines, self.boardData)
        padsDict = self._getPadsFromPADS(fileLines)
        artworksDict = self._getArtWorksFromARTWORKS(fileLines)
        padstackDict = self._getPadstacksFromPADSTACKS(fileLines, padsDict)
        shapeToComponentsDict = self._getComponentsFromCOMPONENTS(fileLines, self.boardData)
        shapesDict = self._getAreaPinsfromSHAPES_ARTWORKS(fileLines, artworksDict)
        self._addShapePadDataToComponent(self.boardData, shapeToComponentsDict, shapesDict, padstackDict)
        self._getNetsFromSIGNALS(fileLines, self.boardData)
        return self.boardData
    
    def _setFilePath(self, filePath:str):
        self.filePath = filePath
    
    def _getFileLines(self) -> list[str]:
        with open(self.filePath, 'r') as file:
            fileLines = file.readlines()
        return [line.replace('\n', '') for line in fileLines]
    
    def _getSectionsLinesBeginEnd(self, fileLines:list[str]):
        for i, line in enumerate(fileLines):
            sectionName = line[1:]
            if sectionName in self.sectionsLineNumbers or (sectionName:=sectionName[3:]) in self.sectionsLineNumbers:
                self.sectionsLineNumbers[sectionName].append(i)
    
    def _getBoardDimensions(self, fileLines:list[str], boardInstance:board.Board):
        boardOutlineRange = self._calculateRange('BOARD')
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        shapes = []

        for i in boardOutlineRange:
            if ' ' in fileLines[i]:
                keyWord, *line  = self._splitButNotBetweenCharacterAndUpperCase(fileLines[i])
                if keyWord == 'ARTWORK':
                    break
                if keyWord not in self.handleShape:
                    continue
                shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](line, bottomLeftPoint, topRightPoint)
                shapes.append(shape)
        
        boardInstance.setOutlines(shapes)
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
    
    def _getPadsFromPADS(self, fileLines:list[str]) -> dict:
        i, iEnd = self.sectionsLineNumbers['PADS']
        padsDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'PAD' in fileLines[i]:
                line = fileLines[i]
                _, padName, *_  = self._splitButNotBetweenCharacterAndUpperCase(line)                  
                bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
                
                while 'PAD' not in fileLines[i + 1]:
                    i += 1
                    keyWord, *line  =  self._splitButNotBetweenCharacterAndUpperCase(fileLines[i])
                    _, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](line, bottomLeftPoint, topRightPoint)
                
                keyWord = 'RECT' if keyWord != 'CIRCLE' else keyWord
                newPad = self._createPin(padName, keyWord, bottomLeftPoint, topRightPoint)                    
                padsDict[padName] = newPad
            i += 1
        return padsDict
    
    def _getArtWorksFromARTWORKS(self, fileLines:list[str]) -> dict:
        i, iEnd = self.sectionsLineNumbers['ARTWORKS']
        artworksDict = {}

        while i <= iEnd:
            artWorkParameters = {}
            if ' ' in fileLines[i] and 'ARTWORK' in fileLines[i]:
                line = fileLines[i]
                _, artworkName, *_  = self._splitButNotBetweenCharacterAndUpperCase(line)

                isEndOfShapeSection = False                
                while not isEndOfShapeSection:
                    keyWord, *parameters = self._splitButNotBetweenCharacterAndUpperCase(fileLines[i])
                    if not keyWord in artWorkParameters:
                        artWorkParameters[keyWord] = []
                    artWorkParameters[keyWord].append(parameters)
                    i += 1
                    isEndOfShapeSection = 'ARTWORK' == fileLines[i][:7] or i >= iEnd
                                   
                artworksDict[artworkName] = artWorkParameters
                continue
            i += 1
        return artworksDict
    
    def _getPadstacksFromPADSTACKS(self, fileLines:list[str], padsDict:dict) -> dict:
        i, iEnd = self.sectionsLineNumbers['PADSTACKS']
        padstackDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'PADSTACK' in fileLines[i]:
                padstackLine = fileLines[i]
                _, padstackName, *_ = self._splitButNotBetweenCharacterAndUpperCase(padstackLine)
                
                j = 1
                padName = None
                while padName not in padsDict:
                    padLine = fileLines[i + j]
                    _, padName, *_ = self._splitButNotBetweenCharacterAndUpperCase(padLine)
                    j += 1 
            
                padstackDict[padstackName] = padsDict[padName]
            i += 1
        padstackDict.update(padsDict)
        return padstackDict
    
    def _getComponentsFromCOMPONENTS(self, fileLines:list[str], boardInstance:board.Board) -> dict:
        i, iEnd = self.sectionsLineNumbers['COMPONENTS']
        shapeDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'COMPONENT' in fileLines[i][:9]:
                componentParameters = {}
                isEndOfComponentSection = False
                while not isEndOfComponentSection:
                    keyWord, *parameters = self._splitButNotBetweenCharacterAndUpperCase(fileLines[i])
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
    
    def _getAreaPinsfromSHAPES_ARTWORKS(self, fileLines:list[str], artworksDict:dict) -> dict:
        i, iEnd = self.sectionsLineNumbers['SHAPES']

        shapesDict = {}
        while i <= iEnd:
            if ' ' in fileLines[i] and 'SHAPE' in fileLines[i][:5]:
                shapeParameters = {}                
                isEndOfShapeSection = False                
                while not isEndOfShapeSection:
                    keyWord, *parameters = self._splitButNotBetweenCharacterAndUpperCase(fileLines[i])
                    if not keyWord in shapeParameters:
                        shapeParameters[keyWord] = []
                    shapeParameters[keyWord].append(parameters)
                    i += 1
                    isEndOfShapeSection = 'SHAPE' == fileLines[i][:5] or i >= iEnd
                    
                shapeName = shapeParameters['SHAPE'][0][0]
                self._calculateShapeAreaInPlace(shapeParameters)
                if abs(shapeParameters['AREA'][0].getX()) == float('Inf'):
                    shapeParameters.update({'CIRCLE':[], 'RECTANGLE':[], 'LINE':[], 'ARC':[]})
                    for artwork, *_ in shapeParameters['ARTWORK']:
                        self._mergeShapesSectionToDictInPlace(shapeParameters, artworksDict[artwork])
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
                componentArea = copy.deepcopy(shapesDict[shapeName]['AREA'])
                componentAreaType = shapesDict[shapeName]['AREA_NAME']
                
                for pinNumber, padstackName, pinX, pinY, _, pinAngle, _ in pins:
                    if not padstackName in padstackDict:
                        padstackName = list(padstackDict.keys())[0]
                    pinInstance = copy.deepcopy(padstackDict[padstackName])
                    self._addPinAreaIfUnknown(pinInstance, componentArea)
                    self._caclulatePinToBasePosition(pinInstance, float(pinAngle), [float(pinX), float(pinY)])
                    self._calculatePinToComponentPosition(pinInstance, pinNumber, componentInstance)

                self._addAreaAndMountingData(componentInstance, componentAreaType, componentArea, packageType)
                componentInstance.rotateInPlaceAroundCoords(componentInstance.getAngle(), isRotatePins=True)
    
    def _getNetsFromSIGNALS(self, fileLines:list[str], boardInstance:board.Board):
        i, iEnd = self.sectionsLineNumbers['SIGNALS']
        netsDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'SIGNAL' in fileLines[i][:6]:
                line = fileLines[i]
                _, netName = self._splitButNotBetweenCharacterAndUpperCase(line)
                netsDict[netName] = {}
                isEndOfSignalsSection = False
                i += 1
                while not isEndOfSignalsSection:
                    line = fileLines[i]
                    keyWord, *parameters = self._splitButNotBetweenCharacterAndUpperCase(line)
                    if keyWord == 'NODE':
                        componentName, pinName = parameters
                        componentInstance, pinInstance = self._getComponentAndPinByNames(boardInstance, componentName, pinName)
                        pinInstance.setNet(netName)

                        if not componentName in netsDict[netName]:
                            netsDict[netName][componentName] = {'componentInstance':componentInstance, 'pins':[]}
                        netsDict[netName][componentName]['pins'].append(pinName)
                    
                    i += 1
                    isEndOfSignalsSection = 'SIGNAL' == fileLines[i][:6] or i >= iEnd
                continue
            i += 1
        boardInstance.setNets(netsDict)

    def _createPin(self, name:str, shape:str, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> pin.Pin:
        newPin = pin.Pin(name)
        newPin.setShape(shape)
        newPin.setArea(bottomLeftPoint, topRightPoint)
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
    
    def _mergeShapesSectionToDictInPlace(self,  targetDict:dict, sourceDict:dict):
        targetDict['CIRCLE'] += sourceDict.get('CIRCLE', [])
        targetDict['ARC'] +=  sourceDict.get('ARC', [])
        targetDict['RECTANGLE'] += sourceDict.get('RECTANGLE', [])
        targetDict['LINE'] += sourceDict.get('LINE', [])

    def _getComponentAndPinByNames(self, boardInstance:board.Board, componentName:str, pinName:str) -> tuple[comp.Component, pin.Pin]:
        componentInstance = boardInstance.getElementByName('components', componentName)
        pinInstance = componentInstance.getPinByName(pinName)
        return componentInstance, pinInstance
    
    def _addAreaAndMountingData(self, componentInstance:comp.Component, componentAreaType:str, componentArea:list[gobj.Point, gobj.Point], componentMountingType:str):
        componentMountingType = 'TH' if 'TH' in componentMountingType[:2] else 'SMT'
        componentAreaX, componentAreaY = componentArea
        componentInstance.setShape(componentAreaType)
        componentInstance.setMountingType(componentMountingType)

        moveVector = componentInstance.getCoordsAsTranslationVector()
        componentAreaX.translateInPlace(moveVector)
        componentAreaY.translateInPlace(moveVector)
        componentInstance.setArea(componentAreaX, componentAreaY)
        componentInstance.caluclateShapeData()
    
    def _addPinAreaIfUnknown(self, pinInstance:pin.Pin, componentArea:tuple[gobj.Point, gobj.Point]):
        bottomLeftPoint, topRightPoint = pinInstance.getArea()
        areaValues = Shape.getAreaAsXYXY((bottomLeftPoint, topRightPoint))
        if float('Inf') in areaValues or float('-Inf') in areaValues:            
            PIN_AREA_AS_A_FRACTION_OF_COMPONENT_AREA = 0.07
            componentBottomLeftPoint, componentTopRightPoint = componentArea

            newBottomLeftPoint = gobj.Point.scale(componentBottomLeftPoint, PIN_AREA_AS_A_FRACTION_OF_COMPONENT_AREA)
            newTopRightPoint = gobj.Point.scale(componentTopRightPoint, PIN_AREA_AS_A_FRACTION_OF_COMPONENT_AREA)
            pinInstance.setArea(newBottomLeftPoint, newTopRightPoint)
            pinInstance.setShape('RECT')
            pinInstance.calculateCenterDimensionsFromArea()
    
    def _caclulatePinToBasePosition(self, pinInstance:pin.Pin, angle:float|int, translationVector:list[float|int, float|int]):
        pinInstance.caluclateShapeData()
        if angle % 90 == 0:
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
            _, bottomLeftPoint, topRightPoint = self.handleShape['CIRCLE'](circle[:3], bottomLeftPoint, topRightPoint) # extract only first circle
        else:
            shape = 'RECT'
            rectangles = self._unnestRectanglesList(shapeParameters.get('RECTANGLE', []))
            lines = self._unnestCoordsList(shapeParameters.get('LINE', []))
            arcs = self._unnestCoordsList(shapeParameters.get('ARC', []))
            bottomLeftPoint, topRightPoint = self._coordsListToBottomLeftTopRightPoint(rectangles + arcs + lines)
        
        shapeParameters['AREA_NAME'] = shape
        shapeParameters['AREA'] = [bottomLeftPoint, topRightPoint]
    
    def _coordsListToBottomLeftTopRightPoint(self, coordsList:list[str|float]) -> tuple[str, gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

        while coordsList:
            x = gobj.floatOrNone(coordsList.pop(0))
            y = gobj.floatOrNone(coordsList.pop(0))
            point = gobj.Point(x, y)
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint

    def _splitButNotBetweenCharacterAndUpperCase(self, line:str, splitCharacter:str=' ', ignoreCharacter:str='"') -> list[str]:
        initialSplit = [val for val in line.split(splitCharacter) if val]
        result = []

        while initialSplit:
            current = initialSplit.pop(0)
            if current[0] == ignoreCharacter:
                concatenated = current
                while current[-1] != ignoreCharacter:
                    current = initialSplit.pop(0)
                    concatenated += f'{splitCharacter}{current}'
                current = concatenated.replace(ignoreCharacter, '')
            result.append(current.upper())
        return result
    
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    
    def _unnestRectanglesList(self, rectanglesNestedList: list[list[float]]) -> list:
        result = []
        for rect in rectanglesNestedList:
                bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
                _, bottomLeftPoint, topRightPoint = self.handleShape['RECTANGLE'](rect, bottomLeftPoint, topRightPoint)
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
    fileLines = loader.loadFile(r'C:\Users\kbalcerzak\Documents\schematy z Q\Schematic\CITYVAN-STOPTAIL-LH.gcd')
    loader.processFileLines(fileLines)