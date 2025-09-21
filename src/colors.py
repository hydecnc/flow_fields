import colorsys
import random
from abc import ABC, abstractmethod
from typing import override

from vector import Vec3


class Color(ABC):
    r: float
    b: float
    g: float

    @abstractmethod
    def get(self, t: float) -> tuple[float, float, float]:
        pass


class SolidColor(Color):
    def __init__(self, r: float, g: float, b: float) -> None:
        self.r: float = r
        self.b: float = b
        self.g: float = g

    @override
    def get(self, t: float) -> tuple[float, float, float]:
        return self.r, self.b, self.g


class HSVGradient(Color):
    def __init__(self, r: float, g: float, b: float) -> None:
        self.r: float = r
        self.b: float = b
        self.g: float = g
        # h, s, v = colorsys.rgb_to_hsv(r, g, b)
        # self.h: float = h
        # self.s: float = s
        # self.v: float = v

    @override
    def get(self, t: float) -> tuple[float, float, float]:
        hsv = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        return colorsys.hsv_to_rgb(
            (hsv[0] + 0.5 * t) % 1.0,
            hsv[1],
            t,
        )


def random_color() -> Vec3:
    return Vec3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))


def hsv_colors(color: Vec3, t: float) -> tuple[float, float, float]:
    hsv = colorsys.rgb_to_hsv(color.r, color.g, color.b)
    v = 1 - abs(1 - 2 * t)
    return colorsys.hsv_to_rgb(
        (hsv[0] + 0.2 * t) % 1.0,
        hsv[1],
        v,
    )
