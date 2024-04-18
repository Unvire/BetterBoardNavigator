import sys, os, copy, re
sys.path.append(os.getcwd())
import tarfile,  unlzw3
import geometryObjects as gobj
import component as comp
import board, pin

class ODBPlusPlusLoader():
    def __init__(self):
        self.filePath = None
        self.boardData = board.Board()
        self.fileLines = {'eda':[], 'comp_+_top':[], 'comp_+_bot':[], 'profile':[]}
        self.handleShape = {'CR':gobj.getCircleAndAreaFromValArray, 'RC':gobj.getRectangleAndAreaFromValArray, 
                            'SQ':gobj.getSquareAndAreaFromValArray, 'OS':gobj.getLineAndAreaFromNumArray, 
                            'OC':gobj.getArcAndAreaFromValArray}

    def loadFile(self, filePath:str):
        self._setFilePath(filePath)
        self._getFileLinesFromTar()
        self._getBoardOutlineFromProfileFile(self.fileLines['profile'], self.boardData)
        matchDict = self._getComponentsFromCompBotTopFiles(self.fileLines['comp_+_bot'], self.fileLines['comp_+_top'], self.boardData)
        packagesDict = self._getPackagesFromEda(self.fileLines['eda'])

    def _setFilePath(self, filePath:str):
        self.filePath = filePath

    def _getFileLinesFromTar(self):
        with tarfile.open(self.filePath, 'r') as file:
            allTarPaths = file.getnames()
        
        tarPaths = self._getTarPathsToEdaComponents(allTarPaths)
        fileLinesKeys = list(self.fileLines.keys())
        for key, path in zip(fileLinesKeys, tarPaths):
            lines = self._extractFileInsideTar(path)
            self.fileLines[key] = lines
    
    def _getComponentsFromCompBotTopFiles(self, botFileLines:list[str], topFileLines:list[str], boardInstance:board.Board):
        matchDict = {}
        
        for side, fileLines in zip(['B', 'T'], [botFileLines, topFileLines]):  
            i, iEnd = 0, len(fileLines)
            while i < iEnd - 1: # -1, because the file component always end with "#" line
                while 'CMP' not in fileLines[i][:3]:
                    i += 1

                componentLine = fileLines[i].split(';')[0]
                _, packageReference, xComp, yComp, angle, _, componentName, *_ = componentLine.split(' ')
                componentInstance = self._createComponent(componentName, xComp, yComp, angle, side)
                matchDict[componentName] = {'packageID':packageReference}
                i += 1
                
                while fileLines[i] != '#':
                    pinLine = fileLines[i].split(';')[0]
                    _, pinNumber, xPin, yPin, _, _, netNumber, *_ = pinLine.split(' ')
                    pinInstance = self._createPin(pinNumber, xPin, yPin)
                    componentInstance.addPin(pinNumber, pinInstance)
                    matchDict[componentName][pinNumber] = netNumber
                    i += 1
                boardInstance.addComponent(componentName, componentInstance)

        return matchDict
    
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
        mountTypeDict = {'T': 'TH', 'S':'SMT', 'B':'SMT'}
        while i < iEnd and '#' in fileLines[i]:
            if '# PKG' in fileLines[i]:
                _, _, packageID = fileLines[i].split(' ')
                shapeName, i, bottomLeftPoint, topRightPoint = self._getShapeData(fileLines, i + 2)
                newPackage = {'Area':[bottomLeftPoint, topRightPoint], 'Shape':shapeName, 'Pins':{}}

                while fileLines[i][0] != '#':
                    if 'PIN' in fileLines[i][:3]:
                        _, pinNumber, mountingType, *_ = fileLines[i].split(' ')
                        shapeName, i, bottomLeftPoint, topRightPoint = self._getShapeData(fileLines, i + 1)
                        newPin = {'Area':[bottomLeftPoint, topRightPoint], 'Shape':shapeName}

                        newPackage['Mounting type'] = mountTypeDict[mountingType]
                        newPackage['Pins'][pinNumber] = newPin
                    i += 1

                packagesDict[packageID] = newPackage
            i += 1
        return packagesDict

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
    
    def _getShapesAndPointsFromConturSection(self, fileLines:list[str], i:int, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[list[gobj.Point|gobj.Arc|gobj.Circle|gobj.Rectangle], int, gobj.Point, gobj.Point]:
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
        componentsFilePattern = '^\w+\/steps\/\w+\/layers\/comp_\+_(bot|top)\/components(.(z|Z))?$' # matches comp_+_bot and comp_+_top files both zipped and uzipped
        edaFilePattern = '^\w+\/steps\/\w+\/eda\/data(.(z|Z))?$' # matches eda path both zipped and unzipped
        profileFilePattern = '^\w+\/steps\/\w+\/profile(.(z|Z))?$'  # matches profile path both zipped and unzipped
        pattern = f'{componentsFilePattern}|{edaFilePattern}|{profileFilePattern}'

        result = []
        for name in tarPaths:
            if re.match(pattern, name):
                result.append(name)
            if len(result) == 4:
                break
        return sorted(result)
    
    def _extractFileInsideTar(self, pathInTar) -> list[str]:
        with tarfile.open(self.filePath, 'r') as file:
            with file.extractfile(pathInTar) as extractedFile:
                if pathInTar[-2:].upper() == '.Z':
                    compressedFile = extractedFile.read()
                    decompressedFile = unlzw3.unlzw(compressedFile).decode('utf-8')
                    lines = decompressedFile.split('\n')
                else:
                    lines = [line.decode('utf-8').replace('\r\n', '') for line in extractedFile.readlines()]
        return lines

if __name__ == '__main__':
    loader = ODBPlusPlusLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\odb\660891125.tgz')