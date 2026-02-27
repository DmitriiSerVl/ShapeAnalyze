import math

from model.point import Point
from shape import Shape
import numpy as np

class Triangle(Shape):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def area(self) -> float:
        a = np.array([self.p2.x - self.p1.x, self.p2.y - self.p1.y])
        b = np.array([self.p3.x - self.p1.x, self.p3.y - self.p1.y])
        return float(0.5 * abs(np.cross(a, b)))

    def is_valid(self) -> bool:
        if self.p1 == self.p2 or self.p2 == self.p3 or self.p1 == self.p3:
            return False
        return True

    @property
    def centroid(self) -> Point:
        return Point(
            (self.p1.x + self.p2.x + self.p3.x) / 3.0,
            (self.p1.y + self.p2.y + self.p3.y) / 3.0
        )

    def _side_lengths(self):
        a = self.p2.distance_to(self.p3)
        b = self.p3.distance_to(self.p1)
        c = self.p1.distance_to(self.p2)
        return a, b, c

    def angles(self):
        a, b, c = self._side_lengths()

        def clamp(x: float) -> float:
            return max(-1.0, min(1.0, x))

        cosA = clamp((b * b + c * c - a * a) / (2 * b * c))
        cosB = clamp((a * a + c * c - b * b) / (2 * a * c))
        cosC = clamp((a * a + b * b - c * c) / (2 * a * b))

        A = math.acos(cosA)
        B = math.acos(cosB)
        C = math.acos(cosC)

        return (A, B, C)






