from logging import info
from time import sleep
from random import randint, uniform

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
        return (self.is_right_color(718,984, 59,75,84) and self.is_right_color(1209,966, 56,76,81))


    def is_death(self):
        return self.is_right_color(778,810, 233,233,233)


    def is_bad_connect(self):
        return self.is_right_color()


    def is_death(self):
        return (self.is_right_color(748,812, 14,15,14) and self.is_right_color(1007,869, 26,0,0))


    def click_is_death_ok(self):
        sleep(uniform(1.5, 2.5))
        self.left_click(904, 924)
        sleep(uniform(.5, .8))


    def click_start_game(self):
        sleep(uniform(1.5, 2.5))
        self.left_click(151, 835)
        sleep(uniform(.5, .8))


    def click_teleport(self):
        sleep(uniform(1.5, 2.5))
        self.left_click()
        sleep(uniform(.5, .8))


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


    def right_click(self, x=None, y=None, a=1,b=4,c=1,d=4):
        '''Randomized left click'''
        if x == None or y == None:
            input_helper.rightClick()
        else:
            ex = randint(a, b)
            fx = x + ex
            ey = randint(c, d)
            fy = y + ey
            input_helper.rightClick(fx, fy)


    def key_press(self, keys):
        input_helper.press(keys)


    def loot_process(self, j=30):
        for i in range(j):
            if not pickit.pick_it():
                break


    def wait_for_loading(self):
        sleep(uniform(1.5, 2.5))
        while self.is_on_loading():
            sleep(uniform(.5, .8))
        sleep(uniform(1.5, 2.5))

    
    def get_helltide_loc(self):
        self.key_press('m')
        input_helper.mouseScroll(-15)
        sleep(uniform(.5, .8))
        input_helper.mouseScroll(2)
        screen_region = (400, 50, 1500, 870)
        helltide_area = image_helper.locate_needle('.\\assets\\helltide_zoom.png', conf=0.8, region=screen_region)

        if helltide_area:
            x, y = image_helper.locate_needle('.\\assets\\treasure1.png', conf=0.8, loctype='c', region=screen_region)
            x2, y2 = image_helper.locate_needle('.\\assets\\treasure2.png', conf=0.8, loctype='c', region=screen_region)

            if x != -1 and y != -1:
                self.right_click(x, y)
                info("Found armor treasure, moving to map position %d,%d" % (x, y))
            elif x2 != -1 and y2 != -1:
                self.right_click(x2, y2)
                info("Found jewellery treasure, moving to map position %d,%d" % (x2, y2))
        else:
            input_helper.mouseScroll(-2)
            input_helper.centerMap()
            x, y = image_helper.locate_needle('.\\assets\\helltide.png', conf=0.8, loctype='c', region=screen_region)

            if x != -1 and y != -1:
                x2, y2 = image_helper.locate_needle('.\\assets\\waypoint.png', conf=0.8, loctype='c', region=(x-150, y-150, x+150, y+150))

                if x2 != -1 and y2 != -1:
                    self.left_click(x2,y2, 1,4,1,4)
                    info("Found helltide, moving to map position %d,%d" % (x2, y2))
                    #self.click_teleport()
        
        sleep(uniform(1.5, 2.5))
        self.key_press('m')
                
    

    def game_manager(self, move=True, loot=False):
        '''Game handling routine'''
        if self.is_death():
            info('Death state')
            self.click_is_death_ok()
            self.wait_for_loading()
        elif self.is_in_game():
            info('Game state')
            if move == True:
                move_to = pather.move_to_ref_location()
                if move_to == False:
                    self.get_helltide_loc()
            mob = image_helper.line_detection('mob')
            if mob != False:
                x, y = mob
                combat.rotation(x, y)
                self.game_manager(False, True)
            elif loot:
                self.loot_process()
                
