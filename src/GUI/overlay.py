from keyboard import add_hotkey
from threading import Thread, Lock
from time import sleep
from sys import exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QComboBox, QPlainTextEdit, QMainWindow, QGridLayout,
                             QGroupBox, QPushButton, QHBoxLayout, QStyleFactory, QWidget)

from helper import config_helper, logging_helper, process_helper
from bot import manager, rotation
from GUI import toolbox

class Overlay(QMainWindow):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.running = False
        self._lock = Lock()
        self.pause_req = False
        self.cfg = config_helper.read_config()
        self.name = self.cfg.get('apptitle', 'Overlay')
        self.proc = process_helper.ProcessHelper()
        self.robot = manager.Manager()

        # Window setup
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('./assets/layout/mmorpg_helper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle(self.name)
        self.setGeometry(1425, 825, 470, 170)
        self.setFixedSize(470, 170)
        visible_window = QWidget(self)
        visible_window.setFixedSize(470, 170)

        # Hotkey setup
        add_hotkey('end', lambda: self.on_press('exit'))
        add_hotkey('del', lambda: self.on_press('pause'))
        add_hotkey('capslock', lambda: self.on_press('pause'))

        # UI setup
        self.createDropdownBox()
        self.createStartBox()
        self.createToolBox()
        self.createLoggerConsole()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.dropdownBox, 0, 0)
        mainLayout.addWidget(self.startBox, 0, 1)
        mainLayout.addWidget(self.toolBox, 0, 2)
        mainLayout.addWidget(self.loggerConsole, 1, 0, 1, 3)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setCentralWidget(visible_window)
        visible_window.setLayout(mainLayout)

    # Dropdown box
    def update_class(self, item, value=None):
        logging_helper.log_info(f'Preset {item}: {value}')
        config_helper.save_config(item, value)

    def passCurrentText(self):
        self.update_class('class', self.ComboBox.currentText())

    def get_class(self):
        class_array = ['Druid', 'Spiritborn', 'Barbarian', 'Necromancer', 'Sorceress', 'Rogue']
        for class_var in class_array:
            item = QStandardItem(class_var)
            self.model.appendRow(item)
        self.ComboBox.setCurrentIndex(0)

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

    # Logger console
    def createLoggerConsole(self):
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        handler = logging_helper.LogHandler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setStyleSheet('background-color: rgba(255,255,255, 0); color: white')
        log_text_box.setReadOnly(True)

        logging_helper.logger.addHandler(handler)
        handler.new_record.connect(log_text_box.appendPlainText)

        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def closeEvent(self, event):
        root_logger = logging_helper.logger
        handler = logging_helper.LogHandler(self)
        root_logger.removeHandler(handler)
        exit(0)

    # Start box
    def createStartBox(self):
        self.startBox = QGroupBox()
        layout = QHBoxLayout()

        toggleStartButton = QPushButton("BOT")
        toggleStartButton.clicked.connect(lambda: self.get_rotation_thread(True))

        toggleAssistButton = QPushButton("ASSISTANT")
        toggleAssistButton.clicked.connect(lambda: self.get_rotation_thread(False))

        layout.addStretch(1)
        layout.addWidget(toggleStartButton)
        layout.addStretch(1)
        layout.addWidget(toggleAssistButton)
        layout.addStretch(1)
        self.startBox.setLayout(layout)

    # Tool box
    def createToolBox(self):
        self.toolBox = QGroupBox()
        layout = QHBoxLayout()

        toggleToolButton = QPushButton("TOOLBOX")
        toggleToolButton.clicked.connect(self.littlehelper_toolbox)

        layout.addStretch(1)
        layout.addWidget(toggleToolButton)
        layout.addStretch(1)
        self.toolBox.setLayout(layout)

    # Hotkey actions
    def on_press(self, key):
        if key == 'exit':
            logging_helper.log_info('_EXIT')
            if self.running:
                self.running = False
                self.rotation_thread.join()
        elif key == 'pause':
            self.set_pause(not self.should_pause())
            if self.pause_req:
                logging_helper.log_info('_PAUSE')
            else:
                logging_helper.log_info('_RUN')

    # Thread-safe pause handling
    def should_pause(self):
        with self._lock:
            return self.pause_req

    def set_pause(self, pause):
        with self._lock:
            self.pause_req = pause

    # Rotation thread handling
    def get_rotation_thread(self, bot_state):
        if not hasattr(self, 'rotation_thread') or not self.rotation_thread.is_alive():
            self.rotation_thread = Thread(target=lambda: self.get_rotation(bot_state))
            self.rotation_thread.start()

    def get_rotation(self, bot_state):
        logging_helper.log_info('LittleHelper started')
        self.proc.set_foreground_window()
        self.running = True

        while self.running:
            while self.should_pause():
                sleep(0.25)
            if bot_state:
                self.robot.game_manager()
            else:
                rotation.rotation()

        logging_helper.log_info("LittleHelper stopped")

    def littlehelper_toolbox(self):
        app_toolbox = toolbox.Toolbox()
        app_toolbox.show()
