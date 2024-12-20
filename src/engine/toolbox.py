from os import listdir, path
from threading import Thread
from keyboard import add_hotkey
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                              QGroupBox, QHBoxLayout, QLabel, QPushButton, QStyleFactory)

from helper import recorder_helper, image_helper, config_helper, logging_helper

class Toolbox(QDialog):
    def __init__(self, parent=None):
        super(Toolbox, self).__init__(parent)
        self.running = False
        self.image_name = 'default'
        self.image_path = '.\\assets\\skills\\'
        self.abs_x_coord = 0
        self.abs_y_coord = 0
        self.x_coord = 10
        self.y_coord = 10
        self.file_name = 'default'
        self.file_name_replay = 'default.txt'
        self.recording = []
        self.started = False
        self.replay_thread = None
        self.record = recorder_helper.Record()
        self.cfg = config_helper.read_config()
        self.name = self.cfg.get('apptitle', 'MMORPG Helper')

        try:
            self.setWindowIcon(QIcon('.\\assets\\layout\\mmorpg_helper.ico'))
            self.pixmap = QPixmap('.\\assets\\layout\\mmorpg_helper_background.png')
        except Exception as e:
            logging_helper.log_error(f"Error loading resources: {e}")
            self.pixmap = QPixmap()

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle(self.name)
        self.setGeometry(700, 300, 600, 250)
        self.setFixedSize(600, 250)

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        add_hotkey('F12', lambda: self.on_press('image'))
        add_hotkey('F11', lambda: self.on_press('coords'))
        add_hotkey('F10', lambda: self.on_press('color'))
        add_hotkey('end', lambda: self.on_press('exit'))

        self.createImageCrop()
        self.createRecordBox()
        self.createReplayBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.imageCrop, 0, 0, 1, 2)
        mainLayout.addWidget(self.recordBox, 1, 0, 1, 2)
        mainLayout.addWidget(self.replayBox, 2, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def set_image_name(self):
        self.image_name = str(self.text_box1.text())
        self.text_box1.setText(str(self.image_name))

    def set_image_path(self):
        self.image_path = str(self.text_box2.text())
        self.text_box2.setText(str(self.image_path))

    def get_x_coord(self):
        self.abs_x_coord = int(self.text_box5.text())
        self.text_box5.setText(str(self.abs_x_coord))

    def get_y_coord(self):
        self.abs_y_coord = int(self.text_box6.text())
        self.text_box6.setText(str(self.abs_y_coord))

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

    def check_folder(self):
        self.model.clear()
        for p in listdir("record"):
            if p.endswith(".txt"):
                self.model.appendRow(QStandardItem(p))
        self.replayComboBox.setCurrentIndex(0)

    def save_as(self):
        if self.recording:
            file_path = f".\\record\\{self.file_name}.txt"
            if path.exists(file_path):
                logging_helper.log_error("Filename already taken")
            else:
                with open(file_path, "w") as f:
                    f.write(str(self.recording))
                self.check_folder()
                logging_helper.log_info(f"File saved as: {self.file_name}.txt")
        else:
            logging_helper.log_error("Nothing recorded yet")

    def start(self):
        self.record.prepare_record_start()
        logging_helper.log_info("Recording...")
        self.started = True

    def stop(self):
        if self.started:
            self.recording = self.record.record_stop()
            logging_helper.log_info("Recording stopped")
            self.started = False
        else:
            logging_helper.log_error("Nothing to stop")

    def replay(self):
        try:
            logging_helper.log_info("Replaying...")
            rec = recorder_helper.Replay(f".\\record\\{self.file_name_replay}")
            self.replay_thread = Thread(target=rec.replay_run, daemon=True)
            self.running = True

            self.replay_thread.start()
            self.replay_thread.join()
            logging_helper.log_info("Replay stopped")
        except FileNotFoundError as e:
            logging_helper.log_error(f"File not found: {e}")
        except SyntaxError as e:
            logging_helper.log_error(f"Syntax error in file: {e}")

    def createImageCrop(self):
        self.imageCrop = QGroupBox('Image Crop')
        self.imageCrop.setStyleSheet('QGroupBox:title {color: rgb(255,255,0);}')
        layout = QHBoxLayout()

        common_style = 'background:rgb(204,153,51);'

        self.text_box1 = QLineEdit(str(self.image_name))
        self.text_box1.setStyleSheet(common_style)
        self.text_box1.setFixedSize(80, 20)
        self.text_box1.textChanged.connect(self.set_image_name)

        self.text_box2 = QLineEdit(str(self.image_path))
        self.text_box2.setStyleSheet(common_style)
        self.text_box2.setFixedSize(240, 20)
        self.text_box2.textChanged.connect(self.set_image_path)

        self.text_box5 = QLineEdit(str(self.abs_x_coord))
        self.text_box5.setStyleSheet(common_style)
        self.text_box5.setFixedSize(30, 20)
        self.text_box5.setValidator(QIntValidator())
        self.text_box5.setMaxLength(4)
        self.text_box5.textChanged.connect(self.get_x_coord)

        self.text_box6 = QLineEdit(str(self.abs_y_coord))
        self.text_box6.setStyleSheet(common_style)
        self.text_box6.setFixedSize(30, 20)
        self.text_box6.setValidator(QIntValidator())
        self.text_box6.setMaxLength(4)
        self.text_box6.textChanged.connect(self.get_y_coord)

        self.text_box3 = QLineEdit(str(self.x_coord))
        self.text_box3.setStyleSheet(common_style)
        self.text_box3.setFixedSize(25, 20)
        self.text_box3.setValidator(QIntValidator())
        self.text_box3.setMaxLength(2)
        self.text_box3.textChanged.connect(self.set_x_coord)

        self.text_box4 = QLineEdit(str(self.y_coord))
        self.text_box4.setStyleSheet(common_style)
        self.text_box4.setFixedSize(25, 20)
        self.text_box4.setValidator(QIntValidator())
        self.text_box4.setMaxLength(2)
        self.text_box4.textChanged.connect(self.set_y_coord)

        self.imageLabel = QLabel(self)
        pixmap = QPixmap(self.image_path + self.image_name)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

        layout.addWidget(self.text_box1)
        layout.addStretch(1)
        layout.addWidget(self.text_box2)
        layout.addStretch(1)
        layout.addWidget(self.text_box5)
        layout.addStretch(1)
        layout.addWidget(self.text_box6)
        layout.addStretch(1)
        layout.addWidget(self.text_box3)
        layout.addStretch(1)
        layout.addWidget(self.text_box4)
        layout.addStretch(3)
        layout.addWidget(self.imageLabel)
        layout.addStretch(5)
        self.imageCrop.setLayout(layout)

    def createRecordBox(self):
        self.recordBox = QGroupBox('Recorder')
        self.recordBox.setStyleSheet('QGroupBox:title {color: rgb(255,255,0);}')
        layout = QHBoxLayout()

        toggleStartButton = QPushButton("Start")
        toggleStartButton.setCheckable(False)
        toggleStartButton.clicked.connect(self.start)

        toggleStopButton = QPushButton("Stop")
        toggleStopButton.setCheckable(False)
        toggleStopButton.clicked.connect(self.stop)

        self.saveTextBox = QLineEdit(str(self.file_name))
        self.saveTextBox.setStyleSheet('background:rgb(204,153,51);')
        self.saveTextBox.setFixedSize(80, 20)
        self.saveTextBox.textChanged.connect(self.set_file_name)

        toggleSaveButton = QPushButton("Save as")
        toggleSaveButton.setCheckable(False)
        toggleSaveButton.clicked.connect(self.save_as)

        layout.addWidget(toggleStartButton)
        layout.addStretch(1)
        layout.addWidget(toggleStopButton)
        layout.addStretch(7)
        layout.addWidget(self.saveTextBox)
        layout.addStretch(1)
        layout.addWidget(toggleSaveButton)
        layout.addStretch(1)
        self.recordBox.setLayout(layout)

    def createReplayBox(self):
        self.replayBox = QGroupBox('Player')
        self.replayBox.setStyleSheet('QGroupBox:title {color: rgb(255,255,0);}')
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.replayComboBox = QComboBox()
        self.replayComboBox.setModel(self.model)
        self.check_folder()
        self.replayComboBox.activated.connect(self.set_file_name_replay)

        toggleReplayButton = QPushButton("Replay")
        toggleReplayButton.setCheckable(False)
        toggleReplayButton.clicked.connect(self.replay)

        layout.addWidget(self.replayComboBox)
        layout.addStretch(1)
        layout.addWidget(toggleReplayButton)
        layout.addStretch(20)
        self.replayBox.setLayout(layout)

    def on_press(self, key):
        actions = {
            'image': self.get_image_from_pos,
            'coords': self.get_image_from_coord,
            'color': self.get_color_from_pos,
            'exit': self.exit_app
        }
        action = actions.get(key)
        if action:
            action()
        else:
            logging_helper.log_error(f"Unknown key: {key}")

    def get_color_from_pos(self):
        x, y, r, g, b = image_helper.get_pixel_color_at_cursor()
        self.text_box5.setText(str(x))
        self.text_box6.setText(str(y))
        logging_helper.log_info(f"Position and color: x,y, r,g,b={x},{y}, {r},{g},{b}")

    def get_image_from_pos(self):
        if path.exists(self.image_path + self.image_name + '.png'):
            logging_helper.log_error("Filename already taken")
        else:
            x, y = image_helper.get_image_at_cursor(self.x_coord, self.y_coord, self.image_name, self.image_path)
            logging_helper.log_info(f"File saved as: {self.image_name}.png location: {self.image_path} position: x={x}, y={y}, size={self.x_coord}, {self.y_coord}")
            self.update_image_label()

    def get_image_from_coord(self):
        if path.exists(self.image_path + self.image_name + '.png'):
            logging_helper.log_error("Filename already taken")
        else:
            x, y = image_helper.get_image_from_coordinates(self.abs_x_coord, self.abs_y_coord, self.image_name, self.image_path)
            logging_helper.log_info(f"File saved as: {self.image_name}.png location: {self.image_path} absolute coordinates: x={x}, y={y}")
            self.update_image_label()

    def update_image_label(self):
        pixmap = QPixmap(self.image_path + self.image_name)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

    def exit_app(self):
        logging_helper.log_info("Exiting application")
        QApplication.quit()
