import threading
import time
import random
import logging
import pyautogui
from PIL import ImageOps
import traceback
import sys

from helper import config_helper
from engine import bookmarks as bkmk, docked as doc, drones, mining as mng, navigation as nav, overview as o, controller
from engine.controller import originx, originy, system_mining, windowx, windowy, conf, total_sites, unsuitable_site, runs_var, playerfound


class LittleHelper:
    def __init__(self):
        self._lock = threading.Lock()
        self.pause_req = False
    
    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req

    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()

    def set_config(self):
        cfg = config_helper.read_config()
        return cfg
    
    def miner(self):
        """An automatic mining script."""

        # Ores to mine, in order of priority.
        o1 = './assets/overview/ore_types/plagioclase.bmp'
        o2 = './assets/overview/ore_types/pyroxeres.bmp'
        o3 = './assets/overview/ore_types/veldspar.bmp'
        o4 = './assets/overview/ore_types/scordite.bmp'
        o5 = 0

        global playerfound, unsuitable_site, runs_var, pc_list, npc_list

        timer_var = 0
        logging.info('beginning run ' + (str(runs_var)))
        
        while doc.is_docked() == 0 and unsuitable_site <= total_sites:
            # Check if ship has any drones in space.
            if controller.mlocate('./assets/indicators/drones/0_drone_in_bay.bmp',
                        conf=conf) == 1:
                o.focus_client()
                drones.recall_drones(drone_num)
            if bkmk.iterate_through_bookmarks_rand(total_sites) == 1:
                # Once arrived at site, check for hostile npcs and human players.
                # If either exist, warp to another site.
                # If no hostiles npcs or players are present, check for asteroids.
                # If no asteroids exist,  warp to another site.
                if o.select_overview_tab('general') == 1:
                    if o.look_for_ship(npc_list, pc_list) == 1:
                        unsuitable_site += 1
                        self.miner()
                o.select_overview_tab('mining')
                target = o.look_for_targets(o1, o2, o3, o4, o5)
                while target != 0:
                    unsuitable_site = 0
                    drones.launch_drones(drone_num)
                    if o.initiate_target_lock(target) == 0:
                        self.miner()
                    time.sleep(float(random.randint(5000, 15000)) / 1000)
                    mng.activate_miners(module_num)
                    # If ship inventory isn't full, continue to mine ore and wait
                    # for popups or errors.
                    # Switch back to the general tab for easier ship detection
                    o.select_overview_tab('general')
                    client = pyautogui.screenshot(region=(
                        originx, originy, windowx, windowy))
                    ship_full = controller.mlocate('./assets/popups/ship_inv_full.bmp',
                                        haystack=client, conf=conf)

                    # main mining loop # -------------------------------------------
                    while ship_full == 0:
                        time.sleep(1)
                        logging.debug('loop START -----')
                        # overview = pyautogui.screenshot(region=(
                        #    (originx + (windowx - (int(windowx / 3)))),
                        #    originy, (int(windowx / 3)), windowy))
                        client = pyautogui.screenshot(region=(
                            originx, originy, windowx, windowy))
                        overview = ImageOps.crop(client, (755, 0, 0, 0))

                        ship_full = controller.mlocate('./assets/popups/ship_inv_full.bmp',
                                            haystack=client, conf=conf)
                        timer_var += 1
                        
                        if controller.mlocate('./assets/popups/asteroid_depleted.bmp',
                                    haystack=client, conf=conf) == 1:
                            # Sleep to wait for all mining modules to disable
                            # themselves automatically
                            logging.info('waiting for modules to deactivate')
                            time.sleep(float(random.randint(10000, 15000)) / 1000)
                            o.select_overview_tab('mining')
                            target = o.look_for_targets(o1, o2, o3, o4, o5)
                            if target == 0:
                                self.miner()
                            elif target != 0:
                                if o.initiate_target_lock(target) == 0:
                                    self.miner()
                                # This sleep is experimental, and prevents the
                                # script from attempting to mine an asteroid that
                                # is too far away.
                                time.sleep(
                                    float(random.randint(5000, 15000)) / 1000)
                                mng.activate_miners(module_num)
                                ship_full = controller.mlocate(
                                    './assets/popups/ship_inv_full.bmp',
                                    haystack=client, conf=conf)
                                continue

                        if mng.time_at_site(timer_var) == 1 or controller.mlocate(
                                './assets/indicators/no_object_selected.bmp',
                                haystack=client, conf=conf) == 1:
                            drones.recall_drones(drone_num)
                            self.miner()

                        if o.look_for_ship(npc_list, pc_list, haystack=overview) \
                                == 1 \
                                or o.is_jammed(detect_jam, haystack=overview) == 1:
                            drones.recall_drones(drone_num)
                            self.miner()
                        logging.info('loop END -----')
                    # end of main mining loop --------------------------------------

                    if ship_full == 1:
                        # Once inventory is full, dock at home station and unload.
                        drones.recall_drones(drone_num)
                        logging.info('finishing up run ' + (str(runs_var)))
                        if system_mining == 0:
                            if bkmk.set_home() == 1:
                                if self.navigator() == 1:
                                    doc.unload_ship()
                                    doc.wait_for_undock()
                                    playerfound = 0
                                    time.sleep(3)
                                    runs_var += 1
                                    self.miner()
                        # If ship is mining in the same system it will dock in,
                        # a different set of functions is required.
                        elif system_mining == 1:
                            bkmk.dock_at_local_bookmark()
                            doc.unload_ship()
                            doc.wait_for_undock()
                            playerfound = 0
                            time.sleep(3)
                            runs_var += 1
                            self.miner()

                if target == 0:
                    unsuitable_site += 1
                    logging.debug('unsuitable_site is' + (str(unsuitable_site)))
                    logging.debug('no targets, restarting')
                    self.miner()

            elif bkmk.iterate_through_bookmarks_rand(total_sites) == 0:
                nav.emergency_terminate()
                sys.exit(0)
                
        if doc.is_docked() == 1 and unsuitable_site <= total_sites:
            o.focus_client()
            doc.wait_for_undock()
            self.miner()
            
        if doc.is_docked() == 1 and unsuitable_site > total_sites:
            logging.debug('unsuitable site limit reached')
            sys.exit()
            
        if doc.is_docked() == 0 and unsuitable_site > total_sites:
            logging.debug('unsuitable site limit reached')
            nav.emergency_terminate()
            nav.emergency_logout()
            sys.exit()


    def navigator(self):
        """A standard warp-to-zero autopilot script. Warp to the destination, then
        terminate."""
        logging.debug('running navigator')
        nav.has_route()
        dockedcheck = doc.is_docked()

        while dockedcheck == 0:
            o.focus_overview()
            selectwaypoint = nav.warp_to_waypoint()
            while selectwaypoint == 1:  # Value of 1 indicates stargate waypoint.
                time.sleep(5)  # Wait for jump to begin.
                detectjump = nav.wait_for_jump()
                if detectjump == 1:
                    selectwaypoint = nav.warp_to_waypoint()
                else:
                    logging.critical('error detecting jump')
                    nav.emergency_terminate()
                    traceback.print_exc()
                    traceback.print_stack()
                    sys.exit()

            while selectwaypoint == 2:  # Value of 2 indicates a station waypoint.
                time.sleep(5)
                detectdock = nav.wait_for_dock()
                if detectdock == 1:
                    logging.info('arrived at destination')
                    return 1
            else:
                logging.warning('likely at destination')
                return 1

        while dockedcheck == 1:
            doc.wait_for_undock()
            time.sleep(5)
            self.navigator()


    def collector(self):
        """Haul all items from a predetermined list of stations to a single 'home'
        station, as specified by the user. The home station is identified by a
        station bookmark beginning with '000', while the remote stations are any
        station bookmark beginning with the numbers 1-9. This means up to 10
        remote stations are supported."""
        logging.debug('running collector')
        dockedcheck = doc.is_docked()
        while dockedcheck == 0:
            selectwaypoint = nav.warp_to_waypoint()

            while selectwaypoint == 1:
                time.sleep(3)  # Wait for warp to start.
                detectjump = nav.wait_for_jump()
                if detectjump == 1:
                    selectwaypoint = nav.warp_to_waypoint()
            while selectwaypoint == 2:
                time.sleep(3)
                detectdock = nav.wait_for_dock()
                if detectdock == 1:
                    self.collector()
            else:
                logging.critical('error with at_dest_check_var and '
                                'at_home_check_var')
                traceback.print_exc()
                traceback.print_stack()
                sys.exit()

        while dockedcheck == 1:
            athomecheck = bkmk.is_home()
            # If docked at home station, set a destination waypoint to a remote
            # station and unload cargo from ship into home station inventory.
            if athomecheck == 1:
                doc.unload_ship()
                bkmk.set_dest()
                doc.wait_for_undock()
                self.collector()
            elif athomecheck == 0:
                logging.debug('not at home')
                loadship = doc.load_ship()
                logging.debug('loadship is ' + (str(loadship)))

                if loadship == 2 or loadship == 0 or loadship is None:
                    atdestnum = bkmk.detect_bookmark_location()
                    if atdestnum == -1:
                        doc.wait_for_undock()
                        self.collector()
                    else:
                        bkmk.set_dest()
                        bkmk.blacklist_station()
                        doc.wait_for_undock()
                        self.collector()
                elif loadship == 1:  # Value of 1 indicates ship is full.
                    bkmk.set_home()
                    doc.wait_for_undock()
                    self.collector()

            else:
                logging.critical('error with detect_at_home and at_dest_check')
                traceback.print_exc()
                traceback.print_stack()
                sys.exit()
        if dockedcheck is None:
            self.collector()


    def get_color_from_pos(self):
        # debug function
        while True:
            while self.should_pause():
                time.sleep(.5)
            r1,g1,b1 = controller.pixel_color(1037,972)
            r2,g2,b2 = controller.pixel_color(1092,971)
            r3,g3,b3 = controller.pixel_color(1147,970)
            r4,g4,b4 = controller.pixel_color(1201,970)
            r5,g5,b5 = controller.pixel_color(1257,967)
            r6,g6,b6 = controller.pixel_color(624,978)
            r7,g7,b7 = controller.pixel_color(885,925)
            x, y, r,g,b = controller.get_pixel_color()
            img = controller.get_img(0,0,1920,1080, PATHCOORDS+REFIMG) # cv2.matchTemplate
            if x<1920 and y<1080:
                logging.debug("Mouse[x,y, r,g,b: %d,%d, %d,%d,%d - Reference: \"%s\"]" % (x,y, r,g,b, img))
                logging.debug("R[1037,972, %d,%d,%d]" % (r1,g1,b1))
                logging.debug("Y[1092,971, %d,%d,%d]" % (r2,g2,b2))
                logging.debug("X[1147,970, %d,%d,%d]" % (r3,g3,b3))
                logging.debug("C[1201,970, %d,%d,%d]" % (r4,g4,b4))
                logging.debug("E[1257,967, %d,%d,%d]" % (r5,g5,b5))
                logging.debug("Q[624,978, %d,%d,%d]" % (r6,g6,b6))
                logging.debug("s4[885,925, %d,%d,%d]" % (r7,g7,b7))
                time.sleep(.2)


