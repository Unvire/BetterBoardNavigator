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
        matchedComponents = self._getNetsFromNETLIST(fileLines, padsDict, self.boardData)
        componentWithoutpackages = self._getPackages(fileLines, partNumberToComponents, self.boardData)
        self._rotateComponents(self.boardData, componentWithoutpackages)
        self._removeNotMatchedComponents(self.boardData, matchedComponents)

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
                _, name, partNumber, _, _, side, angle = [parameter.strip() for parameter in line.split(',')]
                side = sideDict[side]
                newComponent = self._createComponent(name, float(angle), side)
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
        matchedComponentsSet = set()
        for i in netlistRange:
            if ',' in fileLines[i]:
                line = fileLines[i]
                _, netName, componentName, pinName , pinX, pinY, mountingType, padID = [parameter.strip() for parameter in line.split(',')]
                self._addBlankNet(nets, netName, componentName)     
                components = boardInstance.getComponents()

                if padID in padsDict:
                    pad = self._calculatePinCoordsAndAddNet(padsDict[padID], pinX, pinY, netName)
                    if componentName not in components:
                        componentOnNet = self._createComponent(componentName, 0, mountingType)
                        boardInstance.addComponent(componentName, componentOnNet)
                    else:
                        componentOnNet = boardInstance.getElementByName('components', componentName)
                        if mountingType == 'A':
                            componentOnNet.setMountingType('TH')
                    
                    componentOnNet.addPin(pinName, pad)

                    nets[netName][componentName]['componentInstance'] = componentOnNet
                    nets[netName][componentName]['pins'].append(pinName)
                    matchedComponentsSet.add(componentName)
        
        boardInstance.setNets(nets)
        return matchedComponentsSet
    
    def _getPackages(self, fileLines:list[str], partNumberToComponents:dict, boardInstance:board.Board) -> list[str]:
        packagesDict = self._getPackagesfromPACKAGES(fileLines)
        pnDict = self._getPNDATA(fileLines)
        componentWithoutpackages = self._matchPackagesToComponents(packagesDict, pnDict, partNumberToComponents, boardInstance)

        for compName in componentWithoutpackages:
            componentInstance = boardInstance.getElementByName('components', compName)
            pinsDict = componentInstance.getPins()
            if len(pinsDict) == 1:
                self._addPackageFor1PinComponent(componentInstance)
            else:
                componentInstance.calculateAreaFromPins()
            componentInstance.caluclateShapeData()

        return componentWithoutpackages
        
    def _rotateComponents(self, boardInstance:board.Board, noRotateComponentNamesList:list[str]):
        componentsDict = boardInstance.getComponents()
        for componentName, componentInstance in componentsDict.items():
            self._addPackageDataIfCoordsMissing(componentInstance)
            
            angle = componentInstance.getAngle()
            if componentName not in noRotateComponentNamesList:
                componentInstance.rotateInPlaceAroundCoords(angle, isRotatePins=False)

            if angle % 180 == 0:
                for _, pinInstance in componentInstance.getPins().items():
                    pinInstance.rotateInPlaceAroundCoords(90)
    
    def _createComponent(self, name:str, angle:float, side:str) -> comp.Component:
        newComponent = comp.Component(name)
        newComponent.setCoords(gobj.Point(None, None))
        newComponent.setAngle(float(angle))
        if side == 'A':
            newComponent.setSide('B')
            newComponent.setMountingType('TH')
        else:
            newComponent.setSide(side)
        newComponent.setShape('RECT')
        return newComponent    
    
    def _createPin(self, name:str, shape:str, width:float|None, height:float|None) -> pin.Pin: 
        newPin = pin.Pin(name)
        newPin.setShape(shape)
        newPin.setDimensions(width, height)
        return newPin
    
    def _removeNotMatchedComponents(self, boardInstance:board.Board, matchedComponentsSet:set):
        boardComponentsSet = set(boardInstance.getComponents().keys())
        removeComponents = list(boardComponentsSet - matchedComponentsSet)
        for componentName in removeComponents:
            boardInstance.removeComponent(componentName)

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
    
    def _getPackagesfromPACKAGES(self, fileLines:list[str]) -> dict:
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
    
    def _addPackageFor1PinComponent(self, componentInstance:comp.Component):
        pinsDict = componentInstance.getPins()
        pinName = list(pinsDict.keys())[0]
        pinInstance = pinsDict[pinName]

        shape = pinInstance.getShapeData()
        bottomLeftPoint, topRightPoint = shape.calculateArea()
        
        componentInstance.setArea(bottomLeftPoint, topRightPoint)
        componentInstance.calculateCenterFromPins()
    
    def _addPackageDataIfCoordsMissing(self, componentInstance:comp.Component):
        coords = componentInstance.getCoords()
        if None in coords.getXY():
            componentInstance.calculateCenterFromPins()
            componentInstance.calculateAreaFromPins()
            componentInstance.caluclateShapeData()
    
    def _calculatePackageBottomRightAndTopLeftPoints(self, componentInstance:comp.Component, dimesions:tuple[float, float]) -> tuple[gobj.Point, gobj.Point]:
        width, height = dimesions
        x0, y0 = self._calculateMoveVectorFromWidthHeight(width, height)
        packageBottomLeftPoint = gobj.Point.translate(componentInstance.coords, (x0, y0))
        packageTopRightPoint = gobj.Point.translate(componentInstance.coords, (-x0, -y0))
        return packageBottomLeftPoint, packageTopRightPoint
    
    def _calculateMoveVectorFromWidthHeight(self, width:float, height:float) -> tuple[float, float]:
        return round(-width / 2, gobj.Point.DECIMAL_POINT_PRECISION), round(-height / 2, gobj.Point.DECIMAL_POINT_PRECISION)

    def _calculateRange(self, sectionName:str) -> range:
        return range(self.sectionsLineNumbers[sectionName][0], self.sectionsLineNumbers[sectionName][1])
    

if __name__ == '__main__':
    #filePath = r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad'
    filePath = r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\cerm.cad'
    loader = CamCadLoader()
    fileLines = loader.loadFile(filePath)
    boardData = loader.processFileLines(fileLines)
    for componentName, component in boardData.components.items():
        print(componentName, component.area)