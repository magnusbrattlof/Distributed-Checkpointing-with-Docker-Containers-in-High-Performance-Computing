#!/usr/bin/python2.7

import os
import time

cf_rl = ['checkpoint01', 'checkpoint02', 'checkpoint03', 'checkpoint04']
cl_rf = ['checkpoint04', 'checkpoint03', 'checkpoint02', 'checkpoint01']
cf_rf = ['checkpoint01', 'checkpoint02', 'checkpoint03', 'checkpoint04']
cl_rl = ['checkpoint04', 'checkpoint03', 'checkpoint02', 'checkpoint01']

def main():
    # CF RL
    for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 4 -hosts checkpoint01,checkpoint02,checkpoint03,checkpoint04 /hpc/cg.C.4 >> /tmp/yum.log & exit'")
        time.sleep(60)
        checkpoint(1)
        time.sleep(90)
        os.system('sync')
        move()
        os.system("ssh guma02 'sync'")
        time.sleep(60)
        restore(1)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cf_rl.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        time.sleep(10)
        restore(1)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cf_rl_robust.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        os.system("rm -rf /tmp/checkpoint0* ; 'ssh guma02 rm -rf /tmp/checkpoint0*'")
        time.sleep(10)
   # CL RF
    '''for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 4 -hosts checkpoint01,checkpoint02,checkpoint03,checkpoint04 /hpc/cg.C.4 >> /tmp/yum.log & exit'")
        time.sleep(60)
        checkpoint(2)
        time.sleep(120)
        restore(2)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cl_rf.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        time.sleep(10)
        restore(2)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cl_rf_robust.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        os.system('rm -rf /tmp/checkpoint0*')
        time.sleep(10)
    # CF RF
    for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 4 -hosts checkpoint01,checkpoint02,checkpoint03,checkpoint04 /hpc/cg.C.4 >> /tmp/yum.log & exit'")
        time.sleep(60)
        checkpoint(3)
        time.sleep(120)
        restore(3)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cf_rf.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        time.sleep(10)
        restore(3)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cf_rf_robust.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        os.system('rm -rf /tmp/checkpoint0*')
        time.sleep(10)
    # CL RL
    for i in range(1,11):
        os.system("ssh 192.168.16.2 'mpirun -n 4 -hosts checkpoint01,checkpoint02,checkpoint03,checkpoint04 /hpc/cg.C.4 >> /tmp/yum.log & exit'")
        time.sleep(60)
        checkpoint(4)
        time.sleep(120)
        restore(4)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cl_rl.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        time.sleep(10)
        restore(4)
        time.sleep(120)
        os.system("ssh guma02 'docker exec checkpoint01 cp /tmp/yum.log /hpc/logs/cmr_scp/cl_rl_robust.{}'".format(i))
        os.system("ssh guma02 'docker exec checkpoint01 rm -rf /tmp/yum.log ; docker exec checkpoint01 touch /tmp/yum.log'")
        restart()
        os.system('rm -rf /tmp/checkpoint0*')
        time.sleep(10)'''

def checkpoint(number):
    if number == 1:
        for cont in cf_rl:
            os.system('docker checkpoint create --checkpoint-dir=/tmp {} {} > /dev/null'.format(cont, cont))
            print 'Checkpointed container: {}'.format(cont)
    elif number == 2:
        for cont in cl_rf:
            os.system('docker checkpoint create --checkpoint-dir=/tmp {} {} > /dev/null'.format(cont, cont))
            print 'Checkpointed container: {}'.format(cont)
    elif number == 3:
        for cont in cf_rf:
            os.system('docker checkpoint create --checkpoint-dir=/tmp {} {} > /dev/null'.format(cont, cont))
            print 'Checkpointed container: {}'.format(cont)
    else:
        for cont in cl_rl:
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
    elif number == 3:
        for cont in cf_rf:
            os.system("ssh guma02 'docker start --checkpoint-dir=/tmp --checkpoint={} {}'".format(cont, cont))
            print 'Restored container: {}'.format(cont)
            time.sleep(30)
    else:
        for cont in cl_rl:
            os.system("ssh guma02 'docker start --checkpoint-dir=/tmp --checkpoint={} {}'".format(cont, cont))
            print 'Restored container: {}'.format(cont)
            time.sleep(30)
def move():
    os.system('scp -r /tmp/checkpoint01 guma02:/tmp > /dev/null')
    print 'Moved checkpoint01'
    os.system('scp -r /tmp/checkpoint02 guma02:/tmp > /dev/null')
    print 'Moved checkpoint02'
    os.system('scp -r /tmp/checkpoint03 guma02:/tmp > /dev/null')
    print 'Moved checkpoint03'
    os.system('scp -r /tmp/checkpoint04 guma02:/tmp > /dev/null')
    print 'Moved checkpoint04'

def restart():
    print 'Restarting containers'
    os.system("docker restart checkpoint01 checkpoint02 checkpoint03 checkpoint04 ; \
    ssh guma02 'docker restart checkpoint01 checkpoint02 checkpoint03 checkpoint04 ; \
    docker stop checkpoint01 checkpoint02 checkpoint03 checkpoint04'")

if __name__ == '__main__':
    main()
