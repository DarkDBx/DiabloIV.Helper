import os
import logging
import keyboard
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit, QComboBox, QDialog, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory, QVBoxLayout, QWidget)

from helper import config_helper, logging_helper
from engine import littlehelper, toolbox_gui


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.run =  False
        self.setGeometry(150, 150, 500, 250)
        self.setWindowTitle("LittleHelper")
        self.setFixedSize(500, 250)
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.label = QLabel(self)
        self.pixmap = QPixmap('.\\assets\\layout\\lilhelperbp.png') 
        self.label.setPixmap(self.pixmap) 
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        
        keyboard.add_hotkey('end', lambda: self.on_press('end'))
        keyboard.add_hotkey('q', lambda: self.on_press('q'))

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createLoggerConsole()
        self.loggerConsole.setDisabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 0, 0)
        mainLayout.addWidget(self.topRightGroupBox, 0, 1)
        mainLayout.addWidget(self.loggerConsole, 1, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def update_class(self, item, value=None):
        logging.info('Preset '+item+': '+value)
        config_helper.save_config(item, value)

    def passCurrentText(self):
        self.update_class('file', self.ComboBox.currentText())

    def check_folder(self):
        lt = []
        for p in os.listdir('src'):
            if p == 'main.py':
                pass
            elif p[-2:] == 'py':
                lt = QStandardItem(p)
                self.model.appendRow(lt)
        self.ComboBox.setCurrentIndex(0)

    # dropdown menu
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox()
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.ComboBox = QComboBox()
        self.ComboBox.setModel(self.model)
        styleLabelGame = QLabel("&Combat Rotation:")
        styleLabelGame.setStyleSheet("color: #ffd343")
        styleLabelGame.setBuddy(self.ComboBox)
        
        self.check_folder()
        self.ComboBox.activated.connect(self.passCurrentText)

        layout.addWidget(styleLabelGame)
        layout.addWidget(self.ComboBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    # buttons
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()
        layout = QVBoxLayout()

        toggleStartButton = QPushButton("LittleHelper")
        toggleStartButton.setCheckable(False)
        toggleStartButton.setChecked(False)
        toggleStartButton.clicked.connect(self.engine_run)
        
        toggleToolBoxButton = QPushButton("ToolBox")
        toggleToolBoxButton.setCheckable(False)
        toggleToolBoxButton.setChecked(False)
        toggleToolBoxButton.clicked.connect(self.toolbox_run)

        layout.addWidget(toggleStartButton)
        layout.addWidget(toggleToolBoxButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    # logger console
    def createLoggerConsole(self):
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        handler = logging_helper.Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setReadOnly(True)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        # connect QPlainTextEdit.appendPlainText slot
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def on_press(self, key): 
        if key == 'end':
            logging.info('Exit key pressed')
            self.run = False
        elif key == 'q':
            logging.info('Pause key pressed')
            littlehelper.lilHelp.set_pause(not littlehelper.lilHelp.should_pause())

    def engine_run(self):
        #process_helper.set_foreground_window()
        #process_helper.set_window_pos()
        logging.info('LittleHelper started')
        self.run = True
        while self.run == True:
            littlehelper.run_bot()

    def toolbox_run(self):
        self.toolbox = toolbox_gui.ToolBoxGUI()
        #process_helper.set_foreground_window()
        #process_helper.set_window_pos()
        logging.info('ToolBox started')
        self.toolbox.show()

