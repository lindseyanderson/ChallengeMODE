#!/usr/bin/python
"""
Challenge 5:
Write a script that creates a Cloud Database instance. This instance should 
contain at least one database, and the database should have at least one user 
that can connect to it.

@author: Lindsey Anderson
@date  : March 21st, 2013
"""

import pyrax
import pyrax.exceptions as ex
import sys
from imports import auth

if __name__ == '__main__':
	auth.verify_input()
	cdb = pyrax.cloud_databases
	
	cloud_database_instance   = raw_input("Please enter an instance name: ")
	cloud_database_name       = raw_input("Please enter a database name: ")
	print "Flavors are available in the following: "

	# Preset possible flavors to users
	flavors = cdb.list_flavors()
	count = 0 
	for flavor in flavors:
		print "{0}) Flavor name: {1} ".format(count, flavor.name)
		count = count +1
	cloud_database_flavor = raw_input("Please enter a memory size: ")
	try:
		chosen_flavor = flavors[int(cloud_database_flavor)]
	except ex.IndexError:
		print "Invalid flavor choice."
		sys.exit(1)

	# get disk space
	cloud_database_size   = raw_input("Please Enter disk size in GB: ")	

	# Check and see if our database instance exists
	try:
		instance = [ iname for iname in cdb.list()
				if iname.name == cloud_database_instance][0]
	# If not, create it!
	except:
		try: 
			instance = cdb.create(cloud_database_instance, 
				flavor=chosen_flavor, volume=cloud_database_size )
			print "Instance {0} created".format(str(cloud_database_instance))
		except:
			print "Instance could not be created."
			sys.exit(1)

	# Wait for our instance to finish building
	status_check = [ inst for inst in cdb.list()
			if inst.name == cloud_database_instance ][0]
	pyrax.utils.wait_until(status_check, "status", ['ACTIVE','ERROR'], 
			interval=20, attempts=60,verbose=True)
	
	# Create the database:
	try:
		database = instance.create_database(cloud_database_name)
		print "Database created:", cloud_database_name
	except ex.BadRequest as e :
		print "Database cannot be created:",e
	# Create the user
	try:
		cloud_database_user       = raw_input("Please enter a username: ")
		cloud_database_pass       = raw_input("Please enter a password: ")
		user = instance.create_user(cloud_database_user, cloud_database_pass, 
			database_names=cloud_database_name)
		print "User added:", cloud_database_user
	except ex.BadRequest as e :
		print "User cannot be added:",e	


