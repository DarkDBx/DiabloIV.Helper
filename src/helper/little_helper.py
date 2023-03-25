import threading
import time
import logging

from helper import config_helper, image_helper
from engine import skill_rotation


class LittleHelper:
    def __init__(self):
        self._lock = threading.Lock()
        self.pause_req = False
        self.cfg = config_helper.read_config()
    
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
        while self.should_pause():
            time.sleep(.5)
        if self.cfg['class'] == 'Scourge Support':
            skill_rotation.skillRota.necromant_scourge()
            logging.info('Skill rotation set for scourge')
        elif self.cfg['class'] == 'Harbinger':
            skill_rotation.skillRota.necromant_harbinger()
            logging.info('Skill rotation set for harbinger')
        elif self.cfg['class'] == 'Willbender':
            skill_rotation.skillRota.guardian_wb()
            logging.info('Skill rotation set for willbender')
        elif self.cfg['class'] == 'Heal FB':
            skill_rotation.skillRota.guardian_fb()
            logging.info('Skill rotation set for firebrand')
        elif self.cfg['class'] == 'Vindicator':
            skill_rotation.skillRota.revenant()
            logging.info('Skill rotation set for revenant')
        elif self.cfg['class'] == 'Untamed':
            skill_rotation.skillRota.ranger()
            logging.info('Skill rotation set for untamed')
        elif self.cfg['class'] == 'Specter':
            skill_rotation.skillRota.thief()
            logging.info('Skill rotation set for thief')
        else:
            logging.error('no class set')

    def get_color_from_pos(self):
        # debug function
        while True:
            while self.should_pause():
                time.sleep(.5)
            x,y, r,g,b = image_helper.imgHelp.get_pixel_color_at_cursor()
            img = image_helper.imgHelp.locate_img('.\\assets\\skills\\WeaponSwitch.png')
            if x<1920 and y<1080:
                logging.info("Mouse[x,y, r,g,b: %d,%d, %d,%d,%d - Reference: \"%s\"]" % (x,y, r,g,b, img))
                time.sleep(.2)


lilHelp = LittleHelper()

def run():
    lilHelp.set_rotation()

def debug():
    lilHelp.get_color_from_pos()

