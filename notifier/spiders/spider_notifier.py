import os
import smtplib
import ssl
import time

import schedule
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest

from info import *


def run_intervals():
    print('Scheduler initialised')
    schedule.every(20).seconds.do(lambda: os.system('python3 notifier/spiders/spider_notifier.py'))
    print('Next job is set to run at: ' + str(schedule.next_run()))

    while True:
        schedule.run_pending()
        time.sleep(1)


def send_email():
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)
    print("##--------------------------------------------------------##")
    print("##----------------- Grades is available! -----------------##")
    print("##--------------------------------------------------------##")


def check_status(data_dict):
    if data_dict["status"].strip() != "Temporarily unavaible".strip():
        send_email()


class SpiderNotifier(scrapy.Spider):
    name = "notifier"

    def start_requests(self):
        yield scrapy.Request(url=URL, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response, formdata=FORM_DATA, callback=self.parse)

    def parse(self, response, **kwargs):
        data = response.css("table.profile-table > tr:nth-of-type(4) > td::text").getall()
        my_data = [info.strip() for info in data]
        grade_view = dict(label=[my_data[0]], status=my_data[1])
        check_status(grade_view)
        print(grade_view)
        yield grade_view


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SpiderNotifier)
    process.start()
    run_intervals()
