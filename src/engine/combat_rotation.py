"""EXAMPLE FILE"""
import random
import time
import logging

from helper import input_helper, image_helper, timer_helper, config_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"

"""ADD TIMER IF NEEDED"""
timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')
timer4 = timer_helper.TimerHelper('timer4')
timer5 = timer_helper.TimerHelper('timer5')
timer6 = timer_helper.TimerHelper('timer6')
timer7 = timer_helper.TimerHelper('timer7')
timer8 = timer_helper.TimerHelper('timer8')
timer9 = timer_helper.TimerHelper('timer9')
timer10 = timer_helper.TimerHelper('timer10')
timer11 = timer_helper.TimerHelper('timer11')
timer12 = timer_helper.TimerHelper('timer12')

def press_combo(key1, key2):
    input_helper.keyDown(key1)
    input_helper.press(key2)
    input_helper.keyUp(key1)

def default_rotation():
    """set up the skill rotation for a specific function injected by the config"""
    cfg = config_helper.read_config()
    func = cfg['func']
    if func == 'default_combat':
        logging.info('cr.default_combat()')
        time.sleep(0.25)
    elif func == 'eso_dk_pve':
        eso_dk_pve()
    elif func == 'eso_nb_pve':
        eso_nb_pve()
    elif func == 'eso_nb_pvp':
        eso_nb_pvp()
    elif func == 'gw2_rev_pvp':
        gw2_rev_pvp()
    elif func == 'gw2_sb_pvp':
        gw2_sb_pvp()
    else:
        logging.error('No vaible function')


"""EDIT BELOW THIS LINE"""
# https://www.linktoyourbuild.com/
def default_combat():
    # target check
    if image_helper.pixel_matches_color(784,95, 149,34,18):
        # health check
        if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'game_name\\class_name\\heal.png') and timer1.GetTimerState() == TIMER_STOPPED: # heal at 60%
            timer2.StartTimer(5) # set timer to 5 seconds
            input_helper.press('h')
            time.sleep(0.25)
        # class skill checks
        elif image_helper.locate_needle(SKILLPATH+'game_name\\class_name\\03.png') and timer2.GetTimerState() == TIMER_STOPPED:
            timer1.StartTimer(7)
            input_helper.press('3')
            time.sleep(0.4)
        elif image_helper.locate_needle(SKILLPATH+'game_name\\class_name\\example.png') and timer3.GetTimerState() == TIMER_STOPPED:
            timer3.StartTimer(9)
            press_combo('ctrl', 'k')
            time.sleep(0.75)
        else:
            input_helper.rightClick()
        
        time.sleep(random.uniform(0.10, 0.15))
        input_helper.leftClick()
        time.sleep(0.25)


"""dragonknight pve"""
# https://alcasthq.com/eso-stamina-dragonknight-tank-build-pve/
def eso_dk_pve():
    # target check
    if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
        # weapon swap
        if timer1.GetTimerState() == TIMER_STOPPED:
            timer1.StartTimer(4)
            input_helper.press('tab')
        # ultimate
        elif timer12.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\06.png', conf=0.98) == 1:
            timer12.StartTimer(9)
            input_helper.press('r')
        # quickslot bar 1
        elif timer2.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\05.png'):
            timer2.StartTimer(23)
            input_helper.press('5')
        elif timer5.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\02.png'):
            timer5.StartTimer(15)
            input_helper.press('2')
        elif timer6.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\01.png'):
            timer6.StartTimer(12)
            input_helper.press('1')
        elif timer3.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\03.png'):
            timer3.StartTimer(6)
            input_helper.press('3')
        # quickslot bar 2
        elif timer8.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\05-2.png'):
            timer8.StartTimer(10)
            input_helper.press('5')
        elif timer10.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\02-2.png'):
            timer10.StartTimer(15)
            input_helper.press('2')
        elif timer11.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\03-2.png'):
            timer11.StartTimer(15)
            input_helper.press('3')
        elif timer7.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\dragonknight\\tank_pve\\01-2.png'):
            timer7.StartTimer(20)
            input_helper.press('1')
        else:
            input_helper.rightClick()
            
        time.sleep(random.uniform(0.11, 0.15))
        input_helper.leftClick()
        time.sleep(0.25)


"""nightblade pve"""
# https://alcasthq.com/eso-stamina-nightblade-bow-build-for-pve/
def eso_nb_pve():
    # target check
    if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
        # weapon swap
        if timer1.GetTimerState() == TIMER_STOPPED:
            timer1.StartTimer(4)
            input_helper.press('tab')
        # ultimate
        elif timer12.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\06-2.png', conf=0.98) == 1: # ulti
            timer12.StartTimer(9)
            input_helper.press('r')
        # quickslot bar 1
        elif timer2.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05.png'):
            timer2.StartTimer(60)
            input_helper.press('5')
        elif timer3.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03.png'):
            timer3.StartTimer(20)
            input_helper.press('3')
        elif timer6.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01.png'):
            timer6.StartTimer(3)
            input_helper.press('1')
        elif timer5.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02.png'):
            timer5.StartTimer(3)
            input_helper.press('2')
        elif timer4.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04.png'):
            timer4.StartTimer(3)
            input_helper.press('4')
        # quickslot bar 2
        elif timer9.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\03-2.png'):
            timer9.StartTimer(22)
            input_helper.press('3')
        elif timer8.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\04-2.png'):
            timer8.StartTimer(17)
            input_helper.press('4')
        elif timer7.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\05-2.png'):
            timer7.StartTimer(5)
            input_helper.press('5')
        elif timer10.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\02-2.png'):
            timer10.StartTimer(20)
            input_helper.press('2')
        elif timer11.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pve\\01-2.png'):
            timer11.StartTimer(15)
            input_helper.press('1')
        else:
            input_helper.rightClick()
        
        time.sleep(random.uniform(0.11, 0.15))
        input_helper.leftClick()
        time.sleep(0.25)


