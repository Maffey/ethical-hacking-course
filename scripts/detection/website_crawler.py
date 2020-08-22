#! /usr/bin/env python
# Compatibility: Python 3.x
# TODO: Probably change the shebang everywhere.

import requests


def request(url):
    try:
        return requests.get(f"https://{url}")
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.InvalidURL:
        pass


target_url = "google.com"

with open("../../resources/subdomains.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        tested_url = f"{word}.{target_url}"
        response = request(tested_url)
        if response:
            print(f"[+] Discovered subdomain --> {tested_url}")
