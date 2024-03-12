import re
import geometryObjects

class CamCadLoader:
    def __init__(self):
        self.boardData = {'SHAPE':[]}
        self.sectionsLineNumbers = {'BOARDINFO':[], 'PARTLIST':[], 'PNDATA':[], 'NETLIST':[], 'PAD':[], 'PACKAGES':[], 'BOARDOUTLINE':[]}

    def loadFile(self, filePath):
        self.setFilePath(filePath)
        fileLines = self._getFileLines()
        self._getSectionsLinesBeginEnd(fileLines)
        self._getBoardDimensions(fileLines)

        return self.boardData

    def setFilePath(self, filePath:str):
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
    
    def _getBoardDimensions(self, fileLines:list[str]):
        boardOutlineRange = self._calculateRange('BOARDOUTLINE')
        minXminYPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        maxXmaxYPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
        for i in boardOutlineRange:
            if ',' in fileLines[i]:
                _, xStart, yStart, xEnd, yEnd = fileLines[i].split(',')
                startPoint = geometryObjects.Point(float(xStart), float(yStart))              
                endPoint = geometryObjects.Point(float(xEnd), float(yEnd))

                self.boardData['SHAPE'].append(geometryObjects.Line(startPoint, endPoint))
                minXminYPoint, maxXmaxYPoint = self._minMaxXYCoords(minXminYPoint, maxXmaxYPoint, startPoint)       
                minXminYPoint, maxXmaxYPoint = self._minMaxXYCoords(minXminYPoint, maxXmaxYPoint, endPoint)
        self.boardData['AREA'] = [minXminYPoint, maxXmaxYPoint]

    def _minMaxXYCoords(self, currentMinPoint:geometryObjects.Point, currentMaxPoint:geometryObjects.Point, checkedPoint:geometryObjects.Point) -> (geometryObjects.Point, geometryObjects.Point):
        currentMinPoint = self._minXYCoords(currentMinPoint, checkedPoint)
        currentMaxPoint = self._maxXYCoords(currentMaxPoint, checkedPoint)
        return currentMinPoint, currentMaxPoint


    def _minXYCoords(self, currentMinPoint:geometryObjects.Point, checkedPoint:geometryObjects.Point) -> geometryObjects.Point:
        currentX, currentY = currentMinPoint.x, currentMinPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        minX = min(currentX, checkedX)        
        minY = min(currentY, checkedY)
        currentMinPoint.setX(minX)
        currentMinPoint.setX(minY)
        return currentMinPoint
    
    def _maxXYCoords(self, currentMaxPoint:geometryObjects.Point, checkedPoint:geometryObjects.Point) -> geometryObjects.Point:
        currentX, currentY = currentMaxPoint.x, currentMaxPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        minX = max(currentX, checkedX)        
        minY = max(currentY, checkedY)
        currentMaxPoint.setX(minX)
        currentMaxPoint.setX(minY)
        return currentMaxPoint
    
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    


if __name__ == '__main__':
    filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)