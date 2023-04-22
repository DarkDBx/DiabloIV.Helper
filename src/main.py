#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
import logging
from PyQt5.QtWidgets import QApplication

from engine import littlehelper_gui
from helper import config_helper


def main():
    app = QApplication(argv)
    gui = littlehelper_gui.GUI()
    gui.show()

    cfg = config_helper.read_config()
    logging.info(('====== %s %s ======') % ("LittleHelper", "v0.8.7"))
    logging.info('Starting up bot engine...')
    logging.info('Preset func: '+cfg['func']+' is initialized')
    exit(app.exec_())


if __name__ == '__main__':
    main()

