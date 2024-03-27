import os
import sys
from PIL import Image, ImageOps, ExifTags

# write a code to modify all images within a folder
# image size 600*400px
# default backgroud color is #000000
# image output format is jpg
# image output quality is 50%
# image should not be streached

def resize_image(image_path, output_path, size=(600, 400), color=(0, 0, 0), format='JPEG', quality=50):
    image = Image.open(image_path)

    # Fix orientation using EXIF data
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # In case the image doesn't have EXIF data
        pass

    # Resize the image without cropping
    image.thumbnail(size, Image.ANTIALIAS)

    # Create a new image with the desired size and black background
    new_image = Image.new('RGB', size, color)

    # Calculate the position to paste the image onto the new image
    position = ((new_image.width - image.width) // 2, (new_image.height - image.height) // 2)

    # Paste the image onto the new image
    new_image.paste(image, position)

    # Convert RGBA images to RGB
    if new_image.mode in ('RGBA', 'LA'):
        background = Image.new(new_image.mode[:-1], new_image.size, color)
        background.paste(new_image, new_image.split()[-1])
        new_image = background

    new_image.save(output_path, format=format, quality=quality)



# Usage: python script.py <input_folder> <output_folder>
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python script.py <input_folder> <output_folder>')
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.JPG'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path)
            print(f'{filename} resized successfully')
