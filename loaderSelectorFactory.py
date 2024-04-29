import camcadLoader, gencadLoader, odbPlusPlusLoader
import board

class LoaderSelectorFactory:
    def __init__(self, extension:str):
        self.loadersDict = {
            'cad': camcadLoader.CamCadLoader,
            'gcd': gencadLoader.GenCadLoader,
            'tgz': odbPlusPlusLoader.ODBPlusPlusLoader
        }
        self.loaderInstance = self.loadersDict[extension]()

    def loadFile(self, filePath:str) -> list[str]:
        fileLines = self.loaderInstance.loadFile(filePath)
        return fileLines
    
    def processFile(self, fileLines:list[str]) -> board.Board:
        boardInstance = self.loaderInstance.processFile(fileLines)
        return boardInstance