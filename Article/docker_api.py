#!/usr/bin/python3.5
import docker
import time
import os

class CheckpointAlreadyExists(Exception):
    pass

def checkpoint(containers, sequence):
    os.system('rm -rf /tmp/')
    if sequence == 'll' or sequence == 'lf':
        containers = containers[::-1]
    for container in containers:
        os.system('docker checkpoint create --checkpoint-dir /tmp {} {} >> /dev/null'.format(container, container))
        print('Successfully checkpointed {}'.format(container))

def restore(containers, sequence):
    if sequence == 'll' or sequence == 'fl':
        containers = containers[::-1]
    for container in containers:
        os.system('docker start --checkpoint {} {} --checkpoint-dir /tmp'.format(container, container))
        time.sleep(30)
        print('Successfully restored {}'.format(container))

def restart(containers):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    for cont in containers:
        client.restart(cont)
