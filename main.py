import math
import random
import colorsys
import argparse
from utils import Perlin2D

import numpy as np
from PIL import Image, ImageDraw


def generate_image(
    width=800,
    height=800,
    color=100,
    backgrondColor=(0, 0, 0),
    perlinFactorW=2,
    perlinFactorH=2,
    step=0.001,
    scale=2,
):
    # scale the image 2x for antialias
    img_width = width * scale
    img_height = height * scale

    seed = random.randint(0, 100000000)

    # set random seed
    np.random.seed(seed)

    image = Image.new("RGB", (img_width, img_height), backgrondColor)
    draw = ImageDraw.Draw(image)

    p_noise = Perlin2D(img_width, img_height, perlinFactorW, perlinFactorH)

    MAX_LENGTH = 2 * img_width
    STEP_SIZE = step * max(img_width, img_height)
    NUM = int(img_width * img_height / 1000)
    POINTS = [
        (random.randint(0, img_width - 1), random.randint(0, img_height - 1))
        for i in range(NUM)
    ]

    for k, (x_s, y_s) in enumerate(POINTS):
        print(f"{100 * (k + 1) / len(POINTS):.1f}".rjust(5) + "% Complete", end="\r")
        c_len = 0

        while c_len < MAX_LENGTH:
            sat = 200 * (MAX_LENGTH - c_len) / MAX_LENGTH
            hue = (color + 130 * (img_height - y_s) / img_height) % 360
            hsv = colorsys.hsv_to_rgb(hue / 255, sat / 255, 1)
            float_rgb = (
                int(hsv[0] * 255),
                int(hsv[1] * 255),
                int(hsv[2] * 255),
            )

            angle = p_noise[int(x_s), int(y_s)] * math.pi

            x_f = x_s + STEP_SIZE * math.cos(angle)
            y_f = y_s + STEP_SIZE * math.sin(angle)

            draw.line([(x_s, y_s), (x_f, y_f)], fill=float_rgb)

            c_len += math.sqrt((x_f - x_s) ** 2 + (y_f - y_s) ** 2)

            if (
                x_f < 0
                or x_f >= img_width
                or y_f < 0
                or y_f >= img_height
                or c_len > MAX_LENGTH
            ):
                break
            else:
                x_s, y_s = x_f, y_f
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.save("result.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="flow field generator")

    parser.add_argument("--width", default=800, type=int, help="Width of the image")
    parser.add_argument("--height", default=800, type=int, help="Height of the image")
    parser.add_argument(
        "--perlin_factor_w", default=2, type=int, help="Perlin factor for width"
    )
    parser.add_argument(
        "--perlin_factor_h", default=2, type=int, help="Perlin factor for height"
    )
    parser.add_argument("--step", default=0.001, type=int, help="Step value")
    parser.add_argument("--color", default=100, type=str, help="Color option")
    parser.add_argument("--scale", default=2, type=float, help="Scale value")

    args = parser.parse_args()

    generate_image(
        width=args.width,
        height=args.height,
        color=args.color,
        perlinFactorW=args.perlin_factor_w,
        perlinFactorH=args.perlin_factor_h,
        step=args.step,
        scale=args.scale,
    )
