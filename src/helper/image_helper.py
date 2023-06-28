from logging import debug, info
from pyautogui import screenshot, locate, locateOnScreen, locateCenterOnScreen
from numpy import array, ndarray, pi
from cv2 import cvtColor, COLOR_BGR2HSV, inRange, Canny, HoughLinesP
from PIL import ImageGrab

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


def pixel_matches_color(x,y, exR,exG,exB, tolerance=25):
    """Get rgb color at coordinate"""
    r, g, b = screenshot().getpixel((x, y))
    if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
        return True
    return False


def path_detection():
    image_grab = ImageGrab.grab(bbox=(1650, 50, 1850, 250))
    np_array = array(image_grab)
    hsv = cvtColor(np_array, COLOR_BGR2HSV)
    mask = inRange(hsv, array([60, 180, 80]), array([120, 255, 140]))
    edges = Canny(mask, 50, 150, apertureSize=3, L2gradient=True)
    lines = HoughLinesP(image=edges, rho=1, theta=pi/15, threshold=15, lines=array([]), minLineLength=10, maxLineGap=30)
    mask_backup = inRange(hsv, array([40, 160, 60]), array([140, 255, 160]))
    edges_backup = Canny(mask_backup, 30, 90, apertureSize=5, L2gradient=True)
    lines_backup = HoughLinesP(image=edges_backup, rho=1, theta=pi/5, threshold=5, lines=array([]), minLineLength=5, maxLineGap=60)

    if type(lines) is ndarray:
        info('found path, 1st try')
        return lines[0][0][0], lines[0][0][1], lines[0][0][2], lines[0][0][3]
    elif type(lines_backup) is ndarray:
        info('found path, 2nd try')
        return lines_backup[0][0][0], lines_backup[0][0][1], lines_backup[0][0][2], lines_backup[0][0][3]
        
    return False


def mob_detection():
    image_grab = ImageGrab.grab(bbox=(400,140,1500,870))
    np_array = array(image_grab)
    hsv = cvtColor(np_array, COLOR_BGR2HSV)
    mask = inRange(hsv, array([110, 10, 0]), array([190, 40, 15]))
    edges = Canny(mask, 1, 3, apertureSize=3, L2gradient=True)
    lines = HoughLinesP(image=edges, rho=1, theta=pi/180, threshold=15, lines=array([]), minLineLength=7, maxLineGap=20)

    if type(lines) is ndarray:
        info('found mob')
        return lines[0][0][0], lines[0][0][1], lines[0][0][2], lines[0][0][3]
        
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

