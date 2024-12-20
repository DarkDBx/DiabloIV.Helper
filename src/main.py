#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
from PyQt5.QtWidgets import QApplication

from GUI import overlay
from helper import config_helper, logging_helper
from helper.logging_helper import DEBUG

APPNAME = 'D4.Helper'
APPVERSION = '1.2024.1220.1341'

def main():
    """
    Entry point for the application.
    Initializes the GUI and reads configuration.
    """
    try:
        app = QApplication(argv)
        app_gui = overlay.Overlay()
        app_gui.show()

        cfg = config_helper.read_config()
        logging_helper.logger.setLevel(DEBUG)
        logging_helper.log_info(f"====== {APPNAME} {APPVERSION} ======")
        logging_helper.log_info("Starting up bot engine...")
        logging_helper.log_info(f"Preset class {cfg['class']} is initialized")

        # Execute the QApplication event loop
        exit(app.exec_())
    except Exception as e:
        logging_helper.log_error("Unexpected exception occurred!", exc_info=e)

if __name__ == '__main__':
    main()
