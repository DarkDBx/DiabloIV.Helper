#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
from typing import Mapping

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, QTimer

from GUI import overlay
from helper import config_helper, logging_helper

APPNAME = 'notepad'
APPVERSION = '1.2026.0502.2312'


def main() -> int:
    """
    Entry point for the application.
    Initialisiert die GUI, liest Konfiguration und startet die QApplication-Schleife.
    Gibt einen Exit-Code zurueck (0 = OK, >0 = Fehler).
    """
    app = None
    try:
        cfg: Mapping = config_helper.read_config() or {}

        app_title = cfg.get('apptitle', APPNAME)
        app_class = cfg.get('class', 'unknown')

        QCoreApplication.setApplicationName(app_title)
        QCoreApplication.setApplicationVersion(APPVERSION)

        app = QApplication(sys.argv)

        # Signal-Handler fuer sauberes Beenden bei STRG+C
        def _handle_sigint(sig, frame):
            logging_helper.log_info("Received interrupt signal, quitting...")
            QCoreApplication.quit()

        signal.signal(signal.SIGINT, _handle_sigint)
        # Timer to keep signal handling responsive on some platforms
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)
        try:
            app_gui = overlay.Overlay()
            app_gui.show()
        except Exception as ex:
            logging_helper.log_error("Failed to initialize GUI overlay: %s" % ex)
            return 2

        # Logging-Level setzen (sofern DEBUG verfuegbar)
        """
        try:
            logging_helper.logger.setLevel(DEBUG)
        except Exception:
            # Falls logger oder DEBUG nicht wie erwartet vorhanden sind, ignoriere Fehler
            logging_helper.log_debug("Could not set logging level to DEBUG")
        """

        logging_helper.log_info("====== %s %s ======" % (APPNAME, APPVERSION))
        logging_helper.log_info("Starting up bot engine...")
        logging_helper.log_info("Preset class %s is initialized" % app_class)

        # Event loop starten und Exit-Code zurueckgeben
        exit_code = app.exec_()
        return int(exit_code)
    except getattr(config_helper, 'ConfigError', Exception) as ce:
        # Wenn ConfigError vorhanden ist, behandeln wir sie speziell
        logging_helper.log_error("Configuration error occurred: %s" % ce)
        return 3
    except KeyboardInterrupt:
        logging_helper.log_info("Interrupted by user")
        return 0
    except Exception as e:
        logging_helper.log_error("Unexpected exception occurred: %s" % e)
        return 1
    finally:
        # Sicherstellen, dass QApplication beendet wird
        if app is not None:
            try:
                app.quit()
            except Exception:
                pass


if __name__ == '__main__':
    sys.exit(main())
