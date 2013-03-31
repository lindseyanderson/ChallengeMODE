#!/usr/bin/python
"""
Challenge 10
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page. 
- Create a DNS record based on a FQDN for the LB VIP. 
- Write the error page html to a file in cloud files for backup.

"""
import time
import pyrax
import pyrax.exceptions as exc
from imports import auth
from imports import cloudservers

if __name__ == '__main__':
	
	auth.verify_input()
	cs   = pyrax.cloudservers
	clb  = pyrax.cloud_loadbalancers
	cdns = pyrax.cloud_dns
	cf   = pyrax.cloudfiles
	fqdn_input = "challenge10.justcurl.com"

	image = [img for img in cs.images.list()
        	if "CentOS 6.3" in img.name][0]
	size  = [flavor for flavor in cs.flavors.list()
       		if flavor.ram == 512][0]
	# This is the data we'll be adding to the new servers
	public_key_data = """ SSH KEY DATA """
	files = { "/root/.ssh/authorized_keys" : public_key_data }

	# Create 2 new servers
	server_list = []
	for ittid in range(2):
		server_name = "Challenge10-Server" + str(ittid + 1)
		print "Creating", server_name
		new_server = cs.servers.create(server_name, image.id, size.id, files=files)
		pyrax.utils.wait_until(new_server, "status", ['ACTIVE', 'ERROR'], interval=20, 
					attempts=60, verbose=True)
		server_list.append(new_server)
		print "Server", server_name, "completed."
			
	# Create a new Cloud Files container, input our error page
	container_name = "Challenge10-Container"
	print "Creating container", container_name
	container = cf.create_container(container_name)	
	# Enable the CDN
	container.make_public(ttl=1200)	

	# Upload custom error page:
	error_page = """<html>
	<head><title>Challenge 10 - Custom Error</title></head>
	<body>
		Custom Error Page Here.
	</body>
	</html>
	"""
	error_object = cf.store_object(container, "error.html", error_page)
	print "Error page has been added to", container.name, "for backup."
	print "Download here:", container.cdn_uri + "/error.html"
	
	# Create a Load Balancer
	lb_name  = "Challenge10-LB"
	lb_nodes = []
	print "Creating", lb_name
	lb_vip	 = clb.VirtualIP(type="PUBLIC")
	# we have to do some magic to repopulate the server network list 
	cs_dfw = pyrax.connect_to_cloudservers(region="ORD")
	cs_ord = pyrax.connect_to_cloudservers(region="DFW")
	new_server_list = cs_dfw.servers.list() + cs_ord.servers.list()

	for count,server in enumerate(server_list):
		for nserver in new_server_list:
			if server.id == nserver.id:
				private_ip = nserver.networks['private'][0]
		lb_nodes.append(clb.Node(address=private_ip, port=80, condition="ENABLED"))

	loadbalancer = clb.create(lb_name, port=80, protocol="HTTP",
				nodes=[lb_nodes[0], lb_nodes[1]], virtual_ips=[lb_vip])
	pyrax.utils.wait_until(loadbalancer, "status", ['ACTIVE', 'ERROR'], interval=20,
					attempts=60, verbose=True)
	print "Load balancer", loadbalancer.name, "created."
	lb_vip = loadbalancer.virtual_ips[0].address
	print "Load balancer IP",lb_vip 
	# Add a health monitor to the load balancer
	loadbalancer.add_health_monitor(type="CONNECT", delay=5, timeout=30)
	print "Load balancer health monitor added."
	# Add a new error page
	# we have to sleep first, otherwise it will be immutable
	pyrax.utils.wait_until(loadbalancer, "status", ['ACTIVE', 'ERROR'], interval=20,
					attempts=60, verbose=True)
	loadbalancer.set_error_page(error_page)
	print "Load balancer error page added."


	# Create a FQDN to point to the VIP of the load balancer
        try:
                domain = dns.find(name=fqdn_input)
        except exc.NotFound:
                try:
                        domain = cdns.create(name=fqdn_input, emailAddress="ipadmin@stabletransit.net",
                                ttl=300, comment=fqdn_input)
                except exc.DomainCreationFailed as ex:
                        print "!! Domain could not be created:", ex
                        sys.exit(1)
                print "Domain created: {0}.".format(str(domain.name))

        # create the dict for the record
        arecord = {"type": "A",
                   "name": fqdn_input,
                   "data": lb_vip,
                   "ttl": 300}

        # try to create the record for the domain
        try:
                domain.add_records(arecord)
                print "A Record added successfull!"
        except exc.DomainRecordAdditionFailed as ex:
                print "Record could not be added:", ex	
