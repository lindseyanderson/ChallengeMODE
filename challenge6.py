#!/usr/bin/python
"""
Challenge 6:
Write a script that creates a CDN-enabled container in Cloud Files.

@author: Lindsey Anderson
@date  : March 23st, 2013
"""

import pyrax
import pyrax.exceptions as ex
import sys
from imports import auth

if __name__ == '__main__':
	auth.verify_input()

	cf = pyrax.cloudfiles

	container_name = "cdn_test_container"
	try:
		container = cf.get_container(container_name)
		print "Container {0} exists.".format(str(container.name))
	except ex.NoSuchContainer:
		container = cf.create_container(container_name)
		print "Container {0} created.".format(str(container.name))	

	# enable the CDN on your container
	container.make_public(ttl=300)


	# return our new CDN URL
	print "CDN URI:", container.cdn_uri
	print "CDN SSL URI:", container.cdn_ssl_uri
	print "CDN Streaming URI:", container.cdn_streaming_uri
