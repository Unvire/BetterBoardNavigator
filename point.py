class Point:
    def __init__(self, x:float|int, y:float|int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point x={self.x}, y={self.y}'

    def __eq__(self, point:'Point'):
        return self.x == point.x and self.y == point.y

if __name__ == '__main__':
    A = Point(0, 0)
    print(A)
    print(A.__str__())