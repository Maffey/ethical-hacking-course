#! /usr/bin/env python
# Compatibility: Python 3.x

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.InvalidURL:
        pass


target_url = "http://10.0.2.4/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

soup = BeautifulSoup(response.content.decode(errors="ignore"), features="lxml")
forms_list = soup.find_all("form")

for form in forms_list:
    action = form.get("action")
    post_url = urljoin(target_url, action)
    method = form.get("method")

    inputs_list = form.find_all("input")
    post_data = {}
    for form_input in inputs_list:
        input_name = form_input.get("name")
        input_type = form_input.get("type")
        input_value = form_input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value

    post_result = requests.post(post_url, data=post_data)
    print(post_result.content.decode(errors="ignore"))
