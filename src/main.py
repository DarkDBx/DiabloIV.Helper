#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import exit, argv
import logging
from PyQt5.QtWidgets import QApplication

from engine import gui
from helper import config_helper


def main():
    app = QApplication(argv)
    app_gui = gui.GUI()
    app_gui.show()

    cfg = config_helper.read_config()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(('====== %s %s ======') % ("LittleHelper", "v0.9.7"))
    logging.info('Starting up bot engine...')
    logging.info('Preset class: '+cfg['class']+' is initialized')
    exit(app.exec_())


if __name__ == '__main__':
    main()

