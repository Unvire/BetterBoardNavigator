class CamCadLoader:
    def __init__(self, filePath:str):
        self.filePath = filePath
        self.boardData = {}
        self.sectionsLineNumbers = {'BOARDINFO':[], 'PARTLIST':[], 'PNDATA':[], 'NETLIST':[], 'PAD':[], 'PACKAGES':[], 'ROUTING':[], 'BOARDOUTLINE':[]}

if __name__ == '__main__':
    pass