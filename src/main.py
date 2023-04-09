#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
import logging
from PyQt5.QtWidgets import QApplication

from helper import gui_helper


def main():
    """try:"""
    app = QApplication(argv)
    gui = gui_helper.GUI()
    gui.show()
    logging.info(('====== %s %s ======') % ("LittleHelper", "v0.7.5"))
    logging.info('Starting up bot engine...')
    exit(app.exec_())
    """except SystemExit:
        logging.error("Shutting down bot, caused by previous warning or fatal.\n")
    except Exception as e:
        logging.error(f"Shutting down bot, error:\n{e}\n")"""


if __name__ == '__main__':
    main()

