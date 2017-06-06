#!/usr/bin/python2.7
import checkpoint
import time
import os

# Containers to be checkpointed and moved
containers = ['cont01', 'cont02', 'cont03', 'cont04',
              'cont05', 'cont06', 'cont07', 'cont08']
# Containers on the node where the script executes (Alpha)
local = containers[:4]
# Containers on the remote node (Beta)
remote = containers[4:]
app = 'cg.C.8'

for i in range(1, 101):
    # Restart containers, remove potential processes still executing
    checkpoint.restart(containers, local, remote)
    # Delete old checkpoints from NFS
    os.system('rm -rf /home/hpc/nfs/checkpoint0*')
    # Restore routes
    checkpoint.route()
    # Start the job within the selected container
    checkpoint.start_job('192.168.16.2', 8, containers, app)
    # Let it execute for 60s, this is application specific
    time.sleep(60)
    # Checkpoint all containers, select where to store them
    checkpoint.checkpoint(containers, '/home/hpc/nfs')
    # Reroute 
    checkpoint.route(True)
    time.sleep(30)
    # Make sure everything is written to disk
    os.system('sync')
    os.system("ssh guma02 'sync'")
    # Restore the containers
    checkpoint.restore(containers, '/home/hpc/nfs')
    # Give them 180s to finish, then restart everything
    time.sleep(180)
    print 'Done with iteration {}'.format(i)
