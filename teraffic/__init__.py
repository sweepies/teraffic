#!/usr/bin/python

import sys
import subprocess
from optparse import OptionParser

try:
	import netifaces
except ImportError:
	print("Missing dependency: netifaces")
	exit()

def main():

	parser = OptionParser()

	parser.add_option("-r", "--raw", help="don't format the number of bytes", action="store_true")
	parser.add_option("-i", "--in", help="only show ingress traffic", action="store_true", dest="ingress")
	parser.add_option("-o", "--out", help="only show egress traffic", action="store_true")
	(options, args) = parser.parse_args()

	try:
		interface = args[0]
	except IndexError:
		print("Usage: teraffic.py --help") # Show usage with no arguments
		exit()

	try:
		outgoing = open('/sys/class/net/' + interface + '/statistics/tx_bytes', 'r').read() # Get 
		incoming = open('/sys/class/net/' + interface + '/statistics/rx_bytes', 'r').read()
	except IOError: # Make sure interface exists
		print("Could not find interface \"" + interface + "\"")
		exit()

	def getuptime():
		raw = subprocess.check_output('uptime').replace(',','')
		days = int(raw.split()[2])
		if 'min' in raw:
			hours = 0
			minutes = int(raw[4])
		else:
			hours, minutes = map(int,raw.split()[4].split(':'))
		totalsecs = days*24*60*60 + hours*60*60 + minutes*60    
		return totalsecs

	def printtotalfancy():
		if interface in netifaces.interfaces():
			print("Total network traffic on " + interface + " since last boot (~" + str(getuptime() / 60 / 60 / 24) + " days):\n")
			print("Incoming: " + str(int(incoming) / 1000000000) + "GB")
			print("Outgoing: " + str(int(outgoing) / 1000000000) + "GB")
		else:
			print("Could not find interface \"" + interface + "\"") # Failsafe for previous IOError


	non_default_output = None

	if options.ingress:
		if not options.raw: # If --raw option is not present, format the output
			print(str(int(incoming) / 1000000000) + "GB")
			non_default_output = True
		else:
			print(incoming.strip())
			non_default_output = True

	if options.out:
		if not options.raw:
			print(str(int(outgoing) / 1000000000) + "GB")
			non_default_output = True
		else:
			print(outgoing.strip())
			non_default_output = True

	if options.raw:
		if not options.out:
			if not options.ingress:
				print(incoming.strip())
				print(outgoing.strip())
				non_default_output = True

	if not non_default_output:
		printtotalfancy()
