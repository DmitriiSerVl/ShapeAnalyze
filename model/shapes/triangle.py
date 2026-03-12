import math

import numpy as np

from model.point import Point
from model.shape import Shape


class Triangle(Shape):
    def __init__(self, a: Point, b: Point, c: Point):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        a = np.array([self.b.x - self.a.x, self.b.y - self.a.y])
        b = np.array([self.c.x - self.a.x, self.c.y - self.a.y])
        return float(0.5 * abs(np.cross(a, b)))

    def is_valid(self) -> bool:
        if self.a == self.b or self.b == self.c or self.a == self.c:
            return False
        return True

    @property
    def centroid(self) -> Point:
        return Point(
            (self.a.x + self.b.x + self.c.x) / 3.0,
            (self.a.y + self.b.y + self.c.y) / 3.0
        )

    def side_lengths(self):
        a = self.b.distance_to(self.c)
        b = self.c.distance_to(self.a)
        c = self.a.distance_to(self.b)
        return a, b, c

    def angles(self):
        a, b, c = self.side_lengths()

        def clamp(x: float) -> float:
            return max(-1.0, min(1.0, x))

        cos_a = clamp((b * b + c * c - a * a) / (2 * b * c))
        cos_b = clamp((a * a + c * c - b * b) / (2 * a * c))
        cos_c = clamp((a * a + b * b - c * c) / (2 * a * b))

        angle_a = math.acos(cos_a)
        andle_b = math.acos(cos_b)
        angle_c = math.acos(cos_c)

        return f"{angle_a:.2f} {andle_b:.2f} {angle_c:.2f}"