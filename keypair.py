
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
try:
 keypair = raw_input('Enter key name: ')

 check = conn.compute.find_keypair(str(keypair), ignore_missing=False)

 print ('Key found ' , check.name)

except :

 print ('Error!!! key not founf')

 ans = raw_input('Enter y/n to create key: ')
 if ans == 'y':
  key = conn.compute.create_keypair(name=keypair)
  filename = keypair+'.pem'
  file = open(filename,"w")
  file.write(key.private_key)
  file.close()
  print ('private key downloaded' + filename)
 elif ans == 'n':
  print ('closed')
 else:
  print ('please enter correct option')

