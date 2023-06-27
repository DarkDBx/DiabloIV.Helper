from logging import debug
from pyautogui import screenshot, pixelMatchesColor, locate, locateOnScreen, locateCenterOnScreen
from numpy import linspace, meshgrid, vstack
from itertools import product

from helper import input_helper


def get_pixel_color_at_cursor():
    """Get the color of per cursor selected pixel"""
    x, y = input_helper.position()
    r, g, b = screenshot().getpixel((x, y))

    return x, y, r, g, b


def get_image_at_cursor(name='default', path='.\\assets\\skills\\', ix=25, iy=25):
    """Get the image of per cursor selected pixel"""
    x, y = input_helper.position()
    img = screenshot(region=(x,y, ix, iy))
    img.save(path + name + ".png")

    return x, y


def pixel_matches_color(x, y, exR, exG, exB, tolerance=25):
    """Get rgb color at coordinate"""
    r, g, b = screenshot().getpixel((x, y))
    if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
        return True
    return False


def coord_matches_color_rect():
    """Get a set rgb color at a rectangle around the minimap player position"""
    points_x = linspace(1720,1780,40, dtype=int)
    points_y = linspace(120,180,40, dtype=int)
    grid_x, grid_y = meshgrid(points_x, points_y, copy=False, sparse=True)
    positions = vstack([grid_x.ravel(), grid_y.ravel()])

    for x, y in product(positions[0], positions[1]):
        if (x == min(points_x)) | (x == max(points_x)) | \
                (y == min(points_y)) | (y == max(points_y)):
            if pixelMatchesColor(x.item(), y.item(), (104,74,56), tolerance=5):
                return x, y
    return -1, -1
    

def mob_detection():
    """Get mob type and position"""
    x, y = locate_needle('.\\assets\\target\\elite.png', conf=0.97, loctype='c', region=(400,140,1500,870))
    if x != -1 and y != -1:
        return x, y
    x, y = locate_needle('.\\assets\\target\\normal.png', conf=0.97, loctype='c', region=(400,140,1500,870))
    if x != -1 and y != -1:
        return x, y
    x, y = locate_needle('.\\assets\\target\\normal_shield.png', conf=0.97, loctype='c', region=(400,140,1500,870))
    if x != -1 and y != -1:
        return x, y
    return False


def locate_needle(needle, haystack=0, conf=0.8, loctype='l', grayscale=True, region=(525,875,1380,1050)):
    """Searches the haystack image for the needle image, returning a tuple
    of the needle's coordinates within the haystack. If a haystack image is
    not provided, searches the client window or the overview window,
    as specified by the loctype parameter."""
    
    # with haystack image, return coordinates
    if haystack != 0:
        locate_var = locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            debug('found needle ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)))
            return locate_var
        else:
            debug('cant find needle ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)) + ', conf=' + (str(conf)))
            return -1, -1
        
    # without haystack image, return 1 or 0
    elif loctype == 'l':  # 'l' for regular 'locate'
        locate_var = locateOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            debug('found l image ' + (str(needle)) + ', ' + (str(locate_var)))
            # If the center of the image is not needed, don't return any coordinates.
            return True
        elif locate_var is None:
            debug('cannot find l image ' + (str(needle)) + ' conf=' + (str(conf)))
            return False
        
    # without haystack image, return coordinates
    elif loctype == 'c':  # 'c' for 'center'
        locate_var = locateCenterOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            debug('found c image ' + (str(needle)) + ', ' + (str(locate_var)))
            # Return the xy coordinates for the center of the image, relative to the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            debug('cannot find c image ' + (str(needle)) + ', conf=' + (str(conf)))
            return -1, -1

