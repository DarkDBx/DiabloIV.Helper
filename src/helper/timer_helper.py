from logging import debug
from timeit import default_timer


TIMER_RUNNING = 1
TIMER_STOPPED = 0


class TimerHelper:
    def __init__(self, ID):
        self.timerPool = {}
        self.timeID = ID

        """Initilialize the timer like below if any new timer to be added"""
        self.timerPool[self.timeID] = {}
        self.timerPool[self.timeID]['state'] = TIMER_STOPPED
        self.timerPool[self.timeID]['start'] = 0
        self.timerPool[self.timeID]['duration'] = 0
        self.timerPool[self.timeID]['time'] = 0


    """Interface to start the timer"""
    def StartTimer(self, time):
        self.timerPool[self.timeID]['time'] = time
        self.timerPool[self.timeID]
        if (self.timerPool[self.timeID]['state'] == TIMER_STOPPED):
            self.timerPool[self.timeID]['start'] = default_timer()
            self.timerPool[self.timeID]['state'] = TIMER_RUNNING
        return self.timerPool[self.timeID]['state']


    """
    Interface to get the timer status.
    Return "TIMER_STOPPED" when timer completed
    """
    def GetTimerState(self):
        time = self.timerPool[self.timeID]['time']
        if self.timerPool[self.timeID]['state'] == TIMER_RUNNING:
            self.timerPool[self.timeID]['duration'] = default_timer() - self.timerPool[self.timeID]['start']

        if  self.timerPool[self.timeID]['duration'] >= time:
            self.timerPool[self.timeID]['state'] = TIMER_STOPPED
            self.timerPool[self.timeID]['duration'] = 0
        
        debug('timer '+str(self.timeID)+' state: '+str(self.timerPool[self.timeID]['state']))
        return self.timerPool[self.timeID]['state']

