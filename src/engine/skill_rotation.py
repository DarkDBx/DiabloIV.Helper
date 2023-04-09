
import time

from helper import input_helper, image_helper


SKILLPATH = ".\\assets\\skills\\"

class SkillRotation:
    def __init__(self):
        self.asleep = 0.25

    def press_combo(self, key1, key2):
        input_helper.keyDown(key1)
        input_helper.press(key2)
        input_helper.keyUp(key1)

    """harbinger pvp"""
    def necromant_pvp(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'necro\\06.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+.75)
            elif not image_helper.pixel_matches_color(960,1028, 112,13,5) and image_helper.locate_needle(SKILLPATH+'necro\\08.png') == 1: # at 40%
                input_helper.press('x')
                time.sleep(self.asleep)
            elif not image_helper.pixel_matches_color(960,1028, 112,13,5) and image_helper.locate_needle(SKILLPATH+'necro\\10.png') == 1: # at 40%
                input_helper.press('e')
                time.sleep(self.asleep+.75)
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'necro\\07.png') == 1:
                input_helper.press('z')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\09.png') == 1:
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s1.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\s1-3.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s2.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\s2-3.png') == 1:
                self.press_combo('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s1-2.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s2-2.png') == 1:
                self.press_combo('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s3.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\s3-2.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\s3-3.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\s4.png') == 1:
                self.press_combo('shift', '4')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'necro\\s5.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\s5-2.png') == 1:
                    self.press_combo('shift', '5')
                    time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwitch.png') == 1:
                input_helper.press('q')
                time.sleep(self.asleep)
            # standard rotation
            elif image_helper.locate_needle(SKILLPATH+'necro\\04.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\04-2.png') == 1:
                input_helper.press('4')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\03.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\03-2.png') == 1:
                input_helper.press('3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\05.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\05-2.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'necro\\02.png') == 1 or image_helper.locate_needle(SKILLPATH+'necro\\02-2.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep)
        else:
            time.sleep(self.asleep)

    """willbender pvp"""
    def guardian_pvp(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'guard\\06.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+.75)
            elif not image_helper.pixel_matches_color(960,1028, 112,13,5) and image_helper.locate_needle(SKILLPATH+'guard\\08.png') == 1: # at 40%
                input_helper.press('x')
                time.sleep(self.asleep)
            elif not image_helper.pixel_matches_color(960,1028, 112,13,5) and image_helper.locate_needle(SKILLPATH+'guard\\10.png') == 1: # at 40%
                input_helper.press('e')
                time.sleep(self.asleep+.75)
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'guard\\07.png') == 1:
                input_helper.press('z')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\09.png') == 1:
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s1.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\s1-3.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s2.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\s2-3.png') == 1:
                self.press_combo('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s1-2.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s2-2.png') == 1:
                self.press_combo('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s3.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\s3-2.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\s3-3.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\s4.png') == 1:
                self.press_combo('shift', '4')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'guard\\s5.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\s5-2.png') == 1:
                    self.press_combo('shift', '5')
                    time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwitch.png') == 1:
                input_helper.press('q')
                time.sleep(self.asleep)
            # standard rotation
            elif image_helper.locate_needle(SKILLPATH+'guard\\04.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\04-2.png') == 1:
                input_helper.press('4')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\03.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\03-2.png') == 1:
                input_helper.press('3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\05.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\05-2.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'guard\\02.png') == 1 or image_helper.locate_needle(SKILLPATH+'guard\\02-2.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep)
        else:
            time.sleep(self.asleep)

    """vindicator pvp"""
    def revenant_pvp(self):
        # target check
        if image_helper.pixel_matches_color(783,124, 147,33,18):
            if image_helper.pixel_matches_color(797,892, 255,255,255) or image_helper.pixel_matches_color(813,889, 186,250,254):
                self.press_combo('shift', '2')
                time.sleep(.5)
            elif image_helper.pixel_matches_color(824,888, 217,217,218):
                self.press_combo('shift', '3')
            # health check
            elif not image_helper.pixel_matches_color(961,932, 176,27,2) and (image_helper.pixel_matches_color(1257,967, 83,159,126) or image_helper.pixel_matches_color(1257,967, 254,234,0) or image_helper.pixel_matches_color(1257,967, 24,24,25)): # at 30%
                input_helper.press('e')
                time.sleep(1)
            elif not image_helper.pixel_matches_color(961,932, 176,27,2) and (image_helper.pixel_matches_color(1202,965, 88,67,74) or image_helper.pixel_matches_color(1202,965, 248,197,107) or image_helper.pixel_matches_color(1202,965, 16,20,24)): # at 30%
                input_helper.press('c')
            elif not image_helper.pixel_matches_color(962,985, 110,11,5) and (image_helper.pixel_matches_color(1037,972, 160,122,172) or image_helper.pixel_matches_color(1037,972, 110,32,6) or image_helper.pixel_matches_color(1037,972, 15,23,44)): # heal at 80%
                input_helper.press('r')
                time.sleep(.75)
            # skill check
            elif image_helper.pixel_matches_color(1092,971, 32,5,17) or image_helper.pixel_matches_color(1092,971, 17,1,1) or image_helper.pixel_matches_color(1092,971, 45,66,72):
                input_helper.press('z')
                time.sleep(.25)
            elif image_helper.pixel_matches_color(1147,970, 139,221,185) or image_helper.pixel_matches_color(1147,970, 89,26,15) or image_helper.pixel_matches_color(1147,970, 68,255,255):
                input_helper.press('x')
                time.sleep(.5)
            elif not image_helper.pixel_matches_color(660, 914, 0, 0, 0):
                self.press_combo('shift', '1')
                time.sleep(.25)
            elif image_helper.pixel_matches_color(624,978, 162,139,93):
                input_helper.press('q')
                time.sleep(.25)
            '''
            # standard rotation
            elif image_helper.pixel_matches_color(883, 971, 96, 95, 116) or image_helper.pixel_matches_color(883, 968, 255, 230, 136):
                input_helper.press('5')
                time.sleep(.75)
            elif image_helper.pixel_matches_color(718, 971, 219, 16, 23) or image_helper.pixel_matches_color(718, 966, 74, 80, 114):
                input_helper.press('2')
                time.sleep(.75)
            elif image_helper.pixel_matches_color(827, 969, 183, 165, 172) or image_helper.pixel_matches_color(828, 973, 136, 94, 85):
                input_helper.press('4')
                time.sleep(.75)
            elif image_helper.pixel_matches_color(718, 970, 249, 12, 16) or image_helper.pixel_matches_color(773, 967, 61, 76, 105):
                input_helper.press('3')
                time.sleep(.75)
            else:
                pass
                '''

    """soulbeast pvp/wvw"""
    # https://guildjen.com/sic-em-soulbeast-pvp-build/
    # https://guildjen.com/sic-em-soulbeast-roaming-build/
    def ranger_pvp(self):
        # target check
        if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
            # health check
            if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\06.png') == 1: # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep+0.5)
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and (image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\07.png') == 1 or image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\07-2.png') == 1): # at 60%
                input_helper.press('z')
            elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\09.png') == 1: # at 60%
                input_helper.press('c')
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\10-2.png') == 1:
                input_helper.press('e')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\10.png') == 1:
                input_helper.press('e')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\08.png') == 1:
                input_helper.press('x')
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\04.png') == 1 and image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\02.png') == 1:
                input_helper.press('4')
                time.sleep(self.asleep+0.25)
                input_helper.press('2')
                time.sleep(self.asleep+2.25)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\02-2.png') == 1:
                input_helper.press('2')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\05-2.png') == 1:
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'WeaponSwap.png') == 1:
                input_helper.press('q')
                time.sleep(self.asleep)
                if image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s5.png') == 1 or image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s5-2.png') == 1:
                    self.press_combo('shift', '5')
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s1.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s1-2.png') == 1:
                self.press_combo('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s2.png') == 1 or image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s2-2.png') == 1:
                self.press_combo('shift', '2')
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s3.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep+0.5)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s3-2.png') == 1:
                self.press_combo('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s4.png') == 1 or image_helper.locate_needle(SKILLPATH+'ranger\\sb_pvp\\s4-2.png') == 1:
                self.press_combo('shift', '4')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep+0.25)
        else:
            time.sleep(self.asleep)


skillRota = SkillRotation()

