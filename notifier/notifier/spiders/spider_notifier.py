import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest


def send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "#@gmail.com"  # Enter your address
    receiver_email = "#@gmail.com"  # Enter receiver address
    password = "#"
    message = """\
    Subject: Hi there

    Grades Viewing is available!"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def check_status(data_dict):
    if data_dict["status"].strip() != "# #".strip():
        send_email()


class SpiderNotifier(scrapy.Spider):
    name = "notifier"

    def start_requests(self):
        yield scrapy.Request(url="#", callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response, formdata={
            "#": "#",
            "#": "#",
            "#": "#"
        }, callback=self.parse)

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
