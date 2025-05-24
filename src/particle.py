from vector import Vec2D


class Particle:
    def __init__(self, x: float, y: float, angle: float):
        self.x = x
        self.y = y
        self.angle = angle

    def pos(self) -> Vec2D:
        return Vec2D(self.x, self.y)
