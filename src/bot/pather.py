from random import randint
from functools import wraps
from pydirectinput import leftClick, press

from helper import image_helper, config_helper, logging_helper

# Konstanten für die Bildschirmmitte und Minimap-Koordinaten
PLAYER_X = 960  # Bildschirmmitte X
PLAYER_Y = 520  # Bildschirmmitte Y
MAP_X = 1750
MAP_Y = 150

def stuck_check(func):
    """
    Dekorator zur Überprüfung, ob der Charakter stecken bleibt.
    Führt Wiederholungsversuche aus, falls eine Bewegung blockiert ist.
    """
    stuck_count = [0]  # Zählervariable für blockierte Bewegungen

    @wraps(func)
    def decorated(*args, **kwargs):
        if stuck_count[0] > 10:
            logging_helper.log_debug("[Character is stuck, try to escape]")
            stuck_count[0] = 0
            for _ in range(2):
                func(*args, **kwargs, stuck=True)
            return True
        if func(*args, **kwargs):
            stuck_count[0] += 1
            return True
        else:
            stuck_count[0] = 0
            return False

    return decorated

def get_player_ref_location(trans=False):
    """
    Ermittelt die Position des Spielers relativ zur Minimap.
    Parameters:
        trans (bool): Wenn True, skaliert die Koordinaten um den Faktor 10.
    Returns:
        tuple: Die berechneten relativen oder transformierten Koordinaten (x, y).
    """
    path = image_helper.detect_lines()

    if not path:
        logging_helper.log_debug("Path not found")
        return -1, -1

    x, y, w, h = path
    x = x + w
    y = y + h

    x = (MAP_X - x) - 1675
    y = (MAP_Y - y) - 75

    if trans:
        return x * 10, y * 10
    else:
        return x, y

@stuck_check
def move_to_ref_location(stuck=False):
    """
    Bewegt den Spieler basierend auf der Position des Referenzobjekts.
    Parameters:
        stuck (bool): Wenn True, führt eine zufällige Bewegung aus, um Blockierungen zu umgehen.
    Returns:
        bool: True, wenn die Bewegung erfolgreich war, False bei Fehlschlag.
    """
    cfg = config_helper.read_config()
    evade_var = cfg.get('evade', 'space')  # Standardmäßig 'space', falls 'evade' nicht vorhanden ist

    # Überprüfen, ob eine kletterbare Oberfläche erkannt wird
    if image_helper.locate_needle('.\\assets\\skills\\climb.png', conf=0.7, region=(750, 250, 1250, 750)):
        press(evade_var)

    # Berechnung der relativen Position zur Referenz
    x, y = get_player_ref_location()

    if x == -1 and y == -1:
        return False

    logging_helper.log_debug("Relative coords %d, %d, absolute coords %d, %d" % (x, y, PLAYER_X - x, PLAYER_Y - y))

    if not stuck:
        leftClick(PLAYER_X - x, PLAYER_Y - y)
        logging_helper.log_info("Moving to %d,%d" % (PLAYER_X - x, PLAYER_Y - y))
        return True
    else:
        # Zufällige Bewegung bei Blockierung
        leftClick(PLAYER_X + randint(-250, 250), PLAYER_Y + randint(-250, 250))
        logging_helper.log_info("Got stuck, performing random move")
        return False
