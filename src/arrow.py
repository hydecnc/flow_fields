import math

import cairo

from vector import Vec2, Vec3


class Arrow:
    def __init__(
        self,
        start: Vec2,
        end: Vec2,
        tip_size: float,
        angle: float = math.pi / 4,
        thickness: float = 0.001,
        color: Vec3 | None = None,
    ) -> None:
        if color is None:
            color = Vec3(0, 0, 0)
        self.start: Vec2 = start
        self.end: Vec2 = end
        self.tip_size: float = tip_size
        self.angle: float = angle / 2
        self.thickness: float = thickness
        self.color: Vec3 = color

    def draw(self, ctx: cairo.Context) -> None:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
        # set color and arrow width
        ctx.set_source_rgb(self.color.x, self.color.y, self.color.z)
        ctx.set_line_width(self.thickness)

        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)

        # calculate the displacement between self.start and self.end
        disp = self.start - self.end
        normal_disp = disp / disp.norm()

        # rotate the displacement vector by self.angle
        rot1 = Vec2(
            math.cos(self.angle) * normal_disp.x - math.sin(self.angle) * normal_disp.x,
            math.sin(self.angle) * normal_disp.y + math.cos(self.angle) * normal_disp.y,
        )
        rot2 = Vec2(
            math.cos(-self.angle) * normal_disp.x
            - math.sin(-self.angle) * normal_disp.x,
            math.sin(-self.angle) * normal_disp.y
            + math.cos(-self.angle) * normal_disp.y,
        )

        end1 = self.end + rot1 * self.tip_size
        end2 = self.end + rot2 * self.tip_size

        # draw the lines
        ctx.move_to(self.end.x, self.end.y)
        ctx.line_to(end1.x, end1.y)
        ctx.move_to(self.end.x, self.end.y)
        ctx.line_to(end2.x, end2.y)

        ctx.stroke()
