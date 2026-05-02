from time import sleep
from random import randint, uniform
from typing import Iterable, Optional, Tuple
from pathlib import Path

from pydirectinput import leftClick, rightClick, press

from helper import mouse_helper, image_helper, config_helper, logging_helper
from bot import pather, pickit, rotation

ASSETS_DIR = Path(__file__).resolve().parents[1] / "src/assets"
LOCATION_DIR = str(ASSETS_DIR / "location")

class Manager:
    def __init__(self) -> None:
        # Config beim Start laden; bei Bedarf kann reload_config() verwendet werden
        self.cfg = self.reload_config()

    def reload_config(self):
        try:
            return config_helper.read_config() or {}
        except Exception as ex:
            logging_helper.log_debug("Failed to read config: %s" % ex)
            return {}

    def _safe_locate(self, path: str, **kwargs) -> Tuple[int, int]:
        """
        Wrapper fuer image_helper.locate_needle, der ein konsistentes (-1, -1) zurueckgibt bei Fehlern.
        """
        try:
            res = image_helper.locate_needle(path, **kwargs)
            if res is True:
                return 0, 0
            if not res or res is False:
                return -1, -1
            if hasattr(res, 'x') and hasattr(res, 'y'):
                return int(res.x), int(res.y)
            if isinstance(res, (tuple, list)) and len(res) >= 2:
                if res[0] is None or res[1] is None:
                    return -1, -1
                return int(res[0]), int(res[1])
            return -1, -1
        except Exception as ex:
            logging_helper.log_debug("locate_needle error for %s: %s" % (path, ex))
            return -1, -1

    def pixel_match_check(self, conditions: Iterable[Tuple[int, int, int, int, int]]) -> bool:
        """Check multiple pixel conditions for state validation."""
        try:
            return all(image_helper.pixel_matches_color(*cond) for cond in conditions)
        except Exception as ex:
            logging_helper.log_debug("pixel_match_check error: %s" % ex)
            return False

    def is_on_landing(self) -> bool:
        conditions = [(3, 2, 22, 30, 31), (491, 888, 18, 17, 18)]
        return self.pixel_match_check(conditions)

    def is_on_menu(self) -> bool:
        conditions = [(74, 314, 235, 8, 2), (70, 302, 148, 10, 3)]
        return self.pixel_match_check(conditions)

    def is_on_loading(self) -> bool:
        try:
            return image_helper.pixel_matches_color(1, 1, 0, 0, 0, tolerance=0)
        except Exception as ex:
            logging_helper.log_debug("is_on_loading pixel check failed: %s" % ex)
            return False

    def is_in_game(self) -> bool:
        conditions = [(718, 984, 59, 75, 84), (1209, 966, 56, 76, 81)]
        return self.pixel_match_check(conditions)

    def is_death(self) -> bool:
        conditions = [(831, 859, 147, 81, 32), (846, 898, 47, 1, 1)]
        return self.pixel_match_check(conditions)

    def click_randomized(self, x: Optional[int] = None, y: Optional[int] = None,
                         jitter: Tuple[int, int, int, int] = (-5, 35, -5, 5), button: str = 'left') -> None:
        """Perform a randomized click action."""
        try:
            if x is None or y is None:
                if button == 'left':
                    leftClick()
                else:
                    rightClick()
                logging_helper.log_debug("Clicked at current cursor position (%s)" % button)
                return

            ex = randint(jitter[0], jitter[1])
            ey = randint(jitter[2], jitter[3])
            fx, fy = int(x + ex), int(y + ey)

            if button == 'left':
                leftClick(fx, fy)
            else:
                rightClick(fx, fy)

            logging_helper.log_debug("Clicked randomized at %d,%d (base %d,%d) button=%s" % (fx, fy, x, y, button))
        except Exception as ex:
            logging_helper.log_debug("click_randomized failed: %s" % ex)

    def key_press(self, key: str) -> None:
        try:
            press(key)
            logging_helper.log_debug("Pressed key: %s" % key)
        except Exception as ex:
            logging_helper.log_debug("key_press failed for %s: %s" % (key, ex))

    def wait_and_retry(self, condition_func, max_attempts: int = 10, delay: float = 0.5) -> bool:
        """Wait for a condition to be met with retries."""
        for attempt in range(max_attempts):
            try:
                if condition_func():
                    return True
            except Exception as ex:
                logging_helper.log_debug("wait_and_retry condition error: %s" % ex)
                return False
            sleep(delay)
        return False

    def loot_process(self, attempts: int = 30) -> None:
        """Versucht mehrere Male Loot aufzunehmen (non-blocking)."""
        for _ in range(attempts):
            try:
                if not pickit.pick_it():
                    break
                # leichte Pause zwischen erfolgreichen Picks
                sleep(uniform(0.2, 0.4))
            except Exception as ex:
                logging_helper.log_debug("loot_process error: %s" % ex)
                break

    def wait_for_loading(self) -> None:
        if not self.wait_and_retry(self.is_on_loading, delay=0.5):
            sleep(uniform(1.5, 2.5))

    def navigate_to_treasure(self) -> None:
        logging_helper.log_info("Attempting to locate treasure.")
        try:
            self.key_press('TAB')
            sleep(uniform(0.5, 0.8))
            mouse_helper.move_smooth(800, 600)
            sleep(uniform(0.5, 0.8))

            # Scroll to adjust the view
            for _ in range(4):
                mouse_helper.mouseScroll(-1)
                sleep(uniform(0.2, 0.4))
            for _ in range(3):
                mouse_helper.mouseScroll(1)
                sleep(uniform(0.2, 0.4))

            screen_region = (50, 50, 1900, 870)
            x, y = self._safe_locate(str(Path(LOCATION_DIR) / "treasure.png"),
                                     conf=0.8, loctype='c', region=screen_region)

            if x != -1 and y != -1:
                self.click_randomized(x, y, button='right')
                logging_helper.log_info("Found armor treasure at map position %d, %d." % (x, y))
                return

            logging_helper.log_info("Treasure not found; attempting fallback locations.")
            self.fallback_navigation(screen_region)
        except Exception as ex:
            logging_helper.log_debug("navigate_to_treasure error: %s" % ex)

    def fallback_navigation(self, region: Tuple[int, int, int, int]) -> Optional[bool]:
        try:
            if self._safe_locate(str(Path(LOCATION_DIR) / "onyxWatchtower.png"), conf=0.8, region=region)[0] != -1:
                self.key_press('m')
                return True
            if self._safe_locate(str(Path(LOCATION_DIR) / "rakhatKeep.png"), conf=0.8, region=region)[0] != -1:
                # feste Koordinate als Fallback
                self.click_randomized(1097, 764, button='right')
                return True
            return self.search_helltide(region)
        except Exception as ex:
            logging_helper.log_debug("fallback_navigation error: %s" % ex)
            return None

    def search_helltide(self, region: Tuple[int, int, int, int]) -> Optional[bool]:
        try:
            for _ in range(3):
                mouse_helper.mouseScroll(-1)
                sleep(uniform(0.2, 0.4))

            x, y = self._safe_locate(str(Path(LOCATION_DIR) / "helltide.png"),
                                     conf=0.8, loctype='c', region=region)
            if x == -1:
                return None

            left = max(x - 25, 0)
            top = max(y - 75, 0)
            waypoint_region = (left, top, 50, 100)
            x2, y2 = self._safe_locate(str(Path(LOCATION_DIR) / "waypoint.png"),
                                      conf=0.8, loctype='c', region=waypoint_region)

            if x2 != -1 and y2 != -1:
                self.click_randomized(x2, y2, jitter=(1, 4, 1, 4), button='left')
                logging_helper.log_info("Found helltide waypoint at %d, %d. Teleporting." % (x2, y2))
                # Teleport action: sichere Klickkoordinate
                self.click_randomized(850, 640, button='left')
                return True

            # close map to continue if nothing found
            self.key_press('m')
            return None
        except Exception as ex:
            logging_helper.log_debug("search_helltide error: %s" % ex)
            return None

    def game_manager(self, move: bool = True, loot: bool = False) -> None:
        """Main game handling routine - fuehrt genau einen Zyklus aus (keine Rekursion)."""
        try:
            # Aktualisiere ggf. die Konfiguration
            self.cfg = self.reload_config()

            if self.is_on_menu():
                logging_helper.log_info("Player is on menu. Starting game.")
                self.click_randomized(220, 710, button='left')
                return

            if self.is_death():
                logging_helper.log_info("Player is dead. Reviving.")
                self.click_randomized(904, 924, button='left')
                self.wait_for_loading()
                return

            if self.is_in_game():
                logging_helper.log_info("Player is in-game.")
                try:
                    mob = image_helper.detect_lines('mob')
                except Exception as ex:
                    logging_helper.log_debug("detect_lines error in game_manager: %s" % ex)
                    mob = None

                if mob:
                    # mob zur�ckgeben kann (x,y,w,h)
                    try:
                        x, y, w, h = mob
                        rotation.rotation(x, y)
                    except Exception as ex:
                        logging_helper.log_debug("rotation call failed: %s" % ex)
                    # nach Kampf evtl Loot verarbeiten, aber keinen rekursiven Aufruf
                    if loot:
                        self.loot_process()
                    return

                # Wenn kein Mob gefunden
                if loot:
                    self.loot_process()

                if move:
                    moved = False
                    try:
                        moved = pather.move_to_ref_location()
                    except Exception as ex:
                        logging_helper.log_debug("pather.move_to_ref_location error: %s" % ex)

                    if not moved:
                        # navigiere zur Truhe, falls Bewegung nicht m�glich
                        self.navigate_to_treasure()
                return

            # Sonstiger Zustand: warte kurz
            sleep(uniform(0.2, 0.5))
        except Exception as ex:
            logging_helper.log_debug("game_manager unexpected error: %s" % ex)
