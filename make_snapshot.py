#!/usr/bin/env python
import os
import pyrax
import time

from pprint import pprint

commit = os.environ['OSAD_SHA']
instance_name = "openstack-ansible-{0}".format(commit)

pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("~/.pyrax")
pyrax.set_credential_file(creds_file)
cs = pyrax.connect_to_cloudservers(region='IAD')
img = pyrax.connect_to_images(region='IAD')

print("Requesting a snapshot...")
server = next(x for x in cs.servers.list() if x.name == instance_name)
image = cs.servers.create_image(server.id, server.name)

while True:
    image = img.list(name=server.name)[0]
    pprint(image)
    if image.status == 'active':
        print("Image active!")
        break
    print("Image not active yet...")
    time.sleep(5)
