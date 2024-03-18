import sys, os; 
sys.path.append(os.getcwd())
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
        self._getComponenentsFromPARTLIST(fileLines)
        self._getNetsFromNETLIST(fileLines)
        self._getPackages(fileLines)

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
                for point in [startPoint, endPoint]:
                    bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        self.boardData['AREA'] = [bottomLeftPoint, topRightPoint]
    
    def _getComponenentsFromPARTLIST(self, fileLines:list[str]):
        partlistRange = self._calculateRange('PARTLIST')
        sideDict = {'T':'T', 'P':'T', 'B':'B', 'M':'B'}

        for i in partlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, name, partNumber, x, y, side, angle = [parameter.strip() for parameter in line.split(',')]
                side = sideDict[side]
                x, y  = CamCadLoader.floatOrNone(x), CamCadLoader.floatOrNone(y)
                newComponent = self._createComponent(name, partNumber, x, y, float(angle), side)
                self.boardData['COMPONENTS'][name] = newComponent    

    def _getNetsFromNETLIST(self, fileLines:list[str]):
        netlistRange = self._calculateRange('NETLIST')
        for i in netlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, netName, componentName, pinName , pinX, pinY, side, _ = [parameter.strip() for parameter in line.split(',')]
                self._addBlankNet(netName, componentName)
                
                if componentName not in self.boardData['COMPONENTS']:
                    newComponent = self._createComponent(componentName, '', None, None, 0, side)
                    self.boardData['COMPONENTS'][componentName] = newComponent

                componentOnNet = self.boardData['COMPONENTS'][componentName]
                componentOnNet.addPin(pinName, geometryObjects.Point(float(pinX), float(pinY)), netName)
                self.boardData['NETS'][netName][componentName]['componentInstance'] = componentOnNet
                self.boardData['NETS'][netName][componentName]['pins'].append(pinName)
    
    def _getPackages(self, fileLines:list[str]):
        packagesDict = self._getPackagesfromPACKAGE(fileLines)
        pnDict = self._getPNDATA(fileLines)
        componentWithoutpackages = self._matchPackagesToComponents(packagesDict, pnDict)
        
        for comp in componentWithoutpackages:
            comp.calculatePackageFromPins()
    
    def _createComponent(self, name:str, partNumber:str, x:float|None, y:float|None, angle:float, side:str) -> component.Component:
        newComponent = component.Component(name)
        newComponent.setPartNumber(partNumber)
        center = geometryObjects.Point(x, y)
        newComponent.setCoords(center)
        newComponent.setAngle(float(angle))
        newComponent.setSide(side)
        return newComponent
    
    @staticmethod
    def floatOrNone(x:str):
        try:
            x = float(x)
        except ValueError:
            x = None
        return x        
    
    def _addBlankNet(self, netName:str, componentName:str):
        if not netName in self.boardData['NETS']:
            self.boardData['NETS'][netName] = {}
        if not componentName in self.boardData['NETS'][netName]:
            self.boardData['NETS'][netName][componentName] = {'componentInstance':None, 'pins':[]}
    
    def _getPackagesfromPACKAGE(self, fileLines:list[str]) -> dict:
        packagesRange = self._calculateRange('PACKAGES')
        packagesDict = {}
        for i in packagesRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                partNumber, pinType, width, height, _ = [parameter.strip() for parameter in line.split(',')]
                width, height  = CamCadLoader.floatOrNone(width), CamCadLoader.floatOrNone(height)
                packagesDict[partNumber] = {'pinType': pinType, 'dimensions':(width, height)}
        return packagesDict
    
    def _getPNDATA(self, fileLines:list[str]) -> dict:
        pnRange = self._calculateRange('PNDATA')
        pnDict = {}
        for i in pnRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                componentPN, _, _, _, _, _, _, partNumber = [parameter.strip() for parameter in line.split(',')]
                pnDict[componentPN] = partNumber
        return pnDict
    
    def _matchPackagesToComponents(self, packagesDict:dict, pnDict:dict) -> list[component.Component]:
        noPackagesMatch = []
        for componentName in self.boardData['COMPONENTS']:
            componentInstance = self.boardData['COMPONENTS'][componentName]
            componentpartNumber = self._componentPartNumber(componentInstance, pnDict)

            if componentpartNumber in packagesDict:
                if not componentInstance.isCoordsValid():   
                    componentInstance.calculateCenterFromPins()
                
                width, height = packagesDict[componentpartNumber]['dimensions']
                x0, y0 = self._calculateMoveVectorFromWidthHeight(width, height, 3)
                packageBottomLeftPoint = geometryObjects.Point.translate(componentInstance.coords, (x0, y0))
                packageTopRightPoint = geometryObjects.Point.translate(componentInstance.coords, (-x0, -y0))

                componentInstance.setPackage(packageBottomLeftPoint, packageTopRightPoint)                
                componentInstance.setPackageType(packagesDict[componentpartNumber]['pinType'])
            else:
                noPackagesMatch.append(componentInstance)
        return noPackagesMatch

    def _componentPartNumber(self, componentInstance:component.Component, pnDict:dict) -> str:
        componentPartNumber = componentInstance.partNumber
        if componentPartNumber in pnDict:
            return pnDict[componentPartNumber]
        return ''
    
    def _calculateMoveVectorFromWidthHeight(self, width:float, height:float, roundDigits:int) -> (float, float):
        return round(-width / 2, roundDigits), round(-height / 2, roundDigits)

    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    

if __name__ == '__main__':
    filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)
    print(loader.boardData['AREA'][0], loader.boardData['AREA'][1])