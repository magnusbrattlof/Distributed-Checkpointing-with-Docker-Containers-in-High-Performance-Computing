#!/usr/bin/python3.5
from docker_api import *
import docker
import time

def start_job(job, iteration, sequence):
    print("Started job {} with iteration {} sequence {}".format(job, iteration, sequence))
    os.system("ssh 192.168.16.2 'mpirun -n 4 -hosts checkpoint01,checkpoint02,checkpoint03,checkpoint04 \
              /hpc/bin/{0} >> /hpc/logs/paper/{0}/{0}_{1}_{2} & exit'".format(job, sequence, iteration))

def job_sleep(job):
    # If job matches key, return the value as integer
    timer = {'bt.C.4': 1050,
             'cg.C.4': 110,
             'ep.C.4': 90,
             'ft.C.4': 240,
             'is.C.4': 20,
             'lu.C.4': 1120,
             'mg.C.4': 100,
             'sp.C.4': 1540}[job]
    return int(timer)

def main():
    jobs = ['bt.C.4', 'cg.C.4', 'ep.C.4', 'ft.C.4', 'is.C.4', 'lu.C.4', 'mg.C.4', 'sp.C.4']
    containers = ['checkpoint01', 'checkpoint02', 'checkpoint03', 'checkpoint04']
    sequence = ['ff', 'll', 'fl', 'lf']
    # Iterate through all benchmarks
    for job in jobs:
        # All benchmarks are executed with 4 sequences
        for seq in sequence:
            # All jobs and sequences are executed 100 times each
            for itr in range(1, 101):
                print('Started iteration {}'.format(itr))
                restart(containers)
                start_job(job, itr, seq)
                # Ugly work around due to is.C.4 only executes for 6 seconds
                if job == 'is.C.4':
                    time.sleep(3)
                else:
                    time.sleep(30)
                # Start checkpoint containers
                checkpoint(containers=containers, sequence=seq)
                # Let the files be written to disk and sync
                time.sleep(30)
                os.system('sync')
                # Start restoring process
                restore(containers=containers, sequence=seq)
                # Depending on the job, different sleep timers are implemented
                time.sleep(job_sleep(job) + 120)

if __name__ == '__main__':
    main()
