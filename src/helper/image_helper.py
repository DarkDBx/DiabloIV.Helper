import os
from pyautogui import screenshot, locate, locateOnScreen, locateCenterOnScreen, ImageNotFoundException
from numpy import array as npArray
from cv2 import cvtColor, inRange, Canny, findContours, arcLength, approxPolyDP, boundingRect
from cv2 import RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, COLOR_BGR2HSV
from PIL import ImageGrab
from math import sqrt

from helper import mouse_helper, logging_helper

def get_pixel_color_at_cursor():
    """
    Get the color of the pixel under the cursor.
    Returns:
        tuple: (x, y, r, g, b) - Cursor coordinates and pixel color.
    """
    x, y = mouse_helper.position()
    r, g, b = screenshot().getpixel((x, y))
    return x, y, r, g, b

def get_pixel_color_at_coords(x, y):
    """
    Get the color of the pixel at coordinates.
    Returns:
        tuple: (r, g, b) - Pixel color.
    """
    r, g, b = screenshot().getpixel((x, y))
    return r, g, b

def save_image(region, name, path):
    """
    Save a screenshot of a specific region to a file.
    Parameters:
        region (tuple): (x, y, width, height) - The region to capture.
        name (str): Name of the saved file.
        path (str): Directory where the file will be saved.
    """
    os.makedirs(path, exist_ok=True)  # Ensure the path exists
    img = screenshot(region=region)
    filepath = os.path.join(path, f"{name}.png")
    img.save(filepath)


def get_image_at_cursor(ix=10, iy=10, name='default', path='./assets/skills/'):
    """
    Capture an image around the cursor position.
    Parameters:
        ix (int): Width of the image.
        iy (int): Height of the image.
        name (str): Name of the saved image file.
        path (str): Directory to save the image.
    Returns:
        tuple: (x, y) - Cursor coordinates.
    """
    x, y = mouse_helper.position()
    save_image((x, y, ix, iy), name, path)
    return x, y


def get_image_at_coords(x, y, ix=10, iy=10, name='default', path='./assets/skills/'):
    """
    Capture an image at specified coordinates.
    Parameters:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        ix (int): Width of the image.
        iy (int): Height of the image.
        name (str): Name of the saved image file.
        path (str): Directory to save the image.
    Returns:
        tuple: (x, y) - Coordinates of the captured image.
    """
    save_image((int(x), int(y), ix, iy), name, path)
    return x, y


def pixel_matches_color(x, y, exR, exG, exB, tolerance=25):
    """
    Check if a pixel matches the expected RGB color within a tolerance.
    Parameters:
        x (int): X-coordinate of the pixel.
        y (int): Y-coordinate of the pixel.
        exR (int): Expected red value.
        exG (int): Expected green value.
        exB (int): Expected blue value.
        tolerance (int): Allowed deviation for each color channel.
    Returns:
        bool: True if the pixel matches the color, False otherwise.
    """
    r, g, b = screenshot().getpixel((x, y))
    return all(abs(actual - expected) <= tolerance for actual, expected in zip((r, g, b), (exR, exG, exB)))

