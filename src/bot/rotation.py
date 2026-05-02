from random import uniform
from time import sleep
from typing import Optional
from pathlib import Path
from pydirectinput import keyDown, keyUp, press, leftClick, rightClick

from helper import mouse_helper, image_helper, timer_helper, config_helper, logging_helper
from helper.timer_helper import TIMER_STOPPED

# Skill-Assets relativ zum Projekt
SKILLPATH = Path(__file__).resolve().parents[1] / "assets" / "skills"

# Timer-Instanzen für Abklingzeiten
timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')

# Konfigurierbare Werte
MOVE_OFFSET_N = 25
POTION_TIMER_SEC = 3
EVADE_TIMER_SEC = 3
CLICK_DELAY_MIN = 0.11
CLICK_DELAY_MAX = 0.14


def press_combo(key: str) -> None:
    """
    Drückt eine Tastenkombination 'Shift' + key. Stellt sicher, dass Shift wieder losgelassen wird.
    """
    try:
        keyDown('shift')
        press(key)
    finally:
        try:
            keyUp('shift')
        except Exception:
            # KeyUp kann fehlschlagen, aber wir wollen nicht abstürzen
            pass


def rotation(x: Optional[int] = None, y: Optional[int] = None) -> None:
    """
    Setzt die Kampfrotation für eine spezifische Klasse basierend auf der Konfiguration.
    """
    try:
        cfg = config_helper.read_config() or {}
    except Exception as ex:
        logging_helper.log_error("Failed to read config for rotation: %s" % ex)
        return

    class_name = str(cfg.get('class', '')).strip().capitalize()
    valid = {'Druid', 'Spiritborn', 'Barbarian', 'Necromancer', 'Sorceress', 'Rogue'}

    if class_name in valid:
        combat_rotation(class_name.lower(), x, y)
    else:
        logging_helper.log_error("No viable class specified in configuration: %r" % class_name)


def combat_rotation(class_name: str, x: Optional[int], y: Optional[int]) -> None:
    """
    Führt die Kampfrotation aus: Health/Evade prüfen und Skills verwenden.
    """
    try:
        cfg = config_helper.read_config() or {}
    except Exception as ex:
        logging_helper.log_error("Failed to read config in combat_rotation: %s" % ex)
        return

    evade = cfg.get('evade', '')
    pot = cfg.get('pot', '')
    skill1 = cfg.get('skill1', '')
    skill2 = cfg.get('skill2', '')
    skill3 = cfg.get('skill3', '')
    skill4 = cfg.get('skill4', '')

    n = MOVE_OFFSET_N
    target_type = check_target_type(x, y, n)

    if target_type:
        handle_health_and_evade(evade, pot)
        use_skills(class_name, target_type, x, y, skill1, skill2, skill3, skill4)


def check_target_type(x: Optional[int], y: Optional[int], n: int) -> Optional[str]:
    """
    Ermittelt ob Ziel 'normal' oder 'elite' ist.
    Beachtet: reduziert doppelte Aufrufe von detect_lines.
    """
    try:
        detect_mob = image_helper.detect_lines('mob') is not None
    except Exception as ex:
        logging_helper.log_debug("detect_lines error in check_target_type: %s" % ex)
        detect_mob = False

    try:
        # Normal checks
        if (image_helper.pixel_matches_color(801, 45, 107, 2, 1, 20) or
            image_helper.pixel_matches_color(801, 45, 156, 65, 93, 20) or
            image_helper.pixel_matches_color(801, 45, 231, 13, 9, 20) or
            detect_mob):
            if x is not None and y is not None:
                mouse_helper.move_smooth(x + 400 + n, y + 50 + (n * 2), 1)
            return 'normal'

        # Elite checks
        if (image_helper.pixel_matches_color(710, 45, 162, 4, 4, 20) or
            image_helper.pixel_matches_color(710, 45, 124, 71, 98, 20) or
            detect_mob):
            if x is not None and y is not None:
                mouse_helper.move_smooth(x + 400 + (n * 3), y + 50 + (n * 6), 1)
            return 'elite'
    except Exception as ex:
        logging_helper.log_debug("Error in check_target_type pixel checks: %s" % ex)

    return None


