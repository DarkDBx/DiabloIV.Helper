import logging
from PyQt5.QtCore import pyqtSignal, QObject


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
    
    