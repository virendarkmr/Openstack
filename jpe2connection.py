
from openstack import connection
import sys
import os
#import openstack
from time import sleep

auth_args = { 'auth_url': 'https://jpe2.jiocloud.com:5000/v3',
              'user_domain_name': 'default',
              'project_domain_name':'default',
              'project_name': 'JioPhone-PUSH-Staging',
              'username': 'Jiophone.Pushstaging',
              'password': '5q9DS7Cg%;a[X.>r'  }

if __name__ == "__main__":
    conn = connection.Connection(verify=False,**auth_args)

############## Server Details ######################

name = 'pushdevtest'

flavor_id = 'm1.small'
flavor = conn.compute.find_flavor(flavor_id)
print (flavor.name)

image_id = 'Centos-7.3'
image = conn.compute.find_image(image_id)
print (image.name)

key_name = 'virenpush'
keypair = conn.compute.find_keypair(key_name)
print (keypair.name)

netname = 'pushdevnet'
network = conn.network.find_network(netname)
print (network.name)

availability_zone = 'JPHONE-ROW3-POD2'

#root volume size
rvolsize= 20

#sec volume size
svolsize = 50

############################ iterator ####################################

#name of server to start from
sernum = 1

#number of server you want to create
sercount = 2


############################# volume and server creation ###################################
  
for i in range (sernum, sernum+sercount):
 sname= name + '-' + str(i)
 volname= name + '-' + str(i)
 vol = conn.block_store.create_volume(name=volname, size=rvolsize, image_id=image.id, is_bootable='boot', availabilty_zone='nova')
 print (vol.name)

 for i in range(5):
  sleep(5)
  vol1 = conn.block_store.get_volume(vol.id)
  if vol1.status=='available': break


 block_device_mapping = [{'boot_index':'0', 'source_type':'volume', 
                         'destination_type':'volume','uuid':vol.id,
                         'delete_on_termination':False}]


 server = conn.compute.create_server(name=name, flavor_id=flavor.id, key_name=key_name, networks=[{"uuid" : network.id}], availability_zone = availability_zone, block_device_mapping=block_device_mapping )

 server = conn.compute.wait_for_server(server)

############################### SG, FIP and vdb2 ###########################################
 security_group = 'NoRestriction'
 sg = conn.network.find_security_group(security_group)
 print (sg.name)
 vname = conn.compute.find_server(name)
 conn.compute.add_security_group_to_server(vname,sg)

 fip = conn.network.find_available_ip()
 print(fip.floating_ip_address)
 conn.compute.add_floating_ip_to_server(server.id,fip.floating_ip_address)


 vol2_name = 'data' + volname
 print (vol2_name)
 vol2 = conn.block_store.create_volume(name=vol2_name, size=svolsize, availabilty_zone='nova')
 for i in range(5):
  sleep(5)
  vol2 = conn.block_store.get_volume(vol2.id)
  if vol2.status=='available': break
 
 conn.compute.create_volume_attachment(server.id,volumeId=vol2.id)

 print ('server ready, happy working!')







#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################


