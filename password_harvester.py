#! /usr/bin/env python

import requests


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open("resources/" + file_name, "wb") as file:
        file.write(get_response.content)


download("")
