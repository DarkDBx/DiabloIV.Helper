from sys import exit
import os
from time import sleep
import logging
import keyboard
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QIntValidator, QImage
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit, QLineEdit, QComboBox, QDialog, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory, QVBoxLayout, QWidget)

from helper import little_helper, config_helper, process_helper
from engine import macro_recorder


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

        self.game_map = {'None': ['=== Choose Game ==='],
                        'Guild Wars 2': ['Vindicator PvP', 'Soulbeast PvP'],
                        'Elder Scrolls Online': ['Nightblade PvE', 'Nightblade PvP'],
                        'Path of Exile': ['Ranger', 'Marauder']}
        
        self.originalPalette = QApplication.palette()

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
        logging.info('ITEM:'+item+' VALUE:'+value)
        config_helper.save_config(item, value)

    def passCurrentTextGame(self):
        self.update_class('game', self.gameComboBox.currentText())

    def passCurrentTextClass(self):
        self.update_class('class', self.classComboBox.currentText())

    @pyqtSlot(int)
    def updateGameCombo(self, index_arg):
        index_argument = self.model.index(index_arg, 0, self.gameComboBox.rootModelIndex())
        self.classComboBox.setRootModelIndex(index_argument)
        self.classComboBox.setCurrentIndex(index_arg)

    # dropdown menu
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

        handler = Handler(self)
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
            little_helper.lilHelp.set_pause(not little_helper.lilHelp.should_pause())

    def engine_run(self):
        process_helper.set_foreground_window()
        process_helper.set_window_pos()
        logging.info('LittleHelper started')
        self.run = True
        while self.run == True:
            little_helper.run_bot()

    def toolbox_run(self):
        #process_helper.set_foreground_window()
        #process_helper.set_window_pos()
        logging.info('ToolBox started')
        toolBoxGui = ToolBoxGUI()
        toolBoxGui.show()


