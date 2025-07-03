import math

import cairo

import configuration
from math_utils import angle_lerp
from particle import Particle
from vector import Vec2D, Vec3D


def interpolated_angle(
    grid: list[list[Particle]],
    pos: Vec2D,
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

    # distance between the current position and the closest grid points
    dx = gx - x0
    dy = gy - y0

    angle_bottom = angle_lerp(dx, angle_00, angle_10)
    angle_top = angle_lerp(dx, angle_01, angle_11)
    return angle_lerp(dy, angle_bottom, angle_top)


def draw_curve(
    ctx: cairo.Context[cairo.ImageSurface],
    grid: list[list[Particle]],
    start_point: Vec2D,
    num_steps: int,
    step_size: float = 0.003,
    width: float = 0.0005,
    color: Vec3D | None = None,
) -> None:
    if color is None:
        color = Vec3D(0, 1, 0)
    curve = start_point
    ctx.set_source_rgb(color.r, color.g, color.b)
    ctx.set_line_width(width)
    ctx.move_to(curve.x, curve.y)

    for _ in range(num_steps):
        grid_angle = interpolated_angle(grid, curve)

        # NOTE: Try out Runge Kutta approximation

        x_step = step_size * math.cos(grid_angle)
        y_step = step_size * math.sin(grid_angle)

        curve += Vec2D(x_step, y_step)

        # NOTE: Try out collision between lines
        # if the curve goes outside the line stop
        if 0 > curve.x or 1 < curve.x or 0 > curve.y or 1 < curve.y:
            break

        ctx.line_to(curve.x, curve.y)
    ctx.stroke()
