#!/usr/bin/python
# Title: setup.py
# Author: Th3J0k3r
#
import sys
import os


print("[+] Setting up facebookbrute\n\n")
print("Installing mechanize\n");
os.system("pip install mechanize")

print("[+] Installing lazyme\n\n")
os.system("pip install lazyme")

print("[+] Installing color_print\n\n")
os.system("pip install color_print")

print("[+] Installing multiprocessing\n\n")
os.system("pip install multiprocessing")

print("[+] Installing pathlib\n\n")
os.system("pip install pathlib")

print("[+] Creating the passwords directory\n\n")
os.system("mkdir passwords")
