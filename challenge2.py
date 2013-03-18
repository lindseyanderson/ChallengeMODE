#!/usr/bin/python
"""
Challenge 2:
Write a script that clones a server (takes an image and deploys the image as a new server)

@author: Lindsey Anderson
@date  : March 17, 2013
"""
import re
import sys
import pyrax
from imports import cloudservers
from imports import auth


if __name__ == '__main__':
  # auth me!
  auth.verify_input()

  # Setup some static stuffs
  current_server_name = "server1"
  image_name          = current_server_name + "_image"
  new_server_name     = "server1_clone"
  new_server_size     = 512
  
  server              = cloudservers.OpenCloudServer()
  imageID             = server.create_image(image_name, current_server_name)

  # Turns out pyrax has a built in wait_until function
  # Thanks Neill for finding it.  Saves some room (left in for comparison):
  #
  # mine...
  #
  # def image_exists(imageID):
  #   cs = pyrax.cloudservers
  #   tempImage = imageID
  #   for image in cs.images.list():
  #     if imageID == image.id:
  #       if "ACTIVE" == image.status:
  #         time.sleep(10)
  #         return tempImage
  #       elif "SAVING" == image.status:
  #         print "Image is still saving, sleeping 10 seconds and retrying"
  #         time.sleep(10)
  #         image_exists(imageID)
  #       else:
  #         print "STATUS: " + image.status
  #         time.sleep(10)
  #         image_exists(imageID)
  
  # and his...
  status_check = [image for image in pyrax.cloudservers.images.list()
			if imageID == image.id][0]
  pyrax.utils.wait_until(status_check, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=60, verbose=True)
   

  server.create_server(new_server_name, None, new_server_size, imageID)
  # Grab server output
  server.get_server_formatted_details()
