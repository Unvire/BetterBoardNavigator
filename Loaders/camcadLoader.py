import sys, os, copy 
sys.path.append(os.getcwd())
import geometryObjects
import board, component, pin

class CamCadLoader:
    def __init__(self):
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARDINFO':[], 'PARTLIST':[], 'PNDATA':[], 'NETLIST':[], 'PAD':[], 'PACKAGES':[], 'BOARDOUTLINE':[]}

    def loadFile(self, filePath):
        self.setFilePath(filePath)
        fileLines = self._getFileLines()        
        self._getSectionsLinesBeginEnd(fileLines)

        self._getBoardDimensions(fileLines, self.boardData)
        self._getComponenentsFromPARTLIST(fileLines, self.boardData)
        padsDict = self._getPadsFromPAD(fileLines)
        self._getNetsFromNETLIST(fileLines, padsDict, self.boardData)
        self._getPackages(fileLines, self.boardData)

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
    
    def _getBoardDimensions(self, fileLines:list[str], boardInstance:board.Board):
        boardOutlineRange = self._calculateRange('BOARDOUTLINE')
        bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
        shapes = []

        for i in boardOutlineRange:
            if ',' in fileLines[i]:
                _, xStart, yStart, xEnd, yEnd = fileLines[i].split(',')
                startPoint = geometryObjects.Point(float(xStart), float(yStart))              
                endPoint = geometryObjects.Point(float(xEnd), float(yEnd))

                shapes.append(geometryObjects.Line(startPoint, endPoint))
                for point in [startPoint, endPoint]:
                    bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        
        boardInstance.setOutlines(shapes)
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
    
    def _getComponenentsFromPARTLIST(self, fileLines:list[str], boardInstance:board.Board):
        partlistRange = self._calculateRange('PARTLIST')
        sideDict = {'T':'T', 'P':'T', 'B':'B', 'M':'B'}

        components = {}
        for i in partlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, name, partNumber, x, y, side, angle = [parameter.strip() for parameter in line.split(',')]
                side = sideDict[side]
                x, y  = CamCadLoader.floatOrNone(x), CamCadLoader.floatOrNone(y)
                newComponent = self._createComponent(name, partNumber, x, y, float(angle), side)
                components[name] = newComponent                    
        boardInstance.setComponents(components)

    def _getPadsFromPAD(self, fileLines:list[str]) -> dict:
        padlistRange = self._calculateRange('PAD')
        
        padsDict = {}
        for i in padlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                padID, name, shape, width, height, _, _ = [parameter.strip() for parameter in line.split(',')]                
                width = CamCadLoader.floatOrNone(width)
                height = CamCadLoader.floatOrNone(height)                
                padsDict[padID] = self._createPin(name, shape, width, height)
        return padsDict

    def _getNetsFromNETLIST(self, fileLines:list[str], padsDict:dict, boardInstance:board.Board):
        netlistRange = self._calculateRange('NETLIST')
        nets = {}
        for i in netlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i].replace('\n', '')
                _, netName, componentName, pinName , pinX, pinY, side, padID = [parameter.strip() for parameter in line.split(',')]
                self._addBlankNet(nets, netName, componentName)
                
                components = boardInstance.getComponents()
                if componentName not in components:
                    newComponent = self._createComponent(componentName, '', None, None, 0, side)
                    components[componentName] = newComponent
                    boardInstance.setComponents(components)
                
                pad = copy.deepcopy(padsDict[padID])
                pad.setCoords(geometryObjects.Point(float(pinX), float(pinY)))
                pad.calculateArea()
                pad.setNet(netName)

                componentOnNet = boardInstance.getComponents()[componentName]
                componentOnNet.addPin(pinName, pad)

                nets[netName][componentName]['componentInstance'] = componentOnNet
                nets[netName][componentName]['pins'].append(pinName)
            boardInstance.setNets(nets)
    
    def _getPackages(self, fileLines:list[str], boardInstance:board.Board):
        packagesDict = self._getPackagesfromPACKAGE(fileLines)
        pnDict = self._getPNDATA(fileLines)
        componentWithoutpackages = self._matchPackagesToComponents(packagesDict, pnDict, boardInstance)
        
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
    
    def _createPin(self, name:str, shape:str, width:float|None, height:float|None) -> pin.Pin: 
        newPin = pin.Pin(name)
        newPin.setShape(shape)
        newPin.setDimensions(width, height)
        return newPin

    @staticmethod
    def floatOrNone(x:str):
        try:
            x = float(x)
        except ValueError:
            x = None
        return x        
    
    def _addBlankNet(self, netsDict:dict, netName:str, componentName:str):
        if not netName in netsDict:
            netsDict[netName] = {}
        if not componentName in netsDict[netName]:
            netsDict[netName][componentName] = {'componentInstance':None, 'pins':[]}
    
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
    
    def _matchPackagesToComponents(self, packagesDict:dict, pnDict:dict, boardInstance:board.Board) -> list[component.Component]:
        noPackagesMatch = []
        components = boardInstance.getComponents()
        for componentName in components:
            componentInstance = components[componentName]            
            if not componentInstance.isCoordsValid():   
                componentInstance.calculateCenterFromPins()
            
            componentpartNumber = self._componentPartNumber(componentInstance, pnDict)
            if componentpartNumber in packagesDict:                
                width, height = packagesDict[componentpartNumber]['dimensions']
                x0, y0 = self._calculateMoveVectorFromWidthHeight(width, height, 3)
                packageBottomLeftPoint = geometryObjects.Point.translate(componentInstance.coords, (x0, y0))
                packageTopRightPoint = geometryObjects.Point.translate(componentInstance.coords, (-x0, -y0))

                componentInstance.setComponentArea(packageBottomLeftPoint, packageTopRightPoint)                
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
    #filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    filePath = r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    loader.loadFile(filePath)
    print(loader.boardData.area[0], loader.boardData.area[1])  