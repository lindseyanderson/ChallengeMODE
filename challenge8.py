#!/usr/bin/python
"""
Challenge 8:
Write a script that will create a static webpage served out of Cloud Files. The script must create a new container, cdn enable it, enable it to serve an index file, create an index file object, upload the object to the container, and create a CNAME record pointing to the CDN URL of the container.

@author: Lindsey Anderson
@date  : March 23st, 2013
"""

import pyrax
import pyrax.exceptions as ex
import sys
from imports import auth

if __name__ == '__main__':
	auth.verify_input()
	local_file 	= "index.html"
	subdomain	= "challenge8"
	fqdn 		= "justcurl.com"
	cf 		= pyrax.cloudfiles
	cdns 		= pyrax.cloud_dns

	container_name 	= "c8_container"
	try:
		container = cf.get_container(container_name)
		print "Container {0} exists.".format(str(container.name))
	except ex.NoSuchContainer:
		container = cf.create_container(container_name)
		print "Container {0} created.".format(str(container.name))	

	# enable the CDN on your container
	container.make_public(ttl=300)

	# upload your index.html file to the cdn container
	try:
		with open(local_file): pass
	except IOError:
		print "This file {0} does not exist.".format(str(local_file))
	try:
		object = cf.upload_file(container.name, local_file)
		print "Upload completed."
	except ex.UploadFiles as e:
		print "An error occured in the upload of the file:",e
	
	# update metadata to serve index.html file X-Container-Meta-Web-Index
	new_metadata = { "X-Container-Meta-Web-Index": local_file}
	cf.set_container_metadata(container, new_metadata)

	# create a CNAME record to point to the CDN URL of the container
	try: 
		domain = cdns.find(name=fqdn)
	except ex.NotFound:
		try:
			domain = cdns.create(name=fqdn, emailAddress="ipadmin@stabletransit.net",
				ttl=300, comment=fqdn)
		except ex.DomainCreationFailed as ex:
			print "!! Domain could not be created:", ex
			sys.exit(1)
		print "Domain created: {0}.".format(str(domain))
	fqdn = subdomain + '.' + fqdn
	cname_record = {"type": "CNAME",
			"name": fqdn,
			"data": container.cdn_uri,
			"ttl" : 300}

	try:
		domain.add_records(cname_record)
		print "CNAME Added:", fqdn 
		# return our new CDN URL
		print "CDN URI:", container.cdn_uri
		print "CDN SSL URI:", container.cdn_ssl_uri
		print "CDN Streaming URI:", container.cdn_streaming_uri
	except ex.DomainRecordAdditionFailed:
		print "CNAME record already exists."

