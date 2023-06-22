import win32gui, win32con


WINDOW_SUBSTRING = 'Diablo IV'


class ProcessHelper:
    def __init__(self, hwnd=None) -> None:
        self.hwnd = self.get_hwnd(hwnd)


    def get_hwnd(self, hwnd=None):
        if hwnd == None:
            hwnd = self.find_window()
            if hwnd == 0:
                raise Exception("window not found", hwnd)
        else:
            hwnd = hwnd
        return hwnd


    def find_window(self, classname=None):
        '''Get the window handle using the class name and the title of the window, the class name can be empty'''
        hwnd = win32gui.FindWindow(classname, WINDOW_SUBSTRING)
        return hwnd


    def set_foreground_window(self):
        win32gui.SetForegroundWindow(self.hwnd)


    def set_window_pos(self, x=0, y=0, flag=win32con.HWND_TOP):
        '''specify that the window is displayed at the top, etc., see: win32api SetWindowPos '''
        win32gui.SetWindowPos(self.hwnd, flag, x, y, 0, 0, win32con.SWP_NOSIZE)

