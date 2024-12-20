from time import sleep
from random import randint, uniform
from pydirectinput import leftClick, rightClick, press

from helper import mouse_helper, image_helper, config_helper, logging_helper
from bot import pather, pickit, rotation

class Manager:
    def __init__(self) -> None:
        self.cfg = config_helper.read_config()

    def pixel_match_check(self, conditions):
        """Check multiple pixel conditions for state validation."""
        return all(image_helper.pixel_matches_color(*cond) for cond in conditions)

    def is_on_landing(self):
        conditions = [(3, 2, 22, 30, 31), (491, 888, 18, 17, 18)]
        return self.pixel_match_check(conditions)

    def is_on_menu(self):
        conditions = [(74, 314, 235, 8, 2), (70, 302, 148, 10, 3)]
        return self.pixel_match_check(conditions)

    def is_on_loading(self):
        return image_helper.pixel_matches_color(1, 1, 0, 0, 0, tolerance=0)

    def is_in_game(self):
        conditions = [(718, 984, 59, 75, 84), (1209, 966, 56, 76, 81)]
        return self.pixel_match_check(conditions)

    def is_death(self):
        conditions = [(831, 859, 147, 81, 32), (846, 898, 47, 1, 1)]
        return self.pixel_match_check(conditions)

    def click_randomized(self, x=None, y=None, jitter=(-5, 35, -5, 5), button='left'):
        """Perform a randomized click action."""
        if x is None or y is None:
            if button == 'left':
                leftClick()
            else:
                rightClick()
        else:
            ex = randint(jitter[0], jitter[1])
            ey = randint(jitter[2], jitter[3])
            fx, fy = x + ex, y + ey
            if button == 'left':
                leftClick(fx, fy)
            else:
                rightClick(fx, fy)

    def key_press(self, key):
        press(key)

    def wait_and_retry(self, condition_func, max_attempts=10, delay=0.5):
        """Wait for a condition to be met with retries."""
        for attempt in range(max_attempts):
            if condition_func():
                return True
            sleep(delay)
        return False

    def loot_process(self, attempts=30):
        for _ in range(attempts):
            if not pickit.pick_it():
                break

    def wait_for_loading(self):
        if not self.wait_and_retry(self.is_on_loading, delay=0.5):
            sleep(uniform(1.5, 2.5))

    def navigate_to_treasure(self):
        logging_helper.log_info("Attempting to locate treasure.")
        self.key_press('m')
        sleep(uniform(0.5, 0.8))
        mouse_helper.move_smooth(800, 600)
        sleep(uniform(0.5, 0.8))

        # Scroll to adjust the view
        for _ in range(4):
            mouse_helper.mouseScroll(-1)
            sleep(uniform(0.5, 0.8))
        for _ in range(2):
            mouse_helper.mouseScroll(1)
            sleep(uniform(0.5, 0.8))

        screen_region = (50, 50, 1900, 870)
        x, y = image_helper.locate_needle('.\\assets\\location\\treasure.png', conf=0.8, loctype='c', region=screen_region)

        if x != -1 and y != -1:
            self.click_randomized(x, y, button='right')
            logging_helper.log_info(f"Found armor treasure at map position {x}, {y}.")
        else:
            logging_helper.log_info("Treasure not found; attempting fallback locations.")
            self.fallback_navigation(screen_region)

    def fallback_navigation(self, region):
        if image_helper.locate_needle('.\\assets\\location\\onyxWatchtower.png', conf=0.8, region=region):
            self.key_press('m')
        elif image_helper.locate_needle('.\\assets\\location\\rakhatKeep.png', conf=0.8, region=region):
            self.click_randomized(1097, 764, button='right')
        else:
            self.search_helltide(region)

    def search_helltide(self, region):
        for _ in range(2):
            mouse_helper.mouseScroll(-1)
            sleep(uniform(0.5, 0.8))

        x, y = image_helper.locate_needle('.\\assets\\location\\helltide.png', conf=0.8, loctype='c', region=region)
        if x != -1 and y != -1:
            waypoint_region = (x - 25, y - 75, x + 25, y + 25)
            x2, y2 = image_helper.locate_needle('.\\assets\\location\\waypoint.png', conf=0.8, loctype='c', region=waypoint_region)

            if x2 != -1 and y2 != -1:
                self.click_randomized(x2, y2, jitter=(1, 4, 1, 4), button='left')
                logging_helper.log_info(f"Found helltide waypoint at {x2}, {y2}. Teleporting.")
                self.click_randomized(850, 640, button='left')  # Teleport action
                return True

        self.key_press('m')  # Close map if navigation fails

    def game_manager(self, move=True, loot=False):
        """Main game handling routine."""
        if self.is_on_menu():
            logging_helper.log_info('Player is on menu. Starting game.')
            self.click_randomized(220, 710, button='left')
        elif self.is_death():
            logging_helper.log_info('Player is dead. Reviving.')
            self.click_randomized(904, 924, button='left')
            self.wait_for_loading()
        elif self.is_in_game():
            logging_helper.log_info('Player is in-game.')
            mob = image_helper.detect_lines('mob')
            if mob:
                x, y, w, h = mob
                rotation.rotation(x, y)
                self.game_manager(move=False, loot=True)
            elif loot:
                self.loot_process()
            if move:
                if not pather.move_to_ref_location():
                    self.navigate_to_treasure()
