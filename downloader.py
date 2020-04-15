#!/usr/bin/env python

import requests


def download(url):
    get_response = requests.get(url)
    print(get_response.content)


download("https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Kotlin-logo.svg/512px-Kotlin-logo.svg.png")
