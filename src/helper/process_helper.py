from time import sleep, time
from typing import Optional, List

from win32gui import (
    FindWindow,
    SetForegroundWindow,
    SetWindowPos,
    EnumWindows,
    GetWindowText,
    IsWindow,
    IsWindowVisible,
)
from win32con import HWND_TOP, SWP_NOSIZE

from helper import logging_helper


class ProcessError(Exception):
    """Spezielle Ausnahme fuer Prozesse/Window-Operationen."""
    pass


class ProcessHelper:
    """
    Helfer zum Auffinden und Steuern eines Fensters anhand eines Teil-Titels.

    Beispiel:
        ph = ProcessHelper('Diablo IV')
        ph.set_foreground_window()
        ph.set_window_pos(0, 0)
    """

    def __init__(self, window_substring: str = "Diablo IV", hwnd: Optional[int] = None):
        self.window_substring = str(window_substring or "").strip()
        self.hwnd: Optional[int] = None
        # Validiere oder suche HWND
        try:
            self.hwnd = self.get_hwnd(hwnd)
        except ProcessError:
            # Nicht fatal beim Konstruktor � caller kann refresh_hwnd() verwenden
            logging_helper.log_debug(
                f"ProcessHelper init: window '{self.window_substring}' not found during init."
            )
            self.hwnd = None

    def is_valid_hwnd(self, hwnd: Optional[int]) -> bool:
        """Pr�ft, ob ein HWND g�ltig und sichtbar ist."""
        try:
            return bool(hwnd) and IsWindow(int(hwnd)) and IsWindowVisible(int(hwnd))
        except Exception:
            return False

    def get_hwnd(self, hwnd: Optional[int] = None) -> int:
        """
        Liefert einen g�ltigen HWND zur�ck.
        Wenn `hwnd` �bergeben wird, wird dessen Validit�t gepr�ft.
        Andernfalls wird per Suche versucht, ein Fenster mit dem Teil-Titel zu finden.
        Raises ProcessError, wenn kein passendes Fenster gefunden wird.
        """
        if hwnd is not None:
            if self.is_valid_hwnd(hwnd):
                logging_helper.log_debug(f"get_hwnd: provided hwnd {hwnd} is valid.")
                return int(hwnd)
            raise ProcessError(f"Provided hwnd {hwnd} is not valid or not visible.")

        found = self.find_window()
        if found:
            logging_helper.log_debug(f"get_hwnd: found hwnd {found} for '{self.window_substring}'.")
            return found

        raise ProcessError(f"Window containing '{self.window_substring}' not found.")

    def refresh_hwnd(self, timeout: float = 5.0, interval: float = 0.5) -> Optional[int]:
        """
        Versucht f�r `timeout` Sekunden periodisch, ein Fenster mit dem Teil-Titel zu finden.
        Gibt das gefundene HWND zur�ck oder None, wenn nichts gefunden wurde.
        """
        deadline = time() + float(timeout)
        while time() < deadline:
            hwnd = self.find_window()
            if hwnd:
                self.hwnd = hwnd
                logging_helper.log_info(f"refresh_hwnd: found window hwnd={hwnd}")
                return hwnd
            sleep(float(interval))
        logging_helper.log_debug(f"refresh_hwnd: timeout, window '{self.window_substring}' not found.")
        return None

    def find_window(self, classname: Optional[str] = None) -> int:
        """
        Versucht zuerst FindWindow (exakter Match, falls classname gesetzt),
        ansonsten f�llt zur�ck auf substring-basierte Enumeration.
        Gibt 0 zur�ck, wenn nicht gefunden.
        """
        try:
            # Wenn classname angegeben ist, FindWindow mit classname + exact title
            hwnd = FindWindow(classname, self.window_substring) if classname else 0
        except Exception as ex:
            logging_helper.log_debug(f"find_window: FindWindow failed: {ex}")
            hwnd = 0

        if hwnd and self.is_valid_hwnd(hwnd):
            return int(hwnd)

        # Try substring match
        return self.find_window_by_substring()

    def find_window_by_substring(self) -> int:
        """
        Enumeriert alle Fenster und findet das erste sichtbare Fenster,
        dessen Titel das `window_substring` enth�lt (case-insensitive).
        Gibt HWND oder 0 zur�ck.
        """
        substring = self.window_substring.lower()
        candidates: List[int] = []

        def _enum(hwnd, _):
            try:
                if not IsWindow(hwnd) or not IsWindowVisible(hwnd):
                    return
                title = GetWindowText(hwnd) or ""
                if substring and substring in title.lower():
                    candidates.append(int(hwnd))
            except Exception:
                # Ignoriere einzelne Fenster-Fehler
                return

        try:
            EnumWindows(_enum, None)
        except Exception as ex:
            logging_helper.log_debug(f"find_window_by_substring: EnumWindows failed: {ex}")
            return 0

        if candidates:
            logging_helper.log_debug(f"find_window_by_substring: candidates={candidates}")
            return candidates[0]
        return 0

    def set_foreground_window(self, timeout: float = 2.0, force: bool = True) -> None:
        """
        Bringt das Ziel-Fenster in den Vordergrund.
        Wenn fehlschl�gt und `force` True ist, wird zus�tzlich SetWindowPos angewendet.
        Gibt bei Fehler eine ProcessError-Ausnahme.
        """
        if not self.hwnd or not self.is_valid_hwnd(self.hwnd):
            raise ProcessError("HWND is not set or not valid. Call refresh_hwnd() first.")

        try:
            SetForegroundWindow(self.hwnd)
            logging_helper.log_debug(f"set_foreground_window: SetForegroundWindow({self.hwnd}) called.")
            return
        except Exception as ex:
            logging_helper.log_debug(f"set_foreground_window: SetForegroundWindow failed: {ex}")

        if force:
            try:
                # Position kurz neu setzen, um Fokusting zu erzwingen
                SetWindowPos(self.hwnd, HWND_TOP, 0, 0, 0, 0, SWP_NOSIZE)
                sleep(0.05)
                SetForegroundWindow(self.hwnd)
                logging_helper.log_debug("set_foreground_window: forced via SetWindowPos + SetForegroundWindow.")
                return
            except Exception as ex:
                logging_helper.log_error(f"set_foreground_window: forced focus failed: {ex}")
                raise ProcessError(f"Failed to bring window to foreground: {ex}") from ex

        raise ProcessError("Failed to bring window to foreground.")

    def set_window_pos(
        self,
        x: int = 0,
        y: int = 0,
        flag: int = HWND_TOP,
    ) -> None:
        """
        Setzt die Position des Fensters. Beachtet SWP_NOSIZE (Standardeinstellung).
        Falls HWND nicht g�ltig, wird ProcessError geworfen.
        """
        if not self.hwnd or not self.is_valid_hwnd(self.hwnd):
            raise ProcessError("HWND is not set or not valid. Call refresh_hwnd() first.")

        try:
            SetWindowPos(self.hwnd, flag, int(x), int(y), 0, 0, SWP_NOSIZE)
            logging_helper.log_debug(f"set_window_pos: SetWindowPos({self.hwnd}, {flag}, {x}, {y})")
        except Exception as ex:
            logging_helper.log_error(f"set_window_pos failed: {ex}")
            raise ProcessError(f"Failed to set window position: {ex}") from ex
