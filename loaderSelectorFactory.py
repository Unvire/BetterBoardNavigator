import Loaders.camcadLoader
import Loaders.gencadLoader
import Loaders.odbPlusPlusLoader
import board

class LoaderSelectorFactory:
    def __init__(self):
        self.loadersDict = {
            '.cad': Loaders.camcadLoader.CamCadLoader,
            '.gcd': Loaders.gencadLoader.GenCadLoader,
            '.tgz': Loaders.odbPlusPlusLoader.ODBPlusPlusLoader
        }

    def loadFile(self, filePath:str) -> board.Board:
        fileExtension = filePath.split('.')[-1]
        if fileExtension in self.loadersDict:
            loader = self.loadersDict[fileExtension]()
            return loader.loadFile(filePath)