import camcadLoader, gencadLoader, odbPlusPlusLoader, visecadLoader
import board

class LoaderSelectorFactory:
    def __init__(self, fileName:str):
        self.loadersDict = {
            'cad': camcadLoader.CamCadLoader,
            'gcd': gencadLoader.GenCadLoader,
            'tgz': odbPlusPlusLoader.ODBPlusPlusLoader,            
            'zip': odbPlusPlusLoader.ODBPlusPlusLoader,
            'ccz': visecadLoader.VisecadLoader
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
    from pathlib import Path

    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    filePath = Path(openSchematicFile())
    extension = (filePath.suffix).replace('.', '')

    loader = LoaderSelectorFactory(extension)
    fileLines = loader.loadFile(filePath)
    boardInstance = loader.processFileLines(fileLines)
    boardInstance.toJson()