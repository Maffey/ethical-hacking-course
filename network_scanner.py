#! /usr/bin/env python
# network_scanner.py - A network scanner which uses Scapy to find out info about a network.

import scapy.all as scapy


def scan(ip):
    scapy.arping(ip)