import geometryObjects as gobj 
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
    
    def calculateArea(self):
        moveVector = [-self.width / 2, -self.height / 2]
        bottomLeftPoint = gobj.Point.translate(self.coords, moveVector)
        topRightPoint = gobj.Point.translate(bottomLeftPoint, [self.width, self.height])
        self.setPinArea(bottomLeftPoint, topRightPoint)
    
    def calculateCenterDimensionsFromArea(self):
        self._calculateCenterFromArea()
        self._calculateDimensionsFromArea()
    
    def _calculateCenterFromArea(self):
        bottomLeftPoint, topRightPoint = self.pinArea
        xCenter = round((topRightPoint.getX() + bottomLeftPoint.getX()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = round((topRightPoint.getY() + bottomLeftPoint.getY()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        self.setCoords(gobj.Point(xCenter, yCenter))
    
    def _calculateDimensionsFromArea(self):
        bottomLeftPoint, topRightPoint = self.pinArea
        width = round(topRightPoint.getX() - bottomLeftPoint.getX(), gobj.Point.DECIMAL_POINT_PRECISION)
        height = round(topRightPoint.getY() - bottomLeftPoint.getY(), gobj.Point.DECIMAL_POINT_PRECISION)
        self.setDimensions(width, height)
    
    def translateInPlace(self, vector:list[int|float, int|float]):
        self.coords.translateInPlace(vector)
        p1, p2 = self.getPinArea()
        p1.translateInPlace(vector)
        p2.translateInPlace(vector)

    def rotateInPlace(self, rotationPoint:gobj.Point, angleDeg:int|float):
        self.coords.rotate(rotationPoint, angleDeg)
        for point in self.getPinArea():
            point.rotate(rotationPoint, angleDeg)
        self._normalizePinArea()