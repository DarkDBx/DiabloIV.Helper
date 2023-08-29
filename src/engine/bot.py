from logging import info
from time import sleep
from random import randint, uniform
from pydirectinput import leftClick, rightClick, press

from helper import mouse_helper, image_helper, config_helper
from engine import combat, pather, pickit


class Bot:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()


    def is_on_landing(self):
        return (image_helper.pixel_matches_color(3,2, 22,30,31) and image_helper.pixel_matches_color(491,888, 18,17,18))


    def is_on_menu(self):
        return (image_helper.pixel_matches_color(74,314, 235,8,2) and image_helper.pixel_matches_color(70,302, 148,10,3))


    def is_on_loading(self):
        return image_helper.pixel_matches_color(1,1, 0,0,0, tolerance=0)


    def is_in_game(self):
        return (image_helper.pixel_matches_color(718,984, 59,75,84) and image_helper.pixel_matches_color(1209,966, 56,76,81))


    def is_bad_connect(self):
        return image_helper.pixel_matches_color()


    def is_death(self):
        return (image_helper.pixel_matches_color(831,859, 147,81,32) and image_helper.pixel_matches_color(846,898, 47,1,1))


    def is_death_need_repair(self):
        return (image_helper.pixel_matches_color(831,859, 147,81,32) and image_helper.pixel_matches_color(846,898, 47,1,1))


    def click_is_death(self):
        sleep(uniform(1.5, 2.5))
        self.left_click(904, 924)
        sleep(uniform(.5, .8))


    def click_is_death_need_repair(self):
        sleep(uniform(1.5, 2.5))
        self.left_click()
        sleep(uniform(.5, .8))


    def click_start_game(self):
        sleep(uniform(1.5, 2.5))
        self.left_click(220, 710)
        sleep(uniform(1.5, 2.5))


    def click_teleport(self):
        sleep(uniform(1.5, 2.5))
        self.left_click(850, 640)
        sleep(uniform(1.5, 2.5))


    def left_click(self, x=None, y=None, a=-5,b=35,c=-5,d=5):
        '''Randomized left click'''
        if x == None or y == None:
            leftClick()
        else:
            ex = randint(a, b)
            fx = x + ex
            ey = randint(c, d)
            fy = y + ey
            leftClick(fx, fy)


    def right_click(self, x=None, y=None, a=1,b=4,c=1,d=4):
        '''Randomized right click'''
        if x == None or y == None:
            rightClick()
        else:
            ex = randint(a, b)
            fx = x + ex
            ey = randint(c, d)
            fy = y + ey
            rightClick(fx, fy)


    def key_press(self, keys):
        press(keys)


    def loot_process(self, j=30):
        for i in range(j):
            if not pickit.pick_it():
                break


    def wait_for_loading(self):
        sleep(uniform(1.5, 2.5))
        while self.is_on_loading():
            sleep(uniform(.5, .8))
        sleep(uniform(1.5, 2.5))


    def get_treasure():
        pass

    
    def get_helltide_loc(self):
        self.key_press('m')
        sleep(uniform(.5, .8))
        mouse_helper.move_smooth(800,600)
        sleep(uniform(.5, .8))
        
        for n in range(4):
            mouse_helper.mouseScroll(-1)
            sleep(uniform(.5, .8))
        
        for n in range(2):
            mouse_helper.mouseScroll(1)
            sleep(uniform(.5, .8))
        
        screen_region = (50, 50, 1900, 870)
        x, y = image_helper.locate_needle('.\\assets\\location\\treasure.png', conf=0.8, loctype='c', region=screen_region)

        if x != -1 and y != -1:
            self.right_click(x, y)
            info("Found armor treasure, moving to map position %d,%d" % (x, y))
        elif image_helper.locate_needle('.\\assets\\location\\onyxWatchtower.png', conf=0.8, region=screen_region):
            self.key_press('m')
        elif image_helper.locate_needle('.\\assets\\location\\rakhatKeep.png', conf=0.8, region=screen_region):
            self.right_click(1097, 764)
        else:
            for n in range(2):
                mouse_helper.mouseScroll(-1)
                sleep(uniform(.5, .8))
            
            x, y = image_helper.locate_needle('.\\assets\\location\\helltide.png', conf=0.8, loctype='c', region=screen_region)

            if x != -1 and y != -1:
                x2, y2 = image_helper.locate_needle('.\\assets\\location\\waypoint.png', conf=0.8, loctype='c', region=(x-25, y-75, x+25, y+25))

                if x2 != -1 and y2 != -1:
                    self.left_click(x2,y2, 1,4,1,4)
                    info("Found helltide, moving to map position %d,%d" % (x2, y2))
                    self.click_teleport()

                    return True
                
        sleep(uniform(1.5, 2.5))
        self.key_press('m')
                
    
    def game_manager(self, move=True, loot=False):
        '''Game handling routine'''
        if self.is_on_menu():
            info('Choose player on menu.')
            self.click_start_game()
        elif self.is_death():
            info('Player is death, revive.')
            self.click_is_death()
            self.wait_for_loading()
        elif self.is_in_game():
            info('Player is in-game.')
            if move == True:
                i = 0
                
                for n in range(199):
                    move_to = pather.move_to_ref_location()

                    if i == 99:
                        break
                    elif move_to == False:
                        i+=1

                if move_to == False:
                    #self.get_treasure()
                    self.get_helltide_loc()

            mob = image_helper.line_detection('mob')

            if mob != False:
                x, y = mob
                combat.rotation(x, y)
                self.game_manager(False, True)
            elif loot:
                self.loot_process()
                
