from collections import Counter
from rq import Queue
from redis import Redis

from utils import counter

redis_conn = Redis()
q = Queue(connection=redis_conn)

job_list = []
result = Counter()

# TODO parse and populate from a data file.
for i in range(1, 10):
    job_list.append(q.enqueue(counter, "one two three four five"))

while True:
    if not job_list:
        break
    else:
        for job in job_list:
            if job.status == 'finished':
                print job.id, job.status
                result = result + job.result
                job_list.remove(job)
print result
