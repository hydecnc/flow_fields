import math

import cairo
from tqdm import tqdm

import configuration
from math_utils import angle_lerp, lerp
from particle import Particle
from perlin import Perlin2D
from vector import Vec2D, Vec3D


def draw_curve(
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
        gx, gy = curve.x * configuration.NUM_COLS, curve.y * configuration.NUM_ROWS
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
        grid_angle = angle_lerp(dy, angle_bottom, angle_top)

        # NOTE: Try out Runge Kutta approximation

        x_step = step_size * math.cos(grid_angle)
        y_step = step_size * math.sin(grid_angle)

        curve += Vec2D(x_step, y_step)

        # if the curve goes outside the line stop
        if 0 > curve.x or 1 < curve.x or 0 > curve.y or 1 < curve.y:
            break

        ctx.line_to(curve.x, curve.y)
    ctx.stroke()


if __name__ == "__main__":
    # Initial setup
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, configuration.SCALED_WIDTH, configuration.SCALED_HEIGHT
    )
    ctx = cairo.Context(surface)

    ctx.scale(configuration.SCALED_WIDTH, configuration.SCALED_HEIGHT)

    # Set background
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(
        configuration.BACKGROUND_COLOR.r,
        configuration.BACKGROUND_COLOR.g,
        configuration.BACKGROUND_COLOR.b,
    )
    ctx.fill()

    # Setup noise
    perlin_2d = Perlin2D(shuffle_p=False)

    # Add particles to grid
    grid: list[list[Particle]] = []
    row_step = 1 / configuration.NUM_ROWS
    col_step = 1 / configuration.NUM_COLS
    pos = Vec2D(0, 0)
    for row in range(configuration.NUM_ROWS + 1):
        grid_row: list[Particle] = []
        for col in range(configuration.NUM_COLS + 1):
            angle = lerp(
                perlin_2d.fractal_brownian_motion(row, col, configuration.NUM_OCTAVES),
                0,
                2 * math.pi,
            )
            grid_row.append(Particle(pos.x, pos.y, angle))
            pos.x += col_step
        grid.append(grid_row)
        pos.x = 0
        pos.y += row_step

    # Draw particles
    ctx.set_source_rgb(0, 0, 0)
    for row in tqdm(grid, desc="Rows"):
        for particle in tqdm(row, desc="Particles", leave=False):
            # draw a curve at each position of the particle.
            # TODO: Add prettier coloring
            color = Vec3D(1, 1, 1)
            # PERF: Add multiprocessing for faster render times
            draw_curve(
                particle.pos(),
                200,
                color=color,
                width=0.0005,
                step_size=0.001,
            )

    final_surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, configuration.WIDTH, configuration.HEIGHT
    )
    final_ctx = cairo.Context(final_surface)
    final_ctx.set_matrix(
        cairo.Matrix(xx=1 / configuration.SUPERSAMPLE, yy=1 / configuration.SUPERSAMPLE)
    )
    final_ctx.set_source_surface(surface)
    final_ctx.paint()

    final_surface.write_to_png("flow.png")
