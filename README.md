# EthicalHackingCourse
Repository for all the code related to Learn Python &amp; Ethical Hacking From Scratch course. All the work is done on Kali Linux, using both Python 2.7 and 3.x version.

## Important notes
To enable **IP forwarding**, enter the following command into the terminal:  
`echo 1 > /proc/sys/net/ipv4`

To create **net filter queue** (*iptables*), enter the following command:  
`iptables -I FORWARD -j NFQUEUE --queue-num <number>`  
Where the default `<number>` is `0`.
