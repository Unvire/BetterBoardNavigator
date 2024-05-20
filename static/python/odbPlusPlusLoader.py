import copy, re
import tarfile,  unlzw3
import geometryObjects as gobj
import component as comp
import board, pin
from abstractShape import Shape

class ODBPlusPlusLoader():
    def __init__(self):
        self.filePath = None
        self.boardData = board.Board()
        self.fileLines = {'eda':[], 'comp_+_bot':[], 'comp_+_top':[], 'profile':[]}
        self.handleShape = {'CR':gobj.getCircleAndAreaFromValArray, 'RC':gobj.getRectangleAndAreaFromValArray, 
                            'SQ':gobj.getSquareAndAreaFromValArray, 'OS':gobj.getLineAndAreaFromNumArray, 
                            'OC':gobj.getArcAndAreaFromValArray}

    def loadFile(self, filePath:str) -> list[str]:
        self._setFilePath(filePath)
        fileLines = self._getFileLinesFromTar()
        return fileLines

    def processFileLines(self, fileLines:list[str]) -> board.Board:
        self._getSectionsFromFileLines(fileLines)
        self._getBoardOutlineFromProfileFile(self.fileLines['profile'], self.boardData)
        packageIDToComponentNameDict, componentIDToNameDict = self._getComponentsFromCompBotTopFiles(self.fileLines['comp_+_bot'], self.fileLines['comp_+_top'], self.boardData)
        packagesDict = self._getPackagesFromEda(self.fileLines['eda'])
        netsDict = self._getNetsFromEda(self.fileLines['eda'])
        self._assignPackagesToComponents(packageIDToComponentNameDict, packagesDict, self.boardData)
        self._assignNetsAndPins(componentIDToNameDict, netsDict, self.boardData)
        self._fixRotationOfComponents(self.boardData)
        self._fixComponentsAreaScale(self.boardData)
        return self.boardData

    def _setFilePath(self, filePath:str):
        self.filePath = filePath

    def _getFileLinesFromTar(self) -> dict:
        with tarfile.open(self.filePath, 'r') as file:
            allTarPaths = file.getnames()
        
        tarPaths = self._getTarPathsToEdaComponents(allTarPaths)

        fileLines = []
        endLineNumber = -1
        lastLineSectionNumbers = ''
        for path in tarPaths:
            if path:
                startLineNumber = endLineNumber + 1
                lines = self._extractFileInsideTar(path)
                fileLines += lines
                endLineNumber = startLineNumber + len(lines) - 1
                lastLineSectionNumbers += f'{startLineNumber};{endLineNumber};'
            else:
                lastLineSectionNumbers += '0;0;'
        fileLines.append(lastLineSectionNumbers)

        return fileLines
    
    def _getSectionsFromFileLines(self, fileLines:list[str]):
        *sectionsStartEnd, _ = [val for val in fileLines[-1].split(';')] # last item is always ''
        for key in self.fileLines:
            sectionStart = int(sectionsStartEnd.pop(0))
            sectionEnd = int(sectionsStartEnd.pop(0))
            self.fileLines[key] = fileLines[sectionStart:sectionEnd + 1] if bool(sectionStart) or bool(sectionEnd) else []

    def _getComponentsFromCompBotTopFiles(self, botFileLines:list[str], topFileLines:list[str], boardInstance:board.Board) -> tuple[dict, dict]:
        packageIDToComponentNameDict = {}
        componentIDToNameDict = {}
        
        for side, fileLines in zip(['B', 'T'], [botFileLines, topFileLines]):  
            i, iEnd = 0, len(fileLines)
            while i < iEnd - 1: # -1, because the file component always end with "#" line
                if 'CMP' not in fileLines[i]:
                    i += 1
                    continue
                
                *_, componentID = fileLines[i].split(' ')
                i += 1

                componentLine = fileLines[i].split(';')[0]
                _, packageReference, xComp, yComp, angle, _, componentName, *_ = componentLine.split(' ')

                componentIDToNameDict[f'{side}-{componentID}'] = componentName
                componentInstance = self._createComponent(componentName, xComp, yComp, angle, side)
                if not packageReference in packageIDToComponentNameDict:
                    packageIDToComponentNameDict[packageReference] = []
                packageIDToComponentNameDict[packageReference].append(componentName)
                i += 1
                
                while fileLines[i] != '#':
                    if fileLines[i][:3] == 'TOP':
                        pinLine = fileLines[i].split(';')[0]
                        _, pinNumber, xPin, yPin, *_ = pinLine.split(' ') # pins are described 1, 2, 3... in eda
                        pinNumber = str(int(pinNumber) + 1)
                        pinInstance = self._createPin(pinNumber, xPin, yPin)
                        componentInstance.addPin(pinNumber, pinInstance)
                    i += 1
                boardInstance.addComponent(componentName, componentInstance)
        return packageIDToComponentNameDict, componentIDToNameDict
    
    def _getBoardOutlineFromProfileFile(self, fileLines:list[str], boardInstance:board.Board):
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        i, iEnd = 0, len(fileLines)
        shapes = []

        while i < iEnd:
            if 'OB' in fileLines[i]:
                sectionShapes, i, bottomLeftPoint, topRightPoint = self._getShapesAndPointsFromConturSection(fileLines, i, bottomLeftPoint, topRightPoint)
                shapes += sectionShapes
            else:
                keyWord, *parameters = fileLines[i].split(' ')
                if keyWord in self.handleShape:
                    shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](parameters, bottomLeftPoint, topRightPoint)
                    shapes.append(shape)
            i += 1
        
        boardInstance.setArea(bottomLeftPoint, topRightPoint)
        boardInstance.setOutlines(shapes)
    
    def _getPackagesFromEda(self, fileLines:list[str]) -> dict:
        i, iEnd = 0, len(fileLines)
        while fileLines[i] != '# PKG 0':
            i += 1
        
        packagesDict = {}
        while i < iEnd and '#' in fileLines[i]:
            if '# PKG' in fileLines[i]:
                _, _, packageID = fileLines[i].split(' ')
                shapeName, i, bottomLeftPoint, topRightPoint = self._getShapeData(fileLines, i + 2)
                newPackage = {'Area':[bottomLeftPoint, topRightPoint], 'Shape':shapeName, 'Pins':{}}

                while fileLines[i][0] != '#':
                    if 'PIN' in fileLines[i][:3]:
                        shapeName, i, bottomLeftPoint, topRightPoint = self._getShapeData(fileLines, i + 1)
                        newPin = {'Area':[bottomLeftPoint, topRightPoint], 'Shape':shapeName}
                        
                        pinNumber = str(len(newPackage['Pins'].keys()) + 1) # pins are described 1, 2, 3... in eda, but this does not match with their names in comp files. The pins will be named 1, 2, 3 ... for simplier matching
                        newPackage['Pins'][pinNumber] = newPin
                    i += 1

                packagesDict[packageID] = newPackage
            i += 1
        return packagesDict
    
    def _getNetsFromEda(self, fileLines:list[str]) -> dict:
        i, iEnd = 0, len(fileLines)
        while fileLines[i][:3] != 'NET':
            i += 1

        netsDict = {}
        while i < iEnd and 'NET' in fileLines[i]:
            if '#' in fileLines[i]:
                i += 1
            netName = self._getNetName(fileLines, i)
            i, newNetData = self._getPinsOnNet(fileLines, i + 1)
            netsDict[netName] = newNetData
        return netsDict
    
    def _assignPackagesToComponents(self, matchComponentIDDict:dict, packagesDict:dict, boardInstance:board.Board):
        for packageID, componentsNames in matchComponentIDDict.items():
            for componentName in componentsNames: 
                componentInstance = boardInstance.getElementByName('components', componentName)
                packageData = copy.deepcopy(packagesDict[packageID])
                self._addAreaShapeToComponent(componentInstance, packageData)
                self._addAreaShapeToPins(componentInstance, packageData['Pins'])
                componentInstance.rotateInPlaceAroundCoords(componentInstance.getAngle())
    
    def _assignNetsAndPins(self, componentIDToNameDict:dict, netsIDDict:dict, boardInstance:board.Board):
        netsDict = {}
        for netName, componentIDs in netsIDDict.items():
            netsDict[netName] = {}
            for componentID, pinsList in componentIDs.items():
                componentName = componentIDToNameDict[componentID]
                componentInstance = boardInstance.getElementByName('components', componentName)
                
                subnet = {'componentInstance': componentInstance, 'pins':sorted(pinsList, key=lambda x: int(x))}
                for pinNumber in pinsList:
                    pinInstance = componentInstance.getPinByName(pinNumber)
                    if pinInstance:
                        pinInstance.setNet(netName)
                netsDict[netName][componentName] = subnet
        boardInstance.setNets(netsDict)

    def _fixRotationOfComponents(self, boardInstance:board.Board):
        components = boardInstance.getComponents()
        for _, componentInstance in components.items():
            angle = componentInstance.getAngle()
            componentInstance.rotatePinsAroundCoords(componentInstance.getCoords(), angle)
            for _, pinInstance in componentInstance.getPins().items():
                pinInstance.rotateInPlaceAroundCoords(angle)
    
    def _fixComponentsAreaScale(self, boardInstance:board.Board):
        boardArea = boardInstance.getArea()
        boardWidth, boardHeight = Shape.getAreaWidthHeight(boardArea)

        componentsArea = boardInstance.calculateAreaFromComponents()
        componentsWidth, componentsHeight = Shape.getAreaWidthHeight(componentsArea)

        rescaleFactor = min(boardWidth / componentsWidth, boardHeight / componentsHeight)
        if abs(rescaleFactor - 1) >= 0.01:
            self._rescaleOutlinesArea(boardInstance, rescaleFactor)

    def _addAreaShapeToComponent(self, componentInstance:comp.Component, packageData:dict):
        area = packageData['Area']
        shapeName = packageData['Shape']
        self._addAreaShapeToAbstractShape(componentInstance, area, shapeName)
    
    def _addAreaShapeToPins(self, componentInstance:comp.Component, pinsData:dict):
        for pinName in pinsData:
            pinInstance = componentInstance.getPinByName(pinName)
            if pinInstance:
                area = pinsData[pinName]['Area']
                shapeName = pinsData[pinName]['Shape']
                self._addAreaShapeToAbstractShape(pinInstance, area, shapeName)
        
    def _addAreaShapeToAbstractShape(self, instance:comp.Component|pin.Pin, area:list[gobj.Point, gobj.Point], shapeName:str):
        xCoords, yCoords = instance.getCoordsAsTranslationVector()
        xAreaCenter, yAreaCenter = Shape.calculateAreaCenterXY(area)

        bottomLeftPoint, topRightPoint = area
        for point in [bottomLeftPoint, topRightPoint]:
            moveVector = [xCoords - xAreaCenter, yCoords - yAreaCenter]
            point.translateInPlace(moveVector)
        instance.normalizeAndSetArea([bottomLeftPoint, topRightPoint])
        instance.calculateDimensionsFromArea()

        instance.setShape(shapeName)
        instance.caluclateShapeData()

    def _rescaleOutlinesArea(self, boardInstance:board.Board, scaleFactor:float):
        outlines = boardInstance.getOutlines()
        for shape in outlines:
            shape.scaleInPlace(1 / scaleFactor)
        
        area = boardInstance.getArea()
        for point in area:
            point.scaleInPlace(1 / scaleFactor)

    def _getShapeData(self, fileLines:list[str], i:int) -> tuple[int, str, gobj.Point, gobj.Point]:
        shapeName = 'RECT'
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints() 
        if 'CT' in fileLines[i]:
            _, i, bottomLeftPoint, topRightPoint = self._getShapesAndPointsFromConturSection(fileLines, i + 1, bottomLeftPoint, topRightPoint)
        else:
            keyWord, *parameters = fileLines[i].split(' ')
            shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](parameters, bottomLeftPoint, topRightPoint)
            if isinstance(shape, gobj.Circle):
                shapeName = 'CIRCLE'
        return shapeName, i, bottomLeftPoint, topRightPoint
    
    def _getNetName(self, fileLines:list[str], i:int) -> str:
        _, netName, *_ = fileLines[i].split(' ')
        return netName
    
    def _getPinsOnNet(self, fileLines:list[str], i:int) -> tuple[int, dict]:
        newNetData = {}
        while i < len(fileLines) and '#' not in fileLines[i]:
            if 'SNT TOP' in fileLines[i][:7]:
                *_, side, componentID, pinID = fileLines[i].split(' ')
                pinID = str(int(pinID) + 1)
                componentID = f'{side}-{componentID}'
                if not componentID in newNetData:
                    newNetData[componentID] = []
                newNetData[componentID].append(pinID)
            i += 1
        return i, newNetData

    def _createComponent(self, name:str, x:str, y:str, angle:str, side:str) -> comp.Component:
        centerPoint = gobj.Point(gobj.floatOrNone(x), gobj.floatOrNone(y))
        angle = gobj.floatOrNone(angle)

        newComponent = comp.Component(name)
        newComponent.setAngle(angle)
        newComponent.setCoords(centerPoint)
        newComponent.setSide(side)
        return newComponent
    
    def _createPin(self, pinNumber:str, x:str, y:str) -> pin.Pin:
        centerPoint = gobj.Point(gobj.floatOrNone(x), gobj.floatOrNone(y))
                
        newPin = pin.Pin(pinNumber)
        newPin.setCoords(centerPoint)
        return newPin
    
    def _getShapesAndPointsFromConturSection(self, fileLines:list[str], i:int, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[list['gobj.Point|gobj.Arc|gobj.Circle|gobj.Rectangle'], int, gobj.Point, gobj.Point]:
        shapes = []

        _, x, y, *_ = fileLines[i].split(' ')
        pointQueue = [x, y]
        i += 1
        while fileLines[i] != 'OE':
            keyWord, x, y, *rest  = fileLines[i].split(' ')
            pointQueue += [x, y]                
            shapeHandlerArgumentList = pointQueue[:] # shallow copy to prevent overwriting pointQueue
            if keyWord == 'OC':
                xCenter, yCenter, isClockwise = rest
                if isClockwise == 'Y':
                    for _ in range(2):
                        shapeHandlerArgumentList.append(shapeHandlerArgumentList.pop(0)) # swap start point and end point in a shift register way for clockwise arc
                shapeHandlerArgumentList += [xCenter, yCenter]

            shape, bottomLeftPoint, topRightPoint = self.handleShape[keyWord](shapeHandlerArgumentList, bottomLeftPoint, topRightPoint)
            shapes.append(shape)
            pointQueue = pointQueue[2:] # remove first two coordinates -> queue.pop(0) x2
            i += 1

        return shapes, i, bottomLeftPoint, topRightPoint

    def _getTarPathsToEdaComponents(self, tarPaths:list[str]) -> list[str]:
        def findMatchingStrings(pattern:str, strings:list[str]) -> list[str]:
            result = []
            for s in strings:
                if re.match(pattern, s):
                    result.append(s)
            return result

        commonPattern = '^[\w+\s\-]+\/steps\/[\w+\s\-]+\/'
        botComponentsFilePattern = commonPattern + 'layers\/comp_\+_bot\/components(.(z|Z))?$' # matches comp_+_bot files both zipped and uzipped
        topComponentsFilePattern = commonPattern + 'layers\/comp_\+_top\/components(.(z|Z))?$' # matches comp_+_top files both zipped and uzipped
        edaFilePattern = commonPattern + 'eda\/data(.(z|Z))?$' # matches eda path both zipped and unzipped
        profileFilePattern = commonPattern + 'profile(.(z|Z))?$'  # matches profile path both zipped and unzipped

        matchingEdaPaths = findMatchingStrings(edaFilePattern, tarPaths)
        matchingBotComponentPaths = findMatchingStrings(botComponentsFilePattern, tarPaths)
        matchingTopComponentsPaths = findMatchingStrings(topComponentsFilePattern, tarPaths)
        matchingProfilePaths = findMatchingStrings(profileFilePattern, tarPaths)

        result = []
        for pathsList in [matchingEdaPaths, matchingBotComponentPaths, matchingTopComponentsPaths, matchingProfilePaths]:
            subList = [] if not pathsList else pathsList[0]
            result.append(subList)
        return result
    
    def _extractFileInsideTar(self, pathInTar) -> list[str]:
        with tarfile.open(self.filePath, 'r') as file:
            if not pathInTar:
                return []
            with file.extractfile(pathInTar) as extractedFile:
                if pathInTar[-2:].upper() == '.Z':
                    compressedFile = extractedFile.read()
                    decompressedFile = unlzw3.unlzw(compressedFile).decode('utf-8')
                    lines = [line.replace('\r', '') for line in decompressedFile.split('\n')]
                else:
                    lines = [line.decode('utf-8').replace('\n', '').replace('\r', '') for line in extractedFile.readlines()]
        return lines

if __name__ == '__main__':
    loader = ODBPlusPlusLoader()
    fileLines = loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\odb\DEL2114.tgz')
    loader.processFileLines(fileLines)