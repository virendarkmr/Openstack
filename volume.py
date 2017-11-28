
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


#############################################################
server_name='devpushelk-1'

server=conn.compute.find_server(server_name)

print ('server_id : '+ server.id)

vol_attachment=conn.compute.volume_attachments(server.id)


for volatt in vol_attachment:
 if volatt.device=='/dev/vda':
  print('root vol skiping')
 else: 
  print(volatt.device + ' ' +volatt.id)
  #conn.compute.delete_volume_attachment(volatt.id,server.id) 
