#!/usr/bin/python
"""
Challenge 1:
Write a script that builds three 512 MB Cloud Servers that following a similar naming 
convention. (ie., web1, web2, web3) and returns the IP and login credentials for each 
server. Use any image you want.

@author: Lindsey Anderson
@date  : March 17, 2013
"""
import os
import sys
from imports import auth 
from imports import cloudservers


if __name__ == '__main__':
	# Everyone loves to auth!  
        auth.verify_input()

        print "This is going to happen 3 times, so sit back and relax.  The build process can take upto 400 seconds per server."
	print "Check out /r/cigars in the meantime."
	
	#Server Names, update them here or don't hard code them... your choice
        server = ['server1','server2','server3']
        for i in range(3):
	        server_name = str(server[i])
		# whhhhhaaaaaaaa
                server[i] = cloudservers.OpenCloudServer()
		# image name, non-exact
		server_os   = "CentOS 6.3"
		# Server size can be defined as one of the following:
		# 512, 1024, 2048, 4096, 8192, 15872, 30720
		server_size = 512	
                server[i].create_server(server_name, server_os, server_size)

        os.system("clear")
        for i in range(3):
		# pretty formatting is a must
                print "|"+"-"*68+"|"
                print "| {0:<32} | {1:<31} |".format(str("Server Name: "), str(server[i].get_server_name()))
                print "| {0:<32} | {1:<29}MB |".format(str("Server Size: "), str(server[i].get_server_size()))
                print "|"+"-"*68+"|"
                print "| {0:<32} | {1:<31} |".format(str("Server Public IP: "), str(server[i].get_server_ip_public()))
                print "| {0:<32} | {1:<31} |".format(str("Server Private IP: "), str(server[i].get_server_ip_private()))
                print "| {0:<32} | {1:<31} |".format(str("Server Username: "), str("root"))
                print "| {0:<32} | {1:<31} |".format(str("Server Password: "), str(server[i].get_server_admin_pass()))
                print "|"+"-"*68+"|"
