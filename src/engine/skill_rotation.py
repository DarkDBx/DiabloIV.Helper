
import time
import logging

from helper import input_helper, image_helper


SKILLPATH = ".\\assets\\skills\\"

class SkillRotation:
    def __init__(self):
        self.asleep = 0.5

    def use_skill(key1, key2):
        input_helper.press((key1, key2))

    # scourge support
    def necromant_scourge(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            # class skill checks
            if not image_helper.imgHelp.pixel_matches_color(961,932, 176,27,2) and image_helper.imgHelp.pixel_matches_color(839, 896, 239, 191, 30): # shade at 30%
                self.use_skill('shift', '5')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(766, 893, 236, 197, 0): # cascade
                self.use_skill('shift', '3')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(731, 893, 248, 236, 150): # favor
                self.use_skill('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(802, 893, 108, 79, 21): # fear
                self.use_skill('shift', '4')
                time.sleep(self.asleep)
            # health check
            elif not image_helper.imgHelp.pixel_matches_color(961,955, 165,21,5) and image_helper.imgHelp.pixel_matches_color(1036, 965, 194, 222, 158): # heal at 60%
                input_helper.press('r')
                time.sleep(self.asleep)
            # skill checks
            elif image_helper.imgHelp.pixel_matches_color(656, 892, 185, 140, 27) and image_helper.imgHelp.pixel_matches_color(692, 917, 101, 88, 33): # ss1 check
                self.use_skill('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1147, 968, 1, 136, 150): # snakes
                input_helper.press('x')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1200, 968, 8, 44, 23): # spoil
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1089, 967, 31, 91, 75): # epidemie
                input_helper.press('z')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(656, 892, 185, 140, 27) and image_helper.imgHelp.pixel_matches_color(702, 906, 90, 81, 57): # ss2 check
                self.use_skill('shift', '1')
                time.sleep(self.asleep)
            '''
            elif not image_helper.imgHelp.pixel_matches_color(614, 963, 0, 0, 0):
                input_helper.press('q')
                time.sleep(self.asleep)
            # standard rotation
            elif not image_helper.imgHelp.pixel_matches_color(883, 968, 0, 0, 0):
                input_helper.press('5')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(718, 969, 0, 0, 0):
                input_helper.press('2')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(773, 967, 0, 0, 0):
                input_helper.press('3')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(828, 971, 0, 0, 0):
                input_helper.press('4')
                time.sleep(self.asleep)
            else:
                input_helper.press('1')
                time.sleep(self.asleep)
                '''

    # harbinger pvp
    def necromant_harbinger(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            # health check
            if not image_helper.imgHelp.pixel_matches_color(961,932, 176,27,2) and image_helper.imgHelp.pixel_matches_color(960,995, 93,9,5): # at 20%
                self.use_skill('shift', '1')
            elif not image_helper.imgHelp.pixel_matches_color(962,985, 110,11,5) and image_helper.imgHelp.pixel_matches_color(961,940, 181,25,5): # heal at 70%
                input_helper.press('r')
                time.sleep(self.asleep)
            # skill checks
            elif not image_helper.imgHelp.pixel_matches_color(961,955, 165,21,5) and image_helper.imgHelp.pixel_matches_color(959,976, 121,15,5): # at 40%
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1093,967, 124,155,83):
                input_helper.press('z')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1143,971, 112,196,193):
                input_helper.press('x')
                time.sleep(self.asleep)

    # willbender
    def guardian_wb(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            # health check 
            if not image_helper.imgHelp.pixel_matches_color(962,985, 110,11,5) and image_helper.imgHelp.pixel_matches_color(1037,972, 117,166,149): # heal at 80%
                input_helper.press('r')
            elif not image_helper.imgHelp.pixel_matches_color(961,955, 165,21,5) and image_helper.imgHelp.pixel_matches_color(1257,967, 45,79,85): # at 60%
                input_helper.press('e')
                time.sleep(1.5)
            # class skill checks
            elif image_helper.imgHelp.pixel_matches_color(835,924, 32,210,239):
                self.use_skill('shift', '3')
                time.sleep(.75)
            elif image_helper.imgHelp.pixel_matches_color(801,933, 69,240,247):
                self.use_skill('shift', '2')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(751,927, 183,187,208):
                self.use_skill('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1092,971, 36,136,185):
                input_helper.press('z')
            elif image_helper.imgHelp.pixel_matches_color(1147,970, 159,204,156):
                input_helper.press('x')
            elif image_helper.imgHelp.pixel_matches_color(1202,965, 16,169,205):
                input_helper.press('c')
                time.sleep(.75)
            elif not image_helper.imgHelp.pixel_matches_color(614, 963, 0, 0, 0):
                time.sleep(self.asleep)
                input_helper.press('q')
            # standard rotation
            elif image_helper.imgHelp.pixel_matches_color(882,967, 235,237,235) or image_helper.imgHelp.pixel_matches_color(883,964, 41,40,36):
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(718,970, 66,163,222) or image_helper.imgHelp.pixel_matches_color(718,971, 143,226,245):
                input_helper.press('2')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(773,971, 184,213,253) or image_helper.imgHelp.pixel_matches_color(773,973, 51,80,101):
                input_helper.press('3')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(828,970, 132,211,206) or image_helper.imgHelp.pixel_matches_color(828,968, 23,26,29):
                input_helper.press('4')
                time.sleep(self.asleep)
            else:
                pass

    # heal fb
    def guardian_fb(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            # health check
            if not image_helper.imgHelp.pixel_matches_color(961,932, 176,27,2) and image_helper.imgHelp.pixel_matches_color(736, 919, 41, 51, 72): # at 30%
                self.use_skill('shift', '3')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(961,955, 165,21,5) and image_helper.imgHelp.pixel_matches_color(698, 921, 47, 77, 55): # at 60%
                self.use_skill('shift', '2')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(962,985, 110,11,5) and not image_helper.imgHelp.pixel_matches_color(1037, 967, 0, 0, 0): # heal at 80%
                input_helper.press('r')
                time.sleep(self.asleep)
                if not image_helper.imgHelp.pixel_matches_color(1091, 968, 0, 0, 0):
                    input_helper.press('z')
                    time.sleep(self.asleep)
            # class skill checks
            elif not image_helper.imgHelp.pixel_matches_color(1257, 968, 0, 0, 0):
                input_helper.press('e')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(1146, 970, 0, 0, 0):
                input_helper.press('x')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(660, 919, 24, 118, 108):
                self.use_skill('shift', '1')
                time.sleep(self.asleep)
            '''
            # standard rotation
            elif not image_helper.imgHelp.pixel_matches_color(883, 968, 0, 0, 0):
                input_helper.press('5')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(718, 969, 0, 0, 0):
                input_helper.press('2')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(773, 967, 0, 0, 0):
                input_helper.press('3')
                time.sleep(self.asleep)
            elif not image_helper.imgHelp.pixel_matches_color(828, 971, 0, 0, 0):
                input_helper.press('4')
                time.sleep(self.asleep)
            else:
                input_helper.press('q')
                time.sleep(self.asleep)
                '''

    # vindicator
    def revenant(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            if image_helper.imgHelp.pixel_matches_color(797,892, 255,255,255) or image_helper.imgHelp.pixel_matches_color(813,889, 186,250,254):
                self.use_skill('shift', '2')
                time.sleep(.5)
            elif image_helper.imgHelp.pixel_matches_color(824,888, 217,217,218):
                self.use_skill('shift', '3')
            # health check
            elif not image_helper.imgHelp.pixel_matches_color(961,932, 176,27,2) and (image_helper.imgHelp.pixel_matches_color(1257,967, 83,159,126) or image_helper.imgHelp.pixel_matches_color(1257,967, 254,234,0) or image_helper.imgHelp.pixel_matches_color(1257,967, 24,24,25)): # at 30%
                input_helper.press('e')
                time.sleep(1)
            elif not image_helper.imgHelp.pixel_matches_color(961,932, 176,27,2) and (image_helper.imgHelp.pixel_matches_color(1202,965, 88,67,74) or image_helper.imgHelp.pixel_matches_color(1202,965, 248,197,107) or image_helper.imgHelp.pixel_matches_color(1202,965, 16,20,24)): # at 30%
                input_helper.press('c')
            elif not image_helper.imgHelp.pixel_matches_color(962,985, 110,11,5) and (image_helper.imgHelp.pixel_matches_color(1037,972, 160,122,172) or image_helper.imgHelp.pixel_matches_color(1037,972, 110,32,6) or image_helper.imgHelp.pixel_matches_color(1037,972, 15,23,44)): # heal at 80%
                input_helper.press('r')
                time.sleep(.75)
            # skill check
            elif image_helper.imgHelp.pixel_matches_color(1092,971, 32,5,17) or image_helper.imgHelp.pixel_matches_color(1092,971, 17,1,1) or image_helper.imgHelp.pixel_matches_color(1092,971, 45,66,72):
                input_helper.press('z')
                time.sleep(.25)
            elif image_helper.imgHelp.pixel_matches_color(1147,970, 139,221,185) or image_helper.imgHelp.pixel_matches_color(1147,970, 89,26,15) or image_helper.imgHelp.pixel_matches_color(1147,970, 68,255,255):
                input_helper.press('x')
                time.sleep(.5)
            elif not image_helper.imgHelp.pixel_matches_color(660, 914, 0, 0, 0):
                self.use_skill('shift', '1')
                time.sleep(.25)
            elif image_helper.imgHelp.pixel_matches_color(624,978, 162,139,93):
                input_helper.press('q')
                time.sleep(.25)
            '''
            # standard rotation
            elif image_helper.imgHelp.pixel_matches_color(883, 971, 96, 95, 116) or image_helper.imgHelp.pixel_matches_color(883, 968, 255, 230, 136):
                input_helper.press('5')
                time.sleep(.75)
            elif image_helper.imgHelp.pixel_matches_color(718, 971, 219, 16, 23) or image_helper.imgHelp.pixel_matches_color(718, 966, 74, 80, 114):
                input_helper.press('2')
                time.sleep(.75)
            elif image_helper.imgHelp.pixel_matches_color(827, 969, 183, 165, 172) or image_helper.imgHelp.pixel_matches_color(828, 973, 136, 94, 85):
                input_helper.press('4')
                time.sleep(.75)
            elif image_helper.imgHelp.pixel_matches_color(718, 970, 249, 12, 16) or image_helper.imgHelp.pixel_matches_color(773, 967, 61, 76, 105):
                input_helper.press('3')
                time.sleep(.75)
            else:
                pass
                '''

    # untamed
    def ranger(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(784,99, 147,33,18):
            logging.info('got target, look for avaible skill')
            # health check
            if not image_helper.imgHelp.pixel_matches_color(960,1027, 112,13,) and image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\06.png') == 1: # heal at 45%
                input_helper.press('r')
                logging.debug('r - healing')
                time.sleep(1)
            elif not image_helper.imgHelp.pixel_matches_color(959,1034, 104,11,2) and image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\08.png') == 1: # at 25%
                input_helper.press('x')
                logging.debug('x')
            elif not image_helper.imgHelp.pixel_matches_color(961,1049, 88,9,5) and image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\10.png') == 1: # at 10%
                input_helper.press('e')
                logging.debug('e')
                time.sleep(1)
            # class skill checks
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\07.png') == 1:
                input_helper.press('y')
                logging.debug('y')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\09.png') == 1:
                input_helper.press('c')
                logging.debug('c')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s1.png') == 1:
                self.use_skill('shift', '1')
                time.sleep(.75)
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s2.png') == 1:
                self.use_skill('shift', '2')
                time.sleep(.75)
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s1-2.png') == 1:
                self.use_skill('shift', '1')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s2-2.png') == 1:
                self.use_skill('shift', '2')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s3.png') == 1 or image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s3-2.png') == 1:
                self.use_skill('shift', '3')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s4.png') == 1:
                self.use_skill('shift', '4')
                if image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s5.png') == 1 or image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\s5-2.png') == 1:
                    time.sleep(.25)
                    self.use_skill('shift', '5')
            elif image_helper.imgHelp.locate_img(SKILLPATH+'WeaponSwitch.png') == 1:
                input_helper.press('q')
                time.sleep(.25)
            # standard rotation
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\04.png') == 1:
                time.sleep(.25)
                input_helper.press('4')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\03.png') == 1:
                time.sleep(.25)
                input_helper.press('3')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\05.png') == 1:
                time.sleep(.25)
                input_helper.press('5')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.locate_img(SKILLPATH+'ranger\\02.png') == 1:
                time.sleep(.25)
                input_helper.press('2')
                time.sleep(self.asleep)
            else:
                pass

    # specter
    def thief(self):
        # target check
        if image_helper.imgHelp.pixel_matches_color(783,124, 147,33,18):
            # health check
            if not image_helper.imgHelp.pixel_matches_color(962,985, 110,11,5) and image_helper.imgHelp.pixel_matches_color(1037,972, 57,29,40): # heal at 80%
                input_helper.press('r')
                time.sleep(1)
            elif not image_helper.imgHelp.pixel_matches_color(961,955, 165,21,5) and image_helper.imgHelp.pixel_matches_color(1257,967, 97,19,30): # at 60%
                input_helper.press('e')
                time.sleep(self.asleep)
            # class skill checks
            elif image_helper.imgHelp.pixel_matches_color(1092,971, 149,100,7):
                input_helper.press('z')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(1147,970, 9,9,9):
                input_helper.press('x')
            elif image_helper.imgHelp.pixel_matches_color(1202,965, 32,26,24) or image_helper.imgHelp.pixel_matches_color(1202,965, 109,96,98):
                input_helper.press('c')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(659,922, 124,39,25):
                self.use_skill('shift', '1')
                time.sleep(self.asleep)
            elif image_helper.imgHelp.pixel_matches_color(692,923, 164,118,127):
                self.use_skill('shift', '2')


skillRota = SkillRotation

