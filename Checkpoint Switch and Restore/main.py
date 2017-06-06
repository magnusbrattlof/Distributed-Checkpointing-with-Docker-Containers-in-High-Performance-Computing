#!/usr/bin/python2.7
import checkpoint
import time
import os

containers = ['checkpoint01', 'checkpoint02', 'checkpoint03', 'checkpoint04',
              'checkpoint05', 'checkpoint06', 'checkpoint07', 'checkpoint08']
local = containers[:4]
remote = containers[4:]
seq = 'ff'
app = 'cg.C.8'
test = 0

while test is not 4:
    test += 1
    for i in range(1, 2):
        if test == 2:
            seq = 'll'
        elif test == 3:
            seq = 'fl'
        elif test == 4:
            seq = 'lf'
        checkpoint.restart(containers, local, remote)
        os.system('rm -rf /home/hpc/nfs/checkpoint0*')
        checkpoint.route()
        checkpoint.start_job('192.168.16.2', 8, containers, app, seq, str(i))
        time.sleep(60)
        checkpoint.checkpoint(containers, '/home/hpc/nfs', seq)
        checkpoint.route(True)
        time.sleep(30)
        os.system('sync')
        os.system("ssh guma02 'sync'")
        checkpoint.restore(containers, '/home/hpc/nfs', seq)
        time.sleep(180)
        print 'Done with iteration'
