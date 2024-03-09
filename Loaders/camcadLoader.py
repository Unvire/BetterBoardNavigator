class CamCadLoader:
    def __init__(self, filePath:str):
        self.filePath = filePath
        self.boardData = {}
        self.sectionsLineNumbers = {'BOARDINFO':[], 'PARTLIST':[], 'PNDATA':[], 'NETLIST':[], 'PAD':[], 'PACKAGES':[], 'BOARDOUTLINE':[]}

    def loadFile(self):
        fileLines = self._getFileLines()
        self._getSectionsLinesBeginEnd(fileLines)
    
    def _getFileLines(self) -> list[str]:
        with open(self.filePath, 'r') as file:
            fileLines = file.readlines()
        return fileLines

    def _getSectionsLinesBeginEnd(self, fileLines):
        for i, line in enumerate(fileLines):
            sectionName = line[1:-1]
            if sectionName in self.sectionsLineNumbers or (sectionName:=sectionName[3:]) in self.sectionsLineNumbers:
                self.sectionsLineNumbers[sectionName].append(i)
    


if __name__ == '__main__':
    loader = CamCadLoader(r'C:\Users\krzys\Documents\GitHub\boardNavigator\Schematic\lvm Core.cad')