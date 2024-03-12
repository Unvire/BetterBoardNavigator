class Point:
    def __init__(self, x:float|int, y:float|int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point x={self.x}, y={self.y}'

    def __eq__(self, point:'Point'):
        return self.x == point.x and self.y == point.y

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