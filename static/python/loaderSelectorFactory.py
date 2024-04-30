import camcadLoader, gencadLoader, odbPlusPlusLoader
import board

class LoaderSelectorFactory:
    def __init__(self, fileName:str):
        self.loadersDict = {
            'cad': camcadLoader.CamCadLoader,
            'gcd': gencadLoader.GenCadLoader,
            'tgz': odbPlusPlusLoader.ODBPlusPlusLoader
        }
        extension = fileName.split('.')[-1].lower()
        self.loaderInstance = self.loadersDict[extension]()

    def loadFile(self, filePath:str) -> list[str]:
        fileLines = self.loaderInstance.loadFile(filePath)
        return fileLines
    
    def processFileLines(self, fileLines:list[str]) -> board.Board:
        boardInstance = self.loaderInstance.processFileLines(fileLines)
        return boardInstance

if __name__ == '__main__':
    loader = LoaderSelectorFactory('cad')
    fileLines = loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\lvm Core.cad')
    _ = loader.processFileLines(fileLines)
    print('camcad file loaded')

    loader = LoaderSelectorFactory('gcd')
    fileLines = loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\jaguar REV.GCD')
    _ = loader.processFileLines(fileLines)
    print('gencad file loaded')

    loader = LoaderSelectorFactory('tgz')
    fileLines = loader.loadFile(r'C:\Python 3.11.1\Compiled\Board Navigator\Schematic\odb\DEL2114.tgz')
    _ = loader.processFileLines(fileLines)
    print('odb++ file loaded')