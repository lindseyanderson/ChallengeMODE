#!/usr/bin/python
""" 
Challenge 9:
Write an application that when passed the arguments FQDN, image, and flavor it creates a server of the specified 
image and flavor with the same name as the fqdn, and creates a DNS entry for the fqdn pointing to the server's 
public IP.
"""

import pyrax
import pyrax.exceptions as exc
from imports import auth
from imports import cloudservers


if __name__ == '__main__':
	
	auth.verify_input()
	cs = pyrax.cloudservers

	fqdn_input = raw_input("Enter a FQDN:")

	# Get user input for flavor
	print "Please select your instance flavor from the following list."
	flavors = cs.list_flavors()
	for number,each_flavor in enumerate(flavors):
		print "{0} )  - {1}".format(str(number), str(each_flavor.name))
	# Validate our input
	while True:
		try:
			flavor_input = int(raw_input("Selection:"))
		except ValueError:
			print "Please input a number."
		else:
			if flavor_input < 0 or flavor_input >= len(flavors):
				print "Please select a value of 0-{0}.".format(str(len(flavors)-1))
				continue
			else:
				break
	final_flavor = flavors[flavor_input]

	# get user input for the image
	images = cs.list_images()
	for number,each_image in enumerate(images):
		print "{0} ) - {1}".format(str(number), str(each_image.name))
	# Validate input
	while True:
		try:
			image_input = int(raw_input("Selection:"))
		except ValueError:
			print "Please input a number."
		else:
			if image_input <0 or image_input >= len(images):
				print "Please select a value of 0-{0}.".format(str(len(images)-1))
				continue
			else:
				break
	final_image = images[image_input]

	print "Creating your Cloud Server from {0} with a flavor of {1}.".format(str(final_image.name), str(final_flavor.name))

	# Build our new server, with the FQDN as the server name.
	server = cloudservers.OpenCloudServer()
	
	server.create_server(fqdn_input, None, None, final_image.id, final_flavor.id)

	# Get the public IP address
	public_ip = server.get_server_ip_public()	
	
        dns = pyrax.cloud_dns

        # create domain
        try:
                domain = dns.find(name=fqdn_input)
        except exc.NotFound:
                try:
                        domain = dns.create(name=fqdn_input, emailAddress="ipadmin@stabletransit.net",
                                ttl=300, comment=fqdn_input)
                except exc.DomainCreationFailed as ex:
                        print "!! Domain could not be created:", ex
                        sys.exit(1)
                print "Domain created: {0}.".format(str(domain.name))

        # create the dict for the record
        arecord = {"type": "A",
                   "name": fqdn_input,
                   "data": public_ip,
                   "ttl": 300}

        # try to create the record for the domain
        try:
                domain.add_records(arecord)
                print "A Record added successfull!"
        except exc.DomainRecordAdditionFailed as ex:
                print "Record could not be added:", ex
	
