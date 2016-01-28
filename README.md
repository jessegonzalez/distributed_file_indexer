# Distributed File Indexer

DFI is a distributed word count application that relies on Redis[http://redis.io/] and the python RQ[http://python-rq.org/]
library.

Using the RQ library we enqueue work for workers to split text and count the number of words. Logically the flow is a follows:

1. Start Redis
2. Start 1 or more rq workers
3. Run dfi/dfi.py to enqueue work
4. Workers pull jobs off of a redis queue and return the restuls as a collection.Counter Object
5. Once all jobs are complete the rq enqueueing process started in 2. will output the top 10 words found in the input.txt file.

## Diagram

![Image of DFI](https://github.com/jessegonzalez/distributed_file_indexer/blob/master/distributed_file_indexer.png)


## Manual Setup
Install and run Redis. On a mac you can use brew. Run this in a dedicated console window:

```
brew install redis
redis-server
```

Clone this repository:

```
git clone https://github.com/jessegonzalez/distributed_file_indexer.git
cd distributed_file_indexer
```

Create a virtual environment, using virtuelenv, virtualenvwrapper or pyenv:

```
pyenv virtualenv 2.7.6 dfi
pyenv activate dfi
```

Next run python setup.py install:

```
python setup.py install
```

Sample text input is included with this repository as input.txt. Open 3 more console windows/tabs and run rqworker:

```
rqworker
```

Next run dfi/dfi.py, to enqueue work for the rq workers to process:

```
python dfi/dfi.py
```
