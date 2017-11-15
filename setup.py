#!/usr/bin/python

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

print("[+] Creating the passwords directory\n\n")
os.system("mkdir passwords")
