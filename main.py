import os
from pathlib import Path

from PIL import Image
import argparse


def slice_image(source_image_path, number_cols_rows, margin):
    base_path = os.path.dirname(source_image_path)
    image_name = source_image_path.stem
    image_suffix = source_image_path.suffix
    i = Image.open(source_image_path)
    width = i.width
    height = i.height
    pieces = 0
    for y in range(number_cols_rows):
        for x in range(number_cols_rows):
            index = pieces
            pieces = pieces + 1

            img = i.crop((x * width / number_cols_rows, y * height / number_cols_rows, x * width / number_cols_rows + width / number_cols_rows, y * height / number_cols_rows + height / number_cols_rows))

            result = Image.new(img.mode, (int(width / number_cols_rows) + int(margin / number_cols_rows), int(height / number_cols_rows) + int(margin / number_cols_rows)), (255, 255, 255))

            result.paste(img, (x * int(margin / 2), y * int(margin / 2)))

            result.save(Path(f"{base_path}/{image_name}_p{index + 1}{image_suffix}"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("split_image")
    parser.add_argument("source_image_path", help="The source image that will be split", type=str)
    args = parser.parse_args()

    slice_image(Path(args.source_image_path), 2, 60)
