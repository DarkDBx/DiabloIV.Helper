import win32gui, win32con


WINDOW_SUBSTRING = 'Guild Wars 2'

def get_hwnd(hwnd=None):
    if hwnd == None:
        hwnd = find_window(None)
        if hwnd == 0:
            raise Exception("window not found", hwnd)
    else:
        hwnd = hwnd
    return hwnd

def find_window(classname=None):
    '''Get the window handle using the class name and the title of the window, the class name can be empty'''
    hwnd = win32gui.FindWindow(classname, WINDOW_SUBSTRING)
    return hwnd

def set_foreground_window():
    win32gui.SetForegroundWindow(get_hwnd())

def set_window_pos(x=0, y=0, flag=win32con.HWND_TOP):
    '''specify that the window is displayed at the top, etc., see: win32api SetWindowPos '''
    win32gui.SetWindowPos(get_hwnd(), flag, x, y, 0, 0, win32con.SWP_NOSIZE)

