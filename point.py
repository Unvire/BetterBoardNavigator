class Point:
    def __init__(self, x:float|int, y:float|int):
        self.x = x
        self.y = y
    
    def __eq__(self, point:'Point'):
        return self.x == point.x and self.y == point.y