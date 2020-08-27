
from openstack import connection
import sys
import os
from time import sleep
import time

auth_args = { 'auth_url': 'https://jpe2.jiocloud.com:5000/v3',
              'user_domain_name': 'default',
              'project_domain_name':'default',
              'project_name': 'JIOPHONE-COMMONSERVICES',
              'username': '',
              'password': ''  }

if __name__ == "__main__":
 
 conn = connection.Connection(verify=False,**auth_args)
 #volname='viren_vol_1' 
 #vol=conn.block_store.volumes(name=volname)
 #print (list(vol))
 
 server = 'Viren_System'
 serverid = conn.compute.find_server(server)
 #print (serverid) 
 
 serverdetails = conn.compute.get_server(serverid.id)
 volumes = serverdetails.attached_volumes

######################creating snapshot###############################

 for i in range(len(volumes)):
  volid = volumes[i]['id']
  vol=conn.block_store.get_volume(volid)
 # snapshot_name='snapshot'+'-'+vol.name+'-'+str(time.strftime("%d%m%y"))
 # snapshot=conn.block_store.create_snapshot(volume_id=volid,name=snapshot_name,is_forced=True) 
 # 
 # for i in range(5):
 #  sleep(5)
 #  snapshot=conn.block_store.get_snapshot(snapshot.id)
 #  if snapshot.status=='available' : break

####################### Deleting old snapshot#########################
  old_snapshot =  conn.block_store.snapshots(volume_id=volid))   



  #conn.block_store
  #print (volumes[i]['id'])
  
   
 #volume = conn.
 
 #vol='d6d249e5-4605-4ed6-bfe1-88ed12680b18'
 #

 #ssname='viren-snapshot1'+str(date)
 #serverid='cba7a2cc-7618-4f66-b6e3-51f6a4b2c409'

 #print ('#########creating snapshot##########')

 #
 #
 #sp=conn.block_store.create_snapshot(volume_id=vol,name=ssname,is_forced=True)
 #
 #for i in range(5):
 # sleep(5)
 # snapshot  = conn.block_store.get_snapshot(sp.id)
 # if snapshot.status=='available': break
 #
 #print ('#######Snapshot Created########')

 #
 #
