# Distributed File Indexer

DFI is a distributed word count application that relies on [Redis](http://redis.io/) and the python [RQ library](http://python-rq.org/).

Using the RQ library we enqueue work for workers to split text and count the number of words. Logically the flow is a follows:

1. Start Redis
2. Start 1 or more rq workers
3. Run dfi/dfi.py to enqueue work
4. Workers pull jobs off of a redis queue and return the restuls as a collection.Counter Object
5. Once all jobs are complete the rq enqueueing process started in 2. will output the top 10 words found in the input.txt file.

## Diagram

![Distributed File Indexer Diagram](https://github.com/jessegonzalez/distributed_file_indexer/blob/master/distributed_file_indexer.png)


## Manual Setup
Install and run Redis. On a mac you can use brew. Run this in a dedicated console window:

```
$ brew install redis
$ redis-server
```

Clone this repository:

```
$ git clone https://github.com/jessegonzalez/distributed_file_indexer.git
$ cd distributed_file_indexer
```

Create a virtual environment, using virtuelenv, virtualenvwrapper or pyenv:

```
$ pyenv virtualenv 2.7.6 dfi
$ pyenv activate dfi
```

Next run python setup.py install:

```
(dfi) $ python setup.py install
```

Sample text input is included with this repository as input.txt. Open 3 more console windows/tabs and run rqworker:

```
(dfi) $ PYTHONPATH=dfi/ rqworker
```

Next run dfi/dfi.py, to enqueue work for the rq workers to process:

```
(dfi) $ python dfi/dfi.py
```

You will get output sent to stdout that should look similar to the following:

```
the: 2903
and: 1045
johnny: 1017
to: 1009
a: 959
of: 938
he: 838
was: 649
his: 559
in: 520
```

## Automated Execution with Docker Compose
Using Docker Compose starting docker containers that runs redis, rqworker and the rq coordinator is automate.

Start by installing docker-compose by following the instructions for your operating sytem.

* Linux - https://docs.docker.com/compose/install/
* Mac -  https://www.docker.com/products/docker-toolbox
* Windows -  https://www.docker.com/products/docker-toolbox

On Mac it's a single download and package install, the documentation below is based on a Mac docker-toolbox installation.

With docker-toolbox installed, you can start "Docker Quickstart Terminal" from the command line with

```
$ docker_init.sh
```

You will get output similar to the following once the boot2docker.iso image is installed and running within Vagrant.

```
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/


docker is configured to use the default machine with IP 192.168.99.100
For help getting started, check out the docs at https://docs.docker.com
```

Take not of the default machine IP as we can use it later to submit more jobs to the Redis queue. In this case the IP is
_192.168.99.100_.

The docker-compose.yml file has been provided and will start 3 containers as mentioned above redis, rqworker, and a cordinator container.


We'll start by building the container used to run both the worker and the coordinator

```
$ docker-conpose build
```

This step builds the docker container using the Dockerfile found in the root of this projects directory.

From here we have a few options. We'll start by running one container of each as defined in docker-compose.yml.

```
$ docker-compose up
```

I've intentionally disabled logging for all containers except for the coordinator. This will keep the redis and rqworker logs from flooding the screen. The output would look simlar to the following. Control will not return to the shell, you will need to <Ctrl>+C to regain control:

```
Starting dfi_redis_1
Starting dfi_rq_coordinator_1
Recreating dfi_rqworker_1
Attaching to dfi_redis_1, dfi_rq_coordinator_1, dfi_rqworker_1
redis_1          |  WARNING: no logs are available with the 'none' log driver
rqworker_1       |  WARNING: no logs are available with the 'none' log driver
rq_coordinator_1 | the: 2903
rq_coordinator_1 | and: 1045
rq_coordinator_1 | johnny: 1017
rq_coordinator_1 | to: 1009
rq_coordinator_1 | a: 959
rq_coordinator_1 | of: 938
rq_coordinator_1 | he: 838
rq_coordinator_1 | was: 649
rq_coordinator_1 | his: 559
rq_coordinator_1 | in: 520
dfi_rq_coordinator_1 exited with code 0
^CGracefully stopping... (press Ctrl+C again to force)
Stopping dfi_rqworker_1 ... done
Stopping dfi_redis_1 ... done
dfi_rqworker_1 exited with code 0
dfi_redis_1 exited with code 0
```

We also have the option to scale the number of containers to run. In our scenario we will run 1 redis container, 1 coordinator container, and 3 rqworker containers. We are exposing the Redis port 6379, so we need to make sure it is not running locally.

```
$ docker-compose scale redis=1 rqworker=3 rq_coordinator=1
WARNING: The "redis" service specifies a port on the host. If multiple containers for this service are created on a single host, the port will clash.
Creating and starting 1 ... done
Creating and starting 1 ... done
Creating and starting 2 ... done
Creating and starting 3 ... done
```

Since the coordinator terminates after aggregating and printing results, we use the _docker log_ command to see the output:

```
$ docker ps -a
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS                     PORTS                    NAMES
82ba4df1bc9b        dfi_rq_coordinator   "/app/bin/python /app"   3 minutes ago       Exited (0) 3 minutes ago                            dfi_rq_coordinator_1
5926efe1dcfb        dfi_rqworker         "/app/bin/rqworker --"   3 minutes ago       Up 3 minutes                                        dfi_rqworker_3
d1254457fdff        dfi_rqworker         "/app/bin/rqworker --"   3 minutes ago       Up 3 minutes                                        dfi_rqworker_2
c5adaf34c636        dfi_rqworker         "/app/bin/rqworker --"   3 minutes ago       Up 3 minutes                                        dfi_rqworker_1
1f6677883e5f        redis                "/entrypoint.sh redis"   3 minutes ago       Up 3 minutes               0.0.0.0:6379->6379/tcp   dfi_redis_1
```

We see the docker container named dfi_rq_coordinator_1 has exites, so we can view that containers logs:

```
$ docker logs dfi_rq_coordinator_1
the: 2903
and: 1045
johnny: 1017
to: 1009
a: 959
of: 938
he: 838
was: 649
his: 559
in: 520
```

With redis and our 3 workers still running, we can still submit more _input.txt_ files for processing. Back in a terminal with the dfi virtualenv activated, we specify the REDIS_HOST environment variable to submit jobs to the containerized redis. A sample run follows for the file [Project Gutenberg's The Adventures of Huckleberry Finn, by Mark Twain](http://www.gutenberg.org/cache/epub/32325/pg32325.txt). Replace input.txt with another file and execute.

```
(dfi) $ REDIS_HOST=192.168.99.100 python dfi/dfi.py
and: 6436
the: 5017
i: 3676
a: 3220
to: 3011
it: 2561
t: 2127
was: 2071
he: 1864
of: 1780
```
