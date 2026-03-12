from abc import ABC

from numpy import atan2, hypot

from model.point import Point
# from model.shape import Shape


class Polygon():
    def __init__(self, a: Point, b: Point, c: Point, d: Point):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def order_points(self, points: list[Point]) -> list[Point]:
        """Order points around centroid to form a non-self-intersecting contour."""
        cx = sum(p.x for p in points) / len(points)
        cy = sum(p.y for p in points) / len(points)
        return sorted(points, key=lambda p: atan2(p.y - cy, p.x - cx))

    # , p1: Point, p2: Point, p3: Point, p4: Point
    def area(self) -> float:
        pts = self.order_points([self.b, self.b, self.c, self.d])
        s = 0.0
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            s += pts[i].x * pts[j].y - pts[j].x * pts[i].y
        return abs(s) / 2.0

    #  p1: Point, p2: Point, p3: Point, p4: Point
    def perimeter(self) -> float:
        pts = self.order_points([self.b, self.b, self.c, self.d])
        per = 0.0
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            per += hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y)
        return per