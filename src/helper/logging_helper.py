
from logging import getLogger, DEBUG, info, debug, error
from logging import Handler, Formatter as LoggingFormatter
from PyQt5.QtCore import pyqtSignal, QObject

class LogHandler(QObject, Handler):
    """
    A custom logging handler that integrates with PyQt by emitting log records as signals.
    """
    new_record = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Initializes the LogHandler and sets a default formatter.
        """
        QObject.__init__(self, parent)
        Handler.__init__(self)
        log_formatter = LogFormatter('[%(asctime)s][%(levelname)s]: %(message)s')
        self.setFormatter(log_formatter)

    def emit(self, record):
        """
        Emits a formatted log record as a PyQt signal.
        """
        try:
            msg = self.format(record)
            self.new_record.emit(msg)
        except Exception:
            self.handleError(record)

class LogFormatter(LoggingFormatter):
    """
    A custom log formatter to handle exceptions and format messages.
    """

    def formatException(self, exc_info):
        """
        Formats exception information for the log.
        """
        return super().formatException(exc_info)

    def format(self, record):
        """
        Formats a log record, ensuring exception text does not include newlines.
        """
        formatted_message = super().format(record)
        if record.exc_text:
            formatted_message = formatted_message.replace('\n', '')
        return formatted_message

logger = getLogger()
log_info = info
log_debug = debug
log_error = error
