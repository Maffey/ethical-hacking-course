#! /usr/bin/env python
# packet_sniffer.py - packet sniffer that catches HTTP packets and filters out
# all URLs visited and payloads associated with login information.
# TODO: make documentation consistent in all files

import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[+] You are under attack! The ARP table has been poisoned.")
        except IndexError:
            pass


print("ARP spoof detection has been started.")
sniff("eth0")
