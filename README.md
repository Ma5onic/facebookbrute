# facebookbrute
Brute forces facebook accounts

How To Download facebookbrute
------------------------------
git clone https://github.com/ethicalhackingplayground/facebookbrute.git


Setting it up
------------------------------
You might need to add nameserver 8.8.8.8 to /etc/resolv.conf 

facebookbrute runs on a proxy so open up firefox and change the proxy to 127.0.0.1 on port 1234

How To Install facebookbrute
------------------------------
To install facebookbrute all you need to do is run this command

cd facebookbrute/ && chmod +x setup.py && ./setup.py && chmod +x facebookbrute.py 

Now you need to setup the config file you need to specify the username and a wordlist,
after that you can type.

./facebookbrute.py 

And it will attempt to crack the password

This has only been tested in Kali Linux
Enjoy!!
