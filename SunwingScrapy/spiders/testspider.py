import scrapy
import os, sys, json, time
from properties.items import *
from middlewares import CookiesMiddleware 
from utils.utils import cookieString2CookieDict 

class TestspiderSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        self.json_path = os.getcwd() + "/datas/Ticket_.json"
        
        data = None
        if os.path.isfile(self.json_path):
            with open(self.json_path, "r", encoding='utf-8') as fp:
                data=fp.read()

        self.chooses = Chooses() ## <HouseScrapy>所有信息
        self.chooses.init() ## <Chooses>
        if data:
            self.chooses.jsonLoads(data)
            # print(self.chooses.jsonDumps());
            yield self.chooses