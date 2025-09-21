import json
import math

import configuration
from math_utils import fade, lerp

SKEW_2D = 0.366025403784439
UNSKEW_2D = -0.21132486540518713
PRIME_X = 0x5205402B9270C86F
PRIME_Y = 0x598CD327003817B5
RSQUARED_2D = 0.5
HASH_MULTIPLIER = 0x53A3F72DEEC546F5
NORMALIZER_2D = 0.01001634121365712
N_GRADS_2D_EXPONENT = 7
N_GRADS_2D = 1 << N_GRADS_2D_EXPONENT
# fmt: off
grad2 = [0.38268343236509, 0.923879532511287, 0.923879532511287, 0.38268343236509, 0.923879532511287, -0.38268343236509, 0.38268343236509, -0.923879532511287, -0.38268343236509, -0.923879532511287, -0.923879532511287, -0.38268343236509, -0.923879532511287, 0.38268343236509, -0.38268343236509, 0.923879532511287, 0.130526192220052, 0.99144486137381, 0.608761429008721, 0.793353340291235, 0.793353340291235, 0.608761429008721, 0.99144486137381, 0.130526192220051, 0.99144486137381, -0.130526192220051, 0.793353340291235, -0.60876142900872, 0.608761429008721, -0.793353340291235, 0.130526192220052, -0.99144486137381, -0.130526192220052, -0.99144486137381, -0.608761429008721, -0.793353340291235, -0.793353340291235, -0.608761429008721, -0.99144486137381, -0.13052619222005] * 2
GRADIENTS_2D = [grad2[i % len(grad2)] / NORMALIZER_2D for i in range(256)]
# fmt: on


class OpenSimplex2D:
    def __init__(self) -> None:
        pass

    @classmethod
    def noise(cls, seed: int, x: float, y: float) -> float:
        """
        OpenSimplex2 2D Noise based on Kurt Spencer's implementation in Java.
        """
        s = SKEW_2D * (x + y)
        xs = x + s
        ys = y + s

        return cls._noise_unskewed_base(seed, xs, ys)

    @classmethod
    def _noise_unskewed_base(cls, seed: int, xs: float, ys: float) -> float:
        # Get base points and offsets
        xsb = math.floor(xs)
        ysb = math.floor(ys)
        xi = xs - xsb
        yi = ys - ysb

        # Prime pre-multiplication for hash.
        xsbp = xsb * PRIME_X
        ysbp = ysb * PRIME_Y

        # Unskew
        t = (xi + yi) * UNSKEW_2D
        dx0 = xi + t
        dy0 = yi + t

        value = 0.0

        # First vertex
        a0 = RSQUARED_2D - dx0 * dx0 - dy0 * dy0
        if a0 > 0:
            value = (a0 * a0) * (a0 * a0) * cls._grad(seed, xsbp, ysbp, dx0, dy0)

        # Second vertex
        a1 = (2 * (1 + 2 * UNSKEW_2D) * (1 / UNSKEW_2D + 2)) * t + (
            (-2 * (1 + 2 * UNSKEW_2D) * (1 + 2 * UNSKEW_2D)) + a0
        )
        if a1 > 0:
            dx1 = dx0 - (1 + 2 * UNSKEW_2D)
            dy1 = dy0 - (1 + 2 * UNSKEW_2D)
            value += (
                (a1 * a1)
                * (a1 * a1)
                * cls._grad(seed, xsbp + PRIME_X, ysbp + PRIME_Y, dx1, dy1)
            )

        # Third vertex
        if dy0 > dx0:
            dx2 = dx0 - UNSKEW_2D
            dy2 = dy0 - (UNSKEW_2D + 1)
            a2 = RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (
                    (a2 * a2)
                    * (a2 * a2)
                    * cls._grad(seed, xsbp, ysbp + PRIME_Y, dx2, dy2)
                )
        else:
            dx2 = dx0 - (UNSKEW_2D + 1)
            dy2 = dy0 - UNSKEW_2D
            a2 = RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (
                    (a2 * a2)
                    * (a2 * a2)
                    * cls._grad(seed, xsbp + PRIME_X, ysbp, dx2, dy2)
                )

        return value

    @classmethod
    def _grad(cls, seed: int, xsbp: int, ysbp: int, dx: float, dy: float) -> float:
        hash = seed ^ xsbp ^ ysbp
        hash *= HASH_MULTIPLIER
        hash ^= hash >> (64 - N_GRADS_2D_EXPONENT + 1)
        gi = hash & ((N_GRADS_2D - 1) << 1)

        return GRADIENTS_2D[gi | 0] * dx + GRADIENTS_2D[gi | 1] * dy
