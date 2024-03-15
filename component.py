import geometryObjects

class Component:
    def __init__(self, name:str):
        self.name = name
        self.pins = {}
        self.coords = None
        self.side = None
        self.angle = 0
        self.package = []
        self.packageType = 'SMT'

    def addPin(self, pin:str, point:geometryObjects.Point, netName:str):
        self.pins[pin] = {'netName': netName, 'point':point}
    
    def setCoords(self, point:geometryObjects.Point):
        self.coords = point
    
    def setSide(self, side:str):
        self.side = side

    def setAngle(self, angle:float):
        self.angle = angle
    
    def setPackage(self, package:str):
        self.package = package
    
    def setPackageType(self, packageType:str):
        self.packageType = packageType
    
    def isCoordsValid(self):
        return self.coords.x and self.coords.y