from turtle import distance
from material import Material
from vector import *
from intersect import *


class Box(object):
    def __init__(self, minbox, maxbox, material):
        self.minbox = minbox
        self.maxbox = maxbox
        self.material = material

    def ray_intersect(self, origin, direction):
        norm = V3(1, 0, 0)
        self.bounds = [self.minbox, self.maxbox]
        invdir = direction.inverse()
        sign = V3(int(invdir.x < 0), int(invdir.y < 0), int(invdir.z < 0))
        txmin = (self.bounds[sign.x].x - origin.x) * invdir.x
        txmax = (self.bounds[1 - sign.x].x - origin.x) * invdir.x
        tymin = (self.bounds[sign.y].y - origin.y) * invdir.y
        tymax = (self.bounds[1 - sign.y].y - origin.y) * invdir.y
        a, b, c, d = txmin, txmax, tymin, tymax
        if txmin > tymax or tymin > txmax:
            # print("Adentro", txmin, tymax, tymin, txmax)
            return None
        # print("Afuera", txmin, tymax, tymin, txmax)
        if tymin > txmin:
            txmin = tymin
            norm = V3(0, 1, 0)

        if tymax < txmax:
            txmax = tymax
            norm = V3(0, -1, 0)

        tzmin = (self.bounds[sign.z].z - origin.z) * invdir.z
        tzmax = (self.bounds[1 - sign.z].z - origin.z) * invdir.z
        e, f = tzmin, tzmax
        if txmin > tzmax or tzmin > txmax:
            return None

        if tzmin > tzmin:
            txmin = tzmin
            norm = V3(0, 0, -1)

        if tzmax < txmax:
            txmax = tzmax
            norm = V3(0, 0, 1)
        if txmin <= 0:
            txmin = txmax
            norm = V3(-1, 0, 0)
        if txmin < 0:
            return None

        impact = origin + direction * txmin
        EPSI = 0.01
        if abs(impact.x - a) < EPSI:
            norm = V3(-1, 0, 0)
        elif abs(impact.z - f) < EPSI:
            norm = V3(0, 0, 1)
        elif abs(impact.x - b) < EPSI:
            norm = V3(1, 0, 0)
        elif abs(impact.y - c) < EPSI:
            norm = V3(0, -1, 0)
        elif abs(impact.y - d) < EPSI:
            norm = V3(0, 1, 0)
        elif abs(impact.z - e) < EPSI:
            norm = V3(0, 0, -1)
        return Intersect(distance=txmin, point=impact, normal=V3(0, 0, 1))
