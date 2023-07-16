from logging import info
from time import sleep
from random import randint

from helper import process_helper, input_helper, image_helper, config_helper
from engine import combat, pather, pickit


class Bot:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()
        self.proc = process_helper.ProcessHelper()
    

    def set_window_pos(self):
        '''Move the window to 0, 0 and put it on top'''
        self.proc.set_window_pos()


    def set_foreground(self):
        '''Set to foreground window'''
        self.proc.set_foreground_window()


    def is_right_color(self, x,y, r=0,g=0,b=0, tol=25):
        return image_helper.pixel_matches_color(x,y, r,g,b, tolerance=tol)


    def is_on_landing(self):
        return (self.is_right_color(3,2, 22,30,31) and self.is_right_color(491,888, 18,17,18))


    def is_on_menu(self):
        return self.is_right_color(3,2, 22,30,31)


    def is_on_loading(self):
        return self.is_right_color(1,1)


    def is_in_game(self):
        return self.is_right_color(721,994, 56,76,84)


    def is_death(self):
        return self.is_right_color(778,810, 233,233,233)


    def is_bad_connect(self):
        return self.is_right_color()


    def is_death(self):
        return (self.is_right_color(748,812, 14,15,14) and self.is_right_color(1007,869, 26,0,0))


    def click_is_death_ok(self):
        sleep(3)
        self.left_click(904,924)
        sleep(.5)


    def click_start_game(self):
        sleep(1)
        self.left_click(151,835)


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


    def loot_process(self, j=30):
        for i in range(j):
            if not pickit.pick_it():
                break


    def wait_for_loading(self):
        sleep(1)
        while self.is_on_loading():
            sleep(0.5)
        sleep(2)
    

    def game_manager(self, move=True, loot=False):
        '''Game handling routine'''
        if self.is_death():
            info('Death state')
            self.click_is_death_ok()
            self.wait_for_loading()
        elif self.is_in_game():
            info('Game state')
            if move == True:
                pather.move_to_ref_location()
            mob = image_helper.line_detection('mob')
            if mob != False:
                input_helper.mouseUp()
                x, y = mob
                combat.rotation(x, y)
                self.game_manager(False, True)
            elif loot:
                self.loot_process()
                
