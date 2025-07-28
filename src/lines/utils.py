import math
import random

import configuration
from math_utils import angle_to_vector, lerp
from particle import Particle
from vector import Vec2, Vec3


def interpolated_angle(
    grid: list[list[Particle]],
    pos: Vec2,
) -> float:
    gx, gy = pos.x * configuration.NUM_COLS, pos.y * configuration.NUM_ROWS
    x0 = int(gx)
    x1 = min(int(gx) + 1, configuration.NUM_COLS - 1)
    y1 = int(gy)
    y0 = min(int(gy) + 1, configuration.NUM_ROWS - 1)

    # angles at the four closest grid points
    angle_00 = grid[y0][x0].angle
    angle_01 = grid[y1][x0].angle
    angle_10 = grid[y0][x1].angle
    angle_11 = grid[y1][x1].angle

    # convert the angles to a vector
    vector_00 = angle_to_vector(angle_00)
    vector_01 = angle_to_vector(angle_01)
    vector_10 = angle_to_vector(angle_10)
    vector_11 = angle_to_vector(angle_11)

    # distance between the current position and the closest grid points
    dx = gx - x0
    dy = gy - y0

    vec_top = Vec2(
        lerp(dx, vector_01.x, vector_11.x),
        lerp(dx, vector_01.y, vector_11.y),
    )

    vec_bottom = Vec2(
        lerp(dx, vector_00.x, vector_10.x),
        lerp(dx, vector_00.y, vector_10.y),
    )
    final_vec = Vec2(
        lerp(dy, vec_top.x, vec_bottom.x),
        lerp(dy, vec_top.y, vec_bottom.y),
    )
    return math.atan2(final_vec.y, final_vec.x)


def random_color() -> Vec3:
    return Vec3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
