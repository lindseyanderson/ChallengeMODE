#!/usr/bin/python
"""
Basic User Authentication
Using Pyrax, we're going to perform a simple authentication

@inputs:  Username, API Key
@output:  Boolean
@author: Lindsey.Anderson@rackspace.com
"""
import sys
import pyrax
import pyrax.exceptions as exc

def pyrax_auth(username, apikey):
  try:
    pyrax.set_credentials(str(username), str(apikey))
    return True
  except exc.AuthenticationFailed:
    print "Authentication was not successful, please enter your username and API key from your Rackspace Control Panel"
    return False

def verify_input():
  if ( len(sys.argv) != 3 ):
    sys.exit('Usage: %s <username> <apikey>' % sys.argv[0])
  else:
    auth_test = pyrax_auth(sys.argv[1], sys.argv[2])

