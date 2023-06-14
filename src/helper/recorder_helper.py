import threading
import logging
import time
from time import process_time_ns
from pynput import mouse as mo
from pynput import keyboard as ke
from pynput.keyboard import Controller as Controller_k, Key
from pynput.mouse import Controller as Controller_m, Button

from helper import process_helper, image_helper
from engine import bot, combat


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
    "Key.shift_r": 	Key.shift_r,
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
        self.history.append((time.time() - self.st_tm, "{0}".format(button), pressed, x, y))


    def scroll(self, x, y, dx, dy):
        self.history.append((time.time() - self.st_tm, "scroll", dy, x, y))


    def press(self, key):
        try:
            self.history.append((time.time() - self.st_tm, "key", key.char, True, True))
        except AttributeError:
            self.history.append((time.time() - self.st_tm, "key", str(key), True, False))


    def release(self, key):
        try:
            self.history.append((time.time() - self.st_tm, "key", key.char, False, True))
        except AttributeError:
            self.history.append((time.time() - self.st_tm, "key", str(key), False, False))


    def prepare_record_start(self):
        self.replay_thread = threading.Thread(target=self.record_start)
        self.replay_thread.start()


    def record_start(self):
        ph = process_helper.ProcessHelper()
        ph.set_foreground_window()

        self.st_tm = time.time()
        self.m_listener.start()
        self.k_listener.start()


    def record_stop(self):
        self.m_listener.stop()
        self.k_listener.stop()
        self.replay_thread.join()
        self.history.pop()  # deletes last clicks
        self.history.pop()

        x = 0
        y = 1
        le = len(self.history)
        for z in range(le):
            if z != 0:
                if self.history[x][1:] == self.history[y][1:]:
                    self.history.pop(x)  # delete duplicate clicks
                else:
                    x += 1
                    y += 1
        return self.history


class Replay:
    def __init__(self, path) -> None:
        file = open(path, "r")
        self.recording = eval(file.read())
        self.length = len(self.recording)
        self.dic = dic
        self.keyboard = Controller_k()
        self.mouse = Controller_m()
        self.robot = bot.Bot()
        
        replay_thread = threading.Thread(target=self.replay_run)
        replay_thread.start()
        replay_thread.join()
        logging.info("Replay stopped")


    def replay_run(self):
        ph = process_helper.ProcessHelper()
        ph.set_foreground_window()

        for z in range(self.length):
            action = self.recording[z]
            tm = action[0]
            x = action[3]
            y = action[4]

            if action[1][:7] == "Button.":
                #input_helper.move_smooth(x, y, tm)
                time.sleep(tm)
                self.mouse.position = (x, y)
                try:
                    if action[2]:
                        self.mouse.press(self.dic[action[1]])
                    else:
                        self.mouse.release(self.dic[action[1]])
                except KeyError:
                    logging.error("Unknown key " + str(action[2]))

            elif action[1] == "scroll":
                #input_helper.move_smooth(x, y, tm)
                time.sleep(tm)
                self.mouse.position = (x, y)
                self.mouse.scroll(None, action[2])
                
            elif action[1] == "key":
                if action[3]:
                    try:
                        if action[4]:
                            self.keyboard.press(action[2])
                        else:
                            self.keyboard.press(self.dic[action[2]])
                    except KeyError:
                        logging.error("Unknown key " + str(action[2]))
                else:
                    try:
                        if action[4]:
                            self.keyboard.release(action[2])
                        else:
                            self.keyboard.release(self.dic[action[2]])
                    except KeyError:
                        logging.error("Unknown key " + str(action[2]))
            else:
                logging.error("Unknown action")

            self.robot.game_manager()

