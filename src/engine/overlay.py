import logging
import keyboard
import threading
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QComboBox, QPlainTextEdit, QMainWindow, QGridLayout,
                             QGroupBox, QPushButton, QHBoxLayout, QLabel, QStyleFactory, QWidget)

from helper import config_helper, logging_helper
from engine import bot, combat, toolbox


class Overlay(QMainWindow):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("LittleHelper")
        self.setGeometry(720, 50, 470, 170)
        self.setFixedSize(470, 170)
        visible_window = QWidget(self)
        visible_window.setFixedSize(470, 170)
        
        keyboard.add_hotkey('end', lambda: self.on_press('end'))
        keyboard.add_hotkey('del', lambda: self.on_press('del'))
        
        self.running = False
        self.pause = False
        self._lock = threading.Lock()
        self.pause_req = False
        self.cfg = config_helper.read_config()
        self.robot = bot.Bot()

        self.createDropdownBox()
        self.createStartBox()
        self.createToolBox()
        self.createLoggerConsole()
        self.loggerConsole.setDisabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.dropdownBox, 0, 0)
        mainLayout.addWidget(self.startBox, 0, 1)
        mainLayout.addWidget(self.toolBox, 0, 2)
        mainLayout.addWidget(self.loggerConsole, 1, 0, 1, 3)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setCentralWidget(visible_window)
        visible_window.setLayout(mainLayout)


    # prepare dropdownBox
    def update_class(self, item, value=None):
        logging.info('Preset '+item+': '+value)
        config_helper.save_config(item, value)


    def passCurrentText(self):
        self.update_class('class', self.ComboBox.currentText())
            

    def get_class(self):
        result = []
        class_array = ['Druid', 'Barb', 'Necro', 'Sorc', 'Rogue']
        for class_var in class_array:
            result = QStandardItem(class_var)
            self.model.appendRow(result)
        self.ComboBox.setCurrentIndex(0)


    # loggerConsole
    def createLoggerConsole(self):
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        handler = logging_helper.Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setStyleSheet('background:rgb(204,153,51);')
        log_text_box.setReadOnly(True)
        logging.getLogger().addHandler(handler)
        #logging.getLogger().setLevel(logging.DEBUG)
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)
        
    
    def closeEvent(self, event):
        root_logger = logging.getLogger()
        handler = logging_helper.Handler(self)
        root_logger.removeHandler(handler)
        super().closeEvent(event)


    # dropdownBox
    def createDropdownBox(self):
        self.dropdownBox = QGroupBox()
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.ComboBox = QComboBox()
        self.ComboBox.setModel(self.model)
        
        self.get_class()
        self.ComboBox.activated.connect(self.passCurrentText)

        layout.addWidget(self.ComboBox)
        layout.addStretch(1)
        self.dropdownBox.setLayout(layout)


    # startBox
    def createStartBox(self):
        self.startBox = QGroupBox()
        layout = QHBoxLayout()

        toggleStartButton = QPushButton("ROBOT")
        toggleStartButton.setCheckable(False)
        toggleStartButton.setChecked(False)
        toggleStartButton.clicked.connect(self.combat_rotation_thread)

        toggleAssistButton = QPushButton("ASSISTANT")
        toggleAssistButton.setCheckable(False)
        toggleAssistButton.setChecked(False)
        toggleAssistButton.clicked.connect(self.assist_rotation_thread)

        layout.addStretch(1)
        layout.addWidget(toggleStartButton)
        layout.addStretch(1)
        layout.addWidget(toggleAssistButton)
        layout.addStretch(1)
        self.startBox.setLayout(layout)


    # toolBox
    def createToolBox(self):
        self.toolBox = QGroupBox()
        layout = QHBoxLayout()

        toggleToolButton = QPushButton("TOOLBOX")
        toggleToolButton.setCheckable(False)
        toggleToolButton.setChecked(False)
        toggleToolButton.clicked.connect(self.littlehelper_toolbox)

        layout.addStretch(1)
        layout.addWidget(toggleToolButton)
        layout.addStretch(1)
        self.toolBox.setLayout(layout)


    def on_press(self, key): 
        if key == 'end':
            logging.info('_EXIT')
            self.rotation_thread.join()
            self.closeEvent()
            self.running = False
            return self.running
        elif key == 'del':
            self.set_pause(not self.should_pause())
            if self.pause == False:
                self.pause = True
                logging.info('_PAUSE')
            else:
                self.pause = False
                logging.info('_RUN')
            

    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req


    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()


    def combat_rotation_thread(self):
        self.rotation_thread = threading.Thread(target=self.get_combat_rotation)
        self.rotation_thread.start()


    def assist_rotation_thread(self):
        self.rotation_thread = threading.Thread(target=self.get_assist_rotation)
        self.rotation_thread.start()


    def get_combat_rotation(self):
        logging.info('LittleHelper robot started')

        self.robot.set_foreground()
        self.running = True
        while self.running:
            while self.should_pause():
                time.sleep(0.25)
            self.robot.game_manager()

        logging.info("LittleHelper robot stopped")


    def get_assist_rotation(self):
        logging.info('LittleHelper assistant started')

        self.robot.set_foreground()
        self.running = True
        while self.running:
            while self.should_pause():
                time.sleep(0.25)
            combat.rotation()

        logging.info("LittleHelper assistant stopped")


    def littlehelper_toolbox(self):
        app_toolbox = toolbox.Toolbox()
        app_toolbox.show()

