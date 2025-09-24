import math

from cairo import Context
from tqdm import tqdm

import configuration
from grid import SpatialGrid
from lines.utils import interpolated_angle
from particle import Particle
from vector import Vec2


def draw_line(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
    start_point: Vec2,
    num_steps: int,
    spatial_grid: SpatialGrid | None = None,
) -> None:
    """
    Draw a line starting at start_point given the number of steps and other information.

    Args:
        ctx (Context): The pycairo context to draw to.
        grid (list[list[Particle]]): Grid containing the generated angles to be used for the lines.
        start_point (Vec2): Vec2 in [0, 1] x [0, 1] where the line starts.
        num_steps (int): The number of steps (approximation) that will be used to draw the line.
        spatial_grid (SpatialGrid | None): Spatial Grid designed to calculate collision. If None, then no collision is calculated.
    """
    check_collision = spatial_grid is not None
    pos = start_point

    ctx.set_line_width(configuration.line.width)
    ctx.move_to(pos.x, pos.y)

    for step in range(num_steps):
        # Set line color
        ctx.set_source_rgb(*configuration.line.color.get(step / (num_steps - 1) * 4))

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
                # pass
            # record the current position every 10th step
            if step % 20 == 0:
                spatial_grid.add_position(pos)

        ctx.line_to(pos.x, pos.y)
        ctx.stroke()
        ctx.move_to(pos.x, pos.y)

    ctx.stroke()


def draw_flow_field(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
    check_collision: bool = True,
    start_method: str | None = None,
) -> None:
    ctx.set_source_rgb(0, 0, 0)

    # TODO: Start drawing lines in more varying positions
    match start_method:
        case "sparse":
            draw_sparse_flow_field(ctx, grid, check_collision)
        case "full":
            draw_full_flow_field(ctx, grid, check_collision)
        case _:
            pass


def draw_sparse_flow_field(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
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
            range(configuration.NUM_SPARSE_LINES_X), desc="Particles", leave=False
        ):
            # PERF: Add multiprocessing for faster render times
            draw_line(
                ctx,
                grid,
                pos,
                200,
                spatial_grid=spatial_grid,
            )
            pos.x += x_step
        pos.y += y_step


def draw_full_flow_field(
    ctx: Context,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    grid: list[list[Particle]],
    check_collision: bool,
) -> None:
    # Make spatial grid partition for collision detection
    if check_collision:
        spatial_grid = SpatialGrid()
    else:
        spatial_grid = None

    for row in tqdm(grid, desc="Rows"):
        for particle in tqdm(row, desc="Particles", leave=False):
            # PERF: Add multiprocessing for faster render times
            draw_line(
                ctx,
                grid,
                particle.pos(),
                200,
                spatial_grid=spatial_grid,
            )
