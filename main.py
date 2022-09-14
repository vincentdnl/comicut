from PIL import Image


def slice_image(filename, N, splitbetween):
    i = Image.open(filename)
    width = i.width
    height = i.height
    pieces = 0
    for y in range(N):
        for x in range(N):
            index = pieces
            pieces = pieces + 1

            img = i.crop((x * width/N, y * height/N, x * width/N + width/N, y * height/N + height/N))

            result = Image.new(img.mode, (int(width/N)+int(splitbetween/N), int(height/N)+int(splitbetween/N)), (255, 255, 255))

            result.paste(img, (x*int(splitbetween/2), y*int(splitbetween/2)))

            result.save(f"{filename}_sliced_{index}.jpeg")


if __name__ == '__main__':
    slice_image('comic.png', 2, 60)
