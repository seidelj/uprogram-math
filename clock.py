import os
from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(minutes=2)
def timed_job(coalesce=True, misfire_grace_time=0):
    os.system('python utils.py')

sched.start()

while True:
    pass
