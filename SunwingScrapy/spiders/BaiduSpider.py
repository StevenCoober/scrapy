import scrapy


class BaiduspiderSpider(scrapy.Spider):
    name = 'BaiduSpider'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        # 通过导入CookieJar来实现cookie的获取
        from scrapy.http.cookies import CookieJar
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        print(cookie_jar)  # <scrapy.http.cookies.CookieJar object at 0x7f8888a0f940>
        cookie_dict = {}
        for item in cookie_jar:
            cookie_dict[item.name] = item.value
        print("cookie_dict>>>", cookie_dict)
        # cookie_dict>>> {'BDSVRTM': '0', 'BD_HOME': '1', 'H_PS_PSSID': '32293_1465_31669_32380_32359_31254_32046_32116_26350'}
