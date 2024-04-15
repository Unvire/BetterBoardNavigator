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

    def loadFile(self, filePath:str):
        self._setFilePath(filePath)
        self._getFileLinesFromTar()
        matchDict = self._getComponentsFromCompBotTopFiles(self.fileLines['comp_+_bot'], self.fileLines['comp_+_top'], self.boardData)

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
            while i < iEnd - 1: 
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
                self.boardData.addComponent(componentName, componentInstance)

        return matchDict

    def _createComponent(self, name:str, x:str, y:str, angle:str, side:str) -> comp.Component:
        x = gobj.floatOrNone(x)
        y = gobj.floatOrNone(y)
        centerPoint = gobj.Point(x, y)
        angle = gobj.floatOrNone(angle)

        newComponent = comp.Component(name)
        newComponent.setAngle(angle)
        newComponent.setCoords(centerPoint)
        newComponent.setSide(side)
        return newComponent
    
    def _createPin(self, pinNumber:str, x:str, y:str) -> pin.Pin:
        x = gobj.floatOrNone(x)
        y = gobj.floatOrNone(y)
        centerPoint = gobj.Point(x, y)
        
        newPin = pin.Pin(pinNumber)
        newPin.setCoords(centerPoint)
        return newPin
            

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