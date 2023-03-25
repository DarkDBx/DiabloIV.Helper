import logging
import random
import sys
import time
import traceback
import pyautogui as pag

from helper import input_helper
from engine import controller, overview as o
from engine.controller import conf


def has_route():
    # TODO: fix this function, the detect_route image doesn't exist
    """Checks the top-left corner of the client window to see if a route has
     actually been set by the user."""
    return
    route_set_var = controller.mlocate('./assets/indicators/detect_route.bmp', conf=conf)
    if route_set_var == 0:
        logging.error('no route set!')
        sys.exit(0)
    else:
        return


def warp_to_waypoint():
    """Clicks on the current waypoint and uses the warp hotkey to warp to
    waypoint. Currently only supports warping to stargate and station
    waypoints."""
    # TODO: add support for warping to citadels and engineering complexes
    logging.debug('looking for waypoints')
    # Speed up image searching by looking within overview only. This
    # obviously requires the user to place the overview on the right side of
    # the client window.

    for tries in range(1, 15):
        stargate = controller.mlocate('./assets/overview/stargate_waypoint.bmp', conf=conf)
        if stargate != 0:
            logging.debug('found stargate waypoint')
            (x, y) = stargate
            input_helper.mo._move_to((x + (random.randint(-8, 30))), (y + (random.randint(-8, 8))))
            input_helper.leftClick()
            input_helper.press('d')  # 'dock / jump' hotkey.
            # Move mouse to the left side of the client to prevent
            # tooltips from interfering with image searches.
            controller.move_to_neutral()
            return 2

        station = controller.mlocate('./assets/overview/station_waypoint.bmp', conf=conf)
        if station != 0:
            logging.debug('found station waypoint')
            (x, y) = station
            input_helper.mo._move_to((x + (random.randint(-8, 30))),
                       (y + (random.randint(-8, 8))))
            input_helper.leftClick()
            input_helper.press('d')
            controller.move_to_neutral()
            return 2

        if stargate == 0 and station == 0:
            time.sleep(float(random.randint(500, 1500)) / 1000)
            logging.debug('looking for waypoints ' + (str(tries)))

    logging.error('no waypoints found')
    return 0


def wait_for_warp_to_complete():
    """Detects when a warp has started and been
    completed by watching the spedometer."""
    # TODO: force ship to wait a minimum period of time while beginning its
    # warp, similar to what tinyminer does to eliminate possible issues.

    # Wait for warp to begin by waiting until the speedometer is full. Ship
    # might be stuck on something so this could take an variable amount of
    # time.

    for duration in range(1, 300):
        warping = controller.mlocate('./assets/indicators/warping2.bmp', conf=conf)

        if warping != 0:
            logging.debug('warping')
            time.sleep(float(random.randint(1000, 3000)) / 1000)

            # Once warp begins, wait for warp to end by waiting for the
            # 'warping' text on the spedometer to disappear.
            for tries in range(1, 150):
                time.sleep(float(random.randint(1000, 3000)) / 1000)
                warping_done = controller.mlocate('./assets/indicators/warping3.bmp',
                                          conf=conf)

                if warping_done == 0:
                    logging.debug('warp completed')
                    return 1
                elif warping_done != 0:
                    logging.debug('waiting for warp to complete ' +
                                  (str(tries)))

            logging.error('timed out waiting for warp to complete')
            return 0

        elif warping == 0:
            logging.debug('waiting for warp to start ' + (str(duration)))
            time.sleep(float(random.randint(500, 1000)) / 1000)

    logging.error('timed out waiting for warp to start')
    return 0


def wait_for_jump():
    """Waits for a jump by looking for the cyan session-change icon in top left
    corner of the client window. Also checks if the 'low security system
    warning' window has appeared and is preventing the ship from jumping.
    Times out after about four minutes."""
    # Confidence must be lower than normal since icon is partially
    # transparent.
    for tries in range(1, 240):
        jumped = controller.mlocate('./assets/indicators/session_change_cloaked.bmp',
                            conf=0.4)

        if jumped != 0:
            logging.debug('jump detected')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            return 1

        elif jumped == 0:
            losec = controller.mlocate('./assets/warnings/low_security_system.bmp',
                               conf=conf)
            if losec != 0:
                time.sleep(float(random.randint(2000, 5000)) / 1000)
                input_helper.press('enter')
                continue

            logging.debug('waiting for jump ' + (str(tries)))
            time.sleep(float(random.randint(5, 20)) / 10)

    logging.error('timed out waiting for jump')
    emergency_terminate()
    traceback.print_stack()
    sys.exit()


