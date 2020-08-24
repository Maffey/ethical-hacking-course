#! /usr/bin/env python
# Compatibility: Python 3.x

import requests

target_url = "http://10.0.2.4/dvwa/login.php"

# Dictionary keys refer to the "name" attribute in HTML submit classes (POST request form),
# username and password by default. The last one refers to the button we use to submit data.
login_data = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(target_url, data=login_data)

print(response.content)
