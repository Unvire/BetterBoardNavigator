import geometryObjects
import component

class Pin:
    def __init__(self, name:str):
        self.name = name
        self.shape = 'RECTANGLE'
        self.center = None
        self.pinArea = []
        self.parentComponent = None
        self.net = None
        self.width = 0
        self.height = 0
    
    def setShape(self, shape:str):
        self.shape = shape
    
    def setCenter(self, centerPoint:geometryObjects.Point):
        self.center = centerPoint
    
    def setPinArea(self, bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point):
        self.pinArea = [bottomLeftPoint, topRightPoint]
    
    def setParentComponent(self, componentInstance:component.Component):
        self.parentComponent = componentInstance
    
    def setNet(self, netName:str):
        self.net = netName
    
    def setDimensions(self, width:float, height:float):
        self.width = width
        self.height = height