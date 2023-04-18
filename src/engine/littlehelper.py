import os
import threading
import time
import logging
import importlib

from helper import config_helper, image_helper


class LittleHelper:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()
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
        
    def set_import(self, lib):
        mylib = importlib.import_module(lib)
        cr = mylib.CombatRotation()
        cr.default_combat()

    def get_combat_rotation(self):
        """set up the skill rotation for a specific class injected by the config file"""
        while self.should_pause():
            time.sleep(0.25)
        get_file = self.cfg['file']

        if get_file != None:
            module_name, module_ext = os.path.splitext(get_file)
            self.set_import(module_name)
        else:
            logging.error('No vaible file preset')

    def get_color_from_pos(self):
        """debug function, print coordinates and rgb color at mouse position"""
        x,y, r,g,b = image_helper.get_pixel_color_at_cursor()
        logging.info("Position at: x,y, r,g,b = %d,%d, %d,%d,%d" % (x,y, r,g,b))

    def get_image_from_pos(self, name, path, ix, iy):
        """debug function, print coordinates and save image at mouse position"""
        x,y = image_helper.get_image_at_cursor(name, path, ix, iy)
        logging.info("Saved %s in %s at: x=%d, y=%d, size=%d, %d" % (str(name+'.png'),path,x,y,ix,iy))


lilHelp = LittleHelper()

def run_bot():
    lilHelp.get_combat_rotation()

def toolbox_print_pos():
    lilHelp.get_color_from_pos()

def toolbox_save_img(name, path, ix, iy):
    lilHelp.get_image_from_pos(name, path, ix, iy)

