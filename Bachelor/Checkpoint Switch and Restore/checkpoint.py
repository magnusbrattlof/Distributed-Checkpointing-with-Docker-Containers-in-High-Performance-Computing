#!/usr/bin/python2.7

# Function folder for bachelor thesis
import time
import os


def start_job(master, cores, container, app, seq, iteration):
    os.system("ssh 193.10.203.179 'touch /var/lib/docker/volumes/hpc/_data/logs/CG/log_{}_{}.{}'".format(app, seq, iteration))
    os.system("ssh {} 'mpirun -n {} -hosts {} /hpc/{} >> /hpc/logs/CG/log_{}_{}.{} & exit'".format(master, cores, ",".join(container), app, app, seq, iteration))

def checkpoint(containers, path, seq):
    local = containers[:4]
    remote = containers[4:]
    if seq in 'll' or seq in 'lf':
        for container in reversed(containers):
            if container in local:
                os.system('docker checkpoint create --checkpoint-dir={} {} {} > /dev/null'.format(path, container, container))
                print 'Checkpoint: {}'.format(container)
            else:
                os.system("ssh {} 'docker checkpoint create --checkpoint-dir={} {} {} > /dev/null'".format('193.10.203.179', path, container, container))
                print 'Checkpoint: {}'.format(container)
    else:
        for container in containers:
            if container in local:
                os.system('docker checkpoint create --checkpoint-dir={} {} {} > /dev/null'.format(path, container, container))
                print 'Checkpoint: {}'.format(container)
            else:
                os.system("ssh {} 'docker checkpoint create --checkpoint-dir={} {} {} > /dev/null'".format('193.10.203.179', path, container, container))
                print 'Checkpoint: {}'.format(container)


def restore(containers, path, seq):
    local = containers[:4]
    remote = containers[4:]
    if seq in 'fl' or seq in 'll':
        for container in reversed(containers):
            if container in local:
                os.system("ssh {} 'docker start --checkpoint-dir={} --checkpoint={} {}'".format('193.10.203.179', path, container, container))
                print 'Restored: {}'.format(container)
                time.sleep(30)
            else:
                os.system('docker start --checkpoint-dir={} --checkpoint={} {}'.format(path, container, container))
                print 'Restored: {}'.format(container)
                time.sleep(30)
    else:
        for container in containers:
            if container in local:
                os.system("ssh {} 'docker start --checkpoint-dir={} --checkpoint={} {}'".format('193.10.203.179', path, container, container))
                print 'Restored: {}'.format(container)
                time.sleep(30)
            else:
                os.system('docker start --checkpoint-dir={} --checkpoint={} {}'.format(path, container, container))
                print 'Restored: {}'.format(container)
                time.sleep(30)


def restart(container, local, remote):
    # Local
    for c in container:
        os.system('docker restart {} > /dev/nulll'.format(c))
    for c in remote:
        os.system('docker stop {} > /dev/nulll'.format(c))
    # Remote
    for c in container:
        os.system("ssh {} 'docker restart {} > /dev/nulll'".format('193.10.203.179', c))
    for c in local:
        os.system("ssh {} 'docker stop {} > /dev/nulll'".format('193.10.203.179', c))
    print 'Restared containers'
def route(route=False):
    if route == True:
        os.system("ip route replace 192.168.10.0/24 via 192.168.10.1 ;\
         ip route replace 192.168.16.0/24 via 193.10.203.179 ; \
         ssh guma02 'ip route replace 192.168.16.0/24 via 192.168.16.1 \
         ; ip route replace 192.168.10.0/24 via 193.10.203.233'")
    else:
        os.system("ip route replace 192.168.16.0/24 via 192.168.16.1 ;\
        ip route replace 192.168.10.0/24 via 193.10.203.179 ; \
        ssh guma02 'ip route replace 192.168.10.0/24 via 192.168.10.1 \
        ; ip route replace 192.168.16.0/24 via 193.10.203.233'")
