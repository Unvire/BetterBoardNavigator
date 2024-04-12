import sys, os, copy
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

    def _setFilePath(self, filePath:str):
        self.filePath = filePath

if __name__ == '__main__':
    loader = ODBPlusPlusLoader()
    loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\odb\660891125.tgz')