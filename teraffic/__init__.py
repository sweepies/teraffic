#!/usr/bin/python

from optparse import OptionParser
from uptime import uptime

try:
	import netifaces
except ImportError:
	print("Missing dependency: netifaces")
	print("Run 'setup.py install' to install all required packages.")
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
		print("Usage: teraffic.py <interface> [options]") # Show usage with no arguments
		print("Run 'teraffic.py --help' for more information.")
		exit()

	try:
		outgoing = open('/sys/class/net/' + interface + '/statistics/tx_bytes', 'r').read() # Get 
		incoming = open('/sys/class/net/' + interface + '/statistics/rx_bytes', 'r').read()
	except IOError: # Make sure interface exists
		print("Could not find network interface '" + interface + "'")
		print("Run 'ifconfig' to view all interfaces.")
		exit()

	def printtotalfancy():
		if interface in netifaces.interfaces():
			print("Total network traffic on " + interface + " since last boot (~" + str(int(uptime()) / 60 / 60 / 24) + " days):\n")
			print("Incoming: " + str(int(incoming) / 1000000000) + "GB")
			print("Outgoing: " + str(int(outgoing) / 1000000000) + "GB")
		else:
			print("Could not find network interface '" + interface + "'")
			print("Run 'ifconfig' to view all interfaces.")
			exit() # Failsafe for previous IOError


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
