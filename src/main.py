import math

import cairo

import configuration
from lines.draw import draw_flow_field  # pyright: ignore[reportUnknownVariableType]
from math_utils import lerp
from particle import Particle
from perlin import Perlin2D
from simplex import OpenSimplex2D
from vector import Vec2


def setup_grid() -> list[list[Particle]]:
    """
    Return a 2D array of Particle placed in a grid with angle produced with a noise function.
    """
    grid: list[list[Particle]] = []
    row_step = 1 / configuration.NUM_ROWS
    col_step = 1 / configuration.NUM_COLS
    pos = Vec2(0, 0)
    for row in range(configuration.NUM_ROWS + 1):
        grid_row: list[Particle] = []
        for col in range(configuration.NUM_COLS + 1):
            angle = lerp(
                (OpenSimplex2D.noise(configuration.SEED, row * 0.01, col * 0.01) + 1)
                / 2,
                0,
                2 * math.pi,
            )
            grid_row.append(Particle(pos.x, pos.y, angle))
            pos.x += col_step
        grid.append(grid_row)
        pos.x = 0
        pos.y += row_step

    return grid


def main() -> None:
    # Initial setup
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, configuration.SCALED_WIDTH, configuration.SCALED_HEIGHT
    )
    ctx = cairo.Context(surface)

    ctx.scale(configuration.SCALED_WIDTH, configuration.SCALED_HEIGHT)

    # Set background color
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(
        configuration.BACKGROUND_COLOR.r,
        configuration.BACKGROUND_COLOR.g,
        configuration.BACKGROUND_COLOR.b,
    )
    ctx.fill()

    # Setup noise
    Perlin2D.shuffle_p()

    # Add particles to grid
    grid = setup_grid()

    draw_flow_field(ctx, grid, start_method="sparse", check_collision=False)

    # Supersampling; scale down the image.
    final_surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, configuration.WIDTH, configuration.HEIGHT
    )
    final_ctx = cairo.Context(final_surface)
    final_ctx.set_matrix(
        cairo.Matrix(xx=1 / configuration.SUPERSAMPLE, yy=1 / configuration.SUPERSAMPLE)
    )
    final_ctx.set_source_surface(surface)
    final_ctx.paint()

    final_surface.write_to_png("flow-field.png")

    # TODO: Post processing effects


if __name__ == "__main__":
    main()
