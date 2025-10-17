from __future__ import annotations

import copy
import math

import numpy as np
import numpy.typing as npt
from cairo import Context, ImageSurface, LinearGradient
from tqdm import tqdm

import configuration
from grid import SpatialGrid
from lines.utils import interpolated_angle
from vector import Vec2


def trace_line(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    start_point: Vec2,
    num_steps: int,
    spatial_grid: SpatialGrid | None = None,
) -> Vec2:
    """
    Draw a line starting at start_point given the number of steps and other information.

    Args:
        ctx (Context): The pycairo context to draw to.
        grid (npt.NDArray[np.float64]): Grid containing the generated angles to be used for the lines.
        start_point (Vec2): Vec2 in [0, 1] x [0, 1] where the line starts.
        num_steps (int): The number of steps (approximation) that will be used to draw the line.
        spatial_grid (SpatialGrid | None): Spatial Grid designed to calculate collision. If None, then no collision is calculated.
    """
    check_collision = spatial_grid is not None
    pos = copy.copy(start_point)

    ctx.set_line_width(configuration.line.width)
    ctx.move_to(pos.x, pos.y)

    for step in range(num_steps):
        angle = interpolated_angle(angles, pos)

        # NOTE: Try out Runge Kutta approximation

        x_step = configuration.line.step_size * math.cos(angle)
        y_step = configuration.line.step_size * math.sin(angle)
        pos += Vec2(x_step, y_step)

        # if the curve goes outside the line, stop
        if 0 > pos.x or 1 < pos.x or 0 > pos.y or 1 < pos.y:
            break

        if check_collision:
            # check for collision at current position and if there is a collision, stop
            collision = spatial_grid.check_collision(pos)
            if collision:
                break

            # record the current position every 10th step
            if step % 20 == 0:
                spatial_grid.add_position(pos)

        ctx.line_to(pos.x, pos.y)
        ctx.move_to(pos.x, pos.y)
    return pos


def stroke_line(ctx: Context[ImageSurface], start_point: Vec2, end_point: Vec2) -> None:
    # TODO: add swappable color support
    color = LinearGradient(start_point.x, start_point.y, end_point.x, end_point.y)
    color.add_color_stop_rgb(0, 42 / 255, 123 / 255, 155 / 255)
    color.add_color_stop_rgb(0.5, 87 / 255, 199 / 255, 133 / 255)
    color.add_color_stop_rgb(1, 237 / 255, 221 / 255, 83 / 255)
    ctx.set_source(color)
    ctx.stroke()


def draw_flow_field(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    check_collision: bool = True,
    start_method: str | None = None,
) -> None:
    # TODO: Start drawing lines in more varying positions
    match start_method:
        case "sparse":
            draw_sparse_flow_field(ctx, angles, check_collision)
        case "full":
            draw_full_flow_field(ctx, angles, check_collision)
        case _:
            pass


def draw_sparse_flow_field(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    check_collision: bool,
) -> None:
    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None

    pos = Vec2(0, 0)
    x_step = 1 / configuration.NUM_SPARSE_LINES_X
    y_step = 1 / configuration.NUM_SPARSE_LINES_Y
    for _ in tqdm(range(configuration.NUM_SPARSE_LINES_Y), desc="Rows"):
        pos.x = 0
        for _ in tqdm(
            range(configuration.NUM_SPARSE_LINES_X), desc="Points", leave=False
        ):
            # PERF: Add multiprocessing for faster render times
            end_point = trace_line(
                ctx,
                angles,
                pos,
                200,
                spatial_grid=spatial_grid,
            )
            stroke_line(ctx, pos, end_point)
            pos.x += x_step
        pos.y += y_step


def draw_full_flow_field(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    check_collision: bool,
) -> None:
    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None

    for row in tqdm(angles, desc="Rows"):
        for particle in tqdm(row, desc="Points", leave=False):
            # PERF: Add multiprocessing for faster render times
            end_point = trace_line(
                ctx,
                angles,
                particle.pos(),
                200,
                spatial_grid=spatial_grid,
            )
            stroke_line(ctx, particle.pos(), end_point)
