import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest

from notifier.spiders.info import *


def send_email(msg):
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)


def check_grade(data):
    if data["status"].strip() != "Temporarily unavaible".strip():
        send_email(GRADE_MESSAGE)


def check_scholar(data):
    if "Scholarship" in data:
        send_email(SCHOLAR_MESSAGE)


class SpiderNotifier(scrapy.Spider):
    name = "notifier"
    list_of_row = []

    def start_requests(self):
        yield SeleniumRequest(
            url=URL,
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        yield FormRequest.from_response(response, formdata=form_data_login, callback=self.after_login)

    def after_login(self, response):
        status = response.xpath("//table[@class=\"profile-table\"]//td[position() = 1]/text()").getall()
        check_scholar(status)
        course_card = response.xpath("//td[@class=\"sidebar\"]/ul/li[position() = 3]//a/@href").get()
        yield response.follow(course_card, callback=self.parse_grade)

    def parse_grade(self, response):
        for sy in sy_select:
            for term in term_select:
                yield FormRequest.from_response(response, formdata={
                    "term": term,
                    "school_year": sy,
                    "submit": "submit"
                }, callback=self.parse_table)

    def parse_table(self, response):
        table = response.xpath("//table[@class=\"table\"]")
        for row in table.xpath(".//tr"):
            list_of_cell = []
            td = row.xpath(".//td/text()").getall()
            for cell in td:
                list_of_cell.append(cell.strip())

            if list_of_cell and len(list_of_cell) == 6:
                self.list_of_row.append(list_of_cell)
                yield {
                    "Course Code": list_of_cell[0],
                    "Course Title": list_of_cell[1],
                    "Section": list_of_cell[2],
                    "Units": list_of_cell[3],
                    "Midterm": list_of_cell[4],
                    "Final": list_of_cell[5]
                }


if __name__ == "__main__":
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(SpiderNotifier)
    process.start()
