from vector import Vec2


class Particle:
    def __init__(self, x: float, y: float, angle: float):
        self.x: float = x
        self.y: float = y
        self.angle: float = angle

    def pos(self) -> Vec2:
        return Vec2(self.x, self.y)
