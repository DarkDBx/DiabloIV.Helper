from logging import info, debug
from time import sleep
from random import randint
from functools import wraps

from helper import process_helper, input_helper, image_helper, config_helper, timer_helper
from helper.timer_helper import TIMER_STOPPED
from engine import combat


# region constant
IMAGE_DIR = ".\\assets\\"
PLAYER_X = 960 # Center of the screen coordinate X
PLAYER_Y = 520 # Center of the screen coordinate Y
MAP_X = 1750
MAP_Y = 150
# endregion


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


class Bot:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()
        self.proc = process_helper.ProcessHelper()
        self.timer1 = timer_helper.TimerHelper('timer1')
    

    def set_window_pos(self):
        '''Move the window to 0, 0 and put it on top'''
        self.proc.set_window_pos()


    def set_foreground(self):
        '''Set to foreground window'''
        self.proc.set_foreground_window()


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


    def get_ref_location(self, ref_img, conf=0.8, grayscale=True, region=(200,50,1575,900)):
        x, y = image_helper.locate_needle(IMAGE_DIR + ref_img, conf=conf, loctype='c', grayscale=grayscale, region=region)
        return x, y


    def get_player_ref_location(self, trans=True):
        '''Detect path on minimap and calculate player position'''
        path = image_helper.path_detection()
                    
        if path == False:
            debug("Referenceobject not found")
            return -1, -1
        else:
            x, y = path
            x = (MAP_X-x)-1650
            y = (MAP_Y-y)-50
            if trans:
                return x*20, y*20
            else:
                return x, y


    @stuck_check
    def move_to_ref_location(self, stuck=False):
        '''Calculate distance to click for moving'''
        x, y = self.get_player_ref_location()
        if x == -1 and y == -1:
            return False
        
        while abs(x) > 1080 or abs(y) > 360:
            x = int(x/1.5)
            y = int(y/1.5)
        debug("Relative coords %d, %d, absolute coords %d, %d" % (x, y, PLAYER_X-x, PLAYER_Y-y))
        if not stuck:
            self.left_click(PLAYER_X-x, PLAYER_Y-y, 0,0,0,0)
            info("Moving to %d,%d" % (PLAYER_X-x, PLAYER_Y-y))
            return True
        else:
            self.left_click(PLAYER_X+randint(-150, 150), PLAYER_Y+randint(-150, 150), 0,0,0,0)
            info("Got stuck")
            return False


    def pick_it(self):
        '''Looking for some legendary/unique loot and get it'''
        item_image_array = [["pickit\\a.png"],
                        ["pickit\\e.png"],
                        ["pickit\\i.png"],
                        ["pickit\\o.png"],
                        ["pickit\\u.png"],
                        ["pickit\\ancestral.png"]]
        item_color_array = [[1, 4, 248,128,5, 75],
                        [1, 4, 216,166,120, 75]]
        for i in range(5):
            x, y = self.get_ref_location(item_image_array[i][0])
            if (x > -1 and y > -1):
                for j in range(1):
                    color_value = self.is_right_color(x+item_color_array[j][0], 
                                                    y+item_color_array[j][1],
                                                    item_color_array[j][2],
                                                    item_color_array[j][3],
                                                    item_color_array[j][4],
                                                    item_color_array[j][5])
                    if color_value == True:
                        break
        if (x > -1 and y > -1) and color_value == True:
            self.left_click(x+12,y+3, -2,8,-2,2)
            info('Picked item at coords ' + str(x) + str(y))
            sleep(2)
            return True
        return False


    def loot_process(self, j=9):
        for i in range(j):
            if not self.pick_it():
                break


    def wait_for_loading(self):
        sleep(1)
        while self.is_on_loading():
            sleep(0.5)
        sleep(2)
    

    def game_manager(self, move=True):
        '''Game handling routine'''
        if self.is_death():
            info('Death state')
            self.click_is_death_ok()
        elif self.is_in_game():
            info('Game state')
            if move == True:
                self.move_to_ref_location()
            mob = image_helper.mob_detection()
            if mob != False:
                x, y = mob
                combat.rotation(x+400, y+50)
                self.game_manager(False)
            elif self.timer1.GetTimerState() == TIMER_STOPPED:
                self.timer1.StartTimer(7)
                self.loot_process()
                
