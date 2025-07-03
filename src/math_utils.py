import math

from vector import Vec2


def fade(t: float) -> float:
    """Fade function: 6t^5 - 15t^4 + 10t^3"""
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t: float, a: float, b: float) -> float:
    """Linear interpolation between a and b with t."""
    return a + t * (b - a)


def angle_lerp(t: float, a1: float, a2: float) -> float:
    """
    Angle interpolation between angles a1 and a2.
    Use the shortest angle distance between a1 and a2 to lerp with t.
    """
    diff = a2 - a1
    if diff > math.pi:
        diff -= 2 * math.pi
    elif diff < -math.pi:
        diff += 2 * math.pi
    return a1 + t * (diff)


def cosine_lerp(t: float, a: float, b: float) -> float:
    """Cosine interpolation between a and b with t."""
    mu = (1 - math.cos(t * math.pi)) / 2
    return a * (1 - mu) + b * mu


def angle_to_vector(angle: float) -> Vec2:
    return Vec2(math.cos(angle), math.sin(angle))
