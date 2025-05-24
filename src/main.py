import math
import cairo

from arrow import Arrow
from particle import Particle
from perlin import lerp, noise
from vector import Vec2D, Vec3D

WIDTH, HEIGHT = 1000, 1000
BACKGROUND_COLOR = Vec3D(1.0, 1.0, 1.0)
PARTICLE_RADIUS = 0.002
NUM_COLS = 200
NUM_ROWS = 200


def draw_curve(
    start_point: Vec2D,
    num_steps: int,
    step_size: float = 0.003,
    width: float = 0.002,
    color: Vec3D = Vec3D(0, 1, 0),
):
    # draw curve
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
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    ctx.scale(WIDTH, HEIGHT)

    # set background
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(BACKGROUND_COLOR.r, BACKGROUND_COLOR.g, BACKGROUND_COLOR.b)
    ctx.fill()

    # add particles to grid
    grid = []
    row_step = 1 / NUM_ROWS
    col_step = 1 / NUM_COLS
    pos = Vec2D(0, 0)
    for row in range(NUM_ROWS + 1):
        grid_row = []
        for col in range(NUM_COLS + 1):
            # grid_row.append(Particle(pos.x, pos.y, (row / NUM_ROWS) * math.pi))
            angle = (noise(pos.x, pos.y) + 1) / 2
            angle = lerp(angle, 0, 2 * math.pi)
            grid_row.append(Particle(pos.x, pos.y, angle))
            pos.x += col_step
        grid.append(grid_row)
        pos.x = 0
        pos.y += row_step

    # draw particles
    ctx.set_source_rgb(0, 0, 0)
    for row in grid:
        for particle in row:
            # draw the arrow
            # step = (
            #     Vec2D(
            #         math.cos(particle.angle),
            #         math.sin(particle.angle),
            #     )
            #     / 100
            # )
            # arrow = Arrow(particle.pos(), particle.pos() + step, 0.005)
            # arrow.draw(ctx)

            # draw a curve at each position of the particle.
            draw_curve(
                particle.pos(),
                200,
                color=Vec3D(particle.y, particle.x, particle.x * particle.y),
                width=0.001,
                # step_size=0.001,
            )

    surface.write_to_png("flow.png")
