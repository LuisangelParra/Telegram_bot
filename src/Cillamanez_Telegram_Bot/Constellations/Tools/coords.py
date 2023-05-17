def coords_to_pixel(orig_x, orig_y, size):
    """
    Given the x and y coordinates of a star (original_x and original_y), 
    and the size in pixels of the picture, return the x, y location 
    of the star in terms of pixels in the picture.
    """
    # Convert the original coordinates to pixel coordinates
    pixel_x = float((float(orig_x) + 1) * size / 2)
    pixel_y = float((1 - float(orig_y)) * size / 2)
    # Return the pixel coordinates
    return pixel_x, pixel_y

# Path: src\Tools\coords.py
