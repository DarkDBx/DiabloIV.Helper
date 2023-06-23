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


"""Pulverize druid"""
# https://maxroll.gg/d4/build-guides/pulverize-druid-guide
def druid(x=None, y=None):
    # target check
    if image_helper.pixel_matches_color(801,45, 107,2,1, 15) or image_helper.pixel_matches_color(801,45, 156,65,93, 15) or \
                image_helper.pixel_matches_color(801,45, 231,13,9, 15) or image_helper.pixel_matches_color(710,45, 162,4,4, 15) or \
                image_helper.pixel_matches_color(710,45, 124,71,98, 15) or image_helper.mob_detection() != False:
        if x != None and y != None:
            input_helper.moveTo(x, y)

        # health check
        if not image_helper.pixel_matches_color(608,980, 95,10,15, 45) and not image_helper.pixel_matches_color(608,972, 148,14,24, 45) and \
                    not image_helper.pixel_matches_color(607,978, 97,29,82, 45):
            if (image_helper.locate_needle(SKILLPATH+'pot30.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot45.png', conf=0.7) or \
                        image_helper.locate_needle(SKILLPATH+'pot60.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot70.png', conf=0.7)) and \
                        timer1.GetTimerState() == TIMER_STOPPED:
                timer1.StartTimer(3)
                input_helper.press('f')
                logging.info('Use potion')
                time.sleep(random.uniform(0.11, 0.13))
            if image_helper.locate_needle(SKILLPATH+'evade.png', conf=0.7) and timer2.GetTimerState() == TIMER_STOPPED:
                timer2.StartTimer(6)
                input_helper.press('space')
                logging.info('Use evade')
                time.sleep(random.uniform(0.11, 0.13))

        # class skill check
        if image_helper.locate_needle(SKILLPATH+'druid\\04.png', conf=0.5):
            input_helper.press('r')
            logging.info('Use skill 4')
            time.sleep(random.uniform(0.11, 0.13))
        elif image_helper.locate_needle(SKILLPATH+'druid\\03.png', conf=0.6):
            input_helper.press('e')
            logging.info('Use skill 3')
            time.sleep(random.uniform(0.11, 0.13))
        elif image_helper.locate_needle(SKILLPATH+'druid\\01.png', conf=0.6):
            input_helper.press('q')
            logging.info('Use skill 1')
            time.sleep(random.uniform(0.11, 0.13))
        elif image_helper.locate_needle(SKILLPATH+'druid\\02.png', conf=0.6):
            input_helper.press('w')
            logging.info('Use skill 2')
            time.sleep(random.uniform(0.11, 0.13))

        if image_helper.locate_needle(SKILLPATH+'druid\\05.png', conf=0.97):
            input_helper.rightClick()
            logging.info('Use skill right mouse')
            time.sleep(random.uniform(0.11, 0.13))
        elif x != None and y != None:
            input_helper.leftClick()
            logging.info('Use skill left mouse')
            time.sleep(random.uniform(0.11, 0.13))

