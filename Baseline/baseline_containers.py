#!/usr/bin/python2.7

import subprocess as sp
import time

experiment_list = [
    {'processes': '2', 'container': 1, 'npb': '/hpc/cg.C.2',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg2-1c.',
     'hostfile': '/hpc/hostfiles/2p_1c'
    },
    {'processes': '2', 'container': 2, 'npb': '/hpc/cg.C.2',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg2-2c.',
     'hostfile': '/hpc/hostfiles/2p_2c'
    },
    {'processes': '4', 'container': 1, 'npb': '/hpc/cg.C.4',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg4-1c.',
     'hostfile': '/hpc/hostfiles/4p_1c'
    },
    {'processes': '4', 'container': 4, 'npb': '/hpc/cg.C.4',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg4-4c.',
     'hostfile': '/hpc/hostfiles/4p_4c'
    },
    {'processes': '8', 'container': 2, 'npb': '/hpc/cg.C.8',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg8-2c.',
     'hostfile': '/hpc/hostfiles/8p_2c'
    },
    {'processes': '8', 'container': 8, 'npb': '/hpc/cg.C.8',
     'logfile': '/hpc/logs/container_baseline_min_freq/container_baseline_min_freq-cg8-8c.',
     'hostfile': '/hpc/hostfiles/8p_8c'
    }

]
for experiment in experiment_list:
    print "On {} processes with {} containers:".format(experiment['processes'], experiment['container'])
    for loop in range(1, 11):
        print "{} of 20 finished".format(loop)
        process = sp.Popen(['ssh','cont01', 'mpirun', '-map-by', 'rr', '-outfile-pattern', experiment['logfile'] + '{0}'.format(loop),
                '-f', experiment['hostfile'], '-n', experiment['processes'], experiment['npb']], shell=False)
        process.communicate()
        time.sleep(60)
        if loop == 10:
            print "{} processes with {} containers finished successfully".format(experiment['processes'], experiment['container'])
