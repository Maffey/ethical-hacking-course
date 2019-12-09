#! /usr/bin/env python
# network_scanner.py - A network scanner which uses Scapy to find out info about a network.
# Python 2.7 compatible.

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered, unanswered = scapy.srp(arp_packet, timeout=1)


scan("10.0.2.1/24")
