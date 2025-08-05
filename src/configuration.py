import math
from dataclasses import dataclass
from typing import final

from colors import Color, HSVGradient, SolidColor
from vector import Vec3

# NOTE: consider switching to a TOML config
WIDTH, HEIGHT = 1000, 1000
SUPERSAMPLE = 1
SCALED_WIDTH, SCALED_HEIGHT = WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE
BACKGROUND_COLOR = Vec3(0.0, 0.0, 0.0)
NUM_COLS = 150
NUM_ROWS = 150
NUM_OCTAVES = 6
FREQUENCY = 0.005
NUM_PARTITION_ROW = 100
NUM_PARTITION_COL = 100
NUM_SPARSE_LINES_X = 20
NUM_SPARSE_LINES_Y = 20
SOLID_COLOR: int = -1


@final
@dataclass
class Arrow:
    tip_size: float = 0.1
    angle: float = math.pi / 4
    thickness: float = 0.001
    color: Color = SolidColor(1.0, 1.0, 1.0)


@final
@dataclass
class Line:
    width: float = 0.003
    color: Color = HSVGradient(0.0, 0.7, 1.0)
    step_size: float = 0.003


arrow = Arrow()
line = Line()
