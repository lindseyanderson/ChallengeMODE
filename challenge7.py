#!/usr/bin/python
"""
Challenge 7:
Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer

@author: Lindsey Anderson
@date  : March 23, 2013
"""
import os
import sys
import pyrax
from imports import auth 
from imports import cloudservers


if __name__ == '__main__':
        auth.verify_input()
	cloud_lb 	= pyrax.cloud_loadbalancers

	#Server Names, update them here or don't hard code them... your choice
        server 		= ['c7server1','c7server2']
	lb_node		= []
        for i in range(2):
	        server_name = str(server[i])
		# whhhhhaaaaaaaa
                server[i] = cloudservers.OpenCloudServer()
		# image name, non-exact
		server_os   = "CentOS 6.3"
		# Server size can be defined as one of the following:
		# 512, 1024, 2048, 4096, 8192, 15872, 30720
		server_size = 512	
                server[i].create_server(server_name, server_os, server_size)
	# Create the node
	lb_node1 = cloud_lb.Node(address=server[0].get_server_ip_private(),
			port=80, condition="ENABLED")
	lb_node2 = cloud_lb.Node(address=server[1].get_server_ip_private(),
			port=80, condition="ENABLED")

	# Create a new Cloud Load Balancer
	lb_name 	= "c7lb"
	lb_vip	 	= cloud_lb.VirtualIP(type="PUBLIC")
	loadbalancer 	= cloud_lb.create(lb_name, port=80, protocol="HTTP",
				nodes=[lb_node1, lb_node2], virtual_ips=[lb_vip])
	print "Load Balancer {0} created.".format(str(loadbalancer.name))
