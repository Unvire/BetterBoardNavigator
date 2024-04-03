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
        self.mountingType = 'SMT'
    
    def __str__(self):
        remark = f'Component={self.name}, coords={self.coords}, side={self.side}, numOfPins={len(self.pins)}'
        return remark

    def addPin(self, pinName:str, pin:pin.Pin):
        self.pins[pinName] = pin
    
    def setCoords(self, point:gobj.Point):
        self.coords = point
    
    def getCoords(self):
        return self.coords
    
    def setSide(self, side:str):
        self.side = side

    def setAngle(self, angle:float):
        self.angle = angle

    def getAngle(self):
        return self.angle
    
    def setComponentArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.componentArea = [bottomLeftPoint, topRightPoint]
    
    def getComponentArea(self):
        return self.componentArea
    
    def setMountingType(self, mountingType:str):
        self.mountingType = mountingType
    
    def getMountingType(self):
        return self.mountingType
    
    def isCoordsValid(self):
        return bool(self.coords.x and self.coords.y)
    
    def calculateCenterFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()
        xCenter = bottomLeftPoint.x + round((topRightPoint.x - bottomLeftPoint.x) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = bottomLeftPoint.y + round((topRightPoint.y - bottomLeftPoint.y) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        center = gobj.Point(xCenter, yCenter)
        self.setCoords(center)
    
    def calculatePackageFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()        
        bottomLeftPoint.scaleInPlace(0.95)
        topRightPoint.scaleInPlace(0.95)

        x1, y1 = bottomLeftPoint.x, bottomLeftPoint.y
        x2, y2 = topRightPoint.x, topRightPoint.y
        if round(x2 - x1, 3) == 0:
            moveDistance = round((y2 - y1) * 0.1, gobj.Point.DECIMAL_POINT_PRECISION)
            bottomLeftPoint.x = x1 - moveDistance
            topRightPoint.x = x2 + moveDistance
        if round(y2 - y1, 3) == 0:
            moveDistance = round((x2 - x1) * 0.1, gobj.Point.DECIMAL_POINT_PRECISION)
            bottomLeftPoint.y = y1 - moveDistance
            topRightPoint.y = y2 + moveDistance

        self.setComponentArea(bottomLeftPoint, topRightPoint)

    def calculateHitBoxFromPins(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for pin in self.pins:
            centerPoint = self.pins[pin].getCoords()
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, centerPoint)
        return bottomLeftPoint, topRightPoint

    