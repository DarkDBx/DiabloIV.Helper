import logging
import sys
import random
import time
import pyautogui
import logging

from helper import input_helper, config_helper


# pixel recognition confidence
conf = 0.5

# Total number of saved bookmark locations. This variable is set by the user.
total_sites = 10
unsuitable_site = 0
# Number of 'runs' completed by the mining script. This will always start
# at 1
runs_var = 1
playerfound = 0
# Tell the miner script if you're mining in the same
# system you're storing your ore in. 1 is yes, 0 is no.
system_mining = 1

# top left corner of the eve client window. This is necessary  because the image
# searching algorithm returns coordinates to the center of the image rather
# than its top right corner.
originx = 5
originy = 25

cfg = config_helper.read_config()
windowx = cfg['client_width']
windowy = cfg['client_height']

def mlocate(needle, haystack=0, conf=conf, loctype='l', grayscale=False):
    
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
            By default this is 0.95.
        
        loctype: The method and/or haystack used to search for images. If a
                haystack is provided, this parameter is not used.
        
            l: Search the client window. If the needle is found, return '1'.
            
            c: Search the client window for the needle and obtain its xy center
            coordinates. If the needle is found, return the coordinates of its
            center, relative to the coordinate plane of the haystack's resolution.
            
            o: Same as 'l', except searches only within the client's overview, assuming
            it's attached on the right side of the client window.
            
            oc: Same as 'c', but searches only within the client's overivew.
            
        grayscale: Convert the haystack to grayscale before searching within it. Speeds up
                searching by about 30%. Defaults to False."""
    
    if haystack != 0:
        locate_var = pyautogui.locate(needle, haystack, confidence=conf,
                                grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found needle  ' + (str(needle)) +
                        ' in haystack' + (str(haystack)) + ', ' +
                        (str(locate_var)))
            return locate_var
        else:
            logging.debug('cant find needle  ' + (str(needle)) +
                        ' in haystack' + (str(haystack)) + ', ' +
                        (str(locate_var)) + ', conf=' + (str(conf)))
            return 0

    if haystack == 0 and loctype == 'l':  # 'l' for regular 'locate'
        locate_var = pyautogui.locateOnScreen(needle, confidence=conf, region=(
            originx, originy, windowx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found l image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            # If the center of the image is not needed, don't return any
            # coordinates.
            return 1
        elif locate_var is None:
            logging.debug('cannot find l image ' + (
                    str(needle) + ' conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'c':  # 'c' for 'center'
        locate_var = pyautogui.locateCenterOnScreen(needle, confidence=conf, region=(
            originx, originy, windowx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found c image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            # Return the xy coordinates for the center of the image, relative to
            # the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find c image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'o':  # 'o' for 'overview'
        overviewx = (originx + (windowx - (int(windowx / 3))))
        overviewlx = (int(windowx / 3))
        locate_var = pyautogui.locateOnScreen(needle, confidence=conf, region=(
            overviewx, originy, overviewlx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found o image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            return 1
        elif locate_var is None:
            logging.debug('cannot find o image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'co':  # 'co' for 'center of overview'
        overviewx = (originx + (windowx - (int(windowx / 3))))
        overviewlx = (int(windowx / 3))
        locate_var = pyautogui.locateCenterOnScreen(needle, confidence=conf, region=(
            overviewx, originy, overviewlx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found co image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find co image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    else:
        logging.critical('incorrect function parameters')



def click_image(needle, haystack=0, loctype='c', button='left', rx1=0,
                rx2=0, ry1=0, ry2=0):
    """Moves the mouse to the provided needle image and clicks on it. If a
    haystack is provided, searches for the provided image within the
    haystack. If a haystack is not provided, searches within an area defined by
    the loctype parameter.
    parameters:
        needle: a filepath to the image to search for, relative to the
        script's working directory
        haystack: the image to search for the needle within. Must be a PIL
        image variable.
        loctype: if the haystack parameter is 0, this parameter is used to
        create a haystack.
            c: (default) searches client for the xy center of the needle.
            Returns x,y coordinates
            co: Searches the overview for the xy center of the needle.
        button: the mouse button to click when the script locates the image.
        rx1 / ry1: the minimum x/y value to generate a random variable from.
        rx2 / ry2: the maximum x/y/ value to generate a random variable from."""
    logging.debug('searching for and clicking on ' + (str(needle)))
    for tries in range(1, 10):
        target_image = mlocate(needle=needle, loctype=loctype,
                                  haystack=haystack)
        if target_image != 0 and target_image != 1:
            (x, y) = target_image
            input_helper.mo._move_to((x + (random.randint(rx1, rx2))),
                       (y + (random.randint(ry1, ry2))))
            if button == 'left':
                input_helper.leftClick()
            elif button == 'right':
                input_helper.rightClick()
            return 1

        elif target_image == 1:
            logging.error('loctype parameter incorrect, must use c or co')
            sys.exit()
        elif target_image == 0:
            logging.error('cant find image to click on ' + (str(needle)) + ', '
                          + (str(tries)))
            time.sleep(float(random.randint(500, 2000)) / 1000)

    logging.error('timed out looking for image to click ' + (str(needle)))
    return 0


def move_away(direction):
    """Moves the mouse to a random spot on right half or the left half of
    the client window, away from wherever it clicked,
    to prevent tooltips from interfering with the script."""
    time.sleep(float(random.randint(0, 500)) / 1000)
    if direction == 'r':
        print('right')
        input_helper.mo._move_to((random.randint(
            ((windowx - 100) - (windowx / 2)), (windowx - 100))),
            (random.randint(10, (windowy - 100))))
        time.sleep(float(random.randint(0, 500)) / 1000)
        return

    elif direction == 'l':
        print('left')
        input_helper.mo._move_to((random.randint(10, ((windowx - 100) - (windowx / 2)))),
                   (random.randint(10, (windowy - 100))))
        time.sleep(float(random.randint(0, 500)) / 1000)
        return


def move_to_neutral():
    """Moves the mouse to a 'neutral zone', away from any buttons or tooltop
    icons that could get in the way of the script. Designed for the miner()
    gui layout."""
    input_helper.mo._move_to((originx + (random.randint(50, 300))),
               (originy + (random.randint(300, 500))))
    return 1

