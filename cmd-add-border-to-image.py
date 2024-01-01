#!/usr/bin/env python

from PIL import Image, ImageOps

def add_border(input_image_path, output_image_path, border_size, border_color):
    # Open the input image
    img = Image.open(input_image_path)

    # Add border
    img_with_border = ImageOps.expand(img, border=border_size, fill=border_color)

    # Save the result
    img_with_border.save(output_image_path)

# Example usage
input_path = 'docs/generic-example.png'
output_path = 'docs/generic-example.outlined.png'
border_size = 10  # Border size in pixels
border_color = 'grey'  # Border color

add_border(input_path, output_path, border_size, border_color)
