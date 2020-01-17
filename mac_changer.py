#! /usr/bin/env python3
# mac_changer.py - simple MAC address changer for network interfaces.

import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="interface", help="interface to change its MAC address")
    parser.add_argument(dest="mac_address", help="new MAC address")
    arguments = parser.parse_args()
    if arguments.interface is None:
        parser.error("[-] please specify an interface, use --help for more information")
    elif arguments.mac_address is None:
        parser.error("[-] please specify a MAC address, use --help for more information")

    return arguments


def change_mac(interface, mac_address):
    print("[+] changing the MAC address for " + interface + " to " + mac_address + "...")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"(\w\w):(\w\w):(\w\w):(\w\w):(\w\w):(\w\w)", ifconfig_result)
    if mac_address_search_result is not None:
        return mac_address_search_result.group()
    else:
        print("[-] Could not read a MAC address.")


args = get_arguments()
current_mac = get_current_mac(args.interface)
print("[+] current MAC: " + str(current_mac))
change_mac(args.interface, args.mac_address)
current_mac = get_current_mac(args.interface)
if current_mac == args.mac_address:
    print("[+] the MAC address change have been performed successfully")
    print("[+] your new MAC is " + current_mac)
else:
    print("[-] operation failed. MAC address has not been changed")

# TODO: add Python 3.x compatibility to all scripts.
