#! /usr/bin/env python
# email_spammer.py - Script made to test sending emails on different library.
# It can easily be used instead of smtplib, if we use Gmail SMTP.

import yagmail
import time

# TODO make this (and other scripts requiring personal info) use argparse,
#  enviromental variables or some established config file.
contents = ["First line", "Second line", "Third line ;)"]

yag = yagmail.SMTP("sender@gmail.com", "******")

for i in range(8):
	topic = "Hehe #" + str(i + 1)
	yag.send("reciever@gmail.com", topic, contents)
	time.sleep(1)
