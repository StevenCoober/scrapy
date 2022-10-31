import scrapy
from properties.items import *
from datetime import datetime
from urllib.parse import urlencode
from calendar import monthrange
import logging
#print(current_time)
import browser_cookie3
from scrapy.utils.spider import iterate_spider_output
import re
class TicketSpider(scrapy.Spider):
    name = 'ticket'
    allowed_domains = ['sunwing.ca']
    # start_urls = ["https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?engines=S&flex=Y&isMobile=true&searchtype=OW&language=en&code_ag=rds&alias=btd&date_dep=20221025&gateway_dep=YYZ&dest_dep=MIA&nb_adult=2&nb_child=0"]

    def start_requests(self):
        if len(self.start_urls) > 0:
            url = self.start_urls[0]
            cookies = {

            }
            yield scrapy.Request(url,cookies=cookies,callback=self.parse,dont_filter=True)
        self.mock()
        return super().start_requests()

    def mock(self):

        with open("demo/datas/Select Date_roundTrip.html", "r", encoding="utf-8") as f:
            content = f.read()
        selector = scrapy.Selector(text=content)
        selector.text = content
        self.roundTripParse(selector)

    def start_requests(self):
        yield scrapy.Request(url,meta={'cookiejar':1},callback=self.parse)
        print("start_requests")
        # https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?engines=S&flex=Y&isMobile=true&searchtype=RE&language=en&code_ag=rds&alias=btd&date_dep=20221024&gateway_dep=YWG&dest_dep=CUN&nb_adult=1&nb_child=0&date_ret=20221031
        # 往返票
        

    def request_roundTrip(self,origin="YWG",destinations="CUN",fromDay="",toDay=""):
        url = 'https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?'
        if fromDay == "":
            fromDay = datetime.now().strftime('%Y%m%d')

        tomorrowDay = (datetime.datetime.strptime(fromDay, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")
        
        date_ret = toDay
        if date_ret == "":
            allDays = monthrange(datetime.now().year, datetime.now().month )[1]
            date_ret = "%02d%02d%02d"%(datetime.now().year, datetime.now().month, allDays)
            if date_ret == fromDay:
                date_ret = (datetime.datetime.strptime(fromDay, "%Y%m%d") + datetime.timedelta(days=2)).strftime("%Y%m%d")
        
        params = {
            "engines":"S",
            "flex":"Y",
            "isMobile":"true",
            "searchtype":"RE",
            "language":"en",
            "code_ag":"rds",
            "alias":"btd",
            "date_dep": tomorrowDay,
            "gateway_dep": origin,
            "dest_dep": destination,
            "nb_adult":"1",
            "nb_child":"0",
            "date_ret": date_ret,
        }
        url = url + urlencode(params)
        url = "https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?engines=S&flex=Y&isMobile=true&searchtype=RE&language=en&code_ag=rds&alias=btd&date_dep=20221024&gateway_dep=YWG&dest_dep=CUN&nb_adult=1&nb_child=0&date_ret=20221031"
        yield scrapy.Request(url=url, callback=self.roundTripParse)

    # https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?
    def roundTripParse(self,  response):
        available_dates_list = response.xpath('//*[@id="contenu"]/div[2]/form/label')
        for one in available_dates_list:
            forDate = a.xpath('./@for').extract_first()
            # <label for="dep-20221217" class="">Toronto to Melbourne (December 17, 2022)</label>
            if "dep" in forDate:
                pass
            # <label for="ret-20221217" class="">Melbourne - Toronto (December 17, 2022)</label>
            if "ret" in forDate:
                pass

    # https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?engines=S&flex=Y&isMobile=true&searchtype=OW&language=en&code_ag=rds&alias=btd&date_dep=20221027&gateway_dep=YHZ&dest_dep=MLB&nb_adult=1&nb_child=0
    def parse(self, response):
        # logging.warn("......response:%s"%(response.text))
        available_dates_list = response.xpath('//*[@id="contenu"]/div[2]/form/label/text()')
        logging.warn(available_dates_list)
        monthStr = {
            'January':1,
            'February':2,
            'March':3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12,
        }
        for one in available_dates_list:
            # print("..............available_dates_list", one.extract())
            # "Toronto to Miami (December 18, 2022)"
            dateStr = one.extract()

            regex_str = "(\w+) (\d)+, (\d+)"
            result = re.search(regex_str, dateStr)   # 使用match方法进行匹配操作
            if result:
                monthStr, day, year = result.group(1), result.group(2), result.group(3)

            else:
                print('匹配不成功')

