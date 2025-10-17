import math

import cairo
import numpy as np
import numpy.typing as npt

import configuration
from lines.draw import draw_flow_field
from math_utils import lerp
from perlin import Perlin2D
from simplex import OpenSimplex2D


def setup_angle_grid() -> npt.NDArray[np.float64]:
    """
    Return a 2D array of Particle placed in a grid with angle produced with a noise function.
    """
    angles = np.zeros((configuration.NUM_ROWS + 1, configuration.NUM_COLS + 1))
    for row in range(configuration.NUM_ROWS + 1):
        for col in range(configuration.NUM_COLS + 1):
            # noise = Perlin2D.fractal_brownian_motion(row, col, amplitude=50.0)
            noise = OpenSimplex2D.noise(configuration.SEED, row * 0.01, col * 0.01)
            noise = (noise + 1) / 2
            angle = lerp(
                noise,
                0,
                2 * math.pi,
            )
            angles[row, col] = angle

    return angles


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

    # Setup Perlin noise
    Perlin2D.shuffle_p()

    # Get angles on each grid points
    angles = setup_angle_grid()

    draw_flow_field(ctx, angles, start_method="sparse", check_collision=True)

    # Supersampling; scale down the image.
    if configuration.SUPERSAMPLE > 1:
        final_surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, configuration.WIDTH, configuration.HEIGHT
        )
        final_ctx = cairo.Context(final_surface)
        final_ctx.set_matrix(
            cairo.Matrix(
                xx=1 / configuration.SUPERSAMPLE, yy=1 / configuration.SUPERSAMPLE
            )
        )
        # blur_image_surface(surface, radius=10)
        final_ctx.set_source_surface(surface)
        final_ctx.paint()

        final_surface.write_to_png("flow-field.png")
        return

    # TODO: Post processing effects
    # blur_image_surface(surface, 10)
    surface.write_to_png("flow-field.png")


if __name__ == "__main__":
    main()
