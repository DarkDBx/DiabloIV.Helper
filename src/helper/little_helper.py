import threading
import time
import logging

from helper import config_helper, image_helper
from engine import skill_rotation


class LittleHelper:
    def __init__(self):
        self._lock = threading.Lock()
        self.pause_req = False
    
    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req

    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()

    def set_rotation(self):
        cfg = config_helper.read_config()
        while self.should_pause():
            time.sleep(.5)
        if cfg['class'] == 'Scourge Support':
            skill_rotation.skillRota.necromant_scourge()
            logging.info('Skill rotation set for scourge')
        elif cfg['class'] == 'Harbinger':
            skill_rotation.skillRota.necromant_harbinger()
            logging.info('Skill rotation set for harbinger')
        elif cfg['class'] == 'Willbender':
            skill_rotation.skillRota.guardian_wb()
            logging.info('Skill rotation set for willbender')
        elif cfg['class'] == 'Heal FB':
            skill_rotation.skillRota.guardian_fb()
            logging.info('Skill rotation set for firebrand')
        elif cfg['class'] == 'Vindicator':
            skill_rotation.skillRota.revenant()
            logging.info('Skill rotation set for revenant')
        elif cfg['class'] == 'Untamed':
            skill_rotation.skillRota.ranger()
            logging.info('Skill rotation set for untamed')
        elif cfg['class'] == 'Specter':
            skill_rotation.skillRota.thief()
            logging.info('Skill rotation set for thief')
        else:
            pass

    def get_color_from_pos(self):
        # debug function
        while True:
            while self.should_pause():
                time.sleep(.5)
            r1,g1,b1 = image_helper.imgHelp.pixel_color_rgb(1037,972)
            r2,g2,b2 = image_helper.imgHelp.pixel_color_rgb(1092,971)
            r3,g3,b3 = image_helper.imgHelp.pixel_color_rgb(1147,970)
            r4,g4,b4 = image_helper.imgHelp.pixel_color_rgb(1201,970)
            r5,g5,b5 = image_helper.imgHelp.pixel_color_rgb(1257,967)
            r6,g6,b6 = image_helper.imgHelp.pixel_color_rgb(624,978)
            r7,g7,b7 = image_helper.imgHelp.pixel_color_rgb(885,925)
            x,y, r,g,b = image_helper.imgHelp.get_pixel_color_at_cursor()
            img = image_helper.imgHelp.locate_img('.\\assets\\skills\\WeaponSwitch.png')
            if x<1920 and y<1080:
                logging.debug("Mouse[x,y, r,g,b: %d,%d, %d,%d,%d - Reference: \"%s\"]" % (x,y, r,g,b, img))
                logging.debug("R[1037,972, %d,%d,%d]" % (r1,g1,b1))
                logging.debug("Y[1092,971, %d,%d,%d]" % (r2,g2,b2))
                logging.debug("X[1147,970, %d,%d,%d]" % (r3,g3,b3))
                logging.debug("C[1201,970, %d,%d,%d]" % (r4,g4,b4))
                logging.debug("E[1257,967, %d,%d,%d]" % (r5,g5,b5))
                logging.debug("Q[624,978, %d,%d,%d]" % (r6,g6,b6))
                logging.debug("s4[885,925, %d,%d,%d]" % (r7,g7,b7))
                time.sleep(.2)


lilHelp = LittleHelper

def run():
    lilHelp.set_rotation()

def debug():
    lilHelp.get_color_from_pos()

