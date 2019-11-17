#! /usr/bin/env python3
# mac_changer.py - simple MAC address changer for network interfaces.
import subprocess
import optparse

parser = optparse.OptionParser()

interface = input("if > ")
mac_address = input(" MAC > ")

print("Changing the MAC address for " + interface + " to " + mac_address + "...")

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
subprocess.call(["ifconfig", interface, "up"])

print("The MAC address change have been performed successfully.")
