#!/usr/bin/python2.7
import checkpoint
import time
import os

containers = ['cont01', 'cont02', 'cont03', 'cont04',
              'cont05', 'cont06', 'cont07', 'cont08']
local = containers[:4]
remote = containers[4:]
app = 'cg.C.8'

for i in range(1, 101):
    checkpoint.restart(containers, local, remote)
    os.system('rm -rf /home/hpc/nfs/checkpoint0*')
    checkpoint.route()
    checkpoint.start_job('192.168.16.2', 8, containers, app)
    time.sleep(60)
    checkpoint.checkpoint(containers, '/home/hpc/nfs')
    checkpoint.route(True)
    time.sleep(30)
    os.system('sync')
    os.system("ssh guma02 'sync'")
    checkpoint.restore(containers, '/home/hpc/nfs')
    time.sleep(180)
    print 'Done with iteration'
