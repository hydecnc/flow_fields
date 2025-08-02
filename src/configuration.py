from dataclasses import dataclass
from typing import final

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
NUM_SPARSE_LINES_X = 10
NUM_SPARSE_LINES_Y = 10


@final
@dataclass
class Line:
    width: float = 0.005
    color: Vec3 = Vec3(0.3, 0.1, 0.7)
    step_size: float = 0.003


line = Line()
