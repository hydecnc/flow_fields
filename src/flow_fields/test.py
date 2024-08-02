import pygame
import pygame.gfxdraw
import sys
import math

pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Curve Example")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)


# Define the curve function
def smooth_curve(t):
    # Example of a simple quadratic curve
    x = 200 + 100 * math.cos(t)
    y = 150 + 50 * math.sin(t)
    return int(x), int(y)


# Main game loop
running = True
clock = pygame.time.Clock()
t = 0.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Get the next point on the curve
    point = smooth_curve(t)

    # Draw the point on the curve
    pygame.gfxdraw.pixel(screen, *point, black)

    # Update the display
    pygame.display.flip()

    # Increment t for the next point
    t += 0.05

    # Control the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
sys.exit()