lilHelp = LittleHelper()

def start_miner():
    """Starts the main miner() script."""
    global drone_num, module_num, detect_jam
    global detect_pcs, pc_indy, pc_barge, pc_frig_dest, \
        pc_capindy_freighter, pc_cruiser_bc, pc_bs, pc_rookie, pc_pod
    global detect_npcs, npc_frig_dest, npc_cruiser_bc, npc_bs

    cfg = lilHelp.set_config()

    # Set the gui variables to reflect the current gui configuration when the
    # user clicks the start button.
    module_num = (int(cfg['number_of_mining_lasers']))
    drone_num = (int(cfg['number_of_drones']))
    logging.debug((str(module_num)) + ' modules')
    logging.debug((str(drone_num)) + ' drones')

    detect_pcs = (int(cfg['check_for_players']))
    logging.debug('detect pcs is ' + (str(detect_pcs)))

    pc_indy = (int(cfg['check_for_player_industrials']))
    logging.debug('detect pc indy is ' + (str(pc_indy)))

    pc_barge = (int(cfg['check_for_player_mining_barges']))
    logging.debug('detect pc barge is ' + (str(pc_barge)))

    pc_frig_dest = (int(cfg['check_for_player_frigates_and_destroyers']))
    logging.debug('detect pc frig/dest is ' + (str(pc_frig_dest)))

    pc_capindy_freighter = (int(cfg['check_for_player_capital_industrials_and_freighters']))
    logging.debug('detect pc capital indy/freighter is ' + (str(
        pc_capindy_freighter)))

    pc_cruiser_bc = (int(cfg['check_for_player_cruisers_and_battlecruisers']))
    logging.debug('detect pc cruiser/bc is ' + (str(pc_cruiser_bc)))

    pc_bs = (int(cfg['check_for_player_battleships']))
    logging.debug('detect pc bs is ' + (str(pc_bs)))

    pc_rookie = (int(cfg['check_for_player_rookie_ships']))
    logging.debug('detect pc rookie is ' + (str(pc_rookie)))

    pc_pod = (int(cfg['check_for_player_capsules']))
    logging.debug('detect pc pod is ' + (str(pc_pod)))

    detect_npcs = (int(cfg['check_for_rats']))
    logging.debug('detect npcs is ' + (str(detect_npcs)))

    npc_frig_dest = (int(cfg['check_for_rat_frigates_and_destroyers']))
    logging.debug('detect npc frig/dest is ' + (str(npc_frig_dest)))

    npc_cruiser_bc = (int(cfg['check_for_rat_cruisers_and_battlecruisers']))
    logging.debug('detect npc cruiser/bc is ' + (str(npc_cruiser_bc)))

    npc_bs = (int(cfg['check_for_rat_battleships']))
    logging.debug('detect npc bs is ' + (str(npc_bs)))

    detect_jam = (int(cfg['check_for_ECM_jamming']))
    logging.debug('detect ecm jamming is ' + (str(detect_jam)))

    lilHelp.miner()
    return

def start_navigator():
    """Starts the navigator() script."""
    lilHelp.navigator()
    return

def start_collector():
    """Starts the collector() script."""
    lilHelp.collector()
    return

def run():
    start_miner()

def debug():
    lilHelp.get_color_from_pos()

