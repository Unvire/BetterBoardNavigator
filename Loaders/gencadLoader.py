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
        self._getComponentsFromCOMPONENTS(fileLines, self.boardData)

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
    
    def _getComponentsFromCOMPONENTS(self, fileLines:list[str], boardInstance:board.Board):
        i, iEnd = self.sectionsLineNumbers['COMPONENTS']

        while i <= iEnd:
            if ' ' in fileLines[i] and 'COMPONENT' in fileLines[i]:
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
                continue
            i += 1

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
        shapeName = componentParameters['SHAPE'][0]

        newComponent = comp.Component(name)
        newComponent.setCoords(gobj.Point(x, y))
        newComponent.setSide(side)
        newComponent.setAngle(angle)
        newComponent.setPartNumber(shapeName)
        return newComponent
    
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
        x0, y0, x1, y1 = [gobj.floatOrNone(val) for val in fileLine]
        point0 = gobj.Point(x0, y0)
        point1 = gobj.Point(x1, y1)

        checkedPoints = [point0, point1]
        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)
         
        rectangleInstance = gobj.Rectangle(point0, point1)
        return rectangleInstance, bottomLeftPoint, topRightPoint
    
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
    
    
if __name__ == '__main__':
    loader = GenCadLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\wallbox main rev5.GCD')