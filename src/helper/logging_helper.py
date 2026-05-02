import logging
from logging import Handler, Formatter as LoggingFormatter, getLogger
from typing import Any

# PyQt optional import (Headless / Tests sollen nicht brechen)
try:
    from PyQt5.QtCore import pyqtSignal, QObject  # type: ignore
    _QT_AVAILABLE = True
except Exception:
    _QT_AVAILABLE = False

    class QObject:  # Minimal-Stub, damit die Klasse-Definition funktioniert
        pass

    class _DummySignal:
        def emit(self, *args: Any, **kwargs: Any) -> None:
            return None

    def pyqtSignal(*args: Any, **kwargs: Any):
        return _DummySignal()


class LogFormatter(LoggingFormatter):
    """
    Custom formatter: entfernt/newline-Ersatz in Exception-Texten,
    liefert kompakte, einzeilige Log-Zeilen fuer die GUI.
    """

    def formatException(self, exc_info):
        text = super().formatException(exc_info)
        # Einzeilige Darstellung der Exception (vermeidet Layout-Probleme im GUI-Log)
        return text.replace('\n', ' | ')

    def format(self, record):
        # Falls exc_info vorhanden, setze exc_text auf die einzeilige Exception
        if record.exc_info:
            try:
                record.exc_text = self.formatException(record.exc_info)
            except Exception:
                record.exc_text = None
        formatted = super().format(record)
        return formatted.replace('\n', ' | ')


class LogHandler(QObject if _QT_AVAILABLE else object, Handler):
    """
    Logging-Handler der Log-Nachrichten via PyQt-Signal ausgibt.
    Bei fehlendem PyQt wird ein Dummy-Signal verwendet (no-op).
    """
    new_record = pyqtSignal(str)

    def __init__(self, parent=None):
        if _QT_AVAILABLE:
            QObject.__init__(self, parent)
        Handler.__init__(self)
        fmt = LogFormatter('[%(asctime)s][%(levelname)s]: %(message)s')
        self.setFormatter(fmt)

    def emit(self, record):
        try:
            msg = self.format(record)
            # emit signal (bei Dummy-Signal ist emit ein no-op)
            try:
                self.new_record.emit(msg)
            except Exception:
                # Falls Signal-Emission fehlschlaegt, fallback auf stdout
                print(msg)
        except Exception:
            self.handleError(record)


# Modul-Logger initialisieren (idempotent)
logger = getLogger('D4.Helper')
if not logger.handlers:
    # Stream handler fuer Konsole
    stream = logging.StreamHandler()
    stream.setFormatter(LogFormatter('[%(asctime)s][%(levelname)s]: %(message)s'))
    logger.addHandler(stream)

# Qt-Handler hinzufuegen, aber nicht doppelt
_has_qt_handler = any(isinstance(h, LogHandler) for h in logger.handlers)
if not _has_qt_handler:
    try:
        qt_handler = LogHandler()
        logger.addHandler(qt_handler)
    except Exception:
        # Sicherstellen, dass Import/Init nicht bricht
        logging.getLogger().debug('Failed to attach LogHandler (Qt may be unavailable).')

# Default Level
logger.setLevel(logging.DEBUG)

# Utility Wrappers (werden projektweit verwendet)
def log_info(msg: str, *args, **kwargs) -> None:
    logger.info(msg, *args, **kwargs)


def log_debug(msg: str, *args, **kwargs) -> None:
    logger.debug(msg, *args, **kwargs)


def log_error(msg: str, *args, **kwargs) -> None:
    logger.error(msg, *args, **kwargs)
