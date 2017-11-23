
from openstack import connection
import sys
import os
#import openstack
from time import sleep

auth_args = { 'auth_url': 'https://jpe2.jiocloud.com:5000/v3',
              'user_domain_name': 'default',
              'project_domain_name':'default',
              'project_name': 'JioPhone-Push-Prod',
              'username': 'JioPhone-Push-Prod',
              'password': '9)n8Kw`a%8cA.{wJ'  }

if __name__ == "__main__":
    conn = connection.Connection(verify=False,**auth_args)

############## Server Details ######################

name = 'prod-jmn-push-rep'

flavor_id = 'm1.medium'
flavor = conn.compute.find_flavor(flavor_id)
print ('Falvor : ' + flavor.name)

image_id = 'Centos-7.3'
image = conn.compute.find_image(image_id)
print ('image : '+ image.name)

key_name = 'PushProd'
keypair = conn.compute.find_keypair(key_name)
print ('Keypair : '+ keypair.name)

netname = 'PushProdFinal'
network = conn.network.find_network(netname)
print ('network name : ' + network.name)


print ('======================================')

azone = 'JPHONE-ROW3-POD'

#root volume size
rvolsize= 10

#sec volume size
svolsize = 50

############################ iterator ####################################

#name of server to start from
sernum = 52

#number of server you want to create
sercount = 15


############################# volume and server creation ###################################
  
for i in range (sernum, sernum+sercount):
 nzone=(i%3)+1
 zone=azone+str(nzone) 
 sname= name + '-' + str(i)
 volname= name + '-' + str(i)
 
 vol = conn.block_store.create_volume(name=volname, size=rvolsize, image_id=image.id, is_bootable='boot', availabilty_zone='nova')
 print ('volume : ' + vol.name)

 for i in range(6):
  sleep(6)
  vol1 = conn.block_store.get_volume(vol.id)
  if vol1.status=='available': break


 block_device_mapping = [{'boot_index':'0', 'source_type':'volume', 
                         'destination_type':'volume','uuid':vol.id,
                         'delete_on_termination':False}]


 server = conn.compute.create_server(name=sname, flavor_id=flavor.id, key_name=key_name, networks=[{"uuid" : network.id}], availability_zone=zone, block_device_mapping=block_device_mapping )

 server = conn.compute.wait_for_server(server)

############################### SG, FIP and vdb2 ###########################################
 security_group = 'Restricted'
 sg = conn.network.find_security_group(security_group)
 print ('Security Group : ' + sg.name)
 conn.compute.add_security_group_to_server(server.id,sg)
 
### below code will assign the existing free floating IP
### if uncommented pleae comment create floating IP lines
# fip=conn.network.ips(fixed_ip_address='None')
# for ip in fip:
#  if ip.fixed_ip_address==None:
#   float_ip=ip.floating_ip_address 
#   print ('floating ip : ' + float_ip)
#   break
# conn.compute.add_floating_ip_to_server(server.id,float_ip)


### below code will create new floating IP and assign it to server
### if used please comment the above floating IP code.
 extnet=conn.network.find_network('ext-net')
 float_ip=conn.network.create_ip(floating_network_id=extnet.id)
 print ('floating_ip : ' + float_ip.floating_ip_address)
 conn.compute.add_floating_ip_to_server(server.id,float_ip.floating_ip_address)

 
 vol2_name = 'data' + volname
 print ('secondary vol : ' + vol2_name)
 vol2 = conn.block_store.create_volume(name=vol2_name, size=svolsize, availabilty_zone='nova')
 for i in range(5):
  sleep(5)
  vol2 = conn.block_store.get_volume(vol2.id)
  if vol2.status=='available': break
 
 conn.compute.create_volume_attachment(server.id,volumeId=vol2.id)

 print ('server ready, happy deploying!')
 
 print ('==============================================')

 #apend the floating ip to a file for ansible use.
 file = open("newcephost","a+") 
 fip = float_ip.floating_ip_address
 file.write(fip)
 file.close()



#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################


