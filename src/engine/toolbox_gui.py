import os
import logging
import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import (QApplication, QPlainTextEdit, QLineEdit, QComboBox, QDialog,
        QGridLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory, QWidget)

from helper import logging_helper, recorder_helper, image_helper


class ToolBoxGUI(QDialog):
    def __init__(self, parent=None):
        super(ToolBoxGUI, self).__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(150, 150, 500, 350)
        self.setWindowTitle("LittleHelper - ToolBox")
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon('.\\assets\\layout\\lilhelper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.label = QLabel(self)
        self.pixmap = QPixmap('.\\assets\\layout\\lilhelperbp.png') 
        self.label.setPixmap(self.pixmap) 
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        
        keyboard.add_hotkey('insert', lambda: self.on_press('insert'))
        keyboard.add_hotkey('home', lambda: self.on_press('home'))
        
        self.image_name = 'default'
        self.image_path = '.\\assets\\skills\\'
        self.x_coord = 25
        self.y_coord = 25
        self.file_name = 'default'
        self.file_name_replay = 'default.txt'
        self.recording = []
        self.started = False
        self.record = recorder_helper.Record()
        
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

    # prepare recordBox
    def set_file_name(self):
        self.file_name = str(self.saveTextBox.text())

    # prepare replayBox
    def set_file_name_replay(self, index):
        self.file_name_replay = str(self.replayComboBox.itemText(index))

    def check_folder(self):
        lt = []
        for p in os.listdir("record"):
            if p[-4:] == ".txt":
                lt = QStandardItem(p)
                self.model.appendRow(lt)
        self.replayComboBox.setCurrentIndex(0)

    def save_as(self):
        if len(self.recording) != 0:
            if os.path.exists(".\\record\\" + self.file_name + ".txt"):
                logging.error("Filename already taken")
            else:
                f = open(".\\record\\" + self.file_name + ".txt", "x")
                f.write(str(self.recording))
                self.check_folder()
                logging.info("File saved as: {0}".format(self.file_name + ".txt"))
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
            logging.info("Replaying...")
            recorder_helper.Replay(".\\record\\" + self.file_name_replay)
        except SyntaxError:
            logging.error("Wrong file")
        except FileNotFoundError:
            logging.error("File not found")

    # imageCrop
    def createImageCrop(self):
        self.imageCrop = QGroupBox('Image Crop')
        self.imageCrop.setStyleSheet('QGroupBox:title {color: rgb(255,211,67);}')
        layout = QHBoxLayout()

        self.text_box1 = QLineEdit(str(self.image_name))
        self.text_box1.setFixedSize(80, 20)
        self.text_box1.textChanged.connect(self.set_image_name)

        self.text_box2 = QLineEdit(str(self.image_path))
        self.text_box2.setFixedSize(240, 20)
        self.text_box2.textChanged.connect(self.set_image_path)

        self.text_box3 = QLineEdit(str(self.x_coord))
        self.text_box3.setFixedSize(25, 20)
        self.text_box3.setValidator(QIntValidator())
        self.text_box3.setMaxLength(2)
        self.text_box3.textChanged.connect(self.set_x_coord)

        self.text_box4 = QLineEdit(str(self.y_coord))
        self.text_box4.setFixedSize(25, 20)
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
        self.recordBox = QGroupBox('Recorder')
        self.recordBox.setStyleSheet('QGroupBox:title {color: rgb(255,211,67);}')
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

    # replayBox
    def createReplayBox(self):
        self.replayBox = QGroupBox('Player')
        self.replayBox.setStyleSheet('QGroupBox:title {color: rgb(255,211,67);}')
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

        handler = logging_helper.Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setReadOnly(True)
        logging.getLogger().addHandler(handler)
        #logging.getLogger().setLevel(logging.INFO)
        # connect QPlainTextEdit.appendPlainText slot
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def on_press(self, key): 
        if key == 'home':
            self.get_color_from_pos()
        elif key == 'insert':
            self.get_image_from_pos()
            
    def get_color_from_pos(self):
        """debug function, print coordinates and rgb color at mouse position"""
        x,y, r,g,b = image_helper.get_pixel_color_at_cursor()
        logging.info("Position and color: x,y, r,g,b=%d,%d, %d,%d,%d" % (x,y, r,g,b))

    def get_image_from_pos(self, name, path, ix, iy):
        """debug function, print coordinates and save image at mouse position"""
        if os.path.exists(self.image_path + self.image_name + ".png"):
            logging.error("Filename already taken")
        else:
            x,y = image_helper.get_image_at_cursor(name, path, ix, iy)
            logging.info("File saved as: %s location: %s position: x=%d, y=%d, size=%d, %d" % (str(name+'.png'),path,x,y,ix,iy))
            pixmap = QPixmap(self.image_path+self.image_name)
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.resize(pixmap.width(), pixmap.height())

