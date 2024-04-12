import sys, os, copy, re
sys.path.append(os.getcwd())
import tarfile
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
            tarPaths = file.getnames()
        
        self._getTarPathsToEdaComponents(tarPaths)
        
    def _getTarPathsToEdaComponents(self, tarPaths:list[str]) -> list[str]:
        componentsFilePattern = '^\w+\/steps\/\w+\/layers\/comp_\+_(bot|top)\/components(.Z)?$' # matches comp_+_bot and comp_+_top files both zipped and uzipped
        edaFilePattern = '^\w+\/steps\/\w+\/eda\/data(.Z)?$' # matches eda path both zipped and unzipped
        for name in tarPaths:
            print(name)
        

if __name__ == '__main__':
    loader = ODBPlusPlusLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\odb\m10.tgz')