import geometryObjects as gobj 

class Pin:
    def __init__(self, name:str):
        self.name = name
        self.shape = 'RECTANGLE'
        self.coords = None
        self.pinArea = []
        self.net = None
        self.width = 0
        self.height = 0
    
    def __str__(self):
        remark = f'Pad shape={self.shape}, coords={self.coords}, dimensions=[{self.width}, {self.height}]'
        return remark
    
    def setShape(self, shape:str):
        self.shape = shape
    
    def setCoords(self, coords:gobj.Point):
        self.coords = coords
    
    def getCoords(self) -> gobj.Point:
        return self.coords
    
    def setPinArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.pinArea = [bottomLeftPoint, topRightPoint]
    
    def getPinArea(self):
        return self.pinArea
    
    def setNet(self, netName:str):
        self.net = netName
    
    def setDimensions(self, width:float, height:float):
        self.width = width
        self.height = height
    
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
        self.pinArea = [point.translate(vector) for point in self.pinArea]