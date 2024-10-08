import geometryObjects as gobj
import copy

class Shape():
    def __init__(self, name:str):
        self.name = name
        self.shape = 'RECT'
        self.shapeData = None
        self.coords = None
        self.area = []
    
    def setShape(self, shape:str):
        self.shape = shape

    def getShape(self) -> str:
        return self.shape
    
    def caluclateShapeData(self):
        bottomLeftPoint, topRightPoint = copy.deepcopy(self.area)
  
        if self.shape == 'CIRCLE':
            xBL, yBL = bottomLeftPoint.getXY()
            xTR, yTR = topRightPoint.getXY()
            radius = (xTR - xBL) / 2
            centerPoint = gobj.Point((xBL + xTR) / 2, (yBL + yTR) / 2)
            self.shapeData = gobj.Circle(centerPoint, radius)
        else:
            self.shapeData = gobj.Rectangle(bottomLeftPoint, topRightPoint)
    
    def getShapeData(self) -> gobj.Rectangle|gobj.Circle:
        return self.shapeData
    
    def getShapePoints(self) -> tuple[gobj.Point]:
        return self.shapeData.getPoints()
    
    def getShapeDataAsXYsList(self) -> list[tuple[int|float]]:
        pointList = self.getShapePoints()
        result = []
        for point in pointList:
            result.append(point.getXY())
        return result
    
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
    
    def makeAreaNotLinear(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point) -> tuple[gobj.Point, gobj.Point]:
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
    
    def calculateAreaFromWidthHeightCoords(self):
        moveVector = [-self.width / 2, -self.height / 2]
        bottomLeftPoint = gobj.Point.translate(self.coords, moveVector)
        topRightPoint = gobj.Point.translate(bottomLeftPoint, [self.width, self.height])
        self.setArea(bottomLeftPoint, topRightPoint)
    
    def calculateCenterDimensionsFromArea(self):
        self._calculateCenterFromArea()
        self.calculateDimensionsFromArea()
    
    def calculateDimensionsFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        width = round(topRightPoint.getX() - bottomLeftPoint.getX(), gobj.Point.DECIMAL_POINT_PRECISION)
        height = round(topRightPoint.getY() - bottomLeftPoint.getY(), gobj.Point.DECIMAL_POINT_PRECISION)
        self.setDimensions(width, height)
    
    def _calculateCenterFromArea(self):
        bottomLeftPoint, topRightPoint = self.area
        xCenter = round((topRightPoint.getX() + bottomLeftPoint.getX()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        yCenter = round((topRightPoint.getY() + bottomLeftPoint.getY()) / 2, gobj.Point.DECIMAL_POINT_PRECISION)
        self.setCoords(gobj.Point(xCenter, yCenter))

    def translateInPlace(self, vector:list[int|float, int|float]):
        self.coords.translateInPlace(vector)
        for point in self.shapeData.getPoints():
            point.translateInPlace(vector)

        for point in self.getArea():
            point.translateInPlace(vector)
    
    def rotateInPlaceAroundCoords(self, angleDeg:float|int):
        rotationPoint = self.getCoords()
        self.rotateInPlace(rotationPoint, angleDeg)
    
    def rotateInPlace(self, rotationPoint:gobj.Point, angleDeg:int|float):
        self.coords.rotateInPlace(rotationPoint, angleDeg)
        for point in self.shapeData.getPoints():
            point.rotateInPlace(rotationPoint, angleDeg)
        
        for point in self.getArea():
            point.rotateInPlace(rotationPoint, angleDeg)
        self.normalizeAndSetArea(self.getArea())
    
    def normalizeAndSetArea(self, pointList:list[gobj.Point]):
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for point in pointList:
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        self.setArea(bottomLeftPoint, topRightPoint)
    
    def scaleInPlace(self, scaleFactor:float):
        shapePoints = self.getShapePoints()
        pointList = [self.coords] + self.area + shapePoints
        for point in pointList:
            point.scaleInPlace(scaleFactor)

        if self.shape == 'CIRCLE':
            scaledRadius = self.shapeData.getRadius() * scaleFactor
            self.shapeData.setRadius(scaledRadius)
    
    @staticmethod
    def calculateAreaCenterXY(area:tuple[gobj.Point, gobj.Point]) -> tuple[float|int, float|int]:
        bottomLeftPoint, topRightPoint = area
        xBL, yBL = bottomLeftPoint.getXY()
        xTR, yTR = topRightPoint.getXY()
        xAreaCenter, yAreaCenter = (xBL + xTR) / 2, (yBL + yTR) / 2
        return xAreaCenter, yAreaCenter
    
    @staticmethod
    def getAreaWidthHeight(area:tuple[gobj.Point, gobj.Point]) -> tuple[float, float]:
        x0, y0, x1, y1 = Shape.getAreaAsXYXY(area)
        areaWidth = abs(x1 - x0)
        areaHeight = abs(y1 - y0)
        return areaWidth, areaHeight
    
    @staticmethod
    def getAreaAsXYXY(area:tuple[gobj.Point, gobj.Point]) -> tuple[float, float, float, float]:
        bottomLeftPoint, topRightPoint = area
        xBL, yBL = bottomLeftPoint.getXY()
        xTR, yTR = topRightPoint.getXY()
        return xBL, yBL, xTR, yTR
