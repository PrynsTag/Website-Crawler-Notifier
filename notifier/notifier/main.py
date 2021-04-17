import os
import time

import schedule

print('Scheduler initialised')
schedule.every(1).minutes.do(lambda: os.system('scrapy crawl notifier'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)
