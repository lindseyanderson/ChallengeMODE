#!/usr/bin/python
"""
Cloud Server

Making this threaded would be a lot smarter.
"""

import pyrax
import re
import sys, os

class OpenCloudServer:
	def __init__(self):
		self.cs	 = pyrax.cloudservers

	def create_server(self, server_name, server_os, server_size, image_id=None):
		self.server_name = server_name
		self.server_os   = server_os
		self.server_size = int(server_size)
		self.image_id    = image_id
		local_memory = [ memory for memory in self.cs.flavors.list()
					if memory.ram == self.server_size][0]
		if not image_id:
			local_os     = [ image  for image  in self.cs.images.list()
					if self.server_os in image.name][0]
		else:
			local_os     = [ image for image in self.cs.images.list()
					if self.image_id in image.id][0]
		new_server = self.cs.servers.create(self.server_name, local_os.id, local_memory.id)
		self.server_name = new_server.name
		self.root_pass   = new_server.adminPass
		self.server_id   = new_server.id
		print "Building " + str(self.server_name)
		pyrax.utils.wait_until(new_server, "status", ['ACTIVE', 'ERROR'], interval=20, 
					attempts=60, verbose=True)
		self.set_current_server_networks()
	"""
	Returns public IP address of server
	"""
	def get_server_ip_public(self): 
		public_network = self.network[u'public']
		for ip_address in public_network:
			current_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip_address)
			if current_ip: return current_ip[0]

	"""
	Returns private IP address of server
	"""
	def get_server_ip_private(self):
		public_network = self.network[u'private']
		for ip_address in public_network:
			current_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip_address)
			if current_ip: return current_ip[0]		

	"""
	Set Server
	""" 
	def set_current_server_networks(self):
		cs_dfw = pyrax.connect_to_cloudservers(region="ORD")
		cs_ord = pyrax.connect_to_cloudservers(region="DFW")
		dfw_servers = cs_dfw.servers.list()
		ord_servers = cs_ord.servers.list()
		self.servers = dfw_servers + ord_servers
		for server in self.servers:
			if server.name == self.server_name:
				self.network = server.networks	
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
	def get_server_networks(self): return self.network
	"""
	Returns server os
	"""
	def get_server_os(self): return self.server_os
	""" 
	Returns root password	
	"""
	def get_server_admin_pass(self): return self.root_pass

#if __name__ == '__main__':
#	auth.verify_input()
#	
#	print "This is going to happen 3 times, so sit back and relax.  The build process takes upto 400 seconds per server.  Check out /r/cigars in the meantime."
#	server = ['server1','server2','server3']
#	for i in range(3):
#		server[i] = OpenCloudServer()
#		server_name = raw_input("Server Name: ")
#		try:
#			server_size = int(raw_input("Server Size: "))
#		except ValueError:
#			print "Non-integer value entered.  Please try a number."
#			sys.exit(1)
#		server_os	 = raw_input("Server OS  : ")
#		server[i].create_server(server_name, server_os, server_size)	
#		
#	os.system("clear")
#	for i in range(3):
#		print "|"+"-"*68+"|"
#		print "| {0:<32} | {1:<31} |".format(str("Server Name: "), str(server[i].get_server_name()))
#		print "|"+"-"*68+"|"
#		print "| {0:<32} | {1:<31} |".format(str("Server Public IP: "), str(server[i].get_server_ip_public()))
#		print "| {0:<32} | {1:<31} |".format(str("Server Private IP: "), str(server[i].get_server_ip_private()))
#		print "| {0:<32} | {1:<31} |".format(str("Server Root Pass: "), str(server[i].get_server_admin_pass()))
#		print "|"+"-"*68+"|"
