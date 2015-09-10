#!/usr/bin/env python
from datetime import datetime
import os
import pyrax
import sys
import time

from pprint import pprint

commit = os.environ['OSAD_SHA']
instance_name = "openstack-ansible-{0}".format(commit)

print("Looking for an instance named: {0}".format(instance_name))

pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("~/.pyrax")
pyrax.set_credential_file(creds_file)
cs = pyrax.connect_to_cloudservers(region='IAD')
img = pyrax.connect_to_images(region='IAD')

print("Requesting a snapshot...")
listing = [x for x in cs.servers.list() if x.name == instance_name]
server = listing[0]
try:
    image = cs.servers.create_image(server.id, server.name)
except Exception as e:
    print("Looks like the image has already started -- monitoring it...")

while True:
    image = img.list(name=server.name)[0]
    datestring = datetime.now().isoformat(' ')
    if image.status == 'active':
        print("{0} - Image active!".format(datestring))
        break
    print("{0} - Image not active yet...".format(datestring))
    time.sleep(60)
