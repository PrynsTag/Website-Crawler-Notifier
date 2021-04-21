import os
import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest


def send_email(msg):
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_EMAIL_PASS"])
        server.sendmail(os.environ["SENDER_EMAIL"], os.environ["RECEIVER_EMAIL"], msg)


def check_status(data):
    if data["status"].strip() != "Temporarily unavaible".strip():
        send_email(os.environ["GRADE_MESSAGE"])


def check_scholar(data):
    if "Scholarship" in data:
        send_email(os.environ["SCHOLAR_MESSAGE"])


class SpiderNotifier(scrapy.Spider):
    name = "notifier"

    def start_requests(self):
        yield scrapy.Request(url=os.environ["URL"], callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response, formdata=[(os.environ["creds_1"], os.environ["creds_1_ans"]),
                                                             (os.environ["creds_2"], os.environ["creds_2_ans"]),
                                                             (os.environ["creds_3"], os.environ["creds_3_ans"])],
                                         callback=self.parse)

    def parse(self, response, **kwargs):
        status = response.css("table.profile-table > tr > td::text").getall()
        clean_status = [info.strip() for info in status]
        check_scholar(clean_status)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SpiderNotifier)
    process.start()
