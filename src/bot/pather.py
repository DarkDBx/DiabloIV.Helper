from random import randint
from functools import wraps
from pydirectinput import leftClick, press
import os
import time

from helper import image_helper, config_helper, logging_helper

# Konstanten für die Bildschirmmitte und Minimap-Koordinaten
PLAYER_X = 960  # Bildschirmmitte X
PLAYER_Y = 520  # Bildschirmmitte Y
MAP_X = 1750
MAP_Y = 150

# Verhaltens-Konstanten
MAX_STUCK = 10
ESCAPE_TRIES = 2
RANDOM_RADIUS = 250
CLICK_DELAY = 0.05  # kurzer Wait nach Klick um Overlap-Probleme zu reduzieren

def stuck_check(func):
    """
    Dekorator zur Überprüfung, ob der Charakter stecken bleibt.
    Führt Wiederholungsversuche aus, falls eine Bewegung blockiert ist.
    Erwartetes Verhalten der dekorierten Funktion:
        - Rückgabe True  => Bewegung erfolgreich
        - Rückgabe False => Bewegung fehlgeschlagen / stecken geblieben
    """
    stuck_count = [0]  # Zählervariable für blockierte Bewegungen

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except TypeError:
            # Falls func kein bestimmtes kwargs akzeptiert, versuche ohne kwargs
            result = func(*args)

        if result:
            # Erfolg => Zähler zurücksetzen
            stuck_count[0] = 0
            return True

        # Bewegung fehlgeschlagen => Zähler erhöhen
        stuck_count[0] += 1
        logging_helper.log_debug("Movement failed (stuck_count=%d)" % stuck_count[0])

        # Wenn wir zu oft stecken, versuche aus der Situation zu entkommen
        if stuck_count[0] >= MAX_STUCK:
            logging_helper.log_debug("[Character is stuck, trying escape maneuvers]")
            for _ in range(ESCAPE_TRIES):
                try:
                    func(*args, **kwargs, stuck=True)
                except TypeError:
                    # Falls die Funktion das 'stuck' kw nicht akzeptiert, rufe sie einfach erneut auf
                    func(*args)
                time.sleep(0.15)
            stuck_count[0] = 0
            # Nach Escape-Versuchen zurückmelden, dass wir versucht haben zu entkommen
            return False

        return False

    return decorated

def get_player_ref_location(trans=True):
    """
    Ermittelt die Position des Spielers relativ zur Minimap.
    Parameters:
        trans (bool): Wenn True, skaliert die Koordinaten um den Faktor 10.
    Returns:
        tuple: Die berechneten relativen oder transformierten Koordinaten (x, y),
               oder (-1, -1) falls keine Pfad-Referenz gefunden wurde.
    """
    try:
        path = image_helper.detect_lines()
    except Exception as ex:
        logging_helper.log_debug("detect_lines failed: %s" % ex)
        return -1, -1

    if not path:
        logging_helper.log_debug("Path not found")
        return -1, -1

    # Erwartet (x, y, w, h)
    if not (isinstance(path, (list, tuple)) and len(path) == 4):
        logging_helper.log_debug("Unexpected path format: %r" % (path,))
        return -1, -1

    x, y, w, h = path
    # Verwende Rechtecksuntergrenze/rechts als Referenzpunkt
    x = x + w
    y = y + h

    # Anpassung an Map-Offsets (beibehalten, da projekt-spezifisch)
    x = (MAP_X - x) #- 1675
    y = (MAP_Y - y) #- 75

    if trans:
        return int(x * 10), int(y * 10)
    else:
        return int(x), int(y)

@stuck_check
def move_to_ref_location(stuck=False):
    """
    Bewegt den Spieler basierend auf der Position des Referenzobjekts.
    Parameters:
        stuck (bool): Wenn True, führt eine zufällige Bewegung aus, um Blockierungen zu umgehen.
    Returns:
        bool: True, wenn die Bewegung erfolgreich war, False bei Fehlschlag.
    """
    try:
        cfg = config_helper.read_config() or {}
    except Exception:
        cfg = {}

    evade_var = cfg.get('evade', 'space')  # Standardwert 'space'

    # Überprüfen, ob eine kletterbare Oberfläche erkannt wird
    try:
        climb_path = os.path.join('.', 'assets', 'skills', 'climb.png')
        if image_helper.locate_needle(climb_path, conf=0.7, region=(750, 250, 1250, 750)):
            press(evade_var)
            logging_helper.log_debug("Climb detected, pressed evade key '%s'" % evade_var)
    except Exception as ex:
        logging_helper.log_debug("Error while checking climb: %s" % ex)

    # Berechnung der relativen Position zur Referenz
    x, y = get_player_ref_location()

    if x == -1 and y == -1:
        logging_helper.log_debug("No reference location available, cannot move")
        return False

    abs_x = PLAYER_X - x
    abs_y = PLAYER_Y - y
    logging_helper.log_debug("Relative coords %d, %d, absolute coords %d, %d" % (x, y, abs_x, abs_y))

    try:
        if not stuck:
            leftClick(int(abs_x), int(abs_y))
            time.sleep(CLICK_DELAY)
            logging_helper.log_info("Moving to %d,%d" % (abs_x, abs_y))
            return True
        else:
            # Zufällige Bewegung bei Blockierung
            rand_x = PLAYER_X + randint(-RANDOM_RADIUS, RANDOM_RADIUS)
            rand_y = PLAYER_Y + randint(-RANDOM_RADIUS, RANDOM_RADIUS)
            leftClick(int(rand_x), int(rand_y))
            time.sleep(CLICK_DELAY)
            logging_helper.log_info("Got stuck, performing random move to %d,%d" % (rand_x, rand_y))
            return False
    except Exception as ex:
        logging_helper.log_debug("Error during click/move: %s" % ex)
        return False
