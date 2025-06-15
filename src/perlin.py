import json
import math
import random


def fade(t: float) -> float:
    """Fade function: 6t^5 - 15t^4 + 10t^3"""
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t: float, a: float, b: float) -> float:
    """Linear interpolation between a and b with t."""
    return a + t * (b - a)


def shuffle(arr: list) -> None:
    """Mutate arr by shuffling all elements randomly."""
    for e in range(len(arr) - 1, 0, -1):
        index = random.randint(0, e)
        arr[index], arr[e] = arr[e], arr[index]


class Perlin2D:
    def __init__(self, shuffle_p=True) -> None:
        with open("src/permutation_table.json", "r") as file:
            self.P = json.load(file)
            if shuffle_p:
                shuffle(self.P)
            self.P = self.P + self.P

    def noise(self, x: float, y: float) -> float:
        """
        Perlin noise implementation based on Ken Perlin's 2002 paper.
        Note that x and y expected to be normalized from 0.0 to 1.0.
        """
        xi = math.floor(x) & 255
        yi = math.floor(y) & 255
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        u, v = fade(xf), fade(yf)

        aa = self.P[self.P[xi] + yi]  # bottom left
        ab = self.P[self.P[xi] + yi + 1]  # top left
        ba = self.P[self.P[xi + 1] + yi]  # bottom right
        bb = self.P[self.P[xi + 1] + yi + 1]  # top right

        return lerp(
            v,
            lerp(u, self.grad(aa, xf, yf), self.grad(ba, xf - 1, yf)),
            lerp(u, self.grad(ab, xf, yf - 1), self.grad(bb, xf - 1, yf - 1)),
        )

    def grad(self, hash: int, x: float, y: float) -> float:
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

    def fractal_brownian_motion(
        self, x: int, y: int, numOctaves: int, amplitude=1.0, frequency=0.03
    ) -> float:
        """Fractal Brownian Motion for better noise results."""
        result = 0.0

        for _ in range(numOctaves):
            n = amplitude * self.noise(x * frequency, y * frequency)
            result += n

            amplitude *= 0.5
            frequency *= 2.0

        return result
