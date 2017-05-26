#!/usr/bin/python2.7

import subprocess as sp
import time

for i in range(1, 11):
    log = '/home/hpc/logs/baseline/min_freq_new/baseline-cg2.{0}'.format(i)
    print "On CG.2 loop:", i
    process = sp.Popen(['mpirun', '-outfile-pattern', log, '-bind-to', 'rr', '-n', '2', '/home/hpc/cg.C.2'])
    process.communicate()
    time.sleep(60)
    if i == 100:
        print "CG.2 finished successfully!"

for i in range(1, 11):
    log = '/home/hpc/logs/baseline/min_freq_new/baseline-cg4.{0}'.format(i)
    print "On CG.4 loop:", i
    process = sp.Popen(['mpirun', '-outfile-pattern', log, '-bind-to', 'rr', '-n', '4', '/home/hpc/cg.C.4'])
    process.communicate()
    time.sleep(60)
    if i == 10:
        print "CG.4 finished successfully!"

for i in range(1, 11):
    log = '/home/hpc/logs/baseline/min_freq_new/baseline-cg8.{0}'.format(i)
    print "On CG.8 loop:", i
    process = sp.Popen(['mpirun', '-outfile-pattern', log, '-bind-to', 'rr', '-hosts', 'guma01,guma02', '-n', '8', '/home/hpc/cg.C.8'])
    process.communicate()
    time.sleep(60)
    if i == 10:
        print "CG.8 finished successfully!"
