#!/usr/bin/python
"""
Challenge 4:
Write a script that uses Cloud DNS to create a new A record when passed a FQDN 
and IP address as arguments

@author: Lindsey Anderson
@date  : March 21st, 2013
"""

import pyrax
import sys
import pyrax.exceptions as exc 
import pyrax.utils as utils

from imports import auth

if __name__ == '__main__':

	auth.verify_input()

	dns = pyrax.cloud_dns

	# accept out input
	fqdn = raw_input("Please input your domain name as a FQDN: ")
	ipaddr = raw_input("Please input your target IPv4 address: ")

	# create domain
	try: 
		domain = dns.find(name=fqdn)
	except exc.NotFound:
		try:
			domain = dns.create(name=fqdn, emailAddress="ipadmin@stabletransit.net",
				ttl=300, comment=fqdn)
		except exc.DomainCreationFailed as ex:
			print "!! Domain could not be created:", ex
			sys.exit(1)
		print "Domain created: {0}.".format(str(domain))
	
	# create the dict for the record
	arecord = {"type": "A",
		   "name": fqdn,
		   "data": ipaddr,
  		   "ttl": 300}

	# try to create the record for the domain
	try:
		domain.add_records(arecord)
		print "Record added successfull!"
	except exc.DomainRecordAdditionFailed as ex:
		print "Record could not be added:", ex
