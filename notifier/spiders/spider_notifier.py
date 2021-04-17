import os
import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest


def send_email():
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_EMAIL_PASS"])
        server.sendmail(os.environ["SENDER_EMAIL"], os.environ["RECEIVER_EMAIL"], os.environ["MESSAGE"])
    print("##--------------------------------------------------------##")
    print("##----------------- Grades is available! -----------------##")
    print("##--------------------------------------------------------##")


def check_status(data_dict):
    if data_dict["status"].strip() != "Temporarily unavaible".strip():
        send_email()


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