def detect_lines(line_type='path'):
    """
    Detect narrow, curved lines of a given type ('path' or 'mob') by specified color on the screen.
    Returns the coordinates of bounding boxes of detected lines or None if none are found.
    """
    # Define configurations for different line types
    line_config = {
        'path': {
            'array_min': npArray([95, 95, 95]),     # Color min for 'path'
            'array_max' : npArray([125, 125, 125]), # Color max for 'path'
            'screen_box': (1675, 75, 1825, 225)     # Screen region for 'path' (x, y, w, h)
        },
        'mob': {
            'array_min': npArray([0, 0, 0]),    # Color min for 'mob'
            'array_max': npArray([5, 5, 5]),    # Color max for 'mob'
            'screen_box': (550, 125, 1350, 825) # Screen region for 'mob' (x, y, w, h)
        }
    }

    config = line_config[line_type]

    # Capture the region of the screen defined by screen_box
    image_grab = ImageGrab.grab(bbox=config['screen_box'])
    np_array = npArray(image_grab)
    
    # Convert image from RGB to HSV (for better color range handling)
    hsv = cvtColor(np_array, COLOR_BGR2HSV)
    
    # Create mask based on the defined color range
    mask = inRange(hsv, config['array_min'], config['array_max'])
    
    # Apply Canny edge detection
    edges = Canny(mask, 100, 200)

    # Find contours in the detected edges
    contours, _ = findContours(edges, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

    screen_center_x = config['screen_box'][0] + (config['screen_box'][2] // 2)
    screen_center_y = config['screen_box'][1] + (config['screen_box'][3] // 2)
    min_distance = float('inf')
    closest_contour = None

    for contour in contours:
        # Approximate the contour to reduce noise
        epsilon = 0.01 * arcLength(contour, True)
        approx = approxPolyDP(contour, epsilon, True)
        x, y, w, h = boundingRect(contour)

        # Calculate the distance from the center of the bounding box to the center of the screen region
        contour_center_x = x + (w // 2)
        contour_center_y = y + (h // 2)
        distance = sqrt((contour_center_x - screen_center_x) ** 2 + (contour_center_y - screen_center_y) ** 2)

        # Handle curved lines for 'path'
        if line_type == 'path' and len(approx) > 1:  # Curved line: More than specified number vertices
            if distance < min_distance:
                min_distance = distance
                closest_contour = (x, y, w, h)
                logging_helper.log_info(f"Detected curved line ('path') at ({x}, {y}), ({x + w}, {y + h})")

        # Handle straight lines for 'mob'
        elif line_type == 'mob' and w >= 20 and h >= 1 and h <= 4: # Straight line: Minimum width and height
            if distance < min_distance:
                min_distance = distance
                closest_contour = (x, y, w, h)
                logging_helper.log_info(f"Detected straight line ('mob') at {x}, {y}, {w}, {h}")
    
    if closest_contour:
        logging_helper.log_info(f"Closest contour to center: {closest_contour}")
        return closest_contour
    else:
        return None

def locate_needle(
    needle,
    haystack=None,
    conf=0.8,
    loctype='l',
    grayscale=True,
    region=(525, 875, 1380, 1050)
):
    """
    Searches the haystack image or the screen for the needle image.
    Returns the coordinates of the needle, or a boolean if no coordinates are required.

    Parameters:
        needle (str): Path to the image to find.
        haystack (str, optional): Path to the image in which to search. Defaults to None.
        conf (float): Confidence level for the image match. Defaults to 0.8.
        loctype (str): Type of search ('l' for locate, 'c' for center). Defaults to 'l'.
        grayscale (bool): Whether to use grayscale for the search. Defaults to True.
        region (tuple): Region of the screen to search (x, y, width, height). Defaults to (525, 875, 1380, 1050).

    Returns:
        tuple or bool: Coordinates of the needle, or True/False based on search result.
    """
    def log_result(found, context, result=None):
        """Helper to log results consistently."""
        if found:
            logging_helper.log_debug(f"Found {context}: {needle}, {result}")
        else:
            logging_helper.log_debug(f"Cannot find {context}: {needle}, conf={conf}, result={result}")

    if haystack is not None:  # Search in haystack
        try:
            locate_var = locate(needle, haystack, confidence=conf, grayscale=grayscale)
            log_result(True, "needle in haystack", locate_var)
            return locate_var
        except ImageNotFoundException:
            log_result(False, "needle in haystack")
            return (-1, -1)

    # Screen search (loctype-based)
    if loctype == 'l':  # Locate without returning coordinates
        try:
            locate_var = locateOnScreen(needle, minSearchTime=0.1, confidence=conf, region=region, grayscale=grayscale)
            log_result(True, "'l' image", locate_var)
            return True
        except ImageNotFoundException:
            log_result(False, "'l' image")
            return False

    if loctype == 'c':  # Locate and return coordinates
        try:
            locate_var = locateCenterOnScreen(needle, minSearchTime=0.1, confidence=conf, region=region, grayscale=grayscale)
            log_result(True, "'c' image", locate_var)
            return locate_var
        except ImageNotFoundException:
            log_result(False, "'c' image")
            return (-1, -1)

    raise ValueError(f"Invalid loctype '{loctype}'. Must be 'l' or 'c'.")
