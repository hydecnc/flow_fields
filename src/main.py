import colorsys
import math

import cairo
from tqdm import tqdm

from particle import Particle
from perlin import Perlin2D, lerp
from vector import Vec2D, Vec3D

WIDTH, HEIGHT = 1600, 1600
BACKGROUND_COLOR = Vec3D(0.0, 0.0, 0.0)
PARTICLE_RADIUS = 0.002
NUM_COLS = 100
NUM_ROWS = 100
NUM_OCTAVES = 6


def draw_curve(
    start_point: Vec2D,
    num_steps: int,
    step_size: float = 0.003,
    width: float = 0.002,
    color: Vec3D | None = None,
) -> None:
    if color is None:
        color = Vec3D(0, 1, 0)
    curve = start_point
    ctx.set_source_rgb(color.r, color.g, color.b)
    ctx.set_line_width(width)
    ctx.move_to(curve.x, curve.y)

    for _ in range(num_steps):
        column_index = int(curve.x * NUM_COLS)
        row_index = int(curve.y * NUM_ROWS)

        grid_angle = grid[row_index][column_index].angle

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
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    ctx.scale(WIDTH, HEIGHT)

    # Set background
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(BACKGROUND_COLOR.r, BACKGROUND_COLOR.g, BACKGROUND_COLOR.b)
    ctx.fill()

    # Setup noise
    perlin_2d = Perlin2D()

    # Add particles to grid
    grid: list[list[Particle]] = []
    row_step = 1 / NUM_ROWS
    col_step = 1 / NUM_COLS
    pos = Vec2D(0, 0)
    for row in range(NUM_ROWS + 1):
        grid_row: list[Particle] = []
        for col in range(NUM_COLS + 1):
            angle = lerp(
                perlin_2d.fractal_brownian_motion(row, col, NUM_OCTAVES), 0, 2 * math.pi
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
            hue = (particle.x + particle.y) / 2
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            color = Vec3D(r, g, b)
            draw_curve(
                particle.pos(),
                200,
                color=color,
                width=0.001,
                # step_size=0.001,
            )

    surface.write_to_png("flow.png")
