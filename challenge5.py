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

from imports import auth

if __name__ == '__main__':
	auth.verify_input()
	cdb = pyrax.cloud_databases
	
	cloud_database_instance   = raw_input("Please enter an instance name: ")
	cloud_database_name       = raw_input("Please enter a database name: ")
	cloud_database_user       = raw_input("Please enter a username: ")
	cloud_database_pass       = raw_input("Please enter a password: ")
	print "Flavors are available in the following: "

	# Preset possible flavors to users
	flavors = cdb.list_flavors()
	for flavor in flavors:
		print "Flavor name:",flavor.name
		print "Flavor memory:",flavor.ram

	cloud_database_flavor = raw_input("Please enter a memory size: ")
	try:
		chosen_flavor = flavors[cloud_database_flavor]
	except IndexError:
		print "Invalid flavor choice."
		sys.exit(1)
	cloud_database_size   = raw_input("Please Enter disk size in GB: ")	

	# Check and see if our database instance exists
	try:
		instance = [ iname for iname in cdb.list()
				if dbname.name == cloud_database_instance ][0]
	# If not, create it!
	except:
		try: 
			instance = cdb.create(cloud_database_instance, 
				flavor=cloud_database_flavor, cloud_database_size )
			print "Instance {0} created".format(str(cloud_database_instance))
		except:
			print "Instance could not be created."

	# Create the database:
	database = instance.create_database(cloud_database_name)



