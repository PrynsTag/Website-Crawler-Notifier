import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest

from info import *


def send_email(msg):
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)
    print("##--------------------------------------------------------##")
    print("##----------------- Grades is available! -----------------##")
    print("##--------------------------------------------------------##")


def check_grade(data):
    if data["status"].strip() != "Temporarily unavaible".strip():
        send_email(GRADE_MESSAGE)


def check_scholar(data):
    if "Scholarship" in data:
        send_email(SCHOLAR_MESSAGE)


class SpiderNotifier(scrapy.Spider):
    name = "notifier"

    def start_requests(self):
        yield scrapy.Request(url=URL, callback=self.login)

    def login(self, response):
        yield FormRequest.from_response(response, formdata=FORM_DATA, callback=self.parse)

    def parse(self, response, **kwargs):
        status = response.css("table.profile-table > tr > td::text").getall()
        clean_status = [info.strip() for info in status]
        check_scholar(clean_status)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SpiderNotifier)
    process.start()
