#! /usr/bin/env python
# mac_changer.py - simple MAC address changer for network interfaces.

import subprocess
import optparse
import re


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac_address", help="new MAC address")
    opts, args = parser.parse_args()
    if opts.interface is None:
        parser.error("[-] please specify an interface, use --help for more information")
    elif opts.mac_address is None:
        parser.error("[-] please specify a MAC address, use --help for more information")

    return opts


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


options = get_options()
current_mac = get_current_mac(options.interface)
print("[+] current MAC: " + str(current_mac))
change_mac(options.interface, options.mac_address)
current_mac = get_current_mac(options.interface)
if current_mac == options.mac_address:
    print("[+] the MAC address change have been performed successfully")
    print("[+] your new MAC is " + current_mac)
else:
    print("[-] operation failed. MAC address has not been changed")
