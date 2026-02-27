import math

class Point:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def distance_to(self, other: "Point") -> float:
        if not isinstance(other, Point):
            raise TypeError("Error expecting an object of type Point")
        return math.hypot(self.x - other.x, self.y - other.y)

    def midpoint_to(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            raise TypeError("Error expecting an object of type Point")
        return Point(
            (self.x + other.x) / 2,
            (self.y + other.y) / 2
        )

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


