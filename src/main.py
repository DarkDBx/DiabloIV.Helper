#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
import logging
import keyboard
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QLabel, QPushButton, QStyleFactory, QVBoxLayout

from helper import little_helper, config_helper, input_helper, process_helper


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setGeometry(50, 50, 500, 100)
        self.setWindowTitle("LittleHelper")
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        keyboard.add_hotkey('end', lambda: self.on_press('end'))
        keyboard.add_hotkey('del', lambda: self.on_press('del'))
        logging.basicConfig(level=logging.DEBUG)
        self.run =  False
        self.class_map = {'Scourge Support':0,
                            'Harbinger':1,
                            'Willbender':2,
                            'Heal FB':3,
                            'Vindicator':4,
                            'Untamed':5,
                            'Specter':6}
        
        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 0, 0)
        mainLayout.addWidget(self.topRightGroupBox, 0, 1)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setColumnStretch(0, 1)
        self.setLayout(mainLayout)

    def update_class(self, item, value=None):
        logging.info('ITEM:'+item+' VALUE:'+value)
        class_dict = {item: value}
        config_helper.save_config(class_dict)

    def passCurrentText(self):
        self.update_class('class', self.classComboBox.currentText())

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("SELECT")

        self.classComboBox = QComboBox()
        self.classComboBox.addItems(self.class_map)
        
        cfg = config_helper.read_config()
        class_name = 'None'
        for key in self.class_map:
            if key == cfg['class']:
                class_name = key
                break

        self.classComboBox.setCurrentText(class_name)
        self.classComboBox.activated.connect(self.passCurrentText)

        styleLabel = QLabel("&Class:")
        styleLabel.setBuddy(self.classComboBox)
        layout = QVBoxLayout()
        layout.addWidget(styleLabel)
        layout.addWidget(self.classComboBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("START")

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
        self.topRightGroupBox.setLayout(layout)

    def on_press(self, key): 
        if key == 'end':
            logging.info('Exit key pressed')
            self.run = False
            exit()
        elif key == 'del':
            logging.info('Pause key pressed')
            little_helper.lilHelp.set_pause(not little_helper.lilHelp.should_pause())

    def engine_run(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        logging.info('Little Helper started')
        self.run = True
        while self.run == True:
            little_helper.run()

    def debug_run(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        logging.debug('Debug Helper started')
        self.run = True
        while self.run == True:
            little_helper.debug()


def main():
    #try:
    app = QApplication(argv)
    gui = GUI()
    gui.show()
    logging.info(('========== %s %s ==========') % ("Little Helper", "v0.7.1"))
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

