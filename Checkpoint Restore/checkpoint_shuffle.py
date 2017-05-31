#!/usr/bin/python2.7
from random import shuffle
import time
import os
 
def main():
    global containers, local_containers
    local_containers = ['cont01', 'cont02', 'cont03', 'cont04']
    for i in range(1,11):
        print 'On iteration', i
        containers = ['cont01', 'cont02', 'cont03', 'cont04', 'cont05', 'cont06', 'cont07', 'cont08']
        # Shuffle containers (cont02 - cont07)
        to_shuffle = containers[1:]
        shuffle(to_shuffle)
        containers = [containers[0]] + to_shuffle
        # Remove checkpoints
        remove()
        # Restart containers
        restart()
        time.sleep(2)
        # Start MPI within container 01
        print 'Started MPI within cont01'
        os.system("ssh cont01 'mpirun -n 8 -f /hpc/hostfiles/extpause /hpc/cg.C.8 >> /tmp/yum.log & exit'")
        # Checkpoint containers
        time.sleep(30)
        checkpoint()
        time.sleep(30)
        # Reverse the order
        containers = reversed(containers)
        # Restore containers one by one
        restore()
        time.sleep(100)
 
def checkpoint():
    for container in containers:
        if container in local_containers:
            os.system('docker checkpoint create {} c1 > /dev/null'.format(container))
        else:
            os.system("ssh guma02 'docker checkpoint create {} c1 > /dev/null'".format(container))
        print 'Checkpointed container:', container
 
def restore():
    for container in containers:
        if container in local_containers:
            os.system('docker start --checkpoint c1 {}'.format(container))
            time.sleep(30)
        else:
            os.system("ssh guma02 'docker start --checkpoint c1 {}'".format(container))
            time.sleep(30)
        print 'Restored container:', container
 
def remove():
    print 'Removing checkpoints'
    for container in containers:
        if container in local_containers:
            os.system('docker checkpoint rm {} c1'.format(container))
        else:
            os.system("ssh guma02 'docker checkpoint rm {} c1'".format(container))
 
def restart():
    print 'Restarting checkpoints'
    for container in containers:
        if container in local_containers:
            os.system('docker restart {} > /dev/null'.format(container))
        else:
            os.system("ssh guma02 'docker restart {} > /dev/null'".format(container))
 
if __name__ == '__main__':
    main()
 
