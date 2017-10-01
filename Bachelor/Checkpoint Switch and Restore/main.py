#!/usr/bin/python2.7
import checkpoint
import time
import os

# Containers to be checkpointed
containers = ['cont01', 'cont02', 'cont03', 'cont04',
              'cont05', 'cont06', 'cont07', 'cont08']

# Containers which are located where the script is executing (Alpha)
local = containers[:4]
# Remote containers (Beta)
remote = containers[4:]
# Which sequence to start with
seq = 'ff'
# NPB application
app = 'cg.C.8'
# Init
test = 0

while test is not 4:
    # Edit sequence after 100 iterations
    test += 1
    for i in range(1, 101):
        if test == 2:
            seq = 'll'
        elif test == 3:
            seq = 'fl'
        elif test == 4:
            seq = 'lf'
        # Restart containers, remove any potential erros with old processes still executing
        checkpoint.restart(containers, local, remote)
        # Remove old checkpoints from NFS
        os.system('rm -rf /home/hpc/nfs/checkpoint0*')
        # Restore the routes
        checkpoint.route()
        # Start the job within selected container
        checkpoint.start_job('192.168.16.2', 8, containers, app, seq, str(i))
        time.sleep(60)
        # Checkpoint containers, select which location and sequence
        checkpoint.checkpoint(containers, '/home/hpc/nfs', seq)
        # Reroute
        checkpoint.route(True)
        time.sleep(30)
        # Make sure everything is written to disk
        os.system('sync')
        os.system("ssh guma02 'sync'")
        # Restore containers, from where and which sequence
        checkpoint.restore(containers, '/home/hpc/nfs', seq)
        time.sleep(180)
        print 'Done with iteration {}'.format(i)
