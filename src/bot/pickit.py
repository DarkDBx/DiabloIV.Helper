from time import sleep
from random import randint, uniform
from typing import Tuple, List, Sequence
from pydirectinput import leftClick
from pathlib import Path
import os
import logging

from helper import image_helper, logging_helper

# Assets-Pfad (relativ zum Repo-Root, berechnet aus Dateiposition)
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets" / "pickit"
IMAGE_DIR = str(ASSETS_DIR)

# Konstante Einstellungen
DEFAULT_REGION = (400, 50, 1500, 870)
CLICK_PRE_DELAY = (0.05, 0.18)  # Wartezeit vor Klick (sek.)
PICK_COOLDOWN = (1.5, 2.5)  # Wartezeit nach erfolgreichem Aufheben
RANDOM_OFFSET = (-2, 18, -2, 2)  # Standard-Offsets für zufälligen Klick

# Farbprüfungen: [offset_x, offset_y, r, g, b, tolerance]
DEFAULT_ITEM_COLORS: Sequence[Sequence[int]] = [
    [1, 4, 248, 128, 5, 50],
    [1, 4, 216, 166, 120, 50],
    [1, 4, 234, 236, 10, 50],
    [1, 4, 215, 164, 198, 50],
]


def get_ref_location(ref_img: str, region: Tuple[int, int, int, int] = DEFAULT_REGION) -> Tuple[int, int]:
    """
    Suche ein Referenzbild in `IMAGE_DIR` und gebe (x, y) zurück.
    Bei Fehler oder Nicht-Fund wird (-1, -1) zurückgegeben.
    """
    try:
        img_path = os.path.join(IMAGE_DIR, ref_img)
        x, y = image_helper.locate_needle(img_path, loctype='c', region=region)
        if x is None or y is None:
            return -1, -1
        return int(x), int(y)
    except Exception as ex:
        logging_helper.log_debug(f"get_ref_location('{ref_img}') failed: {ex}")
        return -1, -1


def randomized_left_click(x: int = None, y: int = None, a: int = -5, b: int = 35, c: int = -5, d: int = 5) -> None:
    """
    Führe einen Linksklick aus. Wenn x/y angegeben, verwende leichte zufällige Offsets.
    Warte vor dem Klick einen kleinen zufälligen Zeitraum, um menschlicher zu wirken.
    """
    # kurze zufällige Pause vor Klick
    sleep(uniform(CLICK_PRE_DELAY[0], CLICK_PRE_DELAY[1]))

    try:
        if x is None or y is None:
            leftClick()
            logging_helper.log_debug("randomized_left_click: clicking at current cursor position")
        else:
            fx = int(x + randint(a, b))
            fy = int(y + randint(c, d))
            leftClick(fx, fy)
            logging_helper.log_debug(f"randomized_left_click: clicking at {fx},{fy} (base {x},{y})")
    except Exception as ex:
        logging_helper.log_debug(f"randomized_left_click failed: {ex}")


def pick_it() -> bool:
    """
    Suche nach Loot-Items und versuche, sie aufzuheben.
    Gibt True zurück, wenn ein Item aufgesammelt wurde, sonst False.
    """
    item_images = ["a.png", "e.png", "i.png", "o.png", "u.png", "ancestral.png", "cinder.png"]

    try:
        for i, item_image in enumerate(item_images):
            x, y = get_ref_location(item_image)
            if x <= -1 or y <= -1:
                continue

            logging_helper.log_debug(f"Found candidate '{item_image}' at {x},{y}")

            # Wähle passende Farbchecks (für nicht definierte Items wird DEFAULT_ITEM_COLORS benutzt)
            if i < len(DEFAULT_ITEM_COLORS):
                checks = [DEFAULT_ITEM_COLORS[i]]
            else:
                checks = list(DEFAULT_ITEM_COLORS)

            matched = False
            for color in checks:
                if len(color) != 6:
                    continue
                offset_x, offset_y, r, g, b, tolerance = color
                try:
                    px = x + offset_x
                    py = y + offset_y
                    if image_helper.pixel_matches_color(px, py, r, g, b, tolerance):
                        matched = True
                        break
                except Exception as ex:
                    logging_helper.log_debug(f"pixel check failed for {item_image} at {px},{py}: {ex}")

            if matched:
                # Klick leicht versetzt auf das Item
                a, b, c, d = RANDOM_OFFSET
                randomized_left_click(x + 12, y + 3, a, b, c, d)
                logging_helper.log_info(f"Picked item '{item_image}' at coords {x}, {y}")
                sleep(uniform(PICK_COOLDOWN[0], PICK_COOLDOWN[1]))
                return True
            else:
                logging_helper.log_debug(f"No color match for '{item_image}' at {x},{y}")

    except Exception as ex:
        logging_helper.log_debug(f"pick_it unexpected error: {ex}")

    return False
