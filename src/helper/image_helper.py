import math
import logging
import pyautogui

from helper import input_helper


def get_pixel_color_at_cursor():
    """Get the color of per cursor selected pixel"""
    x, y = input_helper.position()
    r, g, b = pyautogui.screenshot().getpixel((x, y))
    return x, y, r, g, b

def get_image_at_cursor(name='default.png', path='.\\assets\\', ix=25, iy=25):
    """Get the image of per cursor selected pixel"""
    x, y = input_helper.position()
    img = pyautogui.screenshot(region=(x,y, ix, iy))
    img.save(path+name)
    return x, y

def pixel_matches_color(x, y, exR, exG, exB, tolerance=25):
    r, g, b = pyautogui.screenshot().getpixel((x, y))
    if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
        #logging.debug('found '+r, g, b+' at '+ x, y)
        return True
    return False
    
def calculate_distance():
    location = locate_needle('.\\assets\\target.png', loctype='c')
    if location != 0:
        dist = math.sqrt((location[1] - 960)**2 + (location[2] - 740)**2)
        logging.debug('found '+dist+' at '+location)
        return dist

def locate_needle(needle, haystack=0, conf=0.7, loctype='l', grayscale=True, region=(580, 880, 1333, 1066)):
    """Searches the haystack image for the needle image, returning a tuple
    of the needle's coordinates within the haystack. If a haystack image is
    not provided, searches the client window or the overview window,
    as specified by the loctype parameter.
    parameters:
        needle: The image to search for. Must be a PIL image object.
        haystack: The image to search within. By default this is not set,
                causing the mlocate function to capture and search the client
                window.
        conf: The confidence value required to match the image successfully.
                By default this is 0.8.
        loctype: The method and/or haystack used to search for images. If a
                haystack is provided, this parameter is not used.
            l: Search the client window. If the needle is found, return '1'.
            c: Search the client window for the needle and obtain its xy center
                coordinates. If the needle is found, return the coordinates of its
                center, relative to the coordinate plane of the haystack's resolution.
        grayscale: Convert the haystack to grayscale before searching within it. Speeds up
                searching by about 30%. Defaults to True.
        region: The region to search within.
                By default this is about the region around the skill bar."""
    # with haystack image, return coordinates
    if haystack != 0:
        locate_var = pyautogui.locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found needle  ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)))
            return locate_var
        else:
            logging.debug('cant find needle  ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)) + ', conf=' + (str(conf)))
            return 0
    # without haystack image, return 1 or 0
    elif loctype == 'l':  # 'l' for regular 'locate'
        locate_var = pyautogui.locateOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found l image ' + (str(needle)) + ', ' + (str(locate_var)))
            # If the center of the image is not needed, don't return any coordinates.
            return 1
        elif locate_var is None:
            logging.debug('cannot find l image ' + (str(needle) + ' conf=' + (str(conf))))
            return 0
    # without haystack image, return coordinates
    elif loctype == 'c':  # 'c' for 'center'
        locate_var = pyautogui.locateCenterOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found c image ' + (str(needle)) + ', ' + (str(locate_var)))
            # Return the xy coordinates for the center of the image, relative to the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find c image ' + (str(needle) + ', conf=' + (str(conf))))
            return 0

