from sys import exit
from time import sleep
import logging
import keyboard
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit, QLineEdit, QComboBox, QDialog, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory, QVBoxLayout, QWidget)

from helper import little_helper, config_helper, process_helper


class Handler(QObject, logging.Handler):
    new_record = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        super(logging.Handler).__init__()
        formatter = Formatter('[%(levelname)s] %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        # emit signal
        self.new_record.emit(msg)


class Formatter(logging.Formatter):
    def formatException(self, ei):
        result = super(Formatter, self).formatException(ei)
        return result

    def format(self, record):
        s = super(Formatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '')
        return s


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setGeometry(150, 150, 600, 400)
        self.setWindowTitle("LittleHelper")
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.label = QLabel(self)
        self.pixmap = QPixmap('.\\assets\\layout\\lilhelperbp.png') 
        self.label.setPixmap(self.pixmap) 
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        
        self.image_name = 'default.png'
        self.image_path = '.\\assets\\'
        self.x_coord = 30
        self.y_coord = 30

        keyboard.add_hotkey('end', lambda: self.on_press('end'))
        keyboard.add_hotkey('del', lambda: self.on_press('del'))
        keyboard.add_hotkey('home', lambda: self.on_press('home'))
        keyboard.add_hotkey('insert', lambda: self.on_press('insert'))
        logging.basicConfig(level=logging.DEBUG)
        self.run =  False
        self.game_map = {'Guild Wars 2': ['Harbinger PvP', 'Willbender PvP', 'Vindicator PvP', 'Soulbeast PvP'],
                            'Elderscrolls Online': ['Nightblade']}
        
        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createImageCrop()
        self.createLoggerConsole()

        self.loggerConsole.setDisabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 0, 0)
        mainLayout.addWidget(self.topRightGroupBox, 0, 1)
        mainLayout.addWidget(self.imageCrop, 1, 0, 1, 2)
        mainLayout.addWidget(self.loggerConsole, 2, 0, 1, 2)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def update_class(self, item, value=None):
        logging.info('ITEM:'+item+' VALUE:'+value)
        config_helper.save_config(item, value)

    def passCurrentTextGame(self):
        self.update_class('game', self.gameComboBox.currentText())

    def passCurrentTextClass(self):
        self.update_class('class', self.classComboBox.currentText())

    def updateGameCombo(self, index_arg):
        index_argument = self.model.index(index_arg, 0, self.gameComboBox.rootModelIndex())
        self.classComboBox.setRootModelIndex(index_argument)
        self.classComboBox.setCurrentIndex(0)

    def set_image_name(self):
        self.image_name = str(self.text_box1.text())
        self.text_box1.setText(str(self.image_name))

    def set_image_path(self):
        self.image_path = str(self.text_box2.text())
        self.text_box2.setText(str(self.image_path))

    def set_x_coord(self):
        self.x_coord = int(self.text_box3.text())
        self.text_box3.setText(str(self.x_coord))

    def set_y_coord(self):
        self.y_coord = int(self.text_box4.text())
        self.text_box4.setText(str(self.y_coord))

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox()
        layout = QHBoxLayout()
        self.model = QStandardItemModel()
        self.gameComboBox = QComboBox()
        self.gameComboBox.setModel(self.model)
        self.classComboBox = QComboBox()
        self.classComboBox.setModel(self.model)
        styleLabelGame = QLabel("&Game:")
        styleLabelGame.setBuddy(self.gameComboBox)
        styleLabelClass = QLabel("&Class:")
        styleLabelClass.setBuddy(self.classComboBox)

        #TODO: get last status from config
        #cfg = config_helper.read_config()

        for k, v in self.game_map.items():
            game_name = QStandardItem(k)
            self.model.appendRow(game_name)
            for value in v:
                class_name = QStandardItem(value)
                game_name.appendRow(class_name)

        self.gameComboBox.currentIndexChanged.connect(self.updateGameCombo)
        self.updateGameCombo(0)

        self.gameComboBox.activated.connect(self.passCurrentTextGame)
        self.classComboBox.activated.connect(self.passCurrentTextClass)

        layout.addWidget(styleLabelGame)
        layout.addWidget(self.gameComboBox)
        layout.addWidget(styleLabelClass)
        layout.addWidget(self.classComboBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()
        toggleStartButton = QPushButton("LittleHelper")
        toggleStartButton.setCheckable(True)
        toggleStartButton.setChecked(False)
        toggleStartButton.clicked.connect(self.engine_run)

        layout = QVBoxLayout()
        layout.addWidget(toggleStartButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createImageCrop(self):
        self.imageCrop = QGroupBox()
        layout = QHBoxLayout()

        self.text_box1 = QLineEdit()
        self.text_box1.setPlaceholderText(str(self.image_name))
        self.text_box1.textChanged.connect(self.set_image_name)
        self.text_box2 = QLineEdit(str(self.image_path))
        self.text_box2.textChanged.connect(self.set_image_path)
        self.text_box3 = QLineEdit()
        self.text_box3.setPlaceholderText(str(self.x_coord))
        self.text_box3.setValidator(QIntValidator())
        self.text_box3.setMaxLength(2)
        self.text_box3.textChanged.connect(self.set_x_coord)
        self.text_box4 = QLineEdit()
        self.text_box4.setPlaceholderText(str(self.y_coord))
        self.text_box4.setValidator(QIntValidator())
        self.text_box4.setMaxLength(2)
        self.text_box4.textChanged.connect(self.set_y_coord)
        
        layout.addWidget(self.text_box1)
        layout.addWidget(self.text_box2)
        layout.addWidget(self.text_box3)
        layout.addWidget(self.text_box4)
        self.imageCrop.setLayout(layout)

    def createLoggerConsole(self):
        self.loggerConsole = QWidget()

        handler = Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setReadOnly(True)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        # connect QPlainTextEdit.appendPlainText slot
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout = QHBoxLayout()
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def on_press(self, key): 
        if key == 'end':
            logging.info('Exit key pressed')
            self.run = False
            exit()
        elif key == 'del':
            logging.info('Pause key pressed')
            little_helper.lilHelp.set_pause(not little_helper.lilHelp.should_pause())
        elif key == 'home':
            self.toolbox_print()
        elif key == 'insert':
            self.toolbox_save()

    def engine_run(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        logging.info('LittleHelper started')
        self.run = True
        while self.run == True:
            little_helper.run_bot()

    def toolbox_print(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        sleep(0.5)
        little_helper.toolbox_print_pos()

    def toolbox_save(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        little_helper.toolbox_save_img(name=self.image_name, path=self.image_path, ix=self.x_coord, iy=self.y_coord)

