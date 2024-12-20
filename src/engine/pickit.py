from time import sleep
from random import randint, uniform
from pydirectinput import leftClick

from helper import image_helper, logging_helper


IMAGE_DIR = ".\\assets\\pickit\\"


def get_ref_location(ref_img):
    """
    Sucht ein Referenzbild und gibt die x, y-Koordinaten zurück.
    Parameters:
        ref_img (str): Der Dateiname des Referenzbildes.
    Returns:
        tuple: Die x, y-Koordinaten des Bildes, oder (-1, -1) bei Nichtauffindbarkeit.
    """
    x, y = image_helper.locate_needle(IMAGE_DIR + ref_img, loctype='c', region=(400, 50, 1500, 870))
    return x, y


def randomized_left_click(x=None, y=None, a=-5, b=35, c=-5, d=5):
    """
    Führt einen zufälligen Linksklick durch, um menschliches Verhalten zu simulieren.
    Parameters:
        x (int): x-Koordinate des Klicks (optional).
        y (int): y-Koordinate des Klicks (optional).
        a, b, c, d (int): Zufallsspanne für den Offset des Klicks.
    """
    if x is None or y is None:
        leftClick()
    else:
        fx = x + randint(a, b)
        fy = y + randint(c, d)
        leftClick(fx, fy)


def pick_it():
    """
    Sucht nach Beute und versucht, diese aufzuheben.
    Returns:
        bool: True, wenn ein Item erfolgreich aufgehoben wurde, False andernfalls.
    """
    item_images = ["a.png", "e.png", "i.png", "o.png", "u.png", "ancestral.png", "cinder.png"]
    item_colors = [
        [1, 4, 248, 128, 5, 50],  # Farbe für Item 1
        [1, 4, 216, 166, 120, 50],  # Farbe für Item 2
        [1, 4, 234, 236, 10, 50],  # Farbe für Item 3
        [1, 4, 215, 164, 198, 50]  # Farbe für Item 4
    ]

    for i, item_image in enumerate(item_images):
        x, y = get_ref_location(item_image)

        if x > -1 and y > -1:
            # Definiere den Farbbereich für das Item basierend auf dem Index
            color_checks = item_colors if i < len(item_colors) else []

            for color in color_checks:
                offset_x, offset_y, r, g, b, tolerance = color
                if image_helper.pixel_matches_color(x + offset_x, y + offset_y, r, g, b, tolerance):
                    randomized_left_click(x + 12, y + 3, -2, 18, -2, 2)
                    logging_helper.log_info(f"Picked item at coords {x}, {y}")
                    sleep(uniform(1.5, 2.5))
                    return True

    return False
