from __future__ import annotations

import math


class Vec2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def r(self):
        return self.x

    @r.setter
    def r(self, val: float):
        self.x = val

    @property
    def g(self):
        return self.y

    @g.setter
    def g(self, val: float):
        self.y = val

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, val: Vec2D) -> Vec2D:
        return Vec2D(self.x + val.x, self.y + val.y)

    def __sub__(self, val: Vec2D) -> Vec2D:
        return Vec2D(self.x - val.x, self.y - val.y)

    def __mul__(self, val: float) -> Vec2D:
        return Vec2D(self.x * val, self.y * val)

    def __truediv__(self, val: float) -> Vec2D:
        return Vec2D(self.x / val, self.y / val)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Vec3D:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def r(self):
        return self.x

    @r.setter
    def r(self, val: float):
        self.x = val

    @property
    def g(self):
        return self.y

    @g.setter
    def g(self, val: float):
        self.y = val

    @property
    def b(self):
        return self.z

    @b.setter
    def b(self, val: float):
        self.z = val

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __add__(self, val: Vec3D) -> Vec3D:
        return Vec3D(self.x + val.x, self.y + val.y, self.z + val.z)

    def __sub__(self, val: Vec3D) -> Vec3D:
        return Vec3D(self.x - val.x, self.y - val.y, self.z - val.z)

    def __mul__(self, val: float) -> Vec3D:
        return Vec3D(self.x * val, self.y * val, self.z * val)

    def __truediv__(self, val: float) -> Vec3D:
        return Vec3D(self.x / val, self.y / val, self.z / val)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
