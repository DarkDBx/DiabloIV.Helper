from timeit import default_timer

from helper import logging_helper

TIMER_RUNNING = 1
TIMER_STOPPED = 0

class TimerHelper:
    def __init__(self, ID):
        """Initialize a new timer with the given ID."""
        self.timerPool = {
            ID: {
                'state': TIMER_STOPPED,
                'start': 0,
                'duration': 0,
                'time': 0
            }
        }
        self.timeID = ID

    def start_timer(self, duration):
        """
        Start the timer with the specified duration (in seconds).
        Returns the timer's state after starting.
        """
        timer = self.timerPool[self.timeID]
        timer['time'] = duration

        if timer['state'] == TIMER_STOPPED:
            timer['start'] = default_timer()
            timer['state'] = TIMER_RUNNING
        
        return timer['state']

    def get_timer_state(self):
        """
        Check and update the state of the timer.
        Returns TIMER_STOPPED when the timer has completed.
        """
        timer = self.timerPool[self.timeID]
        if timer['state'] == TIMER_RUNNING:
            timer['duration'] = default_timer() - timer['start']

        if timer['duration'] >= timer['time']:
            timer['state'] = TIMER_STOPPED
            timer['duration'] = 0  # Reset duration for future use
        
        logging_helper.log_debug(f"Timer {self.timeID} state: {timer['state']}")
        return timer['state']
