import geometryObjects as gobj
import pin

class Component:
    def __init__(self, name:str):
        self.name = name
        self.pins = {}
        self.coords = None
        self.side = None
        self.angle = 0
        self.partNumber = None
        self.componentArea = []
        self.packageType = 'SMT'
    
    def __str__(self):
        remark = f'Component={self.name}, coords={self.coords}, side={self.side}, numOfPins={len(self.pins)}'
        return remark

    def addPin(self, pinName:str, pin:pin.Pin):
        self.pins[pinName] = pin
    
    def setCoords(self, point:gobj.Point):
        self.coords = point
    
    def setSide(self, side:str):
        self.side = side

    def setAngle(self, angle:float):
        self.angle = angle

    def setPartNumber(self, partNumber:str):
        self.partNumber = partNumber
    
    def setComponentArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.componentArea = [bottomLeftPoint, topRightPoint]
    
    def setPackageType(self, packageType:str):
        self.packageType = packageType
    
    def isCoordsValid(self):
        return bool(self.coords.x and self.coords.y)
    
    def calculateCenterFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()
        xCenter = bottomLeftPoint.x + round((topRightPoint.x - bottomLeftPoint.x) / 2, 3)
        yCenter = bottomLeftPoint.y + round((topRightPoint.y - bottomLeftPoint.y) / 2, 3)
        center = gobj.Point(xCenter, yCenter)
        self.setCoords(center)
    
    def calculatePackageFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()        
        bottomLeftPoint = gobj.Point.scale(bottomLeftPoint, 0.95)
        topRightPoint = gobj.Point.scale(topRightPoint, 0.95)

        x1, y1 = bottomLeftPoint.x, bottomLeftPoint.y
        x2, y2 = topRightPoint.x, topRightPoint.y
        if round(x2 - x1, 3) == 0:
            moveDistance = round((y2 - y1) * 0.1, 3)
            bottomLeftPoint.x = x1 - moveDistance
            topRightPoint.x = x2 + moveDistance
        if round(y2 - y1, 3) == 0:
            moveDistance = round((x2 - x1) * 0.1, 3)
            bottomLeftPoint.y = y1 - moveDistance
            topRightPoint.y = y2 + moveDistance

        self.setComponentArea(bottomLeftPoint, topRightPoint)

    def calculateHitBoxFromPins(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint = gobj.Point(float('Inf'), float('Inf'))
        topRightPoint = gobj.Point(float('-Inf'), float('-Inf'))
        for pin in self.pins:
            centerPoint = self.pins[pin].getCoords()
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, centerPoint)
        return bottomLeftPoint, topRightPoint

    