import geometryObjects as gobj

class Shape():
    def __init__(self, name:str):
        self.name = name
        self.shape = 'RECT'
        self.coords = None
        self.area = []
    
    def setShape(self, shape:str):
        self.shape = shape

    def getShape(self) -> str:
        return self.shape
    
    def setCoords(self, coords:gobj.Point):
        self.coords = coords
    
    def getCoords(self) -> gobj.Point:
        return self.coords
    
    def setArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.area = [bottomLeftPoint, topRightPoint]
    
    def getArea(self):
        return self.area
    
    def getCoordsAsTranslationVector(self):
        return [self.coords.getX(), self.coords.getY()]
    
    def isCoordsValid(self):
        return bool(self.coords.x and self.coords.y)

    def setDimensions(self, width:float, height:float):
        self.width = width
        self.height = height  
    
    def calculateAreaFromWidthHeightCoords(self):
        moveVector = [-self.width / 2, -self.height / 2]
        bottomLeftPoint = gobj.Point.translate(self.coords, moveVector)
        topRightPoint = gobj.Point.translate(bottomLeftPoint, [self.width, self.height])
        self.setArea(bottomLeftPoint, topRightPoint)
    
    def calculateCenterDimensionsFromArea(self):
        self._calculateCenterFromArea()
        self._calculateDimensionsFromArea()
    
    def _calculateDimensionsFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        width = round(topRightPoint.getX() - bottomLeftPoint.getX(), gobj.Point.DECIMAL_POINT_PRECISION)
        height = round(topRightPoint.getY() - bottomLeftPoint.getY(), gobj.Point.DECIMAL_POINT_PRECISION)
        self.setDimensions(width, height)
    
    def _calculateCenterFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        xCenter = round((topRightPoint.getX() + bottomLeftPoint.getX()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = round((topRightPoint.getY() + bottomLeftPoint.getY()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        self.setCoords(gobj.Point(xCenter, yCenter))
    
    def _calculateCenterFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        xCenter = round((topRightPoint.getX() + bottomLeftPoint.getX()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = round((topRightPoint.getY() + bottomLeftPoint.getY()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        self.setCoords(gobj.Point(xCenter, yCenter))
    
    def _calculateDimensionsFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        width = round(topRightPoint.getX() - bottomLeftPoint.getX(), gobj.Point.DECIMAL_POINT_PRECISION)
        height = round(topRightPoint.getY() - bottomLeftPoint.getY(), gobj.Point.DECIMAL_POINT_PRECISION)
        self.setDimensions(width, height)

    def translateInPlace(self, vector:list[int|float, int|float]):
        self.coords.translateInPlace(vector)
        for point in self.getArea():
            point.translateInPlace(vector)
    
    def rotateInPlace(self, rotationPoint:gobj.Point, angleDeg:int|float):
        self.coords.rotate(rotationPoint, angleDeg)
        for point in self.getArea():
            point.rotate(rotationPoint, angleDeg)
        self._normalizeArea()
    
    def _normalizeArea(self):
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for point in self.getArea():
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        self.setArea(bottomLeftPoint, topRightPoint)
    