"""nightblade pvp"""
# https://alcasthq.com/eso-stamina-nightblade-bow-gank-build-pvp/
def eso_nb_pvp():
    # target check
    if image_helper.pixel_matches_color(958,101, 118,42,42) or image_helper.pixel_matches_color(958,103, 110,34,34):
        # weapon swap
        if timer1.GetTimerState() == TIMER_STOPPED:
            timer1.StartTimer(4)
            input_helper.press('tab')
        # ultimate
        elif timer12.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\06.png', conf=0.98) == 1: # ulti
            timer12.StartTimer(9)
            input_helper.press('r')
        # quickslot bar 1
        elif timer2.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05.png'):
            timer2.StartTimer(60)
            input_helper.press('5')
        elif timer4.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\04.png'):
            timer4.StartTimer(5)
            input_helper.press('4')
        elif timer5.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02.png'):
            timer5.StartTimer(3)
            input_helper.press('2')
        elif timer6.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01.png'):
            timer6.StartTimer(3)
            input_helper.press('1')
        # quickslot bar 2
        elif timer7.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\01-2.png'):
            timer7.StartTimer(40)
            input_helper.press('1')
        elif timer8.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\05-2.png'):
            timer8.StartTimer(5)
            input_helper.press('5')
        elif timer10.GetTimerState() == TIMER_STOPPED and image_helper.locate_needle(SKILLPATH+'eso\\nightblade\\bow_pvp\\02-2.png'):
            timer10.StartTimer(4)
            input_helper.press('2')
        else:
            input_helper.rightClick()

        time.sleep(random.uniform(0.11, 0.15))
        input_helper.leftClick()
        time.sleep(0.25)


"""vindicator pvp"""
# https://guildjen.com/shiro-vindicator-pvp-build/
def gw2_rev_pvp():
    # target check
    if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
        # health check
        if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06.png'): # heal at 60%
            input_helper.press('r')
            time.sleep(0.5)
        elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\06-2.png'): # heal at 60%
            input_helper.press('r')
            time.sleep(1.5)
        # class skill checks
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\10-2.png'):
            input_helper.press('e')
            time.sleep(0.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09.png'):
            input_helper.press('c')
            time.sleep(0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\09-2.png'):
            input_helper.press('c')
            time.sleep(0.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08.png'):
            input_helper.press('x')
            time.sleep(+0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\08-2.png'):
            input_helper.press('x')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05.png'):
            input_helper.press('5')
            time.sleep(1.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02.png'):
            input_helper.press('2')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\02-2.png'):
            input_helper.press('2')
            time.sleep(0.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\03-2.png'):
            input_helper.press('3')
            time.sleep(0.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\05-2.png'):
            input_helper.press('5')
            time.sleep(1)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\WeaponSwap.png'):
            input_helper.press('q')
            time.sleep(0.25)
            if image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1.png') or image_helper.locate_needle(SKILLPATH+'gw2\\revenant\\v_pvp\\s1-2.png'):
                press_combo('shift', '1')
                time.sleep(0.25)
        else:
            input_helper.press('1')
            time.sleep(0.5)


"""soulbeast pvp/wvw"""
# https://guildjen.com/sic-em-soulbeast-pvp-build/
# https://guildjen.com/sic-em-soulbeast-roaming-build/
def gw2_sb_pvp():
    # target check
    if image_helper.pixel_matches_color(784,95, 149,34,18) or image_helper.pixel_matches_color(784,98, 148,33,18):
        # health check
        if not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\06.png'): # heal at 60%
            input_helper.press('r')
            time.sleep(0.75)
        elif not image_helper.pixel_matches_color(961,999, 170,21,5) and (image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\07-2.png')): # at 60%
            input_helper.press('z')
        elif not image_helper.pixel_matches_color(961,999, 170,21,5) and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\09.png'): # at 60%
            input_helper.press('c')
        # class skill checks
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10-2.png'):
            input_helper.press('e')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\10.png'):
            input_helper.press('e')
            time.sleep(0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\08.png'):
            input_helper.press('x')
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\04.png') and image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02.png'):
            input_helper.press('4')
            time.sleep(0.5)
            input_helper.press('2')
            time.sleep(2.5)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\02-2.png'):
            input_helper.press('2')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\05-2.png'):
            input_helper.press('5')
            time.sleep(0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\WeaponSwap.png'):
            input_helper.press('q')
            time.sleep(0.25)
            if image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s5-2.png'):
                press_combo('shift', '5')
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1.png'):
            press_combo('shift', '1')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s1-2.png'):
            press_combo('shift', '1')
            time.sleep(0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s2-2.png'):
            press_combo('shift', '2')
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3.png'):
            press_combo('shift', '3')
            time.sleep(0.75)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s3-2.png'):
            press_combo('shift', '3')
            time.sleep(0.25)
        elif image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4.png') or image_helper.locate_needle(SKILLPATH+'gw2\\ranger\\sb_pvp\\s4-2.png'):
            press_combo('shift', '4')
            time.sleep(0.25)
        else:
            input_helper.press('1')
            time.sleep(0.5)

