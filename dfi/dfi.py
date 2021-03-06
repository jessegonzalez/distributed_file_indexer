from collections import Counter
import os

from rq import Queue
from redis import Redis

from utils import counter

if __name__ == '__main__':

    # in our docker-compose.yml file we link and expose the 'redis' container setting the REDIS_HOST environment variable
    try:
        redis_host = os.environ['REDIS_HOST']
    except KeyError:
        redis_host = 'localhost'


    redis_conn = Redis(host=redis_host)
    q = Queue(connection=redis_conn)

    job_list   = []
    result     = Counter()
    line_count = 0
    max_lines  = 100
    input_file = 'input.txt'
    input      = ""

    # split the file input.txt on max_lines which is set to 100
    infile = open(input_file, 'r')
    for line in infile:
        input = input + line
        if line_count % max_lines == 0:
            job_list.append(q.enqueue(counter, input ))
            input = ""
        line_count += 1

    if line_count % max_lines != 0:
       job_list.append(q.enqueue(counter, input ))


    # once all jobs have been enqueued, wait for aill jobs to finish, aggregating Counter objects along the way.
    while True:
        if not job_list:
            break
        else:
            for job in job_list:
                if job.status == 'finished':
                    try:
                        if os.environ['DEBUG']:
                            print job.id, job.status
                    except:
                        pass
                    result = result + job.result
                    job_list.remove(job)

    # print the top 10 most common words to standard out
    for word in result.most_common(10):
        print "{}: {}".format(word[0], word[1])
