from PIL import Image, ImageOps
from math import floor

def resize_image(img_path : str, output_path : str, output_bounding_box_size : int, output_image_size : int):
    im = Image.open(img_path)
    current_size = im.size

    ratio = float(output_bounding_box_size)/max(current_size)
    new_size = tuple([int(x * ratio) for x in current_size])

    im = im.resize(new_size, Image.BICUBIC)

    # now figure out padding and paste box
    new_width = new_size[0]
    new_height = new_size[1]

    horz_padding = floor(float(output_image_size - new_width) / 2.0)
    vert_padding = floor(float(output_image_size - new_height) / 2.0)

    new_img = Image.new("RGBA", tuple([output_image_size, output_image_size]), tuple([0, 0, 0, 0]))

    # left, top, right bottom
    paste_box = tuple([horz_padding, vert_padding, horz_padding + new_width, vert_padding + new_height])
    new_img.paste(im, paste_box)
    
    new_img.save(output_path)

# testing code
# image_path = 'images/monsters/anjanath.png'

# output_bb_box = 400
# output_image_size = 512

# resize_image(image_path, 'images/monsters/anjanath-output.png', output_bb_box, output_image_size)