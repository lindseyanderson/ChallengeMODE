#!/usr/bin/python
"""
Challenge 3:
Write a script that accepts a directory as an argument as well as a container 
name. The script should upload the contents of the specified directory to the 
container (or create it if it doesn't exist). The script should handle errors 
appropriately. (Check for invalid paths, etc.)

@author: Lindsey Anderson
@date  : March 17, 2013
"""

import pyrax
import pyrax.exceptions as exc
import pyrax.utils as utils
import os
from imports import auth

if __name__ == "__main__":
	auth.verify_input()

	container  = raw_input("What container would you like to upload to? ")
	local_file = raw_input("What local file would you like to upload? ")

	# We need to connect to Cloud Files
	cf = pyrax.cloudfiles
	
	# See if this container already exists
	# if not, make it.
	try:
		cont = cf.get_container(container)
		print "Container {0} exists.".format(str(cont.name))
	except exc.NoSuchContainer:	
		cont = cf.create_container(container)
		print "Container {0} created.".format(str(cont.name))

	# Make sure we have a valid file	
 	try:
		with open(local_file): pass
	except IOError:
		print "This file {0} does not exist.".format(str(cont.name))

	print "Uploading object from {0}.".format(str(local_file))
	# Store the object in Cloud Files
	try:
		object = cf.upload_file(cont.name, local_file)
		print "Upload completed."
	except exc.UploadFailed:
		print "!! An error occured in the upload process !!" 
