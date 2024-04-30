import abstractShape

class Pin(abstractShape.Shape):
    def __init__(self, name:str):
        super().__init__(name)
        self.net = None
    
    def __str__(self):
        remark = f'Pad shape={self.shape}, coords={self.coords}, dimensions=[{self.width}, {self.height}]'
        return remark
        
    def setNet(self, netName:str):
        self.net = netName
    
    def getNet(self) -> str:
        return self.net