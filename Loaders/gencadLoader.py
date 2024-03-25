import sys, os, copy 
sys.path.append(os.getcwd())
import geometryObjects
import board, component, pin

class GenCadLoader:
    def __init__(self):
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARD':[], 'PADS':[], 'SHAPES':[], 'COMPONENTS':[], 'SIGNALS':[], 'ROUTES':[], 'MECH':[]}
    
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
    
    def _getSectionsLinesBeginEnd(self, fileLines:str):
        for i, line in enumerate(fileLines):
            sectionName = line[1:-1]
            if sectionName in self.sectionsLineNumbers or (sectionName:=sectionName[3:]) in self.sectionsLineNumbers:
                self.sectionsLineNumbers[sectionName].append(i)
    
    def _getBoardDimensions(self, fileLines:str, boardInstance:board.Board):
        boardOutlineRange = self._calculateRange('BOARD')
        bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
        handleShape = {'LINE':self._getLineFromLINE, 'ARC': self._getArcFromARC}
        shapes = []

        for i in boardOutlineRange:
            if len(fileLines[i]) > 2:
                keyWord, *line  = fileLines[i].replace('\n', '').split(' ')
                if keyWord == 'ARTWORK':
                    break
                shape, bottomLeftPoint, topRightPoint = handleShape[keyWord](line, bottomLeftPoint, topRightPoint)
                shapes.append(shape)
        
        boardInstance.setOutlines(shapes)
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
                
    
    def _getLineFromLINE(self, fileLine:list[str], bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point) -> tuple[geometryObjects.Line, geometryObjects.Point, geometryObjects.Point]:
        xStart, yStart, xEnd, yEnd = [geometryObjects.floatOrNone(val) for val in fileLine]
        startPoint = geometryObjects.Point(xStart, yStart)
        endPoint = geometryObjects.Point(xEnd, yEnd)

        for point in [startPoint, endPoint]:
            bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        
        lineInstance = geometryObjects.Line(startPoint, endPoint)
        return lineInstance, bottomLeftPoint, topRightPoint
    
    def _getArcFromARC(self, fileLine:str, bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point) -> tuple[geometryObjects.Arc, geometryObjects.Point, geometryObjects.Point]:
        xStart, yStart, xEnd, yEnd, xCenter, yCenter = [geometryObjects.floatOrNone(val) for val in fileLine.split(' ')]
        startPoint = geometryObjects.Point(xStart, yStart)
        endPoint = geometryObjects.Point(xEnd, yEnd)
        rotationPoint = geometryObjects.Point(xCenter, yCenter)

        for point in [startPoint, endPoint, rotationPoint]:
            bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)

        arcInstance = geometryObjects.Arc(startPoint, endPoint, rotationPoint)
        return arcInstance, bottomLeftPoint, topRightPoint
                
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])

if __name__ == '__main__':
    loader = GenCadLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\wallbox main rev5.GCD')