import cairo

from draw import Arrow
from vector import Vec2D, Vec3D

WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = Vec3D(1.0, 1.0, 1.0)

if __name__ == "__main__":
    arrow = Arrow(Vec2D(0.1, 0.1), Vec2D(0.5, 0.5), 0.1)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    ctx.scale(WIDTH, HEIGHT)

    # set background
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source(
        cairo.SolidPattern(BACKGROUND_COLOR.r, BACKGROUND_COLOR.g, BACKGROUND_COLOR.b)
    )
    ctx.fill()

    arrow.draw(ctx)

    surface.write_to_png("flow.png")