class ToolBoxGUI(QDialog):
    def __init__(self, parent=None):
        super(ToolBoxGUI, self).__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(150, 150, 500, 450)
        self.setWindowTitle("LittleHelper - ToolBox")
        self.setFixedSize(500, 450)
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
        self.file_name = 'default'
        self.file_name_replay = 'default.txt'
        self.recording = []
        self.started = False
        self.record = macro_recorder.Record()
        keyboard.add_hotkey('home', lambda: self.on_press('home'))
        keyboard.add_hotkey('insert', lambda: self.on_press('insert'))
        
        self.originalPalette = QApplication.palette()
        self.createImageCrop()
        self.createRecordBox()
        self.createReplayBox()
        self.createLoggerConsole()
        self.loggerConsole.setDisabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.imageCrop, 0, 0, 1, 2)
        mainLayout.addWidget(self.recordBox, 1, 0, 1, 2)
        mainLayout.addWidget(self.replayBox, 2, 0, 1, 2)
        mainLayout.addWidget(self.loggerConsole, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    # prepare imageCrop
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

    def set_file_name(self):
        self.file_name = str(self.saveTextBox.text())

    def set_file_name_replay(self, index):
        self.file_name_replay = str(self.replayComboBox.itemText(index))

    # prepare recordBox
    def check_folder(self):
        lt = []
        for p in os.listdir("saved"):
            if p[-3:] == "txt":
                lt = QStandardItem(p)
                self.model.appendRow(lt)
        self.replayComboBox.setCurrentIndex(0)

    def save_as(self):
        if len(self.recording) != 0:
            if os.path.exists(".\\saved\\" + self.file_name + ".txt"):
                logging.error("Filename already taken")
            else:
                f = open(".\\saved\\" + self.file_name + ".txt", "x")
                f.write(str(self.recording))
                self.check_folder()
                logging.info("Saved as: {0}".format(self.file_name + ".txt"))
        else:
            logging.error("Nothing recorded yet")

    def start(self):
        self.record.record_start()
        logging.info("Recording...")
        self.started = True

    def stop(self):
        if self.started:
            self.recording = self.record.record_stop()
            logging.info("Recording stopped")
            self.started = False
        else:
            logging.error("Nothing to stop")

    def replay(self):
        try:
            print(self.file_name_replay)
            r = macro_recorder.Replay(".\\saved\\" + self.file_name_replay)
            r.start()
            logging.info("Replaying...")
        except SyntaxError:
            logging.error("Wrong file")
        except FileNotFoundError:
            logging.error("File not found")

    # imageCrop
    def createImageCrop(self):
        self.imageCrop = QGroupBox()
        layout = QHBoxLayout()

        self.text_box1 = QLineEdit()
        self.text_box1.setFixedSize(80, 20)
        self.text_box1.setPlaceholderText(str(self.image_name))
        self.text_box1.textChanged.connect(self.set_image_name)

        self.text_box2 = QLineEdit(str(self.image_path))
        self.text_box2.setFixedSize(240, 20)
        self.text_box2.textChanged.connect(self.set_image_path)

        self.text_box3 = QLineEdit()
        self.text_box3.setFixedSize(25, 20)
        self.text_box3.setPlaceholderText(str(self.x_coord))
        self.text_box3.setValidator(QIntValidator())
        self.text_box3.setMaxLength(2)
        self.text_box3.textChanged.connect(self.set_x_coord)

        self.text_box4 = QLineEdit()
        self.text_box4.setFixedSize(25, 20)
        self.text_box4.setPlaceholderText(str(self.y_coord))
        self.text_box4.setValidator(QIntValidator())
        self.text_box4.setMaxLength(2)
        self.text_box4.textChanged.connect(self.set_y_coord)
        
        self.imageLabel = QLabel(self)
        pixmap = QPixmap(self.image_path+self.image_name)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())
        
        layout.addWidget(self.text_box1)
        layout.addWidget(self.text_box2)
        layout.addWidget(self.text_box3)
        layout.addWidget(self.text_box4)
        layout.addWidget(self.imageLabel)
        self.imageCrop.setLayout(layout)

    # recordBox
    def createRecordBox(self):
        self.recordBox = QGroupBox()
        layout = QHBoxLayout()

        toggleStartButton = QPushButton("Start")
        toggleStartButton.setCheckable(False)
        toggleStartButton.setChecked(False)
        toggleStartButton.clicked.connect(self.start)

        toggleStopButton = QPushButton("Stop")
        toggleStopButton.setCheckable(False)
        toggleStopButton.setChecked(False)
        toggleStopButton.clicked.connect(self.stop)

        self.saveTextBox = QLineEdit(str(self.file_name))
        self.saveTextBox.setFixedSize(80, 20)
        self.saveTextBox.textChanged.connect(self.set_file_name)
        
        toggleSaveButton = QPushButton("Save as")
        toggleSaveButton.setCheckable(False)
        toggleSaveButton.setChecked(False)
        toggleSaveButton.clicked.connect(self.save_as)

        layout.addWidget(toggleStartButton)
        layout.addWidget(toggleStopButton)
        layout.addWidget(self.saveTextBox)
        layout.addWidget(toggleSaveButton)
        layout.addStretch(1)
        self.recordBox.setLayout(layout)

    # recordBox
    def createReplayBox(self):
        self.replayBox = QGroupBox()
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.replayComboBox = QComboBox()
        self.replayComboBox.setModel(self.model)
        self.check_folder()
        self.replayComboBox.activated.connect(self.set_file_name_replay)

        toggleReplayButton = QPushButton("Replay")
        toggleReplayButton.setCheckable(False)
        toggleReplayButton.setChecked(False)
        toggleReplayButton.clicked.connect(self.replay)
        
        layout.addWidget(self.replayComboBox)
        layout.addWidget(toggleReplayButton)
        layout.addStretch(1)
        self.replayBox.setLayout(layout)

    # logger console
    def createLoggerConsole(self):
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        handler = Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setReadOnly(True)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        # connect QPlainTextEdit.appendPlainText slot
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def on_press(self, key): 
        if key == 'home':
            self.toolbox_print()
        elif key == 'insert':
            self.toolbox_save()

    def toolbox_print(self):
        #process_helper.set_foreground_window()
        #process_helper.set_window_pos()
        little_helper.toolbox_print_pos()

    def toolbox_save(self):
        #process_helper.set_foreground_window()
        #process_helper.set_window_pos()
        little_helper.toolbox_save_img(name=self.image_name, path=self.image_path, ix=self.x_coord, iy=self.y_coord)
        pixmap = QPixmap(self.image_path+self.image_name)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

