import math
import random

from cairo import Context
from tqdm import tqdm

import configuration
from grid import SpatialGrid
from lines.utils import interpolated_angle
from particle import Particle
from vector import Vec2, Vec3


def draw_line(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
    start_point: Vec2,
    num_steps: int,
    spatial_grid: SpatialGrid | None = None,
    color: Vec3 | None = None,
) -> None:
    if color is None:
        color = configuration.line.color
    check_collision = spatial_grid is not None
    pos = start_point

    # Set line color
    ctx.set_source_rgb(
        color.r,
        color.g,
        color.b,
    )
    ctx.set_line_width(configuration.line.width)
    ctx.move_to(pos.x, pos.y)

    for step in range(num_steps):
        grid_angle = interpolated_angle(grid, pos)

        # NOTE: Try out Runge Kutta approximation

        x_step = configuration.line.step_size * math.cos(grid_angle)
        y_step = configuration.line.step_size * math.sin(grid_angle)
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
    ctx.stroke()


def draw_lines(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
    check_collision: bool = True,
) -> None:
    ctx.set_source_rgb(0, 0, 0)
    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None
    for row in tqdm(grid, desc="Rows"):
        for particle in tqdm(row, desc="Particles", leave=False):
            # draw a curve at each position of the particle.
            # TODO: Add prettier coloring
            color = configuration.line.color
            # PERF: Add multiprocessing for faster render times
            draw_line(
                ctx,
                grid,
                particle.pos(),
                200,
                spatial_grid=spatial_grid,
                color=color,
            )
