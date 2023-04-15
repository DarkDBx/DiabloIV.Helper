import threading
import time
from time import process_time_ns
from pynput import mouse as mo
from pynput import keyboard as ke
from pynput.keyboard import Controller as Controller_k, Key
from pynput.mouse import Controller as Controller_m, Button

from helper import input_helper


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
        self.history.append((time.time_ns() - self.st_tm, "{0}".format(button), pressed, x, y))

    def scroll(self, x, y, dx, dy):
        self.history.append((time.time_ns() - self.st_tm, "scroll", dy, x, y))

    def press(self, key):
        try:
            self.history.append((time.time_ns() - self.st_tm, "key", key.char, True, True))
        except AttributeError:
            self.history.append((time.time_ns() - self.st_tm, "key", str(key), True, False))

    def release(self, key):
        try:
            self.history.append((time.time_ns() - self.st_tm, "key", key.char, False, True))
        except AttributeError:
            self.history.append((time.time_ns() - self.st_tm, "key", str(key), False, False))

    def record_start(self):
        self.st_tm = time.time_ns()
        self.m_listener.start()
        self.k_listener.start()

    def record_stop(self):
        self.m_listener.stop()
        self.k_listener.stop()
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


class Replay(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)

        file = open(path, "r")
        self.recording = eval(file.read())

        self.length = len(self.recording)
        self.dic = dic
        self.keyboard = Controller_k()
        self.mouse = Controller_m()

    def run(self):
        st_tm = process_time_ns()

        for z in range(self.length):
            action = self.recording[z]

            tm = st_tm + action[0]
            x = action[3]
            y = action[4]

            while process_time_ns() < tm:
                pass

            if action[1][:7] == "Button.":
                self.mouse.position = (x, y)
                try:
                    if action[2]:
                        input_helper.mo._move_to(x, y)
                        self.mouse.press(self.dic[action[1]])
                    else:
                        input_helper.mo._move_to(x, y)
                        self.mouse.release(self.dic[action[1]])
                except KeyError:
                    print("ERROR: unknown key " + str(action[2]))

            elif action[1] == "scroll":
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
                        print("ERROR: unknown key " + str(action[2]))

                else:
                    try:
                        if action[4]:
                            self.keyboard.release(action[2])
                        else:
                            self.keyboard.release(self.dic[action[2]])
                    except KeyError:
                        print("ERROR: unknown key " + str(action[2]))

            else:
                print("ERROR: unknown action")

