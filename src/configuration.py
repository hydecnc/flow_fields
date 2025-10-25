import math
from dataclasses import dataclass
from typing import final

import cairo

from vector import Vec3

# Image & grid configuration
WIDTH, HEIGHT = 2000, 2000
SUPERSAMPLE = 1
SCALED_WIDTH, SCALED_HEIGHT = WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE
BACKGROUND_COLOR = Vec3(0.0, 0.0, 0.0)
NUM_COLS = 150
NUM_ROWS = 150
NUM_PARTITION_ROW = 100
NUM_PARTITION_COL = 100
NUM_SPARSE_LINES_X = 20
NUM_SPARSE_LINES_Y = 20

# Default values for fractal brownian motion
FBM_NUM_OCTAVES = 6
FBM_AMPLITUDE = 1.0
FBM_FREQUENCY = 0.002

# Default seed for OpenSimplex2
SEED: int = 1847362951


# Drawable object configuration
@final
@dataclass
class Arrow:
    tip_size: float = 0.1
    angle: float = math.pi / 4
    thickness: float = 0.001
    color: cairo.SolidPattern = cairo.SolidPattern(1.0, 1.0, 1.0)


@final
@dataclass
class Line:
    width: float = 0.002
    color: cairo.Pattern = cairo.SolidPattern(0.0, 0.7, 1.0)
    step_size: float = 0.003


@final
@dataclass
class Circle:
    radius: float = 0.004
    color: cairo.Pattern = cairo.SolidPattern(0.0, 0.7, 1.0)
    step_size: float = radius * 3


arrow = Arrow()
line = Line()
circle = Circle()
