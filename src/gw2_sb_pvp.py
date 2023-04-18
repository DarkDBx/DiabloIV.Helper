import random
import time

from helper import input_helper, image_helper, timer_helper
from helper.timer_helper import TIMER_IDLE, TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

class CombatRotation:
    def __init__(self) -> None:
        self.asleep = 0.25

    def press_combo(self, key1, key2):
        input_helper.keyDown(key1)
        input_helper.press(key2)
        input_helper.keyUp(key1)

    """soulbeast pvp/wvw"""
    # https://guildjen.com/sic-em-soulbeast-pvp-build/
    # https://guildjen.com/sic-em-soulbeast-roaming-build/
    def default_combat(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\06.png'): # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+0.5)
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and (image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07-2.png')): # at 60%
                input_helper.press('z')
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\09.png'): # at 60%
                input_helper.press('c')
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10-2.png'):
                input_helper.press('e')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10.png'):
                input_helper.press('e')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\08.png'):
                input_helper.press('x')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\04.png') and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02.png'):
                input_helper.press('4')
                time.sleep(self.asleep+0.25)
                input_helper.press('2')
                time.sleep(self.asleep+2.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02-2.png'):
                input_helper.press('2')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\05-2.png'):
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwap.png'):
                input_helper.press('q')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5-2.png'):
                    self.press_combo('shift', '5')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1.png'):
                self.press_combo('shift', '1')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1-2.png'):
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2-2.png'):
                self.press_combo('shift', '2')
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3.png'):
                self.press_combo('shift', '3')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3-2.png'):
                self.press_combo('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4-2.png'):
                self.press_combo('shift', '4')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep+0.25)
