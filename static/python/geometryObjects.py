import math
from abc import ABC, abstractmethod

class Point:
    DECIMAL_POINT_PRECISION = 6
    def __init__(self, x:float|int, y:float|int):
        self.type = 'Point'
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point x={self.x}, y={self.y}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, point:'Point'):
        result1 = round(abs(self.x - point.x), Point.DECIMAL_POINT_PRECISION) <= 10**(-Point.DECIMAL_POINT_PRECISION)
        result2 = round(abs(self.y - point.y), Point.DECIMAL_POINT_PRECISION) <= 10**(-Point.DECIMAL_POINT_PRECISION)
        return result1 and result2
    
    def setX(self, x:float):
        self.x = x
    
    def setY(self, y:float):
        self.y = y
    
    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y
    
    def getXY(self) -> tuple[float, float]:
        return self.x, self.y
    
    def getType(self) -> str:
        return self.type

    def rotateInPlace(self, rotationPoint:'Point', angleDeg:float):
        xMove, yMove = rotationPoint.getX(), rotationPoint.getY()
        angleRad = math.radians(angleDeg)
        
        # translate point as if it was rotated around (0, 0), rotate, undo rotation
        xMoved = self.x - xMove
        yMoved = self.y - yMove
        xRotated = xMoved * math.cos(angleRad) - yMoved * math.sin(angleRad)
        yRotated = xMoved * math.sin(angleRad) + yMoved * math.cos(angleRad)
        self.x = round(xRotated + xMove, Point.DECIMAL_POINT_PRECISION)
        self.y = round(yRotated + yMove, Point.DECIMAL_POINT_PRECISION)
    
    def scaleInPlace(self, coefficient:float):
        self.x = round(self.x * coefficient, Point.DECIMAL_POINT_PRECISION)
        self.y = round(self.y * coefficient, Point.DECIMAL_POINT_PRECISION)
    
    def translateInPlace(self, vector:list[int|float, int|float]):
        xMove, yMove = vector
        self.x = round(self.x + xMove, Point.DECIMAL_POINT_PRECISION)
        self.y = round(self.y + yMove, Point.DECIMAL_POINT_PRECISION)

    @staticmethod
    def minXY_maxXYCoords(currentMinPoint:'Point', currentMaxPoint:'Point', checkedPoint:'Point') -> tuple['Point', 'Point']:
        return Point.minXYCoords(currentMinPoint, checkedPoint), Point.maxXYCoords(currentMaxPoint, checkedPoint)

    @staticmethod
    def minXYCoords(currentMinPoint:'Point', checkedPoint:'Point') -> 'Point':
        currentX, currentY = currentMinPoint.x, currentMinPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        minX = min(currentX, checkedX)        
        minY = min(currentY, checkedY)
        return Point(minX, minY)
    
    @staticmethod
    def maxXYCoords(currentMaxPoint:'Point', checkedPoint:'Point') -> 'Point':
        currentX, currentY = currentMaxPoint.x, currentMaxPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        maxX = max(currentX, checkedX)        
        maxY = max(currentY, checkedY)
        return Point(maxX, maxY)
    
    @staticmethod
    def translate(point:'Point', vector:list[float]) -> 'Point':
        xPoint, yPoint = point.x, point.y
        x, y = vector
        return Point(round(xPoint + x, Point.DECIMAL_POINT_PRECISION), round(yPoint  + y, Point.DECIMAL_POINT_PRECISION))
    
    @staticmethod
    def scale(point:'Point', coefficient:float) -> 'Point':
        xPoint = point.x * coefficient
        yPoint = point.y * coefficient
        return Point(round(xPoint, Point.DECIMAL_POINT_PRECISION), round(yPoint, Point.DECIMAL_POINT_PRECISION))

