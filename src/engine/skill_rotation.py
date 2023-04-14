
import time
import logging

from helper import input_helper, image_helper, timer_helper
from helper.timer_helper import TIMER_IDLE, TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

class SkillRotation:
    def __init__(self) -> None:
        self.asleep = 0.25
        self.tab = timer_helper.TimerHelper('tab')
        self.vigor = timer_helper.TimerHelper('vigor')
        self.blur = timer_helper.TimerHelper('blur')
        self.shade = timer_helper.TimerHelper('shade')
        self.injection = timer_helper.TimerHelper('injection')
        self.hail = timer_helper.TimerHelper('hail')
        self.focus = timer_helper.TimerHelper('focus')
        self.blade = timer_helper.TimerHelper('blade')
        self.strikes = timer_helper.TimerHelper('strikes')
        self.arrow = timer_helper.TimerHelper('arrow')
        self.spray = timer_helper.TimerHelper('spray')
        self.hunter = timer_helper.TimerHelper('hunter')
        self.shards = timer_helper.TimerHelper('shards')
        self.disguise = timer_helper.TimerHelper('disguise')
        self.maneuver = timer_helper.TimerHelper('maneuver')
        self.attack = timer_helper.TimerHelper('attack')
        self.momentum = timer_helper.TimerHelper('momentum')

    def press_combo(self, key1, key2):
        input_helper.keyDown(key1)
        input_helper.press(key2)
        input_helper.keyUp(key1)

    """
    Guild Wars 2
    """

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


    """
    Elder Scrolls Online
    """

    """nightblade pve"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-build-for-pve/
    def nightblade_pve_rota(self):
        # target check
        if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
            # class skill checks
            if (self.tab.GetTimerState() == TIMER_IDLE or self.tab.GetTimerState() == TIMER_STOPPED):
                logging.info('press "tab"')
                self.tab.StartTimer(4)
                input_helper.press('tab')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\06-2.png', conf=0.995, grayscale=False) == 1: # ulti
                logging.info('press "r"')
                input_helper.press('r')
                time.sleep(self.asleep+0.15)
            elif (self.focus.GetTimerState() == TIMER_IDLE or self.focus.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05.png') == 1:
                logging.info('press "5"')
                self.focus.StartTimer(60)
                input_helper.press('5')
                time.sleep(self.asleep+0.15)
            elif (self.strikes.GetTimerState() == TIMER_IDLE or self.strikes.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03.png') == 1:
                logging.info('press "3"')
                self.strikes.StartTimer(20)
                input_helper.press('3')
                time.sleep(self.asleep+0.15)
            elif (self.blade.GetTimerState() == TIMER_IDLE or self.blade.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04.png') == 1:
                logging.info('press "4"')
                self.blade.StartTimer(3)
                input_helper.press('4')
                time.sleep(self.asleep+0.15)
            elif (self.arrow.GetTimerState() == TIMER_IDLE or self.arrow.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02.png') == 1:
                logging.info('press "2"')
                self.arrow.StartTimer(3)
                input_helper.press('2')
                time.sleep(self.asleep+0.15)
            elif (self.spray.GetTimerState() == TIMER_IDLE or self.spray.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01.png') == 1:
                logging.info('press "1"')
                self.spray.StartTimer(3)
                input_helper.press('1')
                time.sleep(self.asleep+0.15)
            elif (self.vigor.GetTimerState() == TIMER_IDLE or self.vigor.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05-2.png') == 1:
                logging.info('press "5"')
                self.vigor.StartTimer(5)
                input_helper.press('5')
                time.sleep(self.asleep+0.15)
            elif (self.blur.GetTimerState() == TIMER_IDLE or self.blur.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04-2.png') == 1:
                logging.info('press "4"')
                self.blur.StartTimer(17)
                input_helper.press('4')
                time.sleep(self.asleep+0.15)
            elif (self.shade.GetTimerState() == TIMER_IDLE or self.shade.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03-2.png') == 1:
                logging.info('press "3"')
                self.shade.StartTimer(22)
                input_helper.press('3')
                time.sleep(self.asleep+0.15)
            elif (self.injection.GetTimerState() == TIMER_IDLE or self.injection.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02-2.png') == 1:
                logging.info('press "2"')
                self.injection.StartTimer(20)
                input_helper.press('2')
                time.sleep(self.asleep+0.15)
            elif (self.hail.GetTimerState() == TIMER_IDLE or self.hail.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01-2.png') == 1:
                logging.info('press "1"')
                self.hail.StartTimer(15)
                input_helper.press('1')
                time.sleep(self.asleep+0.15)

    """nightblade pvp"""
    # https://alcasthq.com/eso-stamina-nightblade-bow-gank-build-pvp/
    def nightblade_pvp_rota(self):
        # target check
        if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
            # class skill checks
            if (self.tab.GetTimerState() == TIMER_IDLE or self.tab.GetTimerState() == TIMER_STOPPED):
                logging.info('press "tab"')
                self.tab.StartTimer(4)
                input_helper.press('tab')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\06.png', conf=0.995, grayscale=False) == 1: # ulti
                logging.info('press "r"')
                input_helper.press('r')
                time.sleep(self.asleep+0.15)
            elif (self.focus.GetTimerState() == TIMER_IDLE or self.focus.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05.png') == 1:
                logging.info('press "5"')
                self.focus.StartTimer(60)
                input_helper.press('5')
                time.sleep(self.asleep+0.15)
            elif (self.strikes.GetTimerState() == TIMER_IDLE or self.strikes.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\03.png') == 1:
                logging.info('press "3"')
                self.strikes.StartTimer(20)
                input_helper.press('3')
                time.sleep(self.asleep+0.15)
            elif (self.hunter.GetTimerState() == TIMER_IDLE or self.hunter.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\04.png') == 1:
                logging.info('press "4"')
                self.hunter.StartTimer(5)
                input_helper.press('4')
                time.sleep(self.asleep+0.15)
            elif (self.arrow.GetTimerState() == TIMER_IDLE or self.arrow.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02.png') == 1:
                logging.info('press "2"')
                self.arrow.StartTimer(3)
                input_helper.press('2')
                time.sleep(self.asleep+0.15)
            elif (self.shards.GetTimerState() == TIMER_IDLE or self.shards.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01.png') == 1:
                logging.info('press "1"')
                self.shards.StartTimer(3)
                input_helper.press('1')
                time.sleep(self.asleep+0.15)
            elif (self.momentum.GetTimerState() == TIMER_IDLE or self.momentum.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01-2.png') == 1:
                logging.info('press "1"')
                self.momentum.StartTimer(40)
                input_helper.press('1')
                time.sleep(self.asleep+0.15)
            elif (self.vigor.GetTimerState() == TIMER_IDLE or self.vigor.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05-2.png') == 1:
                logging.info('press "5"')
                self.vigor.StartTimer(5)
                input_helper.press('5')
                time.sleep(self.asleep+0.15)
            elif (self.disguise.GetTimerState() == TIMER_IDLE or self.disguise.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\04-2.png') == 1:
                logging.info('press "4"')
                self.disguise.StartTimer(5)
                input_helper.press('4')
                time.sleep(self.asleep+0.15)
            elif (self.attack.GetTimerState() == TIMER_IDLE or self.attack.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02-2.png') == 1:
                logging.info('press "2"')
                self.attack.StartTimer(4)
                input_helper.press('2')
                time.sleep(self.asleep+0.15)
            """elif (self.maneuver.GetTimerState() == TIMER_IDLE or self.maneuver.GetTimerState() == TIMER_STOPPED) and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\03-2.png') == 1:
                logging.info('press "3"')
                self.maneuver.StartTimer(8)
                input_helper.press('3')
                time.sleep(self.asleep+0.15)"""
    

skillRota = SkillRotation()

def nightblade_pve():
    skillRota.nightblade_pve_rota()
    # target check
    if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
        logging.info('mouse left click')
        input_helper.leftClick()
        time.sleep(0.25)

def nightblade_pvp():
    skillRota.nightblade_pvp_rota()
    # target check
    if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
        logging.info('mouse left click')
        input_helper.leftClick()
        time.sleep(0.25)
