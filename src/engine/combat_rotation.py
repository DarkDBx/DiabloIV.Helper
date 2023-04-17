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


    """ASSISTANT"""

    """Guild Wars 2"""

    """vindicator pvp"""
    # https://guildjen.com/shiro-vindicator-pvp-build/
    def revenant_pvp(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+0.25)
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06-2.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+1.25)
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\10-2.png') == 1:
                input_helper.press('e')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09.png') == 1:
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09-2.png') == 1:
                input_helper.press('c')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08.png') == 1:
                input_helper.press('x')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08-2.png') == 1:
                input_helper.press('x')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep+1.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02-2.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\03-2.png') == 1:
                input_helper.press('3')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05-2.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep+0.75)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwap.png') == 1:
                input_helper.press('q')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1.png') == 1 or image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1-2.png') == 1:
                    self.press_combo('shift', '1')
                    time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep+0.25)

    """soulbeast pvp/wvw"""
    # https://guildjen.com/sic-em-soulbeast-pvp-build/
    # https://guildjen.com/sic-em-soulbeast-roaming-build/
    def ranger_pvp(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\06.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+0.5)
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and (image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07.png') == 1 or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07-2.png') == 1): # at 60%
                input_helper.press('z')
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\09.png') == 1: # at 60%
                input_helper.press('c')
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10-2.png') == 1:
                input_helper.press('e')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10.png') == 1:
                input_helper.press('e')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\08.png') == 1:
                input_helper.press('x')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\04.png') == 1 and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02.png') == 1:
                input_helper.press('4')
                time.sleep(self.asleep+0.25)
                input_helper.press('2')
                time.sleep(self.asleep+2.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02-2.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\05-2.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwap.png') == 1:
                input_helper.press('q')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5.png') == 1 or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5-2.png') == 1:
                    self.press_combo('shift', '5')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1-2.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2.png') == 1 or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2-2.png') == 1:
                self.press_combo('shift', '2')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3-2.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4.png') == 1 or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4-2.png') == 1:
                self.press_combo('shift', '4')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep+0.25)


    """Elder Scrolls Online"""

    """nightblade pve"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-build-for-pve/
    def nightblade_pve(self):
        # target check
        if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
            # weapon swap
            if (self.timer1.GetTimerState() == TIMER_IDLE or self.timer1.GetTimerState() == TIMER_STOPPED):
                self.timer1.StartTimer(4)
                input_helper.press('tab')
            # ultimate
            elif (self.timer12.GetTimerState() == TIMER_IDLE or self.timer12.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\06-2.png', conf=0.98) == 1: # ulti
                self.timer12.StartTimer(9)
                input_helper.press('r')
            # quickslot bar 1
            elif (self.timer2.GetTimerState() == TIMER_IDLE or self.timer2.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05.png') == 1:
                self.timer2.StartTimer(60)
                input_helper.press('5')
            elif (self.timer3.GetTimerState() == TIMER_IDLE or self.timer3.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03.png') == 1:
                self.timer3.StartTimer(20)
                input_helper.press('3')
            elif (self.timer6.GetTimerState() == TIMER_IDLE or self.timer6.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01.png') == 1:
                self.timer6.StartTimer(3)
                input_helper.press('1')
            elif (self.timer5.GetTimerState() == TIMER_IDLE or self.timer5.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02.png') == 1:
                self.timer5.StartTimer(3)
                input_helper.press('2')
            elif (self.timer4.GetTimerState() == TIMER_IDLE or self.timer4.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04.png') == 1:
                self.timer4.StartTimer(3)
                input_helper.press('4')
            # quickslot bar 2
            elif (self.timer9.GetTimerState() == TIMER_IDLE or self.timer9.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03-2.png') == 1:
                self.timer9.StartTimer(22)
                input_helper.press('3')
            elif (self.timer8.GetTimerState() == TIMER_IDLE or self.timer8.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04-2.png') == 1:
                self.timer8.StartTimer(17)
                input_helper.press('4')
            elif (self.timer7.GetTimerState() == TIMER_IDLE or self.timer7.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05-2.png') == 1:
                self.timer7.StartTimer(5)
                input_helper.press('5')
            elif (self.timer10.GetTimerState() == TIMER_IDLE or self.timer10.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02-2.png') == 1:
                self.timer10.StartTimer(20)
                input_helper.press('2')
            elif (self.timer11.GetTimerState() == TIMER_IDLE or self.timer11.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01-2.png') == 1:
                self.timer11.StartTimer(15)
                input_helper.press('1')
            else:
                input_helper.rightClick()
            
            time.sleep(random.uniform(0.11, 0.15))
            input_helper.leftClick()
            time.sleep(self.asleep)

    """nightblade pvp"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-gank-build-pvp/
    def nightblade_pvp(self):
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
            elif (self.timer2.GetTimerState() == TIMER_IDLE or self.timer2.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05.png') == 1:
                self.timer2.StartTimer(60)
                input_helper.press('5')
            elif (self.timer4.GetTimerState() == TIMER_IDLE or self.timer4.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\04.png') == 1:
                self.timer4.StartTimer(5)
                input_helper.press('4')
            elif (self.timer5.GetTimerState() == TIMER_IDLE or self.timer5.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02.png') == 1:
                self.timer5.StartTimer(3)
                input_helper.press('2')
            elif (self.timer6.GetTimerState() == TIMER_IDLE or self.timer6.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01.png') == 1:
                self.timer6.StartTimer(3)
                input_helper.press('1')
            # quickslot bar 2
            elif (self.timer7.GetTimerState() == TIMER_IDLE or self.timer7.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01-2.png') == 1:
                self.timer7.StartTimer(40)
                input_helper.press('1')
            elif (self.timer8.GetTimerState() == TIMER_IDLE or self.timer8.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05-2.png') == 1:
                self.timer8.StartTimer(5)
                input_helper.press('5')
            elif (self.timer10.GetTimerState() == TIMER_IDLE or self.timer10.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02-2.png') == 1:
                self.timer10.StartTimer(4)
                input_helper.press('2')
            else:
                input_helper.rightClick()

            time.sleep(random.uniform(0.11, 0.15))
            input_helper.leftClick()
            time.sleep(self.asleep)

    """dragonknight pve"""
    # https://alcasthq.com/eso-stamina-dragonknight-tank-build-pve/
    def dragonknight_pve(self):
        # target check
        if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
            # weapon swap
            if (self.timer1.GetTimerState() == TIMER_IDLE or self.timer1.GetTimerState() == TIMER_STOPPED):
                self.timer1.StartTimer(4)
                input_helper.press('tab')
            # ultimate
            elif (self.timer12.GetTimerState() == TIMER_IDLE or self.timer12.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\06.png', conf=0.98) == 1:
                self.timer12.StartTimer(9)
                input_helper.press('r')
            # quickslot bar 1
            elif (self.timer2.GetTimerState() == TIMER_IDLE or self.timer2.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\05.png') == 1:
                self.timer2.StartTimer(23)
                input_helper.press('5')
            elif (self.timer5.GetTimerState() == TIMER_IDLE or self.timer5.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\02.png') == 1:
                self.timer5.StartTimer(15)
                input_helper.press('2')
            elif (self.timer6.GetTimerState() == TIMER_IDLE or self.timer6.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\01.png') == 1:
                self.timer6.StartTimer(12)
                input_helper.press('1')
            elif (self.timer3.GetTimerState() == TIMER_IDLE or self.timer3.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\03.png') == 1:
                self.timer3.StartTimer(6)
                input_helper.press('3')
            # quickslot bar 2
            elif (self.timer8.GetTimerState() == TIMER_IDLE or self.timer8.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\05-2.png') == 1:
                self.timer8.StartTimer(10)
                input_helper.press('5')
            elif (self.timer10.GetTimerState() == TIMER_IDLE or self.timer10.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\02-2.png') == 1:
                self.timer10.StartTimer(15)
                input_helper.press('2')
            elif (self.timer11.GetTimerState() == TIMER_IDLE or self.timer11.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\03-2.png') == 1:
                self.timer11.StartTimer(15)
                input_helper.press('3')
            elif (self.timer7.GetTimerState() == TIMER_IDLE or self.timer7.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\01-2.png') == 1:
                self.timer7.StartTimer(20)
                input_helper.press('1')
            else:
                input_helper.rightClick()
                
            time.sleep(random.uniform(0.11, 0.15))
            input_helper.leftClick()
            time.sleep(self.asleep)


    """Path of Exile"""

    """ranger"""
    # https://www.
    def ranger(self):
        # target check
        if image_helper.pixel_matches_color():
            # do rotation
            pass

    """marauder"""
    # https://www.pathofexile.com/forum/view-thread/1729700
    def marauder(self):
        # target check
        if image_helper.pixel_matches_color():
            # do rotation
            pass
    

cr = CombatRotation()