def wait_for_dock():
    """Waits for a dock by looking for the undock button on the right half
    of the client window."""
    for tries in range(1, 180):
        docked = controller.mlocate('./assets/buttons/undock.bmp', conf=conf)

        if docked != 0:
            logging.debug('detected dock ' + (str(tries)))
            time.sleep(float(random.randint(1000, 3000)) / 1000)
            return 1

        elif docked == 0:
            logging.debug('waiting for dock ' + (str(tries)))
            time.sleep(float(random.randint(2000, 5000)) / 1000)

    logging.error('timed out waiting for dock')
    return 0


def emergency_terminate():
    """Looks for the nearest station and docks immediately. Incrementally lowers
    the confidence required to match the station icon each time the loop runs
    in order to increase the chances of a warp. If a station cannot be found
    after a certain number of checks, warps to the nearest planet. After warp
    completes, simulates a client disconnection by forcing an unsafe logout
    in space."""
    logging.warning('EMERGENCY TERMINATE CALLED !!!')
    confidence = conf
    o.select_overview_tab('general')

    # Look for a station to dock at until confidence is <0.85
    for tries in range(1, 15):
        station_icon = controller.mlocate('./assets/overview/station.bmp', conf=confidence)

        if station_icon != 0:
            logging.debug('emergency docking ' + (str(tries)))
            (x, y) = station_icon
            input_helper.mo._move_to((x + (random.randint(-2, 50))),
                       (y + (random.randint(-2, 2))))
            input_helper.leftClick()
            time.sleep(float(random.randint(600, 1200)) / 1000)
            pag.keyDown('d')
            time.sleep(float(random.randint(600, 1200)) / 1000)
            pag.keyUp('d')
            controller.move_to_neutral()
            if wait_for_dock() == 1:
                emergency_logout()
            elif wait_for_dock() == 0:
                time.sleep(float(random.randint(20000, 40000)) / 1000)
                emergency_logout()
            return 1

        elif station_icon == 0:
            confidence -= 0.05
            logging.debug('looking for station to dock at' + (str(tries)) +
                          ', confidence is ' + (str(confidence)))
            # Keep time interval relatively short since ship may be in combat.
            time.sleep(float(random.randint(500, 1000)) / 1000)

    # If confidence lowers below threshold, try warping to a planet
    # instead.
    logging.debug('could not find station to emergency dock at, warping to'
                  'planet instead')
    confidence = conf
    o.select_overview_tab('warpto')

    for tries in range(1, 50):
        planet = controller.mlocate('./assets/overview/planet.bmp', conf=confidence)

        if planet != 0:
            logging.debug('emergency warping to planet')
            (x, y) = planet
            input_helper.mo._move_to((x + (random.randint(-2, 50))),
                       (y + (random.randint(-2, 2))))
            input_helper.leftClick()
            time.sleep(float(random.randint(600, 1200)) / 1000)
            input_helper.press('s')
            controller.move_to_neutral()
            wait_for_warp_to_complete()
            emergency_logout()
            return 1

        elif planet == 0:
            logging.debug('looking for planet ' + (str(tries)) +
                          ', confidence is ' + (str(confidence)))
            # Lower confidence on every third try.
            if (tries % 3) == 0:
                confidence -= 0.05
            time.sleep(float(random.randint(600, 2000)) / 1000)

    logging.debug('timed out looking for planet')
    emergency_logout()
    return 0


def emergency_logout():
    """Forcefully kill the client session, don't use the 'log off
    safely' feature."""
    logging.warning('emergency logout called')
    time.sleep(float(random.randint(1000, 5000)) / 1000)
    pag.keyDown('alt')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('shift')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('q')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('alt')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('shift')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('q')
    return 0
