"""EXAMPLE FILE"""
"""use this to create a new file with your own conditions"""
"""supported function is default_name(), so just use one rotation per file"""
import random
import time

from helper import input_helper, image_helper, timer_helper
from helper.timer_helper import TIMER_IDLE, TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

class CombatRotation:
    def __init__(self) -> None:
        self.timer1 = timer_helper.TimerHelper('timer1')
        self.timer2 = timer_helper.TimerHelper('timer2')
        self.timer3 = timer_helper.TimerHelper('timer3')

    def set_pause(self, asleep=0.25):
        time.sleep(asleep)

    def press_combo(self, key1, key2):
        input_helper.keyDown(key1)
        input_helper.press(key2)
        input_helper.keyUp(key1)

    def press_key(self, key):
        input_helper.press(key)

    def get_color(self, x,y, r,g,b):
        image_helper.pixel_matches_color(x,y, r,g,b)

    def get_image(self, name):
        image_helper.locate_needle(SKILLPATH+name+'.png')

    """example rotation with timer"""
    # https://www.linktoyourbuild.com/
    def default_combat(self):
        # target check
        if self.get_color(784,95, 149,34,18) or self.get_color(784,98, 148,33,18):
            # health check
            if not self.get_color(961,999, 170,21,5) and self.get_image(SKILLPATH+'game_name\\class_name\\heal.png') and (self.timer1.GetTimerState() == TIMER_IDLE or self.timer1.GetTimerState() == TIMER_STOPPED): # heal at 60%
                self.timer2.StartTimer(5) # set timer to 5 seconds
                self.press_key('h')
                self.set_pause()
            # class skill checks
            elif self.get_image(SKILLPATH+'game_name\\class_name\\01.png') and (self.timer2.GetTimerState() == TIMER_IDLE or self.timer2.GetTimerState() == TIMER_STOPPED):
                self.timer1.StartTimer(7)
                self.press_key('3')
                self.set_pause()
            elif self.get_image(SKILLPATH+'game_name\\class_name\\example.png') and (self.timer3.GetTimerState() == TIMER_IDLE or self.timer3.GetTimerState() == TIMER_STOPPED):
                self.timer3.StartTimer(9)
                self.press_combo('ctrl', 'k')
                self.set_pause()
            else:
                input_helper.rightClick()
            
            self.set_pause(random.uniform(0.11, 0.15))
            input_helper.leftClick()
            self.set_pause()

