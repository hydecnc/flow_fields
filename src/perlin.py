import json
import math
import random

import configuration
from math_utils import fade, lerp


def shuffle(arr: list[int]) -> None:
    """Mutate arr by shuffling all elements randomly."""
    for e in range(len(arr) - 1, 0, -1):
        index = random.randint(0, e)
        arr[index], arr[e] = arr[e], arr[index]


class Perlin2D:
    @classmethod
    def shuffle_p(cls) -> None:
        with open("src/permutation_table.json", "r") as file:
            cls.perm: list[int] = json.load(file)
            shuffle(cls.perm)
            cls.perm = cls.perm + cls.perm

    @classmethod
    def noise(cls, x: float, y: float) -> float:
        """
        Perlin noise implementation based on Ken Perlin's 2002 paper.
        """
        xi = math.floor(x) & 255
        yi = math.floor(y) & 255
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        u, v = fade(xf), fade(yf)

        aa = cls.perm[cls.perm[xi] + yi]  # bottom left
        ab = cls.perm[cls.perm[xi] + yi + 1]  # top left
        ba = cls.perm[cls.perm[xi + 1] + yi]  # bottom right
        bb = cls.perm[cls.perm[xi + 1] + yi + 1]  # top right

        return lerp(
            v,
            lerp(u, cls.grad(aa, xf, yf), cls.grad(ba, xf - 1, yf)),
            lerp(u, cls.grad(ab, xf, yf - 1), cls.grad(bb, xf - 1, yf - 1)),
        )

    @classmethod
    def grad(cls, hash: int, x: float, y: float) -> float:
        """Return the dot product of each corner of the cell."""
        h = hash & 3
        if h == 0:
            return x  # gradient (1, 0)
        elif h == 1:
            return -x  # gradient (-1, 0)
        elif h == 2:
            return y  # gradient (0, 1)
        else:
            return -y  # gradient (0, -1)

    @classmethod
    def fractal_brownian_motion(
        cls,
        x: float,
        y: float,
        numOctaves: int,
        amplitude: float = 1.0,
        frequency: float = configuration.FREQUENCY,
    ) -> float:
        """Fractal Brownian Motion for better noise results."""
        result = 0.0
        max_value = 0.0

        for _ in range(numOctaves):
            result += amplitude * cls.noise(x * frequency, y * frequency)
            max_value += amplitude

            amplitude *= 0.5
            frequency *= 2.0

        return result / max_value
