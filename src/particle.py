from vector import Vec2D


class Particle:
    def __init__(self, x: float, y: float, angle: float):
        self.x: float = x
        self.y: float = y
        self.angle: float = angle

    def pos(self) -> Vec2D:
        return Vec2D(self.x, self.y)
