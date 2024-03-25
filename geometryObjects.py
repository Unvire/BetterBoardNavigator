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

    @staticmethod
    def minXY_maxXYCoords(currentMinPoint:'Point', currentMaxPoint:'Point', checkedPoint:'Point') -> ('Point', 'Point'):
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
        return f'Line: start point=({self.startPoint}), end point=({self.endPoint}), rotation point=({self.rotationPoint})'
    
    def __eq__(self, arc:'Arc'):
        return self.rotationPoint == arc.rotationPoint and self.startPoint == arc.startPoint and self.endPoint == arc.endPoint

def floatOrNone(x:str):
    try:
        x = float(x)
    except ValueError:
        x = None
    return x    

if __name__ == '__main__':
    A = Point(0, 0)
    print(A)
    print(A.__str__())