from win32gui import FindWindow, SetForegroundWindow, SetWindowPos, EnumWindows, GetWindowText
from win32con import HWND_TOP, SWP_NOSIZE

class ProcessHelper:
    def __init__(self, window_substring='Diablo IV', hwnd=None):
        """
        Initialize the ProcessHelper.
        :param window_substring: Partial title of the window to locate.
        :param hwnd: Optional, specific HWND if already known.
        """
        self.window_substring = window_substring
        self.hwnd = self.get_hwnd(hwnd)

    def get_hwnd(self, hwnd=None):
        """
        Get the window handle (HWND) of the target application.
        :param hwnd: Optional specific handle.
        :return: HWND of the window.
        :raises Exception: If the window cannot be found.
        """
        if hwnd is None:
            hwnd = self.find_window()
            if hwnd == 0:
                raise Exception(f"Window containing '{self.window_substring}' not found.")
        return hwnd

    def find_window(self, classname=None):
        """
        Locate the HWND using a class name or window title substring.
        :param classname: Optional class name for precise matching.
        :return: HWND of the window or 0 if not found.
        """
        hwnd = FindWindow(classname, self.window_substring)
        if hwnd == 0:  # Attempt substring match with EnumWindows if FindWindow fails
            hwnd = self.find_window_by_substring()
        return hwnd

    def find_window_by_substring(self):
        """
        Enumerates all windows and matches based on title substring.
        :return: HWND of the matching window or 0 if not found.
        """
        matching_hwnd = 0

        def enum_callback(hwnd, _):
            nonlocal matching_hwnd
            if self.window_substring.lower() in GetWindowText(hwnd).lower():
                matching_hwnd = hwnd
                return False  # Stop iteration

        EnumWindows(enum_callback, None)
        return matching_hwnd

    def set_foreground_window(self):
        """
        Bring the target window to the foreground.
        :raises Exception: If the operation fails.
        """
        if not self.hwnd:
            raise Exception("HWND is not set. Cannot bring window to the foreground.")
        SetForegroundWindow(self.hwnd)

    def set_window_pos(self, x=0, y=0, flag=HWND_TOP):
        """
        Set the window position on the screen.
        :param x: X-coordinate for the window position.
        :param y: Y-coordinate for the window position.
        :param flag: Z-order flag, default is HWND_TOP.
        """
        if not self.hwnd:
            raise Exception("HWND is not set. Cannot reposition the window.")
        SetWindowPos(self.hwnd, flag, x, y, 0, 0, SWP_NOSIZE)
