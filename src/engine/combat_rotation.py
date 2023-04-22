"""EXAMPLE FILE"""
import random
import time

from helper import input_helper, image_helper, timer_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

class CombatRotation:
    def __init__(self) -> None:
        """ADD TIMER IF NEEDED"""
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

    def mouse_click(self, button='left'):
        input_helper.click(button)


    """EDIT BELOW THIS LINE"""
    # https://www.linktoyourbuild.com/
    def default_combat(self):
        print('check')
        # target check
        if self.get_color(784,95, 149,34,18):
            # health check
            if not self.get_color(961,999, 170,21,5) and self.get_image(SKILLPATH+'game_name\\class_name\\heal.png') and self.timer1.GetTimerState() == TIMER_STOPPED: # heal at 60%
                self.timer2.StartTimer(5) # set timer to 5 seconds
                self.press_key('h')
                self.set_pause()
            # class skill checks
            elif self.get_image(SKILLPATH+'game_name\\class_name\\03.png') and self.timer2.GetTimerState() == TIMER_STOPPED:
                self.timer1.StartTimer(7)
                self.press_key('3')
                self.set_pause()
            elif self.get_image(SKILLPATH+'game_name\\class_name\\example.png') and self.timer3.GetTimerState() == TIMER_STOPPED:
                self.timer3.StartTimer(9)
                self.press_combo('ctrl', 'k')
                self.set_pause()
            else:
                self.mouse_click('right')
            
            self.set_pause(random.uniform(0.11, 0.15))
            self.mouse_click()
            self.set_pause()


    """dragonknight pve"""
    # https://alcasthq.com/eso-stamina-dragonknight-tank-build-pve/
    def eso_dk_pve(self):
        # target check
        if self.get_image(958,101, 118,42,42) or self.get_image(958,103, 110,34,34):
            # weapon swap
            if self.timer1.GetTimerState() == TIMER_STOPPED:
                self.timer1.StartTimer(4)
                self.press_key('tab')
            # ultimate
            elif self.timer12.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\06.png', conf=0.98) == 1:
                self.timer12.StartTimer(9)
                self.press_key('r')
            # quickslot bar 1
            elif self.timer2.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\05.png'):
                self.timer2.StartTimer(23)
                self.press_key('5')
            elif self.timer5.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\02.png'):
                self.timer5.StartTimer(15)
                self.press_key('2')
            elif self.timer6.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\01.png'):
                self.timer6.StartTimer(12)
                self.press_key('1')
            elif self.timer3.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\03.png'):
                self.timer3.StartTimer(6)
                self.press_key('3')
            # quickslot bar 2
            elif self.timer8.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\05-2.png'):
                self.timer8.StartTimer(10)
                self.press_key('5')
            elif self.timer10.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\02-2.png'):
                self.timer10.StartTimer(15)
                self.press_key('2')
            elif self.timer11.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\03-2.png'):
                self.timer11.StartTimer(15)
                self.press_key('3')
            elif self.timer7.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\dragonknight\\tank_pve\\01-2.png'):
                self.timer7.StartTimer(20)
                self.press_key('1')
            else:
                self.mouse_click('right')
                
            time.sleep(random.uniform(0.11, 0.15))
            self.mouse_click()
            self.set_pause()


    """nightblade pve"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-build-for-pve/
    def eso_nb_pve(self):
        # target check
        if self.get_image(958,101, 118,42,42) or self.get_image(958,103, 110,34,34):
            # weapon swap
            if self.timer1.GetTimerState() == TIMER_STOPPED:
                self.timer1.StartTimer(4)
                self.press_key('tab')
            # ultimate
            elif self.timer12.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\06-2.png', conf=0.98) == 1: # ulti
                self.timer12.StartTimer(9)
                self.press_key('r')
            # quickslot bar 1
            elif self.timer2.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\05.png'):
                self.timer2.StartTimer(60)
                self.press_key('5')
            elif self.timer3.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\03.png'):
                self.timer3.StartTimer(20)
                self.press_key('3')
            elif self.timer6.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\01.png'):
                self.timer6.StartTimer(3)
                self.press_key('1')
            elif self.timer5.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\02.png'):
                self.timer5.StartTimer(3)
                self.press_key('2')
            elif self.timer4.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\04.png'):
                self.timer4.StartTimer(3)
                self.press_key('4')
            # quickslot bar 2
            elif self.timer9.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\03-2.png'):
                self.timer9.StartTimer(22)
                self.press_key('3')
            elif self.timer8.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\04-2.png'):
                self.timer8.StartTimer(17)
                self.press_key('4')
            elif self.timer7.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\05-2.png'):
                self.timer7.StartTimer(5)
                self.press_key('5')
            elif self.timer10.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\02-2.png'):
                self.timer10.StartTimer(20)
                self.press_key('2')
            elif self.timer11.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pve\\01-2.png'):
                self.timer11.StartTimer(15)
                self.press_key('1')
            else:
                self.mouse_click('right')
            
            time.sleep(random.uniform(0.11, 0.15))
            self.mouse_click()
            self.set_pause()


    """nightblade pvp"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-gank-build-pvp/
    def eso_nb_pvp(self):
        # target check
        if self.get_image(958,101, 118,42,42) or self.get_image(958,103, 110,34,34):
            # weapon swap
            if self.timer1.GetTimerState() == TIMER_STOPPED:
                self.timer1.StartTimer(4)
                self.press_key('tab')
            # ultimate
            elif self.timer12.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\06.png', conf=0.98) == 1: # ulti
                self.timer12.StartTimer(9)
                self.press_key('r')
            # quickslot bar 1
            elif self.timer2.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\05.png'):
                self.timer2.StartTimer(60)
                self.press_key('5')
            elif self.timer4.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\04.png'):
                self.timer4.StartTimer(5)
                self.press_key('4')
            elif self.timer5.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\02.png'):
                self.timer5.StartTimer(3)
                self.press_key('2')
            elif self.timer6.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\01.png'):
                self.timer6.StartTimer(3)
                self.press_key('1')
            # quickslot bar 2
            elif self.timer7.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\01-2.png'):
                self.timer7.StartTimer(40)
                self.press_key('1')
            elif self.timer8.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\05-2.png'):
                self.timer8.StartTimer(5)
                self.press_key('5')
            elif self.timer10.GetTimerState() == TIMER_STOPPED and self.get_image(SKILLPATH+'eso\\nightblade\\bow_pvp\\02-2.png'):
                self.timer10.StartTimer(4)
                self.press_key('2')
            else:
                self.mouse_click('right')

            time.sleep(random.uniform(0.11, 0.15))
            self.mouse_click()
            self.set_pause()


    """vindicator pvp"""
    # https://guildjen.com/shiro-vindicator-pvp-build/
    def gw2_rev_pvp(self):
        # target check
        if self.get_image(784,95, 149,34,18) or self.get_image(784,98, 148,33,18):
            # health check
            if not self.get_image(961,999, 170,21,5) and self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\06.png'): # heal at 60%
                self.press_key('r')
                self.set_pause(0.5)
            elif not self.get_image(961,999, 170,21,5) and self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\06-2.png'): # heal at 60%
                self.press_key('r')
                self.set_pause(1.5)
            # class skill checks
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\10-2.png'):
                self.press_key('e')
                self.set_pause(0.5)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\09.png'):
                self.press_key('c')
                self.set_pause()
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\09-2.png'):
                self.press_key('c')
                self.set_pause(0.5)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\08.png'):
                self.press_key('x')
                self.set_pause(+0.25)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\08-2.png'):
                self.press_key('x')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\05.png'):
                self.press_key('5')
                self.set_pause(1.5)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\02.png'):
                self.press_key('2')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\02-2.png'):
                self.press_key('2')
                self.set_pause(0.5)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\03-2.png'):
                self.press_key('3')
                self.set_pause(0.5)
            elif self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\05-2.png'):
                self.press_key('5')
                self.set_pause(1)
            elif self.get_image(SKILLPATH+'WeaponSwap.png'):
                self.press_key('q')
                self.set_pause()
                if self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\s1.png') or self.get_image(SKILLPATH+'gw2\\revenant\\v_pvp\\s1-2.png'):
                    self.press_combo('shift', '1')
                    self.set_pause()
            else:
                self.press_key('1')
                self.set_pause(0.5)


    """soulbeast pvp/wvw"""
    # https://guildjen.com/sic-em-soulbeast-pvp-build/
    # https://guildjen.com/sic-em-soulbeast-roaming-build/
    def gw2_sb_pvp(self):
        # target check
        if self.get_image(784,95, 149,34,18) or self.get_image(784,98, 148,33,18):
            # health check
            if not self.get_image(961,999, 170,21,5) and self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\06.png'): # heal at 60%
                self.press_key('r')
                self.set_pause(0.75)
            elif not self.get_image(961,999, 170,21,5) and (self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\07.png') or self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\07-2.png')): # at 60%
                self.press_key('z')
            elif not self.get_image(961,999, 170,21,5) and self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\09.png'): # at 60%
                self.press_key('c')
            # class skill checks
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\10-2.png'):
                self.press_key('e')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\10.png'):
                self.press_key('e')
                self.set_pause()
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\08.png'):
                self.press_key('x')
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\04.png') and self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\02.png'):
                self.press_key('4')
                self.set_pause(0.5)
                self.press_key('2')
                self.set_pause(2.5)
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\02-2.png'):
                self.press_key('2')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\05-2.png'):
                self.press_key('5')
                self.set_pause()
            elif self.get_image(SKILLPATH+'WeaponSwap.png'):
                self.press_key('q')
                self.set_pause()
                if self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5.png') or self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5-2.png'):
                    self.press_combo('shift', '5')
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1.png'):
                self.press_combo('shift', '1')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1-2.png'):
                self.press_combo('shift', '1')
                self.set_pause()
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2.png') or self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2-2.png'):
                self.press_combo('shift', '2')
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3.png'):
                self.press_combo('shift', '3')
                self.set_pause(0.75)
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3-2.png'):
                self.press_combo('shift', '3')
                self.set_pause()
            elif self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4.png') or self.get_image(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4-2.png'):
                self.press_combo('shift', '4')
                self.set_pause()
            else:
                self.press_key('1')
                self.set_pause(0.5)

