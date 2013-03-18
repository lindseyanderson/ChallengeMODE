#!/usr/bin/python
"""
Challenge 1
"""
import os
import sys
from imports import auth 
from imports import cloudservers


if __name__ == '__main__':
        auth.verify_input()

        print "This is going to happen 3 times, so sit back and relax.  The build process takes upto 400 seconds per server.  Check out /r/cigars in the meantime."
        server = ['server1','server2','server3']
        for i in range(3):
                server[i] = cloudservers.OpenCloudServer()
                server_name = raw_input("Server Name: ")
                try:
                        server_size = int(raw_input("Server Size: "))
                except ValueError:
                        print "Non-integer value entered.  Please try a number."
                        sys.exit(1)
                server_os        = raw_input("Server OS  : ")
                server[i].create_server(server_name, server_os, server_size)

        os.system("clear")
        for i in range(3):
                print "|"+"-"*68+"|"
                print "| {0:<32} | {1:<31} |".format(str("Server Name: "), str(server[i].get_server_name()))
                print "|"+"-"*68+"|"
                print "| {0:<32} | {1:<31} |".format(str("Server Public IP: "), str(server[i].get_server_ip_public()))
                print "| {0:<32} | {1:<31} |".format(str("Server Private IP: "), str(server[i].get_server_ip_private()))
                print "| {0:<32} | {1:<31} |".format(str("Server Root Pass: "), str(server[i].get_server_admin_pass()))
                print "|"+"-"*68+"|"
