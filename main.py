import pygame
import numpy as np
from math import pi as PI
from utils import Point
import random

# constants
image_size_x = 800
image_size_y = 600
resolution = 20

left_x = int(image_size_x * -0.5)
right_x = int(image_size_x * 1.5)
top_y = int(image_size_y * -0.5)
bottom_y = int(image_size_y * 1.5)
# print(f"Left: {left_x}, Right: {right_x}, Top: {top_y}, Bottom: {bottom_y}")

num_columns = (right_x - left_x) // resolution
num_rows = (bottom_y - top_y) // resolution
# print(f"Num col: {num_columns}, Num row: {num_rows}")
angles = np.zeros((num_columns, num_rows))
start_points = [Point(random.randint(0, image_size_x), random.randint(0, image_size_y)) for _ in range(1)]

# pygame setup
pygame.init()
screen = pygame.display.set_mode((image_size_x, image_size_y))
clock = pygame.time.Clock()
running = True
dt = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    # define angles
    for column in range(num_columns):
        for row in range(num_rows):
            angles[column, row] = (row / float(num_rows)) * PI
            angles[column, row] = np.cos((row / float(num_rows)) * PI) + np.sin((column / float(num_columns)) * PI)
            # print(f"Angle at {column} {row}: {(row / float(num_rows)) * PI}")

    # draw lines (vectors)
    line_len = 10
    for column in range(num_columns):
        for row in range(num_rows):
            angle = angles[column, row]
            vec_x = line_len * np.cos(angle)
            vec_y = line_len * np.sin(angle)

            x = column * resolution - image_size_x // 2
            y = row * resolution - image_size_y // 2
            pygame.draw.circle(
                screen,
                "black",
                (x, y),
                2
            )
            pygame.draw.line(
                screen,
                "black",
                (x, y),
                (x + vec_x, y + vec_y),
            )

    # Draw Curves
    for point in start_points:
        step_length = image_size_x * 0.002
        num_steps = 100
        x = point.x
        y = point.y
        for i in range(num_steps):
            pygame.draw.circle(screen, "#4361ee", (x, y), 1)
            x_offset = min(max(x - left_x, 0), right_x)
            y_offset = min(max(y - top_y, 0), bottom_y)

            column_index = int(x_offset / resolution)
            row_index = int(y_offset / resolution)

            angle = angles[column_index, row_index]
            x += step_length * np.cos(angle)
            y += step_length * np.sin(angle)

    pygame.display.flip()

    dt = clock.tick(6) / 1000

pygame.quit()
