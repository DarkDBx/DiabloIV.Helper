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

    """vindicator pvp"""
    # https://guildjen.com/shiro-vindicator-pvp-build/
    def default_combat(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06.png'): # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+0.25)
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06-2.png'): # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+1.25)
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\10-2.png'):
                input_helper.press('e')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09.png'):
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09-2.png'):
                input_helper.press('c')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08.png'):
                input_helper.press('x')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08-2.png'):
                input_helper.press('x')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05.png'):
                input_helper.press('5')
                time.sleep(self.asleep+1.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02.png'):
                input_helper.press('2')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02-2.png'):
                input_helper.press('2')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\03-2.png'):
                input_helper.press('3')
                time.sleep(self.asleep+0.25)
            elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05-2.png'):
                input_helper.press('5')
                time.sleep(self.asleep+0.75)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwap.png'):
                input_helper.press('q')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1.png') or image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1-2.png'):
                    self.press_combo('shift', '1')
                    time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep+0.25)
