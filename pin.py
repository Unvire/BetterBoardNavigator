import geometryObjects

class Pin:
    def __init__(self, name:str):
        self.name = name
        self.shape = 'RECTANGLE'
        self.center = None
        self.pinArea = []
        self.net = None
        self.width = 0
        self.height = 0
    
    def setShape(self, shape:str):
        self.shape = shape
    
    def setCenter(self, centerPoint:geometryObjects.Point):
        self.center = centerPoint
    
    def getCenter(self) -> geometryObjects.Point:
        return self.center
    
    def setPinArea(self, bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point):
        self.pinArea = [bottomLeftPoint, topRightPoint]
    
    def setNet(self, netName:str):
        self.net = netName
    
    def setDimensions(self, width:float, height:float):
        self.width = width
        self.height = height
    
    def calculateArea(self):
        moveVector = [-self.width / 2, -self.height / 2]
        bottomLeftPoint = geometryObjects.Point.translate(self.center, moveVector)
        topRightPoint = geometryObjects.Point.translate(bottomLeftPoint, [self.width, self.height])
        self.setPinArea(bottomLeftPoint, topRightPoint)