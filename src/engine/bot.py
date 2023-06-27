from logging import info, debug
from time import sleep
from random import randint
from functools import wraps

from helper import process_helper, input_helper, image_helper, config_helper
from engine import combat


# region constant
IMAGE_DIR = ".\\assets\\"
PLAYER_X = 960 # Center of the screen coordinate X
PLAYER_Y = 520 # Center of the screen coordinate Y
MAP_X = 1690
MAP_Y = 90
MAP_X_MAX = 1810
MAP_Y_MAX = 210
# endregion


def stuck_check(func):
    n = [0]

    @wraps(func)
    def decorated(*args, **kwargs):
        if n[0] > 10:
            debug("****Character is stuck, try to escape****")
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


class Bot:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()
        self.ph = process_helper.ProcessHelper()
    

    def set_window_pos(self):
        '''Move the window to 0, 0 and put it on top'''
        self.ph.set_window_pos()


    def set_foreground(self):
        '''Set to foreground window'''
        self.ph.set_foreground_window()


    def is_right_color(self, x, y, r=0, g=0, b=0, tol=25):
        return image_helper.pixel_matches_color(x, y, r, g, b, tolerance=tol)


    def is_on_landing(self):
        return self.is_right_color()


    def is_on_menu(self):
        return self.is_right_color()


    def is_on_loading(self):
        return self.is_right_color(1,1, 0,0,0)


    def is_in_game(self):
        return self.is_right_color(721,994, 56,76,84)


    def is_death(self):
        return self.is_right_color(778,810, 233,233,233)


    def click_is_death_ok(self):
        sleep(3)
        self.left_click(904,924)
        sleep(.5)


    def left_click(self, x=None, y=None, a=-5,b=35,c=-5,d=5):
        '''Randomized left click'''
        if x == None or y == None:
            input_helper.leftClick()
        else:
            ex = randint(a, b)
            fx = x + ex
            ey = randint(c, d)
            fy = y + ey
            input_helper.leftClick(fx, fy)


    def key_press(self, keys):
        input_helper.press(keys)


    def get_ref_location(self, ref_img, conf=0.8, region=(200,50,1575,900)):
        x, y = image_helper.locate_needle(IMAGE_DIR + ref_img, conf=conf, loctype='c', region=region)
        return x, y


    def get_player_ref_location(self, trans=False):
        '''Detect path on minimap and calculate player position'''
        n = 60
        x, y = self.get_ref_location('target\\path01.png', conf=0.975, region=(MAP_X,MAP_Y,MAP_X_MAX,MAP_Y_MAX))
        if x == -1 and y == -1:
            x, y = self.get_ref_location('target\\path02.png', conf=0.975, region=(MAP_X,MAP_Y,MAP_X_MAX,MAP_Y_MAX))
            if x == -1 and y == -1:
                x, y = self.get_ref_location('target\\path03.png', conf=0.975, region=(MAP_X,MAP_Y,MAP_X_MAX,MAP_Y_MAX))
                if x == -1 and y == -1:
                    x, y = self.get_ref_location('target\\path04.png', conf=0.975, region=(MAP_X,MAP_Y,MAP_X_MAX,MAP_Y_MAX))
                    """if x == -1 and y == -1:
                        n = 30
                        x, y = image_helper.coord_matches_color_rect()"""
        if x == -1 and y == -1:
            debug("Referenceobject not found: %d, %d" % (x, y))
            return -1, -1
        else:
            dx = (MAP_X+n)-x
            dy = (MAP_Y+n)-y
            if trans:
                return dx*10, dy*10
            else:
                return dx, dy


    @stuck_check
    def move_to_ref_location(self, stuck=False):
        '''Calculate distance to click for moving'''
        dx, dy = self.get_player_ref_location()
        if dx == -1 and dy == -1:
            return False
        distance = int(pow(dx**2+dy**2, 0.5))
        tx = dx if abs(dx) < 10 else dx*10
        ty = dy if abs(dy) < 10 else dy*10
        
        while abs(tx) > 1080 or abs(ty) > 360:
            tx = int(tx/1.5)
            ty = int(ty/1.5)
        debug("Relative coords %d, %d, distance %d, absolute coords %d, %d, get distance %s" %
            (dx, dy, distance, PLAYER_X-tx, PLAYER_Y-ty, distance > 10))
        if distance < 10:
            return False
        if not stuck:
            self.left_click(PLAYER_X-tx, PLAYER_Y-ty, 0,0,0,0)
            info("Moving to %d,%d" % (PLAYER_X-tx, PLAYER_Y-ty))
            return True
        else:
            info("Got stuck")
            return False


    def find_drops(self):
        '''Looking for some legendary/unique loot and get it'''
        item_array = [["pickit\\a.png", 1, 8, 232,119,5, 45],
                    ["pickit\\e.png", 1, 5, 245,127,5, 45],
                    ["pickit\\i.png", 2, 7, 248,128,5, 45],
                    ["pickit\\o.png", 2, 4, 240,124,6, 45],
                    ["pickit\\u.png", 1, 3, 248,128,5, 45]]
        for i in range(4):
            x, y = self.get_ref_location(item_array[i][0])
            color_value = self.is_right_color(x+item_array[i][1], 
                                            y+item_array[i][2],
                                            item_array[i][3],
                                            item_array[i][4],
                                            item_array[i][5],
                                            item_array[i][6])
            if (x > -1 and y > -1) and color_value == True:
                self.left_click(x+30,y+15, -2,8,-2,2)
                info('Picked item value ' + i + ' at coord ' + x, y)
                sleep(2)
                return True
        return False


    def loot_process(self, j=5):
        for i in range(j):
            if not self.find_drops():
                break


    def wait_for_loading(self):
        sleep(1)
        while self.is_on_loading():
            sleep(0.5)
        sleep(2)
    

    def game_manager(self, macro=False):
        '''Game handling routine'''
        if self.is_death():
            info('Death state')
            self.click_is_death_ok()
        elif self.is_in_game():
            info('Game state')
            if macro == False:
                if self.move_to_ref_location() == False:
                    self.left_click(PLAYER_X+randint(-20, 20), PLAYER_Y+randint(-20, 20), 0,0,0,0)
                    info("Looking for coords")
            mob_det = image_helper.mob_detection()
            if mob_det != False:
                info('Battle state')
                x, y = mob_det
                combat.rotation(x, y)
            self.loot_process()
                
