from __future__ import annotations

import copy
import math
import random

import numpy as np
import numpy.typing as npt
from cairo import LINE_CAP_ROUND, LINE_JOIN_ROUND, Context, ImageSurface, LinearGradient
from tqdm import tqdm

import configuration
from grid import SpatialGrid
from lines.utils import interpolated_angle
from math_utils import lerp
from vector import Vec2


def draw_lines(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    start_point: Vec2,
    num_steps: int,
    spatial_grid: SpatialGrid | None = None,
) -> None:
    end_point = trace_line(
        ctx, angles, start_point, num_steps, spatial_grid=spatial_grid
    )
    stroke_line(ctx, start_point, end_point)


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
    ctx.set_line_cap(LINE_CAP_ROUND)
    ctx.set_line_join(LINE_JOIN_ROUND)

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


def draw_circles(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    start_point: Vec2,
    num_steps: int,
    spatial_grid: SpatialGrid | None = None,
) -> None:
    """
    Draw a circles along the line traced out by starting at start_point given the number of steps and other information.

    Args:
        ctx (Context): The pycairo context to draw to.
        grid (npt.NDArray[np.float64]): Grid containing the generated angles to be used for the lines.
        start_point (Vec2): Vec2 in [0, 1] x [0, 1] where the line starts.
        num_steps (int): The number of steps (approximation) that will be used to draw the line.
        spatial_grid (SpatialGrid | None): Spatial Grid designed to calculate collision. If None, then no collision is calculated.
    """
    check_collision = spatial_grid is not None

    # ctx.set_line_width(0.002)
    ctx.set_source(configuration.circle.color)

    for step in range(num_steps):
        radius_scale = lerp(step / num_steps, 0.5, 1.5)
        ctx.new_sub_path()
        ctx.arc(
            start_point.x,
            start_point.y,
            configuration.circle.radius * radius_scale,
            0,
            2 * math.pi,
        )
        ctx.fill()

        angle = interpolated_angle(angles, start_point)

        # NOTE: Try out Runge Kutta approximation

        x_step = configuration.circle.step_size * math.cos(angle)
        y_step = configuration.circle.step_size * math.sin(angle)
        start_point += Vec2(x_step, y_step)

        # if the curve goes outside the line, stop
        if (
            0 > start_point.x
            or 1 < start_point.x
            or 0 > start_point.y
            or 1 < start_point.y
        ):
            break

        if check_collision:
            # check for collision at current position and if there is a collision, stop
            collision = spatial_grid.check_collision(start_point)
            if collision:
                # ctx.set_source_rgb(1.0, 0.0, 0.0)
                # ctx.new_sub_path()
                # ctx.arc(
                #     start_point.x,
                #     start_point.y,
                #     configuration.circle.radius * radius_scale,
                #     0,
                #     2 * math.pi,
                # )
                # ctx.fill()
                break

            spatial_grid.add_position(start_point)
    ctx.stroke()


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
    match start_method:
        case "sparse":
            draw_sparse_flow_field(ctx, angles, check_collision)
        case "full":
            draw_full_flow_field(ctx, angles, check_collision)
        case "random":
            draw_random_flow_field(ctx, angles, check_collision)
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
    x_step = 1 / configuration.NUM_ROWS
    y_step = 1 / configuration.NUM_COLS

    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None

    for iy, ix in tqdm(np.ndindex(angles.shape), total=angles.size, desc="Pixels"):  # pyright: ignore[reportAny]
        # PERF: Add multiprocessing for faster render times
        pos = Vec2(x_step * ix, y_step * iy)  # pyright: ignore[reportAny]
        end_point = trace_line(
            ctx,
            angles,
            pos,
            200,
            spatial_grid=spatial_grid,
        )
        stroke_line(ctx, pos, end_point)


def draw_random_flow_field(
    ctx: Context[ImageSurface],
    angles: npt.NDArray[np.float64],
    check_collision: bool,
) -> None:
    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None

    for i in range(200):
        # TODO: Clean up trace circle code and make switching from line to circles easy
        pos = Vec2(random.random(), random.random())
        # draw_circles(ctx, angles, pos, 200, spatial_grid=spatial_grid)
        draw_lines(ctx, angles, pos, 200, spatial_grid=spatial_grid)
