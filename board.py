import pin, component
import geometryObjects

class Board:
    def __init__(self):
        self.area = []
        self.outlines = []
        self.components = []
        self.nets = []
    
    def setArea(self, bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point):
        self.area = [bottomLeftPoint, topRightPoint]
    
    def getArea(self) -> list[geometryObjects.Point]:
        return self.area
    
    def setOutlines(self, outlinesList:list[geometryObjects.Point|geometryObjects.Arc]):
        self.outlines = outlinesList

    def getOutlines(self) -> list[geometryObjects.Point|geometryObjects.Arc]:
        return self.outlines
    
    def setComponents(self, componentsDict:dict):
        self.components = componentsDict
    
    def getComponents(self) -> dict:
        return self.components
    
    def setNets(self, netsDict):
        self.nets = netsDict
    
    def getNets(self) -> dict:
        return self.nets