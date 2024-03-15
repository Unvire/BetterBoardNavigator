import re
import geometryObjects
import component

class CamCadLoader:
    def __init__(self):
        '''
        self.boardData['AREA'] = [bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point] 
        self.boardData['SHAPE'] = list of geometryObjects.Line and geometryObjects.Arc
        self.boardData['COMPONENTS'] = dict 'componentName': component.Component instance
        self.boardData['NETS'] = dict netName:{componentName:{
                                                'componentInstance': component.Component instance, 
                                                'pins': list[str]}
                                                }
        '''
        self.boardData = {'SHAPE':[], 'COMPONENTS':{}, 'NETS':{}}
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
        sideDict = {'T':'T', 'P':'T', 'B':'B', 'M':'B'}

        for i in partlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, name, packageName, x, y, side, angle = [parameter.strip() for parameter in line.split(',')]
                side = sideDict[side]
                newComponent = self._createComponent(name, packageName, float(x), float(y), float(angle), side)
                self.boardData['COMPONENTS'][name] = newComponent
    
    def _createComponent(self, name:str, packageName:str, x:float|None, y:float|None, angle:float, side:str) -> component.Component:
        newComponent = component.Component(name)
        newComponent.setPackage(packageName)
        center = geometryObjects.Point(x, y)
        newComponent.setCoords(center)
        newComponent.setAngle(float(angle))
        newComponent.setSide(side)
        return newComponent

    def _getNetsfromNETLIST(self, fileLines:list[str]):
        netlistRange = self._calculateRange('NETLIST')
        for i in netlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, netName, componentName, pinName , pinX, pinY, _, _ = [parameter.strip() for parameter in line.split(',')]
                self._addBlankNet(netName, componentName)
                
                componentOnNet = self.boardData['COMPONENTS'][componentName]
                componentOnNet.addPin(pinName, geometryObjects.Point(float(pinX), float(pinY)), netName)
                self.boardData['NETS'][netName][componentName]['componentInstance'] = componentOnNet
                self.boardData['NETS'][netName][componentName]['pins'].append(pinName)
    
    def _addBlankNet(self, netName:str, componentName:str):
        if not netName in self.boardData['NETS']:
            self.boardData['NETS'][netName] = {}
        if not componentName in self.boardData['NETS'][netName]:
            self.boardData['NETS'][netName][componentName] = {'componentInstance':None, 'pins':[]}
                
    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    

if __name__ == '__main__':
    filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)