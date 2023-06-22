#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import exit, argv
import logging
from PyQt5.QtWidgets import QApplication

from engine import overlay
from helper import config_helper


def main():
    app = QApplication(argv)
    app_gui = overlay.Overlay()
    app_gui.show()

    cfg = config_helper.read_config()
    logging.getLogger().setLevel(logging.INFO)

    logging.info(('====== %s %s ======') % ("LittleHelper", "v0.9.10"))
    logging.info('Starting up bot engine...')
    logging.info('Preset class: '+cfg['class']+' is initialized')
    
    exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error("Unexpected exception! %s",e)

