import random
import time
import logging

from helper import input_helper, image_helper, timer_helper, config_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"


timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')


def press_combo(key1, key2):
    input_helper.keyDown(key1)
    input_helper.press(key2)
    input_helper.keyUp(key1)


def rotation():
    """set up the skill rotation for a specific class injected by the config"""
    cfg = config_helper.read_config()
    class_var = cfg['class']

    if class_var == 'Druid':
        druid()
    elif class_var == 'Barb':
        pass
    elif class_var == 'Necro':
        pass
    elif class_var == 'Sorc':
        pass
    elif class_var == 'Rogue':
        pass
    else:
        logging.error('No vaible class')


"""Storm druid"""
# https://maxroll.gg/d4/build-guides/tornado-druid-leveling-guide
def druid():
    # target check
    if image_helper.pixel_matches_color(801,45, 107,2,1, 30) or image_helper.pixel_matches_color(710,45, 162,4,4, 30):
        # health check
        if not image_helper.pixel_matches_color(606,983, 82,7,11, 45) and not image_helper.pixel_matches_color(606,995, 138,6,18, 45):
            if image_helper.locate_needle(SKILLPATH+'pot.png', conf=0.7) and timer1.GetTimerState() == TIMER_STOPPED:
                timer1.StartTimer(3) # set timer to 5 seconds
                input_helper.press('f')
                time.sleep(random.uniform(0.21, 0.26))
            """if image_helper.locate_needle(SKILLPATH+'evade.png') and timer2.GetTimerState() == TIMER_STOPPED:
                timer2.StartTimer(6) # set timer to 5 seconds
                input_helper.press('space')
                time.sleep(random.uniform(0.21, 0.26))"""
        # class skill checks
        if image_helper.locate_needle(SKILLPATH+'druid\\01.png'):
            input_helper.press('q')
            time.sleep(random.uniform(0.21, 0.26))
        elif image_helper.locate_needle(SKILLPATH+'druid\\02.png'):
            input_helper.press('w')
            time.sleep(random.uniform(0.21, 0.26))
        elif image_helper.locate_needle(SKILLPATH+'druid\\03.png'):
            input_helper.press('e')
            time.sleep(random.uniform(0.21, 0.26))
        elif image_helper.locate_needle(SKILLPATH+'druid\\04.png'):
            input_helper.press('r')
            time.sleep(random.uniform(0.21, 0.26))
        elif image_helper.locate_needle(SKILLPATH+'druid\\05.png', conf=0.963):
            input_helper.rightClick()
            time.sleep(random.uniform(0.21, 0.26))
        """else:
            logging.debug('cannot find images, left click')
            input_helper.leftClick()
            time.sleep(random.uniform(0.21, 0.26))"""

