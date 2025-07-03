import math

import cairo
from tqdm import tqdm

import configuration
from curves import draw_curve
from math_utils import lerp
from particle import Particle
from perlin import Perlin2D
from vector import Vec2D, Vec3D


def main() -> None:
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
                ctx,
                grid,
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

    final_surface.write_to_png("current.png")


if __name__ == "__main__":
    main()
