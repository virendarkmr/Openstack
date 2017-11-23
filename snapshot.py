
from openstack import connection
import sys
import os
from time import sleep

auth_args = { 'auth_url': 'https://jpe2.jiocloud.com:5000/v3',
              'user_domain_name': 'default',
              'project_domain_name':'default',
              'project_name': 'JIOPHONE-COMMONSERVICES',
              'username': 'JioPhone.commonservices',
              'password': '&h^J4Qn4y+\^?t)N'  }

if __name__ == "__main__":
 conn = connection.Connection(verify=False,**auth_args)
 #volname='viren_vol_1' 
 #vol=conn.block_store.volumes(name=volname)
 #print (list(vol))
 #vol='d6d249e5-4605-4ed6-bfe1-88ed12680b18'
 vol='f2954567-f0a3-4072-8206-72f042af50f9'
 ssname='viren-snapshot1'
 serverid='cba7a2cc-7618-4f66-b6e3-51f6a4b2c409'

 print ('#########creating snapshot##########')

 
 
 sp=conn.block_store.create_snapshot(volume_id=vol,name=ssname,is_forced=True)
 
 for i in range(5):
  sleep(5)
  snapshot  = conn.block_store.get_snapshot(sp.id)
  if snapshot.status=='available': break
 
 print ('#######Snapshot Created########')

 
 
