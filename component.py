import geometryObjects

class Component:
    def __init__(self, name:str):
        self.name = name
        self.pins = {}
        self.coords = None
        self.side = None
        self.angle = 0
        self.partNumber = None
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

    def setPartNumber(self, partNumber:str):
        self.partNumber = partNumber
    
    def setPackage(self, bottomLeftPoint:geometryObjects.Point, topRightPoint:geometryObjects.Point):
        self.package = [bottomLeftPoint, topRightPoint]
    
    def setPackageType(self, packageType:str):
        self.packageType = packageType
    
    def isCoordsValid(self):
        return bool(self.coords.x and self.coords.y)
    
    def calculateCenterFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()
        xCenter = bottomLeftPoint.x + (topRightPoint.x - bottomLeftPoint.x) / 2
        yCenter = bottomLeftPoint.y + (topRightPoint.y - bottomLeftPoint.y) / 2
        center = geometryObjects.Point(xCenter, yCenter)
        self.setCoords(center)
    
    def calculatePackageFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()        
        bottomLeftPoint = geometryObjects.Point.scale(bottomLeftPoint, 0.95)
        topRightPoint = geometryObjects.Point.scale(topRightPoint, 0.95)

        x1, y1 = bottomLeftPoint.x, bottomLeftPoint.y1
        x2, y2 = topRightPoint.x, topRightPoint.y1
        if round(x2 - x1, 3) == 0:
            moveDistance = (y2 - y1) * 0.1
            bottomLeftPoint.x = x1 - moveDistance
            topRightPoint.x = x2 + moveDistance
        if round(y2 - y1, 3) == 0:
            moveDistance = (x2 - x1) * 0.1
            bottomLeftPoint.y = y1 - moveDistance
            topRightPoint.y = y2 + moveDistance

        self.setPackage(bottomLeftPoint, topRightPoint)

    def calculateHitBoxFromPins(self) -> (geometryObjects.Point, geometryObjects.Point):
        bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
        topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
        for pin in self.pins:
            pinPoint = self.pins[pin]['point']
            bottomLeftPoint, topRightPoint = geometryObjects.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, pinPoint)
        return bottomLeftPoint, topRightPoint

    