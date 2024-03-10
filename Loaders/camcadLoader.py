import re
import point

class CamCadLoader:
    def __init__(self):
        self.boardData = {}
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
        regexPattern = '(-?\d+\.\d+)(\s,-?\d+\.\d+){3}' # match all four coords
        boardInfoRange = self._calculateRange('BOARDINFO')
        for i in boardInfoRange:
            coords = re.search(regexPattern, fileLines[i])
            if coords:
                xMin, yMin, xMax, yMax = [float(coord) for coord in coords.group(0).split(',')]
                minPoint = point.Point(xMin, yMin)
                maxPoint = point.Point(xMax, yMax)
                self.boardData['AREA'] = (minPoint, maxPoint)

    
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    


if __name__ == '__main__':
    filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)