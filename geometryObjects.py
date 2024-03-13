class Point:
    def __init__(self, x:float|int, y:float|int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point x={self.x}, y={self.y}'

    def __eq__(self, point:'Point'):
        return self.x == point.x and self.y == point.y
    
    def setX(self, x:float):
        self.x = x
    
    def setY(self, y:float):
        self.y = y

    @staticmethod
    def minXY_maxXYCoords(currentMinPoint:'Point', currentMaxPoint:'Point', checkedPoint:'Point') -> ('Point', 'Point'):
        currentMinPoint = Point.minXYCoords(currentMinPoint, checkedPoint)
        currentMaxPoint = Point.minXYCoords(currentMaxPoint, checkedPoint)
        return currentMinPoint, currentMaxPoint

    @staticmethod
    def minXYCoords(currentMinPoint:'Point', checkedPoint:'Point') -> 'Point':
        currentX, currentY = currentMinPoint.x, currentMinPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        minX = min(currentX, checkedX)        
        minY = min(currentY, checkedY)
        currentMinPoint.setX(minX)
        currentMinPoint.setX(minY)
        return currentMinPoint
    
    @staticmethod
    def maxXYCoords(currentMaxPoint:'Point', checkedPoint:'Point') -> 'Point':
        currentX, currentY = currentMaxPoint.x, currentMaxPoint.y
        checkedX, checkedY = checkedPoint.x, checkedPoint.y
        minX = max(currentX, checkedX)        
        minY = max(currentY, checkedY)
        currentMaxPoint.setX(minX)
        currentMaxPoint.setX(minY)
        return currentMaxPoint

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

if __name__ == '__main__':
    A = Point(0, 0)
    print(A)
    print(A.__str__())