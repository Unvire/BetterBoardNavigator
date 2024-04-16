import math

class Point:
    DECIMAL_POINT_PRECISION = 3
    def __init__(self, x:float|int, y:float|int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point x={self.x}, y={self.y}'

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
    
    def rotate(self, rotationPoint:'Point', angleDeg:float):
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


class Line:
    def __init__(self, startPoint:Point, endPoint:Point):
        self.startPoint = startPoint
        self.endPoint = endPoint
    
    def __str__(self):
        return f'Line: point1=({self.startPoint}), point2=({self.endPoint})'
    
    def __eq__(self, line:'Line'):
        result1 = self.startPoint == line.startPoint and self.endPoint == line.endPoint
        result2 = self.startPoint == line.endPoint and self.endPoint == line.startPoint
        return result1 or result2

class Arc:
    def __init__(self, startPoint:Point, endPoint:Point, rotationPoint:Point):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.rotationPoint = rotationPoint
    
    def __str__(self):
        return f'Arc: start point=({self.startPoint}), end point=({self.endPoint}), rotation point=({self.rotationPoint})'
    
    def __eq__(self, arc:'Arc'):
        return self.rotationPoint == arc.rotationPoint and self.startPoint == arc.startPoint and self.endPoint == arc.endPoint

class Circle:
    def __init__(self, centerPoint:Point, radius:float):
        self.centerPoint = centerPoint
        self.radius = radius
    
    def __str__(self):
        return f'Circle: center point=({self.centerPoint}), radius=({self.radius})'
    
    def __eq__(self, circle:'Circle'):
        return self.radius == circle.radius and self.centerPoint == circle.centerPoint

    def getPoints(self) -> list[Point]:
        ''' [centerPoint] ''' 
        return [self.centerPoint]
    
class Rectangle:
    def __init__(self, bottomLeftPoint:Point, topRightPoint:Point):
        self.bottomLeftPoint = bottomLeftPoint
        self.topRightPoint = topRightPoint
        xBL, yBL = self.bottomLeftPoint.getXY()
        xTR, yTR = self.topRightPoint.getXY()
        self.bottomRightPoint = Point(xTR, yBL)
        self.topLeftPoint = Point(xBL, yTR)
    
    def __str__(self):
        return f'Rectangle: bottom-left point=({self.bottomLeftPoint}), top-right point=({self.topRightPoint})'
    
    def __eq__(self, rectangle:'Rectangle'):
        bottomLeftEqual = self.bottomLeftPoint == rectangle.bottomLeftPoint
        bottomRightEqual = self.bottomRightPoint == rectangle.bottomRightPoint
        topLeftEqual = self.topLeftPoint == rectangle.topLeftPoint
        topRightEqual = self.topRightPoint == rectangle.topRightPoint 
        return bottomLeftEqual and bottomRightEqual and topLeftEqual and topRightEqual

    def getPoints(self) -> list[Point, Point, Point, Point]:
        ''' [bottomLeftPoint, bottomRightPoint, topRightPoint, topLeftPoint] '''
        return [self.bottomLeftPoint, self.bottomRightPoint, self.topRightPoint, self.topLeftPoint]
    
def floatOrNone(x:str):
    try:
        x = float(x)
    except ValueError:
        x = None
    return x    

def getDefaultBottomLeftTopRightPoints() -> tuple[Point, Point]:
    bottomLeftPoint = Point(float('Inf'), float('Inf'))
    topRightPoint = Point(float('-Inf'), float('-Inf'))
    return bottomLeftPoint, topRightPoint

def updatebottomLeftTopRightPoints(bottomLeftTopRightPoints:tuple[Point, Point],  checkedPoints:list[Point]) -> tuple[Point, Point]:
        bottomLeftPoint, topRightPoint = bottomLeftTopRightPoints
        for point in checkedPoints:
            bottomLeftPoint, topRightPoint = Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint

if __name__ == '__main__':
    A = Point(0, 0)
    print(A)
    print(A.__str__())