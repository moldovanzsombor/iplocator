# iplocator
Finds basic information of a given IP address using web scraping.

# Requirements
* requests
* bs4
* pythonping

# How it works
This program is not a scanner. It works with <https://censys.io/>
The program loads a webpage with a URL with the target IP in it:
https://censys.io/ipv4/93.184.216.34
Then it extracts the information given by censys.io
