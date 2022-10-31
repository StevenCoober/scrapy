# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random, os, sys, requests, json, time, logging
import urllib3
urllib3.disable_warnings()
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import base64
import chardet
from scrapy.http.cookies import CookieJar
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from scrapy.http.cookies import CookieJar
from scrapy.settings import SETTINGS_PRIORITIES, Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider
from scrapy.utils.misc import load_object
from scrapy.utils.python import to_native_str
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
import logging
from utils.utils import cookieString2CookieDict 
logger = logging.getLogger(__name__)

import browser_cookie3
import execjs, os
# 在spider中 主动关闭爬虫:

# self.crawler.engine.close_spider(self, “cookie失效关闭爬虫”)

# 在pipeline 和downloadermiddlewares 主动关闭爬虫：

# spider.crawler.engine.close_spider(spider, “全文结束关闭爬虫”)
proxyEnalbed = False
class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    def process_request(self, request, spider):
        delay = random.uniform(max(0.2, self.delay/3), self.delay)
        time.sleep(delay)
        logging.warn('random delay %s seconds' % delay)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DOWNLOAD_DELAY', 3))

class OneceMiddleware(object):
    def __init__(self):
        self.times = 0

    def process_request(self, request, spider):
        if (self.times == 4):
            spider.crawler.engine.close_spider(spider, "全文结束关闭爬虫")
        self.times = self.times + 1

class fiddle_proxy(object):
    def process_request(self,request,spider):
        proxyServer = "http://127.0.0.1:8888"
        request.meta["proxy"] = proxyServer

class BrowserCookiesMiddleware(CookiesMiddleware):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.load_browser_cookies()
    def load_browser_cookies(self):
        # 加载chrome浏览器中的Cookie
        jar = self.jars['chrome']
        chrome_cookiejar = browser_cookie3.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)

class MyCookiesMiddleware(object):
    datadome = None
    def __init__(self):
        json_path = os.getcwd() + "/utils/utils.js"
        data = None
        if os.path.isfile(json_path):
            with open(json_path, "r", encoding='utf-8') as fp:
                data=fp.read()

        self.utilsJS = execjs.compile(data)

        chrome_cookiejar = browser_cookie3.chrome()
        cookies = {}
        for item in chrome_cookiejar:
            cookies[item.name] = item.value
        self.datadome = cookies["datadome"] 

    def process_request(self,request, spider):
        # coookie_dict = {}
        # request.cookies.update(coookie_dict)
        # request.cookies = coookie_dict
        
        if spider.name == "sunwingTicketSpider":
            url = "https://api-js.datadome.co/js/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                # 'Host': 'sunwing.ca',
                # 'Origin': 'https://book.sunwing.ca.en',
                # 'Referer': 'https://book.sunwing.ca'
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            global proxyEnalbed
            proxies = None
            if proxyEnalbed:
                proxies = {
                    'http': '127.0.0.1:8888',
                    'https': '127.0.0.1:8888',
                }
            
            hrefName = request.url
            if "lastDatadome" in request.meta:
                lastDatadome = request.meta["lastDatadome"]
            else:
                lastDatadome = self.datadome
            jsType = "ch"
            cookieStr = self.utilsJS.call('getQueryParamsString', hrefName, lastDatadome, jsType)

            response = requests.post(url,data = cookieStr, headers=headers, proxies=proxies, verify = False)
            if response.status_code != 200:
                print("...........")
                spider.crawler.engine.close_spider(spider, "无法获取")
                return
            rjson = json.loads(response.text)
            datadome = cookieString2CookieDict(rjson["cookie"])["datadome"]
            request.meta["lastDatadome"] = datadome
            coookie_dict = {
                "datadome": datadome
            }
            request.cookies.update(coookie_dict)

class my_proxy(object):
    def __init__(self):
        global proxyEnalbed
        proxyEnalbed = True
    def try_sunwing(self, proxies):
        r = requests.get('https://services.sunwinggroup.ca/beta/api/search/getGatewayforBrand/en/SWG/RE', proxies=proxies, timeout=3)
        # r = requests.get('http://127.0.0.1:8000/?types=0&count=50&country=国内', proxies=proxies, timeout=2)
        
        # r.encoding = chardet.detect(r.content)['encoding']
        return r.ok
        
    def process_request(self,request,spider):
        #   # 代理服务器
        #   proxyHost = "dyn.horocn.com"
        #   proxyPort = "50000"
        #   # 代理隧道验证信息
        #   proxyUser = "输入蜻蜓代理给你的用户名"
        #   proxyPass = "输入蜻蜓代理给你的密码"
        #   proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #       "host": proxyHost,
        #       "port": proxyPort,
        #       "user": proxyUser,
        #       "pass": proxyPass,
        #   }
        # # 创建ProxyHandler处理器(代理设置)
        #   proxy_handler = urllib.request.ProxyHandler({
        #       "http": proxyMeta,
        #       "https": proxyMeta,
        #   })
        #   opener = urllib.request.build_opener(proxy_handler) # 创建Opener
        #   urllib.request.install_opener(opener) # 安装Opener
        # allProxy = [["139.99.237.62", 80, 10], ["103.18.77.18", 8080, 9], ["103.125.162.134", 84, 9], ["14.140.131.82", 3128, 8], ["223.96.90.216", 8085, 8], ["222.179.155.90", 9091, 7], ["221.122.91.75", 10286, 7], ["103.231.78.36", 80, 7], ["58.220.95.79", 10000, 7], ["221.5.80.66", 3128, 7], ["58.20.184.187", 9091, 7], ["121.8.215.106", 9797, 7], ["183.247.202.208", 30001, 6], ["47.106.105.236", 80, 6], ["47.57.188.208", 80, 6], ["118.140.160.84", 80, 5], ["106.60.70.243", 80, 5], ["43.255.113.232", 84, 5], ["182.90.224.115", 3128, 4], ["51.91.157.66", 80, 4], ["190.26.201.194", 8080, 4], ["222.66.202.6", 80, 4], ["103.220.206.110", 59570, 4], ["218.7.171.91", 3128, 3], ["60.198.53.23", 80, 1], ["221.217.50.66", 9000, 1]]
        proxies = None

        r = requests.get('http://127.0.0.1:8000/?types=0&count=50&country=国内')
        ip_ports = json.loads(r.text)
        ip_port = random.choice(ip_ports)
        ip = ip_port[0]
        port = ip_port[1]
        proxies={
            'http':'http://%s:%s'%(ip,port),
            'https':'http://%s:%s'%(ip,port)
        }
        # self.try_sunwing(proxies)
        proxyServer = proxies['http']
        
        # print("proxyServer", proxyServer)
        request.meta["proxy"] = proxyServer

class business_proxy(object):
    proxyServer = "http://http-dyn.abuyun.com:9020"
    PROXY_USER = "HR56X3M80502143D"
    PROXY_PASS = "0A23B85A76400BBC"
    
    def process_request(self,request,spider):
        proxyServer = self.proxyServer
        PROXY_USER = self.PROXY_USER
        PROXY_PASS = self.PROXY_PASS
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((PROXY_USER + ":" + PROXY_PASS), "ascii")).decode("utf8")
        # 代理服务器
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


class DemoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
