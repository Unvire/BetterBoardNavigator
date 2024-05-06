import copy 
import geometryObjects as gobj
import component as comp
import board, pin

class CamCadLoader:
    def __init__(self):        
        self.filePath = None
        self.boardData = board.Board()
        self.sectionsLineNumbers = {'BOARDINFO':[], 'PARTLIST':[], 'PNDATA':[], 'NETLIST':[], 'PAD':[], 'PACKAGES':[], 'BOARDOUTLINE':[]}

    def loadFile(self, filePath:str) -> list[str]:
        self._setFilePath(filePath)
        fileLines = self._getFileLines()
        return fileLines

    def processFileLines(self, fileLines:list[str]) -> board.Board:       
        self._getSectionsLinesBeginEnd(fileLines)

        ## boardData is modified globally inside these functions
        self._getBoardDimensions(fileLines, self.boardData)
        partNumberToComponents = self._getComponenentsFromPARTLIST(fileLines, self.boardData)
        padsDict = self._getPadsFromPAD(fileLines)
        self._getNetsFromNETLIST(fileLines, padsDict, self.boardData)
        self._getPackages(fileLines, partNumberToComponents, self.boardData)
        self._rotateComponents(self.boardData)

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
        boardOutlineRange = self._calculateRange('BOARDOUTLINE')
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        shapes = []

        for i in boardOutlineRange:
            if ',' in fileLines[i]:
                _, xStart, yStart, xEnd, yEnd = fileLines[i].split(',')
                startPoint = gobj.Point(float(xStart), float(yStart))              
                endPoint = gobj.Point(float(xEnd), float(yEnd))

                shapes.append(gobj.Line(startPoint, endPoint))
                for point in [startPoint, endPoint]:
                    bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        
        boardInstance.setOutlines(shapes)
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
    
    def _getComponenentsFromPARTLIST(self, fileLines:list[str], boardInstance:board.Board) -> dict:
        partlistRange = self._calculateRange('PARTLIST')
        sideDict = {'T':'T', 'P':'T', 'B':'B', 'M':'B'}

        components = {}
        partNumberToComponents = {}
        for i in partlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i]
                _, name, partNumber, x, y, side, angle = [parameter.strip() for parameter in line.split(',')]
                side = sideDict[side]
                x, y  = gobj.floatOrNone(x), gobj.floatOrNone(y)
                newComponent = self._createComponent(name, x, y, float(angle), side)
                components[name] = newComponent

                if not partNumber in partNumberToComponents:
                    partNumberToComponents[partNumber] = []
                partNumberToComponents[partNumber].append(name)
        boardInstance.setComponents(components)
        return partNumberToComponents

    def _getPadsFromPAD(self, fileLines:list[str]) -> dict:
        padlistRange = self._calculateRange('PAD')
        
        padsDict = {}
        for i in padlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i]
                padID, name, shape, width, height, _, _ = [parameter.strip() for parameter in line.split(',')]                
                width = gobj.floatOrNone(width)
                height = gobj.floatOrNone(height)                
                padsDict[padID] = self._createPin(name, shape, width, height)
        return padsDict

    def _getNetsFromNETLIST(self, fileLines:list[str], padsDict:dict, boardInstance:board.Board):
        netlistRange = self._calculateRange('NETLIST')
        nets = {}
        for i in netlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i]
                _, netName, componentName, pinName , pinX, pinY, side, padID = [parameter.strip() for parameter in line.split(',')]
                self._addBlankNet(nets, netName, componentName)     
                components = boardInstance.getComponents()
                pad = self._calculatePinCoordsAndAddNet(padsDict[padID], pinX, pinY, netName)
                
                if componentName not in components:
                    newComponent = self._createComponent(componentName, None, None, 0, side)
                    boardInstance.addComponent(componentName, newComponent)                
                
                componentOnNet = boardInstance.getElementByName('components', componentName)
                componentOnNet.addPin(pinName, pad)

                nets[netName][componentName]['componentInstance'] = componentOnNet
                nets[netName][componentName]['pins'].append(pinName)
            boardInstance.setNets(nets)
    
    def _getPackages(self, fileLines:list[str], partNumberToComponents:dict, boardInstance:board.Board):
        packagesDict = self._getPackagesfromPACKAGE(fileLines)
        pnDict = self._getPNDATA(fileLines)
        componentWithoutpackages = self._matchPackagesToComponents(packagesDict, pnDict, partNumberToComponents, boardInstance)

        for compName in componentWithoutpackages:
            componentInstance = boardInstance.getElementByName('components', compName)
            componentInstance.calculateAreaFromPins()
            componentInstance.caluclateShapeData()
        
    def _rotateComponents(self, boardInstance:board.Board):
        componentsDict = boardInstance.getComponents()
        for _, componentInstance in componentsDict.items():
            coords = componentInstance.getCoords()
            if None in coords.getXY():
                componentInstance.calculateCenterFromPins()
                componentInstance.calculateAreaFromPins()
                componentInstance.caluclateShapeData()
            componentInstance.rotateInPlaceAroundCoords(componentInstance.angle)
    
    def _createComponent(self, name:str, x:float|None, y:float|None, angle:float, side:str) -> comp.Component:
        newComponent = comp.Component(name)
        center = gobj.Point(x, y)
        newComponent.setCoords(center)
        newComponent.setAngle(float(angle))
        newComponent.setSide(side)
        newComponent.setShape('RECT')
        return newComponent
    
    def _createPin(self, name:str, shape:str, width:float|None, height:float|None) -> pin.Pin: 
        newPin = pin.Pin(name)
        newPin.setShape(shape)
        newPin.setDimensions(width, height)
        return newPin

    def _calculatePinCoordsAndAddNet(self, pad:dict, pinX:str, pinY:str, netName:str) -> pin.Pin:
        pad = copy.deepcopy(pad)
        pad.setCoords(gobj.Point(float(pinX), float(pinY)))
        pad.calculateAreaFromWidthHeightCoords()
        pad.setNet(netName)
        pad.caluclateShapeData()
        return pad
    
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
                line = fileLines[i]
                partNumber, pinType, width, height, _ = [parameter.strip() for parameter in line.split(',')]
                width, height  = gobj.floatOrNone(width), gobj.floatOrNone(height)
                packagesDict[partNumber] = {'pinType': pinType, 'dimensions':(width, height)}
        return packagesDict
    
    def _getPNDATA(self, fileLines:list[str]) -> dict:
        pnRange = self._calculateRange('PNDATA')
        pnDict = {}
        for i in pnRange:
            if ',' in fileLines[i]:
                line = fileLines[i]
                componentPN, _, _, _, _, _, _, partNumber = [parameter.strip() for parameter in line.split(',')]
                pnDict[componentPN] = partNumber
        return pnDict
    
    def _matchPackagesToComponents(self, packagesDict:dict, pnDict:dict, partNumberToComponents:dict, boardInstance:board.Board) -> list[comp.Component]:
        noPackagesMatch = set()
        components = boardInstance.getComponents()
        for partNumber, componentNameList in partNumberToComponents.items():
            if not partNumber in pnDict:
                noPackagesMatch.update(componentNameList)
                continue

            packageName = pnDict[partNumber]
            for componentName in componentNameList: 
                componentInstance = components[componentName]
                if not componentInstance.isCoordsValid():   
                    componentInstance.calculateCenterFromPins()

                if not packageName in packagesDict:
                    noPackagesMatch.add(componentName)
                    continue
                
                package = packagesDict[packageName]
                dimensions = package['dimensions']
                packageBottomLeftPoint, packageTopRightPoint = self._calculatePackageBottomRightAndTopLeftPoints(componentInstance, dimensions)
                componentInstance.setArea(packageBottomLeftPoint, packageTopRightPoint)                               
                componentInstance.setMountingType(package['pinType'])
                componentInstance.caluclateShapeData()

        return list(noPackagesMatch)
    
    def _calculatePackageBottomRightAndTopLeftPoints(self, componentInstance:comp.Component, dimesions:tuple[float, float]) -> tuple[gobj.Point, gobj.Point]:
        width, height = dimesions
        x0, y0 = self._calculateMoveVectorFromWidthHeight(width, height, 3)
        packageBottomLeftPoint = gobj.Point.translate(componentInstance.coords, (x0, y0))
        packageTopRightPoint = gobj.Point.translate(componentInstance.coords, (-x0, -y0))
        return packageBottomLeftPoint, packageTopRightPoint
    
    def _calculateMoveVectorFromWidthHeight(self, width:float, height:float, roundDigits:int) -> tuple[float, float]:
        return round(-width / 2, roundDigits), round(-height / 2, roundDigits)

    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    

if __name__ == '__main__':
    #filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    filePath = r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\lvm Core.cad'
    loader = CamCadLoader()
    fileLines = loader.loadFile(filePath)
    loader.processFileLines(fileLines)
    print(loader.boardData.area[0], loader.boardData.area[1])  