import os
import shutil
from pathlib import Path

from PIL import Image
import argparse

# C:\Users\vince\src\comicut\venv\Scripts\python.exe main.py C:\Users\vince\iCloudDrive\dessins\


def slice_image(source_image_path, number_cols_rows, margin):
    base_path = os.path.dirname(source_image_path)
    image_name = source_image_path.stem
    image_suffix = source_image_path.suffix
    i = Image.open(source_image_path)
    width = i.width
    height = i.height
    pieces = 0

    filenames = []
    for y in range(number_cols_rows):
        for x in range(number_cols_rows):
            index = pieces
            pieces = pieces + 1

            img = i.crop((x * width / number_cols_rows, y * height / number_cols_rows, x * width / number_cols_rows + width / number_cols_rows, y * height / number_cols_rows + height / number_cols_rows))

            result = Image.new(img.mode, (int(width / number_cols_rows) + int(margin / number_cols_rows), int(height / number_cols_rows) + int(margin / number_cols_rows)), (255, 255, 255))

            result.paste(img, (x * int(margin / 2), y * int(margin / 2)))

            filenames.append(f"{image_name}_p{index + 1}{image_suffix}")
            result.save(Path(f"{base_path}/{image_name}_p{index + 1}{image_suffix}"))
    return filenames


def copy_files(file_names, base_path, destination_path):
    # Ensure the destination directory exists
    os.makedirs(destination_path, exist_ok=True)

    for file_name in file_names:
        # Construct the full file path
        src_file = os.path.join(base_path, file_name)
        dest_file = os.path.join(destination_path, file_name)

        try:
            shutil.copy(src_file, dest_file)
            print(f"Copied {file_name} to {destination_path}")
        except FileNotFoundError:
            print(f"File {file_name} not found in {base_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("split_image")
    parser.add_argument("source_image_path", help="The source image that will be split", type=str)
    args = parser.parse_args()

    print("Splitting image...")
    filenames = slice_image(Path(args.source_image_path), 2, 60)
    print("Finished splitting image.")

    # print("Copying files to TikTok folder")
    # copy_files(filenames, os.path.dirname(Path(args.source_image_path)), Path("G:\\My Drive\\for tiktok"))
    # print("Files copied.")

    filenames.append(Path(args.source_image_path).name)
    print(filenames)
    print("Copying files to iCloud Photos")
    copy_files(filenames, os.path.dirname(Path(args.source_image_path)), Path("C:\\Users\\vince\\Pictures\\iCloud Photos\\Photos"))
    print("Files copied.")
