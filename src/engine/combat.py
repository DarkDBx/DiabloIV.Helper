from logging import info, error
from random import uniform
from time import sleep
from pydirectinput import keyDown, keyUp, press, leftClick, rightClick

from helper import mouse_helper, image_helper, timer_helper, config_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"


timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')


def press_combo(key):
    keyDown('shift')
    press(key)
    keyUp('shift')


def rotation(x=None, y=None):
    """set up the skill rotation for a specific class, by the config value"""
    cfg = config_helper.read_config()
    class_var = cfg['class']

    if class_var == 'Druid':
        combat_rotation('druid', x, y)
    elif class_var == 'Barb':
        combat_rotation('barb', x, y)
    elif class_var == 'Necro':
        combat_rotation('necro', x, y)
    elif class_var == 'Sorc':
        combat_rotation('sorc', x, y)
    elif class_var == 'Rogue':
        combat_rotation('rogue', x, y)
    else:
        error('No vaible class')


def combat_rotation(value, x, y):
    cfg = config_helper.read_config()
    evade = cfg['evade']
    pot = cfg['pot']
    skill1 = cfg['skill1']
    skill2 = cfg['skill2']
    skill3 = cfg['skill3']
    skill4 = cfg['skill4']
    n = 25
    elite = False
    normal = False

    # target check
    if (image_helper.pixel_matches_color(801,45, 107,2,1, 20) or image_helper.pixel_matches_color(801,45, 156,65,93, 20) or \
                image_helper.pixel_matches_color(801,45, 231,13,9, 20)) or image_helper.line_detection('mob') != False:
        normal = True

        if x != None and y != None:
            mouse_helper.move_smooth(x+400+n, y+50+(n*2), 1)
    elif (image_helper.pixel_matches_color(710,45, 162,4,4, 20) or image_helper.pixel_matches_color(710,45, 124,71,98, 20)) or \
                image_helper.line_detection('mob') != False:
        elite = True

        if x != None and y != None:
            mouse_helper.move_smooth(x+400+(n*3), y+50+(n*6), 1)

    if normal or elite:
        # health check
        if not image_helper.pixel_matches_color(608,980, 95,10,15, 45) and not image_helper.pixel_matches_color(608,972, 148,14,24, 45) and \
                    not image_helper.pixel_matches_color(607,978, 97,29,82, 45):
            if (image_helper.locate_needle(SKILLPATH+'pot10.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot20.png', conf=0.7) or \
                        image_helper.locate_needle(SKILLPATH+'pot30.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot45.png', conf=0.7) or \
                        image_helper.locate_needle(SKILLPATH+'pot60.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot70.png', conf=0.7) or \
                        image_helper.locate_needle(SKILLPATH+'pot_placeholder.png', conf=0.7) or image_helper.locate_needle(SKILLPATH+'pot_placeholder.png', conf=0.7)) and \
                        timer1.GetTimerState() == TIMER_STOPPED:
                timer1.StartTimer(3)
                press(pot)
                info('Use potion')
                sleep(uniform(0.11, 0.13))
            if image_helper.locate_needle(SKILLPATH+'evade.png', conf=0.7) and timer2.GetTimerState() == TIMER_STOPPED:
                timer2.StartTimer(3)
                press(evade)
                info('Use evade')
                sleep(uniform(0.11, 0.13))

        # class skill check
        if value == 'rogue':
            if image_helper.locate_needle(SKILLPATH+value+'\\04.png', conf=0.6) and timer3.GetTimerState() == TIMER_STOPPED:
                timer3.StartTimer(6)
                press(skill4)
                info('Use skill 4')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\03.png', conf=0.6) and timer3.GetTimerState() == TIMER_STOPPED:
                timer3.StartTimer(6)
                press(skill3)
                info('Use skill 3')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\01.png', conf=0.6):
                press(skill1)
                info('Use skill 1')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\02.png', conf=0.6):
                press(skill2)
                info('Use skill 2')
                sleep(uniform(0.11, 0.13))
        else:
            if image_helper.locate_needle(SKILLPATH+value+'\\04.png', conf=0.6):
                press(skill4)
                info('Use skill 4')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\03.png', conf=0.6):
                press(skill3)
                info('Use skill 3')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\01.png', conf=0.6):
                press(skill1)
                info('Use skill 1')
                sleep(uniform(0.11, 0.13))
            elif image_helper.locate_needle(SKILLPATH+value+'\\02.png', conf=0.6):
                press(skill2)
                info('Use skill 2')
                sleep(uniform(0.11, 0.13))

        if (value == 'druid' and image_helper.locate_needle(SKILLPATH+value+'\\05.png', conf=0.96)) or \
                    (value != 'druid' and image_helper.locate_needle(SKILLPATH+value+'\\05.png', conf=0.8)):
            rightClick()
            info('Use skill right mouse')
            sleep(uniform(0.11, 0.13))
        elif x != None and y != None:
            leftClick()
            info('Use skill left mouse')
            sleep(uniform(0.11, 0.13))

