from sys import exit
import win32gui, win32con
import logging

from helper import config_helper


cfg = config_helper.read_config()

'''Get the window handle using the class name and the title of the window, the class name can be empty'''
def find_window(handle):
    hwnd = win32gui.FindWindow(None, handle)
    return hwnd

def get_hwnd(handle=cfg['game'], hwnd=None):
    if hwnd == None:
        hwnd = find_window(handle)
        if hwnd == 0:
            logging.error("Window to look for not found: "+handle)
            logging.error("Shutting down bot engine...")
            return 0
    else:
        hwnd = hwnd
    return hwnd

def set_foreground_window():
    set_hwnd = get_hwnd()
    if set_hwnd != 0:
        win32gui.SetForegroundWindow(set_hwnd)
    else:
        exit()

'''Specify that the window is displayed at the top, etc., see: win32api SetWindowPos'''
def set_window_pos(x=0, y=0, flag=win32con.HWND_TOP):
    win32gui.SetWindowPos(get_hwnd(), flag, x, y, 0, 0, win32con.SWP_NOSIZE)

