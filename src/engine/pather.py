from logging import info, debug
from random import randint
from functools import wraps
from pydirectinput import leftClick, press

from helper import image_helper, config_helper


PLAYER_X = 960 # Center of the screen coordinate X
PLAYER_Y = 520 # Center of the screen coordinate Y
MAP_X = 1750
MAP_Y = 150


def stuck_check(func):
    n = [0]

    @wraps(func)
    def decorated(*args, **kwargs):
        if n[0] > 10:
            debug("***Character is stuck, try to escape***")
            n[0] = 0
            for i in range(2):
                func(*args, **kwargs, stuck=True)
            return True
        if func(*args, **kwargs):
            n[0] += 1
            return True
        else:
            n[0] = 0
            return False
    return decorated


def get_player_ref_location(trans=True):
    '''Detect path on minimap and calculate player position'''
    path = image_helper.line_detection()
                
    if path == False:
        debug("Referenceobject not found")
        return -1, -1
    else:
        x, y = path
        x = (MAP_X-x)-1650
        y = (MAP_Y-y)-50

        if trans:
            return x*5, y*5
        else:
            return x, y


@stuck_check
def move_to_ref_location(stuck=False):
    cfg = config_helper.read_config()
    evade_var = cfg['evade']

    if image_helper.locate_needle('.\\assets\\skills\\climb.png', conf=0.8, region=(500, 300, 1500, 870)):
        press(evade_var)
        
    '''Calculate distance to click for moving'''
    x, y = get_player_ref_location()
    
    if x == -1 and y == -1:
        return False

    debug("Relative coords %d, %d, absolute coords %d, %d" % (x, y, PLAYER_X-x, PLAYER_Y-y))

    if not stuck:
        leftClick(PLAYER_X-x, PLAYER_Y-y)
        info("Moving to %d,%d" % (PLAYER_X-x, PLAYER_Y-y))
        return True
    else:
        leftClick(PLAYER_X-randint(-250, 250), PLAYER_Y-randint(-250, 250))
        info("Got stuck, do random move")
        return False

