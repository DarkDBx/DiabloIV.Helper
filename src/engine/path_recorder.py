import threading
import mouse
import keyboard
import pickle
import sys
import os


class PathRecorder:
    def __init__(self, mouse_file, key_file) -> None:
        self.mouse_file = mouse_file
        self.key_file = key_file
        self.mouse_events = []
        self.keyboard_events = {}

    """Recorder"""
    def rec(self):
        mouse.hook(self.mouse_events.append)
        keyboard.start_recording()

        # waiting for hotkey before recording stops
        keyboard.wait("end")

        mouse.unhook(self.mouse_events.append)
        self.keyboard_events = keyboard.stop_recording()

        self.save_record(self.mouse_events, self.mouse_file)
        self.save_record(self.keyboard_events, self.key_file)

    """Player"""
    def play(self):
        mouse_record = self.read_record(self.mouse_file)
        keyboard_record = self.read_record(self.key_file)

        k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_record))
        k_thread.start()
        m_thread = threading.Thread(target = lambda :mouse.play(mouse_record))
        m_thread.start()

        # waiting for both threadings to be completed
        k_thread.join() 
        m_thread.join()

    """Finds filepath after compiling."""
    def set_file_path(self, file_name):
        if getattr(sys, 'frozen', False):  # we are running in a bundle
            bundle_dir = sys._MEIPASS  # This is where the files are unpacked to
        else:  # normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            bundle_dir = os.path.dirname(bundle_dir)
            bundle_dir = os.path.dirname(bundle_dir)
        return bundle_dir + '\\src\\engine\\recording\\'+file_name+'.rec'

    def save_record(self, data, f_name):
        with open(self.set_file_path(f_name), 'wb') as outfile:
            pickle.dump(data, outfile)


    def read_record(self, f_name):
        with open(self.set_file_path(f_name), 'rb') as outfile:
            record = pickle.load(outfile)
        return record


def main():
    pathRecord = PathRecorder('mouse_events', 'keyboard_events')
    pathRecord.rec()
    pathRecord.play()


if __name__ == '__main__':
    main()

