import logging
import keyboard
import threading
import inspect
import types
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit, QComboBox, QDialog, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory, QVBoxLayout, QWidget)

from helper import config_helper, logging_helper
from engine import toolbox_gui, combat_rotation


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.run =  False
        self.cfg = config_helper.read_config()
        self._lock = threading.Lock()
        self.pause_req = False

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
        keyboard.add_hotkey('del', lambda: self.on_press('del'))

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
        self.update_class('method', self.ComboBox.currentText())

    def get_local_methods(self, clss):
        result = []
        for var in clss.__dict__:
            val = clss.__dict__[var]
            if inspect.isfunction(val):
                if var == '__init__' or var == 'set_pause' or var == 'press_combo' or var == 'press_key' or var == 'get_color' or var == 'get_image' or var == 'mouse_click':
                    pass
                else:
                    result = QStandardItem(var)
                    self.model.appendRow(result)
        self.ComboBox.setCurrentIndex(0)
    
    def call_method(self, o, name):
        return getattr(o, name)()

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
        
        cr = combat_rotation.CombatRotation
        self.get_local_methods(cr)
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
        toggleStartButton.clicked.connect(self.prepare_combat_rotation)
        
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
            
    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req

    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()

    def on_press(self, key): 
        if key == 'end':
            logging.info('Exit key pressed')
            self.run = False
        elif key == 'del':
            logging.info('Pause key pressed')
            self.set_pause(not self.should_pause())

    def prepare_combat_rotation(self):
        running = threading.Event()
        running.set()
        thread = threading.Thread(target=self.get_combat_rotation, args=(running,))
        thread.start()
        logging.info('LittleHelper started')
        if(self.run == False):
            running.clear()
            thread.join()
            logging.info("LittleHelper stopped")

    def get_combat_rotation(self, *args):
        """set up the skill rotation for a specific method injected by the config"""
        method = self.cfg['method']
        cr = combat_rotation.CombatRotation()
        self.run = True
        while self.run == True:
            while self.should_pause():
                pass
            self.call_method(cr, method)

    def toolbox_run(self):
        self.toolbox = toolbox_gui.ToolBoxGUI()
        logging.info('ToolBox started')
        self.toolbox.show()

