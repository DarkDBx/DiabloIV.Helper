import json
import logging
from threading import Thread
from time import time
from pynput import mouse as mo
from pynput import keyboard as ke
from pynput.keyboard import Controller as Controller_k, Key
from pynput.mouse import Controller as Controller_m, Button

from helper import process_helper, mouse_helper
from engine import bot

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

dic = {
    "Key.tab": Key.tab,
    "Key.caps_lock": Key.caps_lock,
    "Key.shift": Key.shift,
    "Key.ctrl_l": Key.ctrl_l,
    "Key.cmd": Key.cmd,
    "Key.alt_l": Key.alt_l,
    "Key.space": Key.space,
    "Key.alt_gr": Key.alt_gr,
    "Key.ctrl_r": Key.ctrl_r,
    "Key.left": Key.left,
    "Key.up": Key.up,
    "Key.down": Key.down,
    "Key.right": Key.right,
    "Key.shift_r": Key.shift_r,
    "Key.enter": Key.enter,
    "Key.backspace": Key.backspace,
    "Key.esc": Key.esc,
    "Button.left": Button.left,
    "Button.right": Button.right,
    "Button.middle": Button.middle,
}

class Record:
    def __init__(self):
        self.history = []
        self.k_listener = ke.Listener(on_press=self.press, on_release=self.release)
        self.m_listener = mo.Listener(on_click=self.click, on_scroll=self.scroll)

    def click(self, x, y, button, pressed):
        self.history.append((time() - self.st_tm, str(button), pressed, x, y))

    def scroll(self, x, y, dx, dy):
        self.history.append((time() - self.st_tm, "scroll", dy, x, y))

    def press(self, key):
        try:
            self.history.append((time() - self.st_tm, "key", key.char, True, True))
        except AttributeError:
            self.history.append((time() - self.st_tm, "key", str(key), True, False))

    def release(self, key):
        try:
            self.history.append((time() - self.st_tm, "key", key.char, False, True))
        except AttributeError:
            self.history.append((time() - self.st_tm, "key", str(key), False, False))

    def prepare_record_start(self):
        if not hasattr(self, 'replay_thread') or not self.replay_thread.is_alive():
            self.replay_thread = Thread(target=self.record_start)
            self.replay_thread.start()

    def record_start(self):
        proc = process_helper.ProcessHelper()
        proc.set_foreground_window()
        self.st_tm = time()
        self.m_listener.start()
        self.k_listener.start()

    def record_stop(self):
        self.m_listener.stop()
        self.k_listener.stop()
        self.replay_thread.join()
        
        # Remove duplicate events
        self.history = [
            event for i, event in enumerate(self.history)
            if i == 0 or event[1:] != self.history[i - 1][1:]
        ]
        return self.history

class Replay:
    def __init__(self, path):
        try:
            with open(path, "r") as file:
                self.recording = json.load(file)
        except Exception as e:
            logger.error(f"Error loading recording file: {e}")
            raise

        self.length = len(self.recording)
        self.dic = dic
        self.keyboard = Controller_k()
        self.mouse = Controller_m()
        self.robot = bot.Bot()

    def replay_run(self):
        proc = process_helper.ProcessHelper()
        proc.set_foreground_window()

        for action in self.recording:
            tm, x, y = action[0], action[3], action[4]

            if action[1].startswith("Button."):
                mouse_helper.move_smooth(x, y, tm)
                try:
                    if action[2]:
                        self.mouse.press(self.dic[action[1]])
                    else:
                        self.mouse.release(self.dic[action[1]])
                except KeyError:
                    logger.error(f"Unknown button: {action[1]}")

            elif action[1] == "scroll":
                mouse_helper.move_smooth(x, y, tm)
                self.mouse.scroll(None, action[2])

            elif action[1] == "key":
                try:
                    if action[3]:
                        if action[4]:
                            self.keyboard.press(action[2])
                        else:
                            self.keyboard.press(self.dic[action[2]])
                    else:
                        if action[4]:
                            self.keyboard.release(action[2])
                        else:
                            self.keyboard.release(self.dic[action[2]])
                except KeyError:
                    logger.error(f"Unknown key: {action[2]}")
            else:
                logger.error(f"Unknown action type: {action[1]}")

            self.robot.game_manager(False)

    @staticmethod
    def add_key_mapping(key_str, key_obj):
        dic[key_str] = key_obj
