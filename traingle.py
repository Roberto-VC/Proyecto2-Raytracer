from tkinter.font import NORMAL
from material import Material
from vector import *
from intersect import *


class Traingle(object):
    def __init__(self, a, b, c, material):
        self.a = a
        self.b = b
        self.c = c
        self.material = material

    def ray_intersect(self, origin, direction):
        ca = self.c - self.a
        ba = self.b - self.a
        normal = (ca * ba).normalize()
        t = normal @ self.a

        d = direction @ normal

        if d == 0:
            return None
        else:
            n = normal @ (origin + (normal * d) * -1)
            dist = -1 * n / d
            impact = (direction * dist) + origin
            ca = self.c - self.a
            qa = impact - self.a

            bc = self.b - self.c
            qc = impact - self.c

            ab = self.a - self.b
            qb = impact - self.b

            inside = (
                (ca * qa) @ normal >= 0
                and (bc * qc) @ normal >= 0
                and (ab * qb) @ normal >= 0
            )
            if t < 0:
                normal *= -1
            if inside:
                return Intersect(distance=t, point=impact, normal=normal)
            else:
                return None
