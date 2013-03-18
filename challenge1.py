#!/usr/bin/python
"""
Cloud Server
"""

import pyrax
import re
import sys
from imports import auth

class OpenCloudServer:
	def __init__(self):
		self.cs	 = pyrax.cloudservers

	def create_server(self, server_name, server_os, server_size):
		self.server_name = server_name
		self.server_os   = server_os
		self.server_size = int(server_size)
		local_memory = [ memory for memory in self.cs.flavors.list()
					if memory.ram == self.server_size][0]
		local_os     = [ image  for image  in self.cs.images.list()
					if self.server_os in image.name][0]
		new_server = self.cs.servers.create(self.server_name, local_os.id, local_memory.id)
		self.server_name = new_server.name
		self.root_pass   = new_server.adminPass
		pyrax.utils.wait_until(new_server, "status", ['ACTIVE', 'ERROR'], interval=20, 
				attempts=60, verbose=True)
		self.network    = new_server.networks
		self.server_os   = local_os.name
		self.server_size = local_memory.name

		print self.network
	"""
	Returns public IP address of server
	"""
	def get_server_ip_public(self): 
		public_network = self.network[u'public']
		for ip_address in public_network:
			current_ip = re.findall(r'[0-9]+(>:\.[0-9]+){3}', ip_address)
			if current_ip: return current_ip[0]

	"""
	Returns private IP address of server
	"""
	def get_server_ip_private(self):
		public_network = self.network[u'private']
		for ip_address in public_network:
			current_ip = re.findall(r'[0-9]+(>:\.[0-9]+){3}', ip_address)
			if current_ip: return current_ip[0]		
	"""
	Returns server name
	"""	
	def get_server_name(self): return self.server_name

	"""
	Returns server memory size
	"""
	def get_server_size(self): return self.server_size

	"""
	Returns server networks
	"""
	def get_server_networks(self): return self.networks
	"""
	Returns server os
	"""
	def get_server_os(self): return self.server_os

if __name__ == '__main__':
	auth.verify_input()
	server1 = OpenCloudServer()
	server_name = raw_input("Server Name: ")
	try:
		server_size = int(raw_input("Server Size: "))
	except ValueError:
		print "Non-integer value entered.  Please try a number."
		sys.exit(1)
	server_os	 = raw_input("Server OS  : ")
	server1.create_server(server_name, server_os, server_size)	
	
	print "Server Name: " + server1.get_server_name()
	print "Server Size: " + server1.get_server_size()
	print "Server OS:   " + server1.get_server_os()
	print "Server Public IP: " + server1.get_server_ip_public()
	print "Server Private IP: " + server1.get_server_ip_private()

