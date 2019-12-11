#! /usr/bin/env python
# network_scanner.py - A network scanner which uses Scapy to find out info about a network.
# Python 2.7 compatible.

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    
    print("".center(33, "="))
    print("IP\t\t\t\tMAC Address")
    print("".center(33, "="))
    for answer in answered:
        print(answer[1].psrc + "\t\t" + answer[1].hwsrc)


scan("10.0.2.1/24")
