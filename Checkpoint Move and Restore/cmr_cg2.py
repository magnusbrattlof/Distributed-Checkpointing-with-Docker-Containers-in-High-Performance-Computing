#!/usr/bin/python2.7

import os
import time
import paramiko

cf_rl = ['checkpoint01', 'checkpoint02']
cl_rf = ['checkpoint02', 'checkpoint01']

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('guma02', username='root', password='VMware6rox!23')
sftp = ssh.open_sftp()

def main():
    # CF RL
    for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 2 -hosts checkpoint01,checkpoint02 /hpc/cg.C.2 >> /tmp/yum.log & exit'")
        time.sleep(120)
        checkpoint(1)
        os.system('sync')
        time.sleep(10)
        move()
        os.system("ssh guma02 'sync'")
        time.sleep(10)
        restore(1)
        time.sleep(120)
        for x in range(1,11):
            os.system("ssh guma02 'docker exec checkpoint01 sync'")
            os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cg2_cf_rl_robust.{}.{}'".format(i, x))
            size = sftp.stat('/var/lib/docker/volumes/hpc/_data/logs/cmr_scp/cg2_cf_rl_robust.{}.{}'.format(i, x))
            os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
            if size.st_size == 0:
                print 'Size was 0, on try: {}'.format(x)
                restart()
                time.sleep(10)
                restore(1)
                time.sleep(120)
            else:
                print '{} iteration successful after {} tries'.format(i, x)
                break
        os.system("rm -rf /tmp/checkpoint0* ; ssh guma02 'rm -rf /tmp/checkpoint0*'")
        restart()
        time.sleep(10)
    # CL RF
    for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 2 -hosts checkpoint01,checkpoint02 /hpc/cg.C.2 >> /tmp/yum.log & exit'")
        time.sleep(120)
        checkpoint(2)
        os.system('sync')
        time.sleep(10)
        move()
        os.system("ssh guma02 'sync'")
        time.sleep(10)
        restore(2)
        time.sleep(120)
        for x in range(1,11):
            os.system("ssh guma02 'docker exec checkpoint01 sync'")
            os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cg2_cl_rf_robust.{}.{}'".format(i, x))
            size = sftp.stat('/var/lib/docker/volumes/hpc/_data/logs/cmr_scp/cg2_cl_rf_robust.{}.{}'.format(i, x))
            os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
            if size.st_size == 0:
                print 'Size was 0, on try: {}'.format(x)
                restart()
                time.sleep(10)
                restore(2)
                time.sleep(120)
            else:
                print '{} iteration successful after {} tries'.format(i, x)
                break
        os.system("rm -rf /tmp/checkpoint0* ; ssh guma02 'rm -rf /tmp/checkpoint0*'")
        restart()
        time.sleep(10)

def checkpoint(number):
    if number == 1:
        for cont in cf_rl:
            os.system('docker checkpoint create --checkpoint-dir=/tmp {} {} > /dev/null'.format(cont, cont))
            print 'Checkpointed container: {}'.format(cont)
    elif number == 2:
        for cont in cl_rf:
            os.system('docker checkpoint create --checkpoint-dir=/tmp {} {} > /dev/null'.format(cont, cont))
            print 'Checkpointed container: {}'.format(cont)

def restore(number):
    if number == 1:
        for cont in reversed(cf_rl):
            os.system("ssh guma02 'docker start --checkpoint-dir=/tmp --checkpoint={} {}'".format(cont, cont))
            print 'Restored container: {}'.format(cont)
            time.sleep(30)
    elif number == 2:
        for cont in reversed(cl_rf):
            os.system("ssh guma02 'docker start --checkpoint-dir=/tmp --checkpoint={} {}'".format(cont, cont))
            print 'Restored container: {}'.format(cont)
            time.sleep(30)

def move():
    os.system('scp -r /tmp/checkpoint01 guma02:/tmp > /dev/null')
    print 'Moved checkpoint01'
    os.system('scp -r /tmp/checkpoint02 guma02:/tmp > /dev/null')
    print 'Moved checkpoint02'

def restart():
    print 'Restarting containers'
    os.system("docker restart checkpoint01 checkpoint02  ; \
    ssh guma02 'docker restart checkpoint01 checkpoint02 ; \
    docker stop checkpoint01 checkpoint02'")

if __name__ == '__main__':
    main()