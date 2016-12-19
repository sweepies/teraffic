#! /usr/bin/python

import sys
import netifaces
import subprocess

try:
	interface = sys.argv[1]
except IndexError:
	print("Could not find interface \"\"")
	exit()

outgoing = open('/sys/class/net/' + interface + '/statistics/tx_bytes', 'r').read() # Get 
incoming = open('/sys/class/net/' + interface + '/statistics/rx_bytes', 'r').read()

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
		print("Could not find interface \"" + interface + "\"")

if len(sys.argv) == 2:
	printtotalfancy()

if "--in" in sys.argv:
	if "--raw" not in sys.argv:
		print(str(int(incoming) / 1000000000) + "GB")
if "--out" in sys.argv:
	if "--raw" not in sys.argv:
		print(str(int(outgoing) / 1000000000) + "GB")

if "--raw" in sys.argv:
	if "--in" in sys.argv:
		print(incoming.strip())
	if "--out" in sys.argv:
		print(outgoing.strip())
	else:
		print(incoming.strip())
		print(outgoing.strip())



