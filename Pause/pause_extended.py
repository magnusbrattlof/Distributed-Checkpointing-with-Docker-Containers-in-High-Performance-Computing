#!/usr/bin/python2.7
import docker
import time
import random
import os
import logging
import subprocess as sp
from random import shuffle
 
 
FNULL = open(os.devnull, 'w')
client = docker.APIClient(base_url='unix://var/run/docker.sock')
    
containers = ['cont01', 'cont02', 'cont03',
              'cont04', 'cont05', 'cont06', 'cont07', 'cont08']
logging.basicConfig(
    filename='/home/hpc/logs/extended_pause.log', level=logging.INFO)
 
 
def main():
    for i in range(1, 101):
        logging.info('\nOn {} iteration of 100'.format(i))
        process = sp.Popen(['ssh', 'cont01', 'mpirun', '-outfile-pattern',
                            '/hpc/logs/extended_pause/logfile.' +
                            '{}'.format(i), '-f', '/hpc/hostfiles/8p_8c', '-n',
                            '8', '/hpc/cg.C.8'], shell=False)
        time.sleep(60)
        pause()
        time.sleep(random.randrange(1, 120))
        unpause()
        process.communicate()
        time.sleep(60)
 
 
def pause():
    shuffle(containers)
    for container in containers:
        try:
            client.pause(container)
        except docker.errors.NotFound:
            sp.Popen(['ssh', 'guma02', 'docker', 'pause', container],
                     shell=False, stdout=FNULL, stderr=sp.STDOUT)
        random_sleep = random.randrange(1, 300)
        logging.info('\nPaused container: {}\nSleeping {} \
        seconds before next container'.format(
            container, random_sleep))
        time.sleep(random_sleep)
 
 
def unpause():
    shuffle(containers)
    for container in containers:
        try:
            client.unpause(container)
        except docker.errors.NotFound:
            sp.Popen(['ssh', 'guma02', 'docker', 'unpause', container],
                     shell=False, stdout=FNULL, stderr=sp.STDOUT)
        random_sleep = random.randrange(1, 300)
        logging.info('\nPaused container: {}\nSleeping {} \
        seconds before next container'.format(
            container, random_sleep))
        time.sleep(random_sleep)
 
 
if __name__ == '__main__':
    main()
