import os
import time

import schedule

print('Scheduler initialised')
schedule.every(20).seconds.do(lambda: os.system('python3 spiders/spider_notifier'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)
