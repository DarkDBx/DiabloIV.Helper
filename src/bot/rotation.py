from random import uniform
from time import sleep
from pydirectinput import keyDown, keyUp, press, leftClick, rightClick

from helper import mouse_helper, image_helper, timer_helper, config_helper, logging_helper
from helper.timer_helper import TIMER_STOPPED

SKILLPATH = ".\\assets\\skills\\"

# Timer-Instanzen für Abklingzeiten
timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')

def press_combo(key):
    """
    Drückt eine Tastenkombination, bestehend aus 'Shift' + einer beliebigen Taste.
    Parameters:
        key (str): Die Taste, die zusammen mit 'Shift' gedrückt werden soll.
    """
    keyDown('shift')
    press(key)
    keyUp('shift')

def rotation(x=None, y=None):
    """
    Setzt die Kampfrotation für eine spezifische Klasse auf Basis der Konfigurationswerte.
    Parameters:
        x, y (int): Koordinaten eines Ziels (optional).
    """
    cfg = config_helper.read_config()
    class_var = cfg.get('class', '').capitalize()

    if class_var in ['Druid', 'Spiritborn', 'Barbarian', 'Necromancer', 'Sorceress', 'Rogue']:
        combat_rotation(class_var.lower(), x, y)
    else:
        logging_helper.log_error('No viable class specified in configuration.')

def combat_rotation(class_name, x, y):
    """
    Führt die Kampfrotation für die angegebene Klasse aus.
    Parameters:
        class_name (str): Name der Klasse (z. B. 'rogue', 'druid').
        x, y (int): Koordinaten eines Ziels (optional).
    """
    cfg = config_helper.read_config()
    evade = cfg['evade']
    pot = cfg['pot']
    skill1, skill2, skill3, skill4 = cfg['skill1'], cfg['skill2'], cfg['skill3'], cfg['skill4']
    n = 25
    target_type = check_target_type(x, y, n)

    if target_type:
        handle_health_and_evade(evade, pot)
        use_skills(class_name, target_type, x, y, skill1, skill2, skill3, skill4)

def check_target_type(x, y, n):
    """
    Überprüft, ob das Ziel ein Normal- oder Elite-Gegner ist.
    Parameters:
        x, y (int): Zielkoordinaten.
        n (int): Offsets zur Zielposition.
    Returns:
        str: 'normal', 'elite' oder None.
    """
    if image_helper.pixel_matches_color(801, 45, 107, 2, 1, 20) or \
       image_helper.pixel_matches_color(801, 45, 156, 65, 93, 20) or \
       image_helper.pixel_matches_color(801, 45, 231, 13, 9, 20) or \
       image_helper.detect_lines('mob') != None:
        if x is not None and y is not None:
            mouse_helper.move_smooth(x + 400 + n, y + 50 + (n * 2), 1)
        return 'normal'

    if image_helper.pixel_matches_color(710, 45, 162, 4, 4, 20) or \
       image_helper.pixel_matches_color(710, 45, 124, 71, 98, 20) or \
       image_helper.detect_lines('mob') != None:
        if x is not None and y is not None:
            mouse_helper.move_smooth(x + 400 + (n * 3), y + 50 + (n * 6), 1)
        return 'elite'

    return None

def handle_health_and_evade(evade, pot):
    """
    Überprüft die Gesundheit und verwendet bei Bedarf Tränke oder Ausweichbewegungen.
    Parameters:
        evade (str): Tastenkürzel für Ausweichbewegungen.
        pot (str): Tastenkürzel für Heiltränke.
    """
    if not image_helper.pixel_matches_color(608, 980, 95, 10, 15, 45) and \
       not image_helper.pixel_matches_color(608, 972, 148, 14, 24, 45) and \
       not image_helper.pixel_matches_color(607, 978, 97, 29, 82, 45):
        if locate_and_use_potion(pot):
            logging_helper.log_info('Used potion')
        if locate_and_use_evade(evade):
            logging_helper.log_info('Used evade')

def locate_and_use_potion(pot):
    """
    Sucht nach Tränken und verwendet sie bei Bedarf.
    Parameters:
        pot (str): Tastenkürzel für Heiltränke.
    Returns:
        bool: True, wenn ein Trank verwendet wurde, sonst False.
    """
    potion_images = ['pot10.png', 'pot20.png', 'pot30.png', 'pot45.png', 
                     'pot60.png', 'pot70.png', 'pot_placeholder.png']
    for img in potion_images:
        if image_helper.locate_needle(SKILLPATH + img, conf=0.7) and timer1.get_timer_state() == TIMER_STOPPED:
            timer1.start_timer(3)
            press(pot)
            sleep(uniform(0.11, 0.14))
            return True
    return False

def locate_and_use_evade(evade):
    """
    Sucht nach Ausweichmöglichkeiten und verwendet sie bei Bedarf.
    Parameters:
        evade (str): Tastenkürzel für Ausweichbewegungen.
    Returns:
        bool: True, wenn eine Ausweichbewegung verwendet wurde, sonst False.
    """
    if image_helper.locate_needle(SKILLPATH + 'evade.png', conf=0.7) and timer2.get_timer_state() == TIMER_STOPPED:
        timer2.start_timer(3)
        press(evade)
        sleep(uniform(0.11, 0.14))
        return True
    return False

def use_skills(class_name, target_type, x, y, skill1, skill2, skill3, skill4):
    """
    Verwendet die Klassenskills basierend auf dem Zieltyp.
    """
    if image_helper.locate_needle(SKILLPATH + class_name + '\\04.png', conf=0.6):
        press(skill4)
        logging_helper.log_info('Used skill 4')
    elif image_helper.locate_needle(SKILLPATH + class_name + '\\03.png', conf=0.6):
        press(skill3)
        logging_helper.log_info('Used skill 3')
    elif image_helper.locate_needle(SKILLPATH + class_name + '\\01.png', conf=0.6):
        press(skill1)
        logging_helper.log_info('Used skill 1')
    elif image_helper.locate_needle(SKILLPATH + class_name + '\\02.png', conf=0.6):
        press(skill2)
        logging_helper.log_info('Used skill 2')

    sleep(uniform(0.21, 0.24))

    if image_helper.locate_needle(SKILLPATH + class_name + '\\05.png', conf=0.9):
        rightClick()
        logging_helper.log_info('Used right mouse skill')
    elif x is not None and y is not None:
        leftClick()
        logging_helper.log_info('Used left mouse skill')

    sleep(uniform(0.21, 0.24))
