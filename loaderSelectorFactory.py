import camcadLoader, gencadLoader, odbPlusPlusLoader
import board

class LoaderSelectorFactory:
    def __init__(self):
        self.loadersDict = {
            '.cad': camcadLoader.CamCadLoader,
            '.gcd': gencadLoader.GenCadLoader,
            '.tgz': odbPlusPlusLoader.ODBPlusPlusLoader
        }

    def loadFile(self, filePath:str) -> board.Board:
        fileExtension = filePath.split('.')[-1]
        if fileExtension in self.loadersDict:
            loader = self.loadersDict[fileExtension]()
            return loader.loadFile(filePath)