class AbstractBaseShape(ABC):
    @abstractmethod
    def __eq__(self):
        pass
    
    @abstractmethod
    def getPoints(self):
        pass
    
    def scaleInPlace(self, factor:float|int):
        for point in self.getPoints():
            point.scaleInPlace(factor)
    
    def translateInPlace(self, vector:list[int|float, int|float]):
        for point in self.getPoints():
            point.translateInPlace(vector)
    
    def rotateInPlace(self, rotationPoint:Point, angleDeg:float):
        for point in self.getPoints():
            point.rotateInPlace(rotationPoint, angleDeg)

class Line(AbstractBaseShape):
    def __init__(self, startPoint:Point, endPoint:Point):
        self.type = 'Line'
        self.startPoint = startPoint
        self.endPoint = endPoint
    
    def __str__(self):
        return f'Line: point1=({self.startPoint}), point2=({self.endPoint})'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, line:'Line'):
        result1 = self.startPoint == line.startPoint and self.endPoint == line.endPoint
        result2 = self.startPoint == line.endPoint and self.endPoint == line.startPoint
        return result1 or result2
    
    def getType(self) -> str:
        return self.type

    def getPoints(self) -> tuple[Point, Point]:
        return self.startPoint, self.endPoint
    
    def getPointsAsXYTuple(self) -> tuple['int|float', 'int|float', 'int|float', 'int|float']:
        x0, y0 = self.startPoint.getXY()
        x1, y1 = self.endPoint.getXY()
        return x0, y0, x1, y1

class Arc(AbstractBaseShape):
    def __init__(self, startPoint:Point, endPoint:Point, rotationPoint:Point):
        self.type = 'Arc'
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.rotationPoint = rotationPoint

        self.calculateAngleRadRepresentation()
    
    def __str__(self):
        return f'Arc: start point=({self.startPoint}), end point=({self.endPoint}), rotation point=({self.rotationPoint})'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, arc:'Arc'):
        return self.rotationPoint == arc.rotationPoint and self.startPoint == arc.startPoint and self.endPoint == arc.endPoint
    
    def getType(self) -> str:
        return self.type
    
    def calculateAngleRadRepresentation(self):
        self.radius = self._calculateRadius()
        self.startAngle = self._calculateAngleRad(self.startPoint, self.rotationPoint)        
        self.endAngle = self._calculateAngleRad(self.endPoint, self.rotationPoint)
    
    def _calculateRadius(self) -> float:
        x0, y0 = self.startPoint.getXY()
        xRot, yRot = self.rotationPoint.getXY()
        return math.sqrt((x0 - xRot)**2 + (y0 - yRot)**2)

    def _calculateAngleRad(self, point:Point, referencePoint:Point) -> float:
        xVector, yVector = referencePoint.getXY()
        x, y = point.getX() - xVector, point.getY() - yVector
        angle = math.atan2(y, x)
        if angle < 0:
            angle += math.pi * 2
        return angle
    
    def getAsCenterRadiusAngles(self) -> tuple[Point, float, float, float]:
        return self.rotationPoint, self.radius, self.startAngle, self.endAngle
    
    def getPoints(self) -> tuple[Point, Point, Point]:
        return self.startPoint, self.endPoint, self.rotationPoint
    
    def scaleInPlace(self, factor: float | int):
        super().scaleInPlace(factor)
        self.radius *= factor
    
    def rotateInPlace(self, rotationPoint: Point, angleDeg: float):
        super().rotateInPlace(rotationPoint, angleDeg)
        self.startAngle = self._calculateAngleRad(self.startPoint, self.rotationPoint)        
        self.endAngle = self._calculateAngleRad(self.endPoint, self.rotationPoint)

class Circle(AbstractBaseShape):
    def __init__(self, centerPoint:Point, radius:float):
        self.type = 'Circle'
        self.centerPoint = centerPoint
        self.radius = radius
    
    def __str__(self):
        return f'Circle: center point=({self.centerPoint}), radius=({self.radius})'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, circle:'Circle'):
        return self.radius == circle.radius and self.centerPoint == circle.centerPoint
    
    def setRadius(self, radius:float):
        self.radius = radius
    
    def getRadius(self) -> float:
        return self.radius
    
    def getType(self) -> str:
        return self.type

    def getPoints(self) -> list[Point]:
        ''' [centerPoint] ''' 
        return [self.centerPoint]
    
    def getCenterRadius(self) -> tuple[Point, float]:
        return self.centerPoint, self.radius
    
    def scaleInPlace(self, factor: float | int):
        super().scaleInPlace(factor)
        self.radius *= factor
    
    def checkIfPointInside(self, point:Point):
        TOLERANCE = 1.02
        x, y = point.getXY()
        xCenter, yCenter = self.centerPoint.getXY()
        distanceFromCenter = math.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2)
        return distanceFromCenter <= self.radius * TOLERANCE
    
    def calculateArea(self) -> tuple[Point, Point]:
        x, y = self.centerPoint.getXY()
        return Point(x - self.radius, y - self.radius), Point(x + self.radius, y + self.radius)
    
class Rectangle(AbstractBaseShape):
    def __init__(self, bottomLeftPoint:Point, topRightPoint:Point):
        self.type = 'Rectangle'
        self.bottomLeftPoint = bottomLeftPoint
        self.topRightPoint = topRightPoint
        xBL, yBL = self.bottomLeftPoint.getXY()
        xTR, yTR = self.topRightPoint.getXY()
        self.bottomRightPoint = Point(xTR, yBL)
        self.topLeftPoint = Point(xBL, yTR)
    
    def __str__(self):
        return f'Rectangle: bottom-left point=({self.bottomLeftPoint}), top-right point=({self.topRightPoint})'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, rectangle:'Rectangle'):
        bottomLeftEqual = self.bottomLeftPoint == rectangle.bottomLeftPoint
        bottomRightEqual = self.bottomRightPoint == rectangle.bottomRightPoint
        topLeftEqual = self.topLeftPoint == rectangle.topLeftPoint
        topRightEqual = self.topRightPoint == rectangle.topRightPoint 
        return bottomLeftEqual and bottomRightEqual and topLeftEqual and topRightEqual

    def getPoints(self) -> list[Point, Point, Point, Point]:
        ''' [bottomLeftPoint, bottomRightPoint, topRightPoint, topLeftPoint] '''
        return [self.bottomLeftPoint, self.bottomRightPoint, self.topRightPoint, self.topLeftPoint]

    def checkIfPointInside(self, pointP:Point):
        TOLERANCE = 1.02
        pointA, pointB, pointC, pointD = self.getPoints()
        
        areaRectangle = self._calculateRectangleAreaWith2VectorsABAC(pointB, pointA, pointC)
        areaTriangleABP = self._calculateRectangleAreaWith2VectorsABAC(pointP, pointA, pointB) / 2
        areaTriangleBCP = self._calculateRectangleAreaWith2VectorsABAC(pointP, pointB, pointC) / 2
        areaTriangleCDP = self._calculateRectangleAreaWith2VectorsABAC(pointP, pointC, pointD) / 2
        areaTriangleDAP = self._calculateRectangleAreaWith2VectorsABAC(pointP, pointA, pointD) / 2
        areaTrianglesSum = areaTriangleABP + areaTriangleBCP + areaTriangleCDP + areaTriangleDAP

        return areaTrianglesSum < areaRectangle * TOLERANCE
    
    def _calculateRectangleAreaWith2VectorsABAC(self, pointA:Point, pointB:Point, pointC:Point) -> float:
        xA, yA = pointA.getXY()
        xB, yB = pointB.getXY()
        xC, yC = pointC.getXY()
        
        vectorAB = xB - xA, yB - yA
        vectorAC = xC - xA, yC - yA
        return abs(vectorAB[0] * vectorAC[1] - vectorAB[1] * vectorAC[0])
    
    def calculateArea(self) -> tuple[Point, Point]:
        defaultPoints = getDefaultBottomLeftTopRightPoints()
        pointList = [self.bottomLeftPoint, self.bottomRightPoint, self.topLeftPoint, self.topRightPoint]
        bottomLeftPoint, topRightPoint = updateBottomLeftTopRightPoints(defaultPoints, pointList)
        return bottomLeftPoint, topRightPoint

    
def floatOrNone(x:str) -> float|None:
    try:
        x = float(x)
    except  (TypeError, ValueError):
        x = None
    return x    

def getDefaultBottomLeftTopRightPoints() -> tuple[Point, Point]:
    bottomLeftPoint = Point(float('Inf'), float('Inf'))
    topRightPoint = Point(float('-Inf'), float('-Inf'))
    return bottomLeftPoint, topRightPoint

def updateBottomLeftTopRightPoints(bottomLeftTopRightPoints:tuple[Point, Point],  checkedPoints:list[Point]) -> tuple[Point, Point]:
        bottomLeftPoint, topRightPoint = bottomLeftTopRightPoints
        for point in checkedPoints:
            bottomLeftPoint, topRightPoint = Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint

def getLineAndAreaFromNumArray(nums:list[str|float], bottomLeftPoint:Point, topRightPoint:Point) -> tuple[Line, Point, Point]:
        x0, y0, x1, y1 = [floatOrNone(val) for val in nums]
        startPoint = Point(x0, y0)
        endPoint = Point(x1, y1)

        checkedPoints = [startPoint, endPoint]
        bottomLeftPoint, topRightPoint = updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)

        lineInstance = Line(startPoint, endPoint)
        return lineInstance, bottomLeftPoint, topRightPoint

def getArcAndAreaFromValArray(nums:list[str|float], bottomLeftPoint:Point, topRightPoint:Point) -> tuple[Arc, Point, Point]:
    x0, y0, x1, y1, xCenter, yCenter = [floatOrNone(val) for val in nums]
    startPoint = Point(x0, y0)
    endPoint = Point(x1, y1)
    centerPoint = Point(xCenter, yCenter)

    checkedPoints = [startPoint, endPoint, centerPoint]
    bottomLeftPoint, topRightPoint = updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)

    arcInstance = Arc(startPoint, endPoint, centerPoint)
    return arcInstance, bottomLeftPoint, topRightPoint

def getRectangleAndAreaFromValArray(nums:list[str|float], bottomLeftPoint:Point, topRightPoint:Point) -> tuple[Rectangle, Point, Point]:
    x, y, width, height = [floatOrNone(val) for val in nums]
    rectangleBottomLeftPoint = Point(x, y)
    rectangleTopLeftPoint = Point(x + width, y + height)

    checkedPoints = [rectangleBottomLeftPoint, rectangleTopLeftPoint]
    bottomLeftPoint, topRightPoint = updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)

    rectangleInstance = Rectangle(rectangleBottomLeftPoint, rectangleTopLeftPoint)
    return rectangleInstance, bottomLeftPoint, topRightPoint

def getCircleAndAreaFromValArray(nums:list[str|float], bottomLeftPoint:Point, topRightPoint:Point) -> tuple[Circle, Point, Point]:
    x, y, radius = [floatOrNone(val) for val in nums]
    circleBottomLeftPoint = Point(x - radius, y - radius)
    circleTopRightPoint = Point(x + radius, y + radius)

    checkedPoints = [circleBottomLeftPoint, circleTopRightPoint]
    bottomLeftPoint, topRightPoint = updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], checkedPoints)

    centerPoint = Point(x, y)
    circleInstance = Circle(centerPoint, radius)
    return circleInstance, bottomLeftPoint, topRightPoint

def getSquareAndAreaFromValArray(nums:list[str|float], bottomLeftPoint:Point, topRightPoint:Point) -> tuple[Rectangle, Point, Point]:
    x, y, halfWidth = [floatOrNone(val) for val in nums]
    return getRectangleAndAreaFromValArray([x, y, 2 * halfWidth, 2 * halfWidth], bottomLeftPoint, topRightPoint)

if __name__ == '__main__':
    A = Point(0, 0)
    print(A)
    print(A.__str__())