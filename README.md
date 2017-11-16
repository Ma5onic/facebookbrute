# facebookbrute
Brute forces facebook accounts

How To Download facebookbrute
------------------------------
git clone https://github.com/ethicalhackingplayground/facebookbrute.git

How To Install facebookbrute
------------------------------
To install facebookbrute all you need to do is run this command

cd facebookbrute/ && chmod +x setup.py && ./setup.py && chmod +x facebookbrute.py 

Now you need to setup the config file you need to specify the username and a wordlist.

Setting it up
------------------------------
You might need to add nameserver 8.8.8.8 to /etc/resolv.conf 

facebookbrute runs on a proxy so open up firefox and change the proxy to 127.0.0.1 on port 1234

Crack the password
-----------------------------
Now run and will attempt to crack the password

./facebookbrute.py 


This has only been tested in Kali Linux
Enjoy!!
