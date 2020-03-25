#! /usr/bin/env python
# WARNING: Not compatible with Python 3.x

import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            re.sub("Accept-Encoding:.?\\r\\n", "", scapy_packet[scapy.Raw].load)

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            print(scapy_packet.show())

    packet.accept()


print("Queue has been created.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
