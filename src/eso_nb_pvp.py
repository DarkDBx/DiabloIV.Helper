import random
import time

from helper import input_helper, image_helper, timer_helper
from helper.timer_helper import TIMER_IDLE, TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

class CombatRotation:
    def __init__(self) -> None:
        self.asleep = 0.25
        self.timer1 = timer_helper.TimerHelper('timer1')
        self.timer2 = timer_helper.TimerHelper('timer2')
        self.timer3 = timer_helper.TimerHelper('timer3')
        self.timer4 = timer_helper.TimerHelper('timer4')
        self.timer5 = timer_helper.TimerHelper('timer5')
        self.timer6 = timer_helper.TimerHelper('timer6')
        self.timer7 = timer_helper.TimerHelper('timer7')
        self.timer8 = timer_helper.TimerHelper('timer8')
        self.timer9 = timer_helper.TimerHelper('timer9')
        self.timer10 = timer_helper.TimerHelper('timer10')
        self.timer11 = timer_helper.TimerHelper('timer11')
        self.timer12 = timer_helper.TimerHelper('timer12')

    def press_combo(self, key1, key2):
        input_helper.keyDown(key1)
        input_helper.press(key2)
        input_helper.keyUp(key1)

    """nightblade pvp"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-gank-build-pvp/
    def default_combat(self):
        # target check
        if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
            # weapon swap
            if (self.timer1.GetTimerState() == TIMER_IDLE or self.timer1.GetTimerState() == TIMER_STOPPED):
                self.timer1.StartTimer(4)
                input_helper.press('tab')
            # ultimate
            elif (self.timer12.GetTimerState() == TIMER_IDLE or self.timer12.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\06.png', conf=0.98) == 1: # ulti
                self.timer12.StartTimer(9)
                input_helper.press('r')
            # quickslot bar 1
            elif (self.timer2.GetTimerState() == TIMER_IDLE or self.timer2.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05.png'):
                self.timer2.StartTimer(60)
                input_helper.press('5')
            elif (self.timer4.GetTimerState() == TIMER_IDLE or self.timer4.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\04.png'):
                self.timer4.StartTimer(5)
                input_helper.press('4')
            elif (self.timer5.GetTimerState() == TIMER_IDLE or self.timer5.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02.png'):
                self.timer5.StartTimer(3)
                input_helper.press('2')
            elif (self.timer6.GetTimerState() == TIMER_IDLE or self.timer6.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01.png'):
                self.timer6.StartTimer(3)
                input_helper.press('1')
            # quickslot bar 2
            elif (self.timer7.GetTimerState() == TIMER_IDLE or self.timer7.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01-2.png'):
                self.timer7.StartTimer(40)
                input_helper.press('1')
            elif (self.timer8.GetTimerState() == TIMER_IDLE or self.timer8.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05-2.png'):
                self.timer8.StartTimer(5)
                input_helper.press('5')
            elif (self.timer10.GetTimerState() == TIMER_IDLE or self.timer10.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02-2.png'):
                self.timer10.StartTimer(4)
                input_helper.press('2')
            else:
                input_helper.rightClick()

            time.sleep(random.uniform(0.11, 0.15))
            input_helper.leftClick()
            time.sleep(self.asleep)
