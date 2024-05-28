import geometryObjects as gobj
from abstractShape import Shape
import pin

class Component(Shape):
    def __init__(self, name:str):        
        super().__init__(name)
        self.pins = {}
        self.side = None
        self.angle = 0
        self.mountingType = 'SMT'
    
    def __str__(self):
        remark = f'Component={self.name}, coords={self.coords}, side={self.side}, numOfPins={len(self.pins)}'
        return remark

    def addPin(self, pinName:str, pin:pin.Pin):
        self.pins[pinName] = pin
    
    def getPinByName(self, pinName:str) -> pin.Pin|None:
        return self.pins.get(pinName, None)
    
    def getPins(self) -> dict:
        return self.pins

    def getCoordsAsTranslationVector(self):
        return self.coords.getXY()
    
    def setSide(self, side:str):
        self.side = side
    
    def getSide(self) -> str:
        return self.side

    def setAngle(self, angle:float):
        self.angle = angle

    def getAngle(self):
        return self.angle
    
    def setMountingType(self, mountingType:str):
        self.mountingType = mountingType.upper()
    
    def getMountingType(self):
        return self.mountingType
    
    def calculateCenterFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()
        xCenter = bottomLeftPoint.x + round((topRightPoint.x - bottomLeftPoint.x) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = bottomLeftPoint.y + round((topRightPoint.y - bottomLeftPoint.y) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        center = gobj.Point(xCenter, yCenter)
        self.setCoords(center)
    
    def calculateAreaFromPins(self):
        bottomLeftPoint, topRightPoint = self.calculateHitBoxFromPins()        
        areaWidth, areaHeight = Shape.getAreaWidthHeight((bottomLeftPoint, topRightPoint))
        
        areaWidth *= 0.03
        areaHeight *= 0.03
        bottomLeftPoint, topRightPoint = self._makeAreaNotLinear(bottomLeftPoint, topRightPoint)
        bottomLeftPoint.translateInPlace([-areaWidth, -areaHeight])
        topRightPoint.translateInPlace([areaWidth, areaHeight])

        self.setArea(bottomLeftPoint, topRightPoint)
    
    def _makeAreaNotLinear(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Point, gobj.Point]:
        x1, y1 = bottomLeftPoint.getXY()
        x2, y2 = topRightPoint.getXY()
        if round(x2 - x1, gobj.Point.DECIMAL_POINT_PRECISION) == 0:
            moveDistance = round((y2 - y1) * 0.1, gobj.Point.DECIMAL_POINT_PRECISION)
            bottomLeftPoint.translateInPlace([-moveDistance, 0])
            topRightPoint.translateInPlace([moveDistance, 0])
        elif round(y2 - y1, gobj.Point.DECIMAL_POINT_PRECISION) == 0:
            moveDistance = round((x2 - x1) * 0.1, gobj.Point.DECIMAL_POINT_PRECISION)
            bottomLeftPoint.translateInPlace([0, -moveDistance])
            topRightPoint.translateInPlace([0, moveDistance])
        return bottomLeftPoint, topRightPoint

    def calculateHitBoxFromPins(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for pin in self.pins:
            centerPoint = self.pins[pin].getCoords()
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, centerPoint)
        return bottomLeftPoint, topRightPoint
    
    def rotateInPlaceAroundCoords(self, angleDeg:float|int, isRotatePins:bool=True):
        rotationPoint = self.getCoords()
        self.rotateInPlace(rotationPoint, angleDeg, isRotatePins)

    def rotateInPlace(self, rotationPoint:gobj.Point, angleDeg:float|int, isRotatePins:bool=True):
        super().rotateInPlace(rotationPoint, angleDeg)
        if isRotatePins:
            self.rotatePinsAroundCoords(rotationPoint, angleDeg)
        self.normalizeAndSetArea(self.getArea() + self.getShapePoints())
    
    def rotatePinsAroundCoords(self, rotationPoint:gobj.Point, angleDeg:float|int):
        for _, pinInstance in self.pins.items():
                pinInstance.rotateInPlace(rotationPoint, angleDeg)
    
    def translateInPlace(self, vector:list[int|float, int|float]):
        super().translateInPlace(vector)
        self.translatePinsInPlace(vector)
    
    def translatePinsInPlace(self, vector:list[int|float, int|float]):
        for _, pinInstance in self.pins.items():
            pinInstance.translateInPlace(vector)
    
    def scaleInPlace(self, scaleFactor: float):
        super().scaleInPlace(scaleFactor)
        self._scalePinsInPlace(scaleFactor)
    
    def _scalePinsInPlace(self, scaleFactor:float):        
        for _, pinInstance in self.pins.items():
                pinInstance.scaleInPlace(scaleFactor)