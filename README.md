# Distributed Checkpointing with Docker Containers in High Performance Computing
Gustaf Berg and Magnus Brattlöf Bachelor Thesis in Computer Engineering

**Abstract**:<br />
*Expensive software licensing costs tied to hardware in the industrial High Performance Computing (HPC) can be alleviated with the help of distributed Docker containers. Updates to the namespace and cgroups features in the Linux kernel has led to a widespread adoption of container-virtualization, which also brings the ability to suspend running containers. Research and experiments was designed to find out if the experimental Docker checkpoint feature could be used in the industrial HPC-community. Docker containers were built that could run the well-known NASA Parallel Benchmark (NPB), Conjugate Gradient (CG) that stress test irregular memory and communication, maxing out the small-scale testbeds. This was demonstrated to be working fully while pausing and unpausing containers. Then, it was further demonstrated, if you carefully consider the order in which you Checkpoint/Restore (C/R) containers, that Docker checkpoint worked. Finally, restoring containers were also possible on a completely separate system under test, that demonstrated the flexibility of this experimental feature and proving that it might very well tip the community over to running their simulations and virtual engineering-applications inside containers instead of running them on native hardware.*

**Disclaimer**:<br />
*These scripts intended purpose was not to be beautiful nor effective, their main focus was in completing a set of tasks as simple as possible.*

**Content**:<br />
* Article
    * main.py
    * docker_api.py

* Bachelor
    * Baseline
    * Pause
    * Checkpoint Move and Restore
    * Checkpoint Switch and Restore
