import sys, os, copy, re
sys.path.append(os.getcwd())
import tarfile,  unlzw3
import geometryObjects as gobj
import component as comp
import board, pin

class ODBPlusPlusLoader():
    def __init__(self):
        self.boardData = board.Board()
        self.fileLines = {'eda':[], 'comp_+_top':[], 'comp_+_bot':[]}

    def loadFile(self, filePath:str):
        self._setFilePath(filePath)
        self._getFileLinesFromTar()

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

    def _getTarPathsToEdaComponents(self, tarPaths:list[str]) -> list[str]:
        componentsFilePattern = '^\w+\/steps\/\w+\/layers\/comp_\+_(bot|top)\/components(.Z)?$' # matches comp_+_bot and comp_+_top files both zipped and uzipped
        edaFilePattern = '^\w+\/steps\/\w+\/eda\/data(.Z)?$' # matches eda path both zipped and unzipped
        pattern = f'{componentsFilePattern}|{edaFilePattern}'

        result = []
        for name in tarPaths:
            if re.match(pattern, name):
                result.append(name)
            if len(result) == 3:
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