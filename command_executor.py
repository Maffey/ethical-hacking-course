#! /usr/bin/env python

import subprocess

command = "msg * You have been hacked!"
subprocess.Popen(command, shell=True)
