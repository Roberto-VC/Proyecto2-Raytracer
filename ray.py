from audioop import reverse
from code import interact
from re import A
from turtle import back
from gl import *
from vector import *
from sphere import *
from intersect import *
from light import *
from material import *
from plane import *
from box import *
from traingle import *


def reflect(I, N):
    return (I - N * 2 * (N @ I)).normalize()


def refract(I, N, roi):
    etai = 1
    etat = roi
    cos1 = -max(-1, min(1, I @ N))
    if cos1 < 0:
        cos1 = cos1 * -1
        etai, etat = etat, etai
        N = N * -1
    eta = etai / etat
    k = 1 - eta**2 * (1 - cos1**2)
    if k < 0:
        return V3(1, 0, 0)

    cost = k ** (1 / 2)

    return ((I * eta) + (N * (eta * cos1 - cost))).normalize()


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spheres = [
            # Sphere(
            #   V3(-1.0, 0, -12),
            #  1,
            #  Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2, 0, 0], spec=0),
            # ),
            # Sphere(
            #    V3(1.0, 0, -12),
            #    1,
            #    Material(diffuse=(210, 125, 45), albedo=[0.95, 0.30, 0, 0], spec=10),
            # ),
            # Sphere(
            #    V3(0, -2, -12),
            #    1,
            #    Material(diffuse=(255, 255, 255), albedo=[0, 1, 0.8, 0], spec=1425),
            # ),
            # Sphere(
            #    V3(0, 0, -9),
            #    0.5,
            #    Material(
            #        diffuse=(150, 180, 200),
            #        albedo=[0, 0.5, 0.1, 0.8],
            #        spec=125,
            #        refractive_index=1.8,
            #    ),
            # ),
            # Box(
            # V3(-10, -10, -8),
            #  V3(-2, -2, -12),
            #   Material(diffuse=(255, 0, 45), albedo=[0.95, 0.30, 0, 0], spec=10),
            # ),
            Box(
                V3(-7, 1.5, -6),
                V3(7, 5, -6),
                Material(diffuse=(56, 255, 23), albedo=[0.5, 0.30, 0, 0], spec=100),
            ),
            # Box(
            #    V3(-10, -10, -15),
            #    V3(10, 10, -15),
            #    Material(diffuse=(225, 246, 255), albedo=[0.95, 0.30, 0, 0], spec=1000),
            # ),
            Plane(
                V3(-0.5, 2.5, -7),
                1,
                1,
                Material(
                    diffuse=(255, 255, 255),
                    albedo=[5, 1, 0, 0],
                    spec=100,
                ),
            ),
            Plane(
                V3(0, 3, -7),
                1,
                1,
                Material(
                    diffuse=(255, 255, 255),
                    albedo=[5, 1, 0, 0],
                    spec=100,
                ),
            ),
            Plane(
                V3(2, 3.2, -7),
                1,
                1,
                Material(
                    diffuse=(255, 255, 255),
                    albedo=[5, 1, 0, 0],
                    spec=100,
                ),
            ),
            Plane(
                V3(2, 2.8, -7),
                1,
                1,
                Material(
                    diffuse=(255, 255, 255),
                    albedo=[5, 1, 0, 0],
                    spec=100,
                ),
            ),
            Plane(
                V3(0, 2, -7),
                1,
                1,
                Material(
                    diffuse=(255, 255, 255),
                    albedo=[5, 1, 0, 0],
                    spec=100,
                ),
            ),
            Box(
                V3(3, -2, -14),
                V3(5, 4.5, -14),
                Material(
                    diffuse=(225, 225, 225),
                    albedo=[0.5, 0.50, 0, 0],
                    spec=100,
                ),
            ),
            Box(
                V3(5, -1, -14),
                V3(7, 4.5, -14),
                Material(
                    diffuse=(225, 225, 225),
                    albedo=[0.5, 0.50, 0, 0],
                    spec=100,
                ),
            ),
            Box(
                V3(4, -1, -12),
                V3(5, 4.5, -12),
                Material(
                    diffuse=(0, 20, 225),
                    albedo=[0.5, 0.50, 0.1, 0.5],
                    spec=100,
                    refractive_index=1.3,
                ),
            ),
            Plane(
                V3(1.25, -0.825, -3),
                1,
                0.75,
                Material(
                    diffuse=(0, 20, 255),
                    albedo=[0.5, 0.60, 0.1, 0.5],
                    spec=10,
                    refractive_index=1.3,
                ),
            ),
            Box(
                V3(-7, 1, -6),
                V3(-1, 1.5, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.95, 0.30, 0, 0], spec=100),
            ),
            Box(
                V3(-4, 0.5, -6),
                V3(-2.5, 1, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.95, 0.30, 0, 0], spec=100),
            ),
            Box(
                V3(-2.5, 0.5, -6),
                V3(-1.5, 1, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.6, 0.30, 0, 0], spec=100),
            ),
            Box(
                V3(-4, 0, -6),
                V3(-2, 0.5, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.6, 0.30, 0, 0], spec=100),
            ),
            Box(
                V3(-2, 0, -6),
                V3(-1.75, 0.5, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.3, 0.30, 0, 0], spec=100),
            ),
            Box(
                V3(-2.25, -1, -6),
                V3(-2, 0, -6),
                Material(diffuse=(150, 73, 23), albedo=[0.75, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2.5, -1, -6),
                V3(-2.25, -0.75, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.75, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2, -1, -6),
                V3(-1.75, -0.75, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.75, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2.25, -1.25, -6),
                V3(-2, -1, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.75, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2.25, -1.25, -6),
                V3(-1.75, -0.75, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.75, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2.5, -1.5, -6),
                V3(-2, -1.25, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.6, 0.30, 0, 0], spec=1000),
            ),
            Box(
                V3(-2.75, -1.5, -6),
                V3(-2.25, -1, -6),
                Material(diffuse=(92, 169, 4), albedo=[0.45, 0.30, 0, 0], spec=1000),
            ),
            Traingle(
                V3(1, 0, 0),
                V3(0, 1, 0),
                V3(0, 0, 1),
                Material(diffuse=(255, 255, 255), albedo=[7, 0.30, 0, 0], spec=10),
            ),
        ]
        self.clear_color = (225, 246, 255)
        self.current_color = (255, 255, 255)
        self.light = Light(V3(0, 0, 0), 1, (255, 255, 255))
        self.clear()

    def point(self, x, y, c=None):
        if y > 0 and y < self.height and x > 0 and x < self.width:
            self.framebuffer[y][x] = c or self.current_color

    def color(self, r, g, b):
        return (b, g, r)

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] for y in range(self.height)
        ]

    def render(self):
        fov = int(pi / 2)
        ar = self.width / self.height
        tana = tan(fov / 2)
        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * ar * tana + 0.000001
                j = (1 - (2 * (y + 0.5) / self.height)) * tana + 0.000001
                direction = V3(i, j, -1).normalize()
                origin = V3(0, 0, 0)
                c = self.cast_ray(origin, direction)
                c = tuple(reversed(c))
                self.point(x, y, c)

    def cast_ray(self, origin, direction, recursion=0):
        if recursion == 3:
            return self.clear_color

        material, intersect = self.scene_intersect(origin, direction)
        if not material:
            return self.clear_color

        if material.albedo[2] > 0:
            reflect_direction = reflect(direction, intersect.normal)
            reflect_bias = 1.1 if reflect_direction @ intersect.normal else -1.1
            reflect_origin = intersect.point + (intersect.normal * reflect_bias)
            reflect_color = self.cast_ray(
                reflect_origin, reflect_direction, recursion + 1
            )
        else:
            reflect_color = (0, 0, 0)

        reflection = (
            int(reflect_color[0] * material.albedo[2]),
            int(reflect_color[1] * material.albedo[2]),
            int(reflect_color[2] * material.albedo[2]),
        )

        if material.albedo[3] > 0:
            refract_dir = refract(
                direction, intersect.normal, material.refractive_index
            )
            refract_bias = 1.1 if refract_dir @ intersect.normal else -1.1
            refract_origin = intersect.point + (intersect.normal * refract_bias)
            refract_color = self.cast_ray(refract_origin, refract_dir, recursion + 1)
        else:
            refract_color = (0, 0, 0)

        refraction = (
            int(refract_color[0] * material.albedo[3]),
            int(refract_color[1] * material.albedo[3]),
            int(refract_color[2] * material.albedo[3]),
        )

        light_dir = (self.light.position - intersect.point).normalize()
        shadow_bias = 0.1
        shadow_orig = intersect.point + (intersect.normal * shadow_bias)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)

        shadow_intensity = 1
        if shadow_material:
            # in shadow
            shadow_intensity = 0.1

        diff_intensity = light_dir @ intersect.normal
        diffuse = (
            int(
                material.diffuse[0]
                * diff_intensity
                * material.albedo[0]
                * shadow_intensity
            ),
            int(
                material.diffuse[1]
                * diff_intensity
                * material.albedo[0]
                * shadow_intensity
            ),
            int(
                material.diffuse[2]
                * diff_intensity
                * material.albedo[0]
                * shadow_intensity
            ),
        )

        light_reflection = reflect(light_dir, intersect.normal)
        reflection_intensity = max(0, light_reflection @ direction)
        specular_intensity = (
            self.light.intensity * reflection_intensity**material.spec
        )
        specular = tuple(
            [x * specular_intensity * material.albedo[1] for x in self.light.c]
        )

        end = (
            int(specular[0] + diffuse[0] + reflection[0] + refraction[0]),
            int(specular[1] + diffuse[1] + reflection[1] + refraction[1]),
            int(specular[2] + diffuse[2] + reflection[2] + refraction[2]),
        )

        return end

    def scene_intersect(self, origin, direction):
        zBuffer = 999999
        material = None
        intersect = None
        for o in self.spheres:
            objintersect = o.ray_intersect(origin, direction)
            if objintersect:
                if objintersect.distance < zBuffer:
                    zBuffer = objintersect.distance
                    material = o.material
                    intersect = objintersect
        return material, intersect

    def write(self, file):
        with open(file, "wb") as f:
            f.write(
                struct.pack(
                    "<hlhhl",
                    19778,
                    14 + 40 + self.height * self.width * 3,
                    0,
                    0,
                    40 + 14,
                )
            )  # Writing BITMAPFILEHEADER
            f.write(
                struct.pack(
                    "<lllhhllllll",
                    40,
                    self.width,
                    self.height,
                    1,
                    24,
                    0,
                    self.width * 3 * self.height,
                    0,
                    0,
                    0,
                    0,
                )
            )  # Writing BITMAPINFO
            for x in range(self.width):
                for y in range(self.height):
                    f.write(
                        struct.pack(
                            "<BBB",
                            max(min(255, self.framebuffer[x][y][0]), 0),
                            max(min(255, self.framebuffer[x][y][1]), 0),
                            max(min(255, self.framebuffer[x][y][2]), 0),
                        )
                    )


ray = Raytracer(500, 500)
ray.render()
ray.write("Scenario.bmp")
