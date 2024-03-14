import re
import geometryObjects
import component

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
        bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
        for i in boardOutlineRange:
            if ',' in fileLines[i]:
                _, xStart, yStart, xEnd, yEnd = fileLines[i].split(',')
                startPoint = geometryObjects.Point(float(xStart), float(yStart))              
                endPoint = geometryObjects.Point(float(xEnd), float(yEnd))

                self.boardData['SHAPE'].append(geometryObjects.Line(startPoint, endPoint))
                bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, startPoint)       
                bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, endPoint)
        self.boardData['AREA'] = [bottomLeftPoint, topRightPoint]
    
    def _getComponenentsFromPARTLIST(self, fileLines:list[str]):
        partlistRange = self._calculateRange('PARTLIST')
        for i in partlistRange:
            if ',' in fileLines[i]:
                _, name, packageName, x, y, side, angle = fileLines[i].split(',')
                newComponent = component.Component(name)
                

    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    


if __name__ == '__main__':
    filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)