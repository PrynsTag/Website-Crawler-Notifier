import os
import time

import schedule

print('Scheduler initialised')
schedule.every(1).minutes.do(lambda: os.system('python3 spiders/spider_notifier.py'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)
