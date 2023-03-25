#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout,
        QGroupBox, QPushButton, QStyleFactory, QVBoxLayout)

from helper import little_helper, config_helper, input_helper, process_helper


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setGeometry(50, 50, 200, 200)
        self.setWindowTitle("LittleHelper")
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.run =  False

        self.cfg = config_helper
        self.prc = process_helper
        
        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 0, 0)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("START")

        toggleStartButton = QPushButton("Little Helper")
        toggleStartButton.setCheckable(True)
        toggleStartButton.setChecked(False)
        toggleStartButton.clicked.connect(self.engine_run)

        toggleDebugButton = QPushButton("Debug Helper")
        toggleDebugButton.setCheckable(True)
        toggleDebugButton.setChecked(False)
        toggleDebugButton.clicked.connect(self.debug_run)

        layout = QVBoxLayout()
        layout.addWidget(toggleStartButton)
        layout.addWidget(toggleDebugButton)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def on_press(self, key):
        # acquire the keyboard hit if exists
        key = input_helper.kbfunc() 
        if key != False and key.decode() == 'end':
            logging.info('Exit key pressed')
            self.run = False
        elif key != False and key.decode() == 'delete':
            logging.info('Pause key pressed')
            little_helper.lilHelp.set_pause(not little_helper.lilHelp.should_pause())

    def engine_run(self):
        self.prc.set_foreground_window()
        self.prc.set_window_pos()
        logging.info('Little Helper started')
        self.run = True
        while self.run == True:
            little_helper.run()

    def debug_run(self):
        self.prc.set_foreground_window()
        self.prc.set_window_pos()
        logging.debug('Debug Helper started')
        self.run = True
        while self.run == True:
            little_helper.debug()


def main():
    #try:
    app = QApplication(argv)
    gui = GUI()
    gui.show()
    logging.info(('========== %s %s ==========') % ("Little Helper", "v0.7.1-eve"))
    logging.info('Booting up bot system...')
    exit(app.exec_())
    """
    except SystemExit:
        logging.error("Shutting down bot, caused by previous warning or fatal.\n")
    except Exception as e:
        logging.error(f"Shutting down bot, error:\n{e}\n")
    """


if __name__ == '__main__':
    main()

