#!/usr/bin/python
"""
Challenge 1
Lindsey Anderson
"""
import os
import sys
from imports import auth 
from imports import cloudservers


if __name__ == '__main__':
	# Everyone loves to auth!  
        auth.verify_input()

        print "This is going to happen 3 times, so sit back and relax.  The build process takes upto 400 seconds per server."
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
                print "| {0:<32} | {1:<31} |".format(str("Server Root Pass: "), str(server[i].get_server_admin_pass()))
                print "|"+"-"*68+"|"
