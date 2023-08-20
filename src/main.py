#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from logging import getLogger, info, error, INFO, DEBUG
from sys import exit, argv
from PyQt5.QtWidgets import QApplication

from engine import overlay
from helper import config_helper


APPNAME = 'LittleHelper'
APPVERSION = 'v0.9.21'


def main():
    app = QApplication(argv)
    app_gui = overlay.Overlay()
    app_gui.show()

    cfg = config_helper.read_config()
    getLogger().setLevel(DEBUG)

    info(('====== %s %s ======') % (APPNAME, APPVERSION))
    info('Starting up bot engine...')
    info('Preset class ' + cfg['class'] + ' is initialized')
    
    exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error("Unexpected exception! %s", e)

