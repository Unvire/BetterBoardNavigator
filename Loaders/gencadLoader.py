import sys, os, copy 
sys.path.append(os.getcwd())
import geometryObjects
import board, component, pin

class GenCadLoader:
    def __init__(self):
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARD':[], 'PADS':[], 'SHAPES':[], 'COMPONENTS':[], 'SIGNALS':[], 'ROUTES':[], 'MECH':[]}
        self.handleShape = {'LINE':self._getLineFromLINE, 'ARC': self._getArcFromARC, 'CIRCLE':self._getCircleFromCIRCLE}
    
    def loadFile(self, filePath:str):
        self._setFilePath(filePath)
        fileLines = self._getFileLines()        
        self._getSectionsLinesBeginEnd(fileLines)

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
        bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
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
        i, iEnd = self.sectionsLineNumbers(['PADS'])
        padsDict = {}

        while i <= iEnd:
            if ' ' in fileLines[i] and 'PAD' in fileLines[i]:
                _, padName, *_  = fileLines[i].replace('\n', '').split(' ')                    
                bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
                topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
                
                while 'PAD' not in fileLines[i + 1]:
                    keyWord, *line  = fileLines[i].replace('\n', '').split(' ')
                    shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](line, bottomLeftPoint, topRightPoint)

                    i += 1
                padsDict[padName] = {}


                
    
    def _getLineFromLINE(self, fileLine:list[str], bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point) -> tuple[geometryObjects.Line, geometryObjects.Point, geometryObjects.Point]:
        xStart, yStart, xEnd, yEnd = [geometryObjects.floatOrNone(val) for val in fileLine]
        startPoint = geometryObjects.Point(xStart, yStart)
        endPoint = geometryObjects.Point(xEnd, yEnd)

        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], [startPoint, endPoint])
        
        lineInstance = geometryObjects.Line(startPoint, endPoint)
        return lineInstance, bottomLeftPoint, topRightPoint
    
    def _getArcFromARC(self, fileLine:list[str], bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point) -> tuple[geometryObjects.Arc, geometryObjects.Point, geometryObjects.Point]:
        xStart, yStart, xEnd, yEnd, xCenter, yCenter = [geometryObjects.floatOrNone(val) for val in fileLine]
        startPoint = geometryObjects.Point(xStart, yStart)
        endPoint = geometryObjects.Point(xEnd, yEnd)
        rotationPoint = geometryObjects.Point(xCenter, yCenter)

        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], [startPoint, endPoint, rotationPoint])

        arcInstance = geometryObjects.Arc(startPoint, endPoint, rotationPoint)
        return arcInstance, bottomLeftPoint, topRightPoint

    def _getCircleFromCIRCLE(self, fileLine:list[str], bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point) -> tuple[geometryObjects.Circle, geometryObjects.Point, geometryObjects.Point]:
        xCenter, yCenter, radius = [geometryObjects.floatOrNone(val) for val in fileLine]
        centerPoint = geometryObjects.Point(xCenter, yCenter)

        checkedPoints = [geometryObjects.Point.translate(centerPoint, [-radius, -radius]), geometryObjects.Point.translate(centerPoint, [radius, radius])]
        bottomLeftPoint, topRightPoint = self._updatebottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)
         
        circleInstance = geometryObjects.Circle(centerPoint, radius)
        return circleInstance, bottomLeftPoint, topRightPoint
    
    def _splitButNotBetweenCharacter(self, line:str, splitCharacter:str=' ', ignoreCharacter:str='"') -> list[str]:
        initialSplit = line.split(splitCharacter)
        result = []

        while initialSplit:
            current = initialSplit.pop(0)
            if current[0] == ignoreCharacter:
                concatenated = current
                while current[-1] != ignoreCharacter:
                    current = initialSplit.pop(0)
                    concatenated += f'_{current}'
                current = concatenated
            result.append(current)
        return result

    def _updatebottomLeftTopRightPoints(self, bottomLeftTopRightPoints:tuple[geometryObjects.Point, geometryObjects.Point],  checkedPoints:list[geometryObjects.Point]) -> tuple[geometryObjects.Point, geometryObjects.Point]:
        bottomLeftPoint, topRightPoint = bottomLeftTopRightPoints
        for point in checkedPoints:
            bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint
    
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])

if __name__ == '__main__':
    loader = GenCadLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\wallbox main rev5.GCD')