import xml.etree.ElementTree as et
from zipfile import ZipFile
import geometryObjects as gobj
import component as comp
import board, pin
from abstractShape import Shape

class VisecadLoader():
    def __init__(self):
        self.boardData = board.Board()

    def loadFile(self, filePath:str) -> list[str]:
        with ZipFile(filePath, 'r') as zippedFile:
            xmlFile = zippedFile.namelist()[0]
            with zippedFile.open(xmlFile) as file:
                fileLines = file.readlines()
        return fileLines
    
    def processFileLines(self, fileLines:list[str]) -> board.Board:
        return self.boardData

if __name__ == '__main__':
    loader = VisecadLoader()
    fileLines = loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\ccz\15017460_02.ccz')
    print(fileLines)
    loader.processFileLines(fileLines)