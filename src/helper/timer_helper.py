from timeit import default_timer
from typing import Union

from helper import logging_helper

TIMER_RUNNING = 1
TIMER_STOPPED = 0


class TimerHelper:
    """
    Einfacher, verlaesslicher Timer-Wrapper.
    Nutzung:
      t = TimerHelper('id')
      t.start_timer(3)        # startet Timer fuer 3s
      state = t.get_timer_state()  # aktualisiert und gibt Zustand zurueck
      t.stop_timer()          # optional stoppen
      t.time_left()           # verbleibende Sekunden (float)
      t.is_running()          # bool
    """

    def __init__(self, ID: Union[str, int]):
        """Initialisiert einen Timer fuer die gegebene ID."""
        self.timeID = str(ID)
        self._state = TIMER_STOPPED
        self._start_time = 0.0
        self._duration_target = 0.0

    def start_timer(self, duration: float, restart: bool = True) -> int:
        """
        Startet den Timer mit der angegebenen Dauer in Sekunden.
        Wenn restart == False und der Timer bereits laeuft, bleibt er unveraendert.
        Rueckgabe: aktueller Timer-Status (TIMER_RUNNING oder TIMER_STOPPED).
        """
        try:
            duration = float(duration)
        except Exception:
            logging_helper.log_debug(f"Timer {self.timeID}: invalid duration '{duration}'")
            return self._state

        if duration <= 0:
            # Keine Wartezeit noetig setze Timer sofort auf gestoppt
            self._state = TIMER_STOPPED
            self._start_time = 0.0
            self._duration_target = 0.0
            logging_helper.log_debug(f"Timer {self.timeID}: duration <= 0, not starting.")
            return self._state

        if self._state == TIMER_RUNNING and not restart:
            logging_helper.log_debug(f"Timer {self.timeID} already running, not restarting.")
            return self._state

        self._duration_target = duration
        self._start_time = default_timer()
        self._state = TIMER_RUNNING
        logging_helper.log_debug(f"Timer {self.timeID} started for {self._duration_target:.2f}s")
        return self._state

    def get_timer_state(self) -> int:
        """
        Aktualisiert den Timer-Zustand und gibt ihn zurueck.
        Wenn die Zielzeit erreicht ist, wird der Timer auf TIMER_STOPPED gesetzt.
        """
        if self._state == TIMER_RUNNING:
            elapsed = default_timer() - self._start_time
            if elapsed >= self._duration_target:
                # Timer abgelaufen zuruecksetzen
                self._state = TIMER_STOPPED
                self._start_time = 0.0
                self._duration_target = 0.0
                logging_helper.log_debug(f"Timer {self.timeID} expired and stopped.")
            else:
                logging_helper.log_debug(f"Timer {self.timeID} running, elapsed={elapsed:.2f}s, target={self._duration_target:.2f}s")
        else:
            logging_helper.log_debug(f"Timer {self.timeID} is stopped.")
        return self._state

    def stop_timer(self) -> None:
        """Stoppt den Timer sofort und setzt Werte zurueck."""
        self._state = TIMER_STOPPED
        self._start_time = 0.0
        self._duration_target = 0.0
        logging_helper.log_debug(f"Timer {self.timeID} stopped manually.")

    def time_left(self) -> float:
        """
        Gibt die verbleibende Zeit in Sekunden zurueck (>= 0).
        Wenn Timer nicht laeuft, wird 0.0 zurueckgegeben.
        """
        if self._state != TIMER_RUNNING:
            return 0.0
        remaining = self._duration_target - (default_timer() - self._start_time)
        return max(0.0, remaining)

    def is_running(self) -> bool:
        """Hilfsfunktion, ob Timer gerade laeuft."""
        return self._state == TIMER_RUNNING