def handle_health_and_evade(evade: str, pot: str) -> None:
    """
    Prüft Lebensanzeige und verwendet bei Bedarf Potion / Evade.
    Hinweis: die Farbe-Checks sind projekt-spezifisch; bei Änderungen der UI anpassen.
    """
    try:
        low_hp = not image_helper.pixel_matches_color(608, 980, 95, 10, 15, 45) and \
                 not image_helper.pixel_matches_color(608, 972, 148, 14, 24, 45) and \
                 not image_helper.pixel_matches_color(607, 978, 97, 29, 82, 45)

        if low_hp:
            if locate_and_use_potion(pot):
                logging_helper.log_info('Used potion')
            if locate_and_use_evade(evade):
                logging_helper.log_info('Used evade')
    except Exception as ex:
        logging_helper.log_debug("handle_health_and_evade error: %s" % ex)


def locate_and_use_potion(pot: str) -> bool:
    """
    Sucht nach Trank-Icons und benutzt den angegebenen Taste für Potion.
    """
    potion_images = ['pot.png']
    try:
        for img in potion_images:
            path = str(SKILLPATH / img)
            try:
                found = image_helper.locate_needle(path, conf=0.7)
            except Exception as ex:
                logging_helper.log_debug("locate_needle error for %s: %s" % (path, ex))
                found = False

            if found and timer1.get_timer_state() == TIMER_STOPPED:
                timer1.start_timer(POTION_TIMER_SEC)
                try:
                    press(pot)
                except Exception as ex:
                    logging_helper.log_debug("press(pot) failed: %s" % ex)
                sleep(uniform(CLICK_DELAY_MIN, CLICK_DELAY_MAX))
                return True
    except Exception as ex:
        logging_helper.log_debug("locate_and_use_potion error: %s" % ex)

    return False


def locate_and_use_evade(evade: str) -> bool:
    """
    Sucht nach Evade-Icon und führt Evade-Taste aus (mit Timer).
    """
    try:
        path = str(SKILLPATH / 'evade.png')
        try:
            found = image_helper.locate_needle(path, conf=0.7)
        except Exception as ex:
            logging_helper.log_debug("locate_needle error for evade: %s" % ex)
            found = False

        if found and timer2.get_timer_state() == TIMER_STOPPED:
            timer2.start_timer(EVADE_TIMER_SEC)
            try:
                press(evade)
            except Exception as ex:
                logging_helper.log_debug("press(evade) failed: %s" % ex)
            sleep(uniform(CLICK_DELAY_MIN, CLICK_DELAY_MAX))
            return True
    except Exception as ex:
        logging_helper.log_debug("locate_and_use_evade error: %s" % ex)

    return False


def use_skills(class_name: str, target_type: str, x: Optional[int], y: Optional[int],
               skill1: str, skill2: str, skill3: str, skill4: str) -> None:
    """
    Verwendet die Klassenskills basierend auf Skill-Icons und Ziel-Typ.
    Reihenfolge der Prüfungen bleibt wie bisher, Logging erweitert.
    """
    try:
        # Standardisierte Pfade für Skill-Icons
        def skill_icon(idx: str) -> str:
            return str(SKILLPATH / class_name / (idx + '.png'))

        if image_helper.locate_needle(skill_icon('04'), conf=0.6):
            press(skill4)
            logging_helper.log_info('Used skill 4')
        elif image_helper.locate_needle(skill_icon('03'), conf=0.6):
            press(skill3)
            logging_helper.log_info('Used skill 3')
        elif image_helper.locate_needle(skill_icon('01'), conf=0.6):
            press(skill1)
            logging_helper.log_info('Used skill 1')
        elif image_helper.locate_needle(skill_icon('02'), conf=0.6):
            press(skill2)
            logging_helper.log_info('Used skill 2')

        sleep(uniform(0.21, 0.24))

        if image_helper.locate_needle(skill_icon('05'), conf=0.9):
            rightClick()
            logging_helper.log_info('Used right mouse skill')
        elif x is not None and y is not None:
            leftClick()
            logging_helper.log_info('Used left mouse skill')

        sleep(uniform(0.21, 0.24))
    except Exception as ex:
        logging_helper.log_debug("use_skills error: %s" % ex)
