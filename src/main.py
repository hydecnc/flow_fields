import math

import cairo

import configuration
from lines.draw import draw_flow_field  # pyright: ignore[reportUnknownVariableType]
from math_utils import lerp
from particle import Particle
from perlin import Perlin2D
from vector import Vec2


def setup_grid(perlin2d: Perlin2D) -> list[list[Particle]]:
    grid: list[list[Particle]] = []
    row_step = 1 / configuration.NUM_ROWS
    col_step = 1 / configuration.NUM_COLS
    pos = Vec2(0, 0)
    for row in range(configuration.NUM_ROWS + 1):
        grid_row: list[Particle] = []
        for col in range(configuration.NUM_COLS + 1):
            angle = lerp(
                perlin2d.fractal_brownian_motion(row, col, configuration.NUM_OCTAVES),
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
    perlin2d = Perlin2D(shuffle_p=True)

    # Add particles to grid
    grid = setup_grid(perlin2d)

    draw_flow_field(ctx, grid, start_method="sparse")

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
