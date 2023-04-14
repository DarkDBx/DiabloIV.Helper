import threading
import time
import logging

from helper import config_helper, image_helper
from engine import skill_rotation


class LittleHelper:
    def __init__(self) -> None:
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

    def get_combat_rotation(self):
        """set up the skill rotation for a specific class injected by the config file"""
        while self.should_pause():
            time.sleep(0.25)
        if self.cfg['game'] == 'Guild Wars 2':
            if self.cfg['class'] == 'Vindicator PvP':
                skill_rotation.skillRota.revenant_pvp()
            elif self.cfg['class'] == 'Soulbeast PvP':
                skill_rotation.skillRota.ranger_pvp()
            else:
                logging.error('No vaible class preset')
        elif self.cfg['game'] == 'Elder Scrolls Online':
            if self.cfg['class'] == 'Nightblade PvE':
                skill_rotation.nightblade_pve()
            elif self.cfg['class'] == 'Nightblade PvP':
                skill_rotation.nightblade_pvp()
            else:
                logging.error('No vaible class preset')
        else:
            logging.error('No vaible game preset')

    def get_color_from_pos(self):
        """debug function, print coordinates and rgb color at mouse position"""
        x,y, r,g,b = image_helper.get_pixel_color_at_cursor()
        logging.info("Mouse[x,y, r,g,b: %d,%d, %d,%d,%d]" % (x,y, r,g,b))

    def get_image_from_pos(self, name, path, ix, iy):
        """debug function, print coordinates and save image at mouse position"""
        x,y = image_helper.get_image_at_cursor(name, path, ix, iy)
        logging.info("Saved %s in %s at x=%d, y=%d, size=%d, %d" % (str(name),path,x,y,ix,iy))


lilHelp = LittleHelper()

def run_bot():
    lilHelp.get_combat_rotation()

def toolbox_print_pos():
    lilHelp.get_color_from_pos()

def toolbox_save_img(name, path, ix, iy):
    lilHelp.get_image_from_pos(name, path, ix, iy)

