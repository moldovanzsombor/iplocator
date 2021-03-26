#!/usr/bin/env python3

import socket
from sys import argv, exit
from bs4 import BeautifulSoup
import pythonping
import requests
import re

def get_intel(ip_addr, network, location, gethost, ping):
	headers = {
		"user_agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
	}
	url = 'https://censys.io/ipv4/' + ip_addr
	result = ''

	if network:
		result += '-' * 103 + '\n'
		try:
			page = requests.get(url, headers = headers)
			soup = BeautifulSoup(page.content, 'html.parser')
			result += soup.find(attrs = {"col-md-8 host-details"}).get_text() + '\n'
		except:
			result += 'Error with network\n'

	if location:
		result += '-' * 103 + '\n'
		try:
			page = requests.get(url, headers = headers)
			soup = BeautifulSoup(page.content, 'html.parser')
			result += soup.find(attrs = {"panel-body"}).get_text() + '\n'
		except:
			result += 'Error with location\n'

	if gethost:
		result += '-' * 103 + '\n'
		try:
			result += str(socket.gethostbyaddr(ip_addr)) + '\n'
		except:
			result += 'Error with gethost\n'

	if ping:
		result += '-' * 103 + '\n'
		try:
			result += str(pythonping.ping(ip_addr)) + '\n'
		except:
			result += 'Failed, target disabled ping. Did you run as root?\n'

	output = ''
	for line in result.splitlines():
		if not re.match(r'^\s*$', line):
			output += line + '\n'

	return output

def usage():
	print(
		"Usage:\n" \
		"ipfinder [Options] [Domain/IP]\n" \
		"\n" \
		"-n --network      # Basic network information\n" \
		"-l --location     # Locoation\n" \
		"-g --gethost         # Gethostbyname/Gethostbyaddr\n" \
		"-p --ping         # Default ping\n" \
		"-a --all          # All of the above\n" \
	)
	exit(0)

if __name__ == '__main__':
	NETWORK, LOCATION, GETHOST, PING = [False] * 4
	TARGET = None

	if len(argv) == 1 or '-h' in argv or '--help' in argv:
		usage()

	for i in range(1, len(argv) - 1):
		if argv[i] in ['-n', '--network']:
			NETWORK = True
		elif argv[i] in ['-l', '--location']:
			LOCATION = True
		elif argv[i] in ['-p', '--ping']:
			PING = True
		elif argv[i] in ['-g', '--gethost']:
			GETHOST = True
		elif argv[i] in ['-a', '--all']:
			NETWORK, LOCATION, GETHOST, PING = [True] * 4

		else:
			print(argv[i], 'Invalid Option')
			usage()

	try:
		TARGET = argv[-1]
		socket.inet_aton(TARGET)
	except:
		print(argv[-1], 'Invalid Target')
		usage()

	if TARGET is not None:
		print(get_intel(TARGET, NETWORK, LOCATION, GETHOST, PING))


