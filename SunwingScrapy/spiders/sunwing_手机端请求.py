import scrapy
import os, sys, json, traceback
import datetime
from calendar import monthrange
# print(client.get(code='MOW'))
# print(client.get(country_code='RU'))
# print(client.get(name='Moscow'))
from properties.items import *
# https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/YYZ/OW
from urllib import parse
import logging, re
import execjs

def cookieString2CookieJar(cookie: str = "") -> dict:
    """
    将字符串形式的cookie转成RequestsCookieJar
    :param cookie: 待转换的cookie字符串
    :return: RequestsCookieJar 对象
    """
    headers = response.headers
    headers["sid"] = sid
    if len(cookie) == 0:
        log("cookie为空，返回空值")
        return RequestsCookieJar()
    cookie = cookie.replace(" ", "")
    cookies = cookie.split(";")
    cookie_dict = {}
    for c in cookies:
        cookie_list = list(c)
        name = ""
        value = ""
        flag = True
        for item in cookie_list:
            if item == "=" and flag:
                flag = False
                continue
            if flag:
                name = name + item
            else:
                value = value + item
        if len(name) != 0 and len(value) != 0:
            cookie_dict[name] = value
    cookie_dict
    return cookie_dict

class ConstAirportCountryInfosCache():
    
    def __init__(self):
        self.json_path = os.getcwd() + "/datas/ConstAirportCountryInfos.json"
        constAirportCountryInfo = ConstAirportCountryInfo() ## <ConstAirportCountryInfo>所有机场国家固定信息
        constAirportCountryInfo.init()
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding='utf-8') as fp:
                jsonStr = fp.read()
                constAirportCountryInfo.jsonLoads(jsonStr)

        self.constAirportCountryInfo = constAirportCountryInfo
    def getConstAirportCountryInfo(self):
        return self.constAirportCountryInfo

    def insert(self, airportCountryInfo):
        code = airportCountryInfo["code"] ## <Serializable><string>三字码
        countryCode = airportCountryInfo["countryCode"] ## <Serializable><string>国家Code
        countryChineaseName = airportCountryInfo["countryChineaseName"] ## <Serializable><string>国家名称

        findAirportCountryInfo = self.getAirportCountryInfoByKeyValue("code", code)
        if not findAirportCountryInfo:
            constAirportCountryInfo = self.constAirportCountryInfo ## <ConstAirportCountryInfo>所有机场国家固定信息

            airportCountryInfos = constAirportCountryInfo["airportCountryInfos"] ## <Serializable><AirportCountryInfo[]>机场国家固定信息
            airportCountryInfos.append(airportCountryInfo)
            with open(self.json_path, "w", encoding='utf-8') as fp:
                jsonStr = constAirportCountryInfo.jsonDumps()
                fp.write(jsonStr)

    def getAirportCountryInfoByKeyValue(self, key, code):
        constAirportCountryInfo = self.constAirportCountryInfo ## <ConstAirportCountryInfo>所有机场国家固定信息

        airportCountryInfos = constAirportCountryInfo["airportCountryInfos"] ## <Serializable><AirportCountryInfo[]>机场国家固定信息
        airportCountryInfoN = (e for i, e in enumerate(airportCountryInfos) if e[key] == code)
        findAirportCountryInfo = next(airportCountryInfoN, None)
        return findAirportCountryInfo


class SunwingSpider2(scrapy.Spider):
    name = 'sunwing2'
    # allowed_domains = ['sunwinggroup.ca']
    # start_urls = ['https://services.sunwinggroup.ca/beta/api/search/getGatewayforBrand/en/SWG/RE']
    
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com']
    
    oneway_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/OW'
    roundtrip_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/RE'
    
    def __init__(self, fromDate=None, returnDate=None, *args, **kwargs):
        super(SunwingSpider2, self).__init__(*args, **kwargs)
        self.constAirportCountryInfosCache = ConstAirportCountryInfosCache()

        nowDate = datetime.datetime.now().strftime('%Y%m%d')
        tomorrowDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
        if fromDate == None:
            fromDate = tomorrowDate

        self.fromDate = fromDate
        
        if returnDate == None:
            allDays = monthrange(datetime.datetime.now().year, datetime.datetime.now().month )[1]
            returnDate = "%02d%02d%02d"%(datetime.datetime.now().year, datetime.datetime.now().month, allDays)
            if returnDate == tomorrowDate:
                returnDate = (datetime.datetime.strptime(fromDate, "%Y%m%d") + datetime.timedelta(days=2)).strftime("%Y%m%d")
        
        self.returnDate = returnDate

        # self.start_urls = ['http://www.example.com/categories/%s' % category]
    # oneway_url = 'https://www.baidu.com'
    # roundtrip_url = 'https://www.baidu.com'
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'demo.pipelines.SunwingPipeline': 2,
    #     },
    # }

    def parse(self, response):
        sunwingInfo = SunwingInfo() ## <SunwingInfo>所有信息
        sunwingInfo.init()
        sunwingInfo.jsonLoads("{\"oneways\":[{\"origin\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MCO\",\"countryId\":\"\",\"airportName\":\"Orlando, Florida, USA (MCO)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]}],\"roundtrips\":[{\"origin\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"FPO\",\"countryId\":\"\",\"airportName\":\"Freeport / Grand Bahama, Bahamas (FPO)\",\"countryName\":\"Bahamas\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ADZ\",\"countryId\":\"\",\"airportName\":\"San Andres, Colombia (ADZ)\",\"countryName\":\"Colombia\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZO\",\"countryId\":\"\",\"airportName\":\"Manzanillo de Cuba, Cuba (MZO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ACA\",\"countryId\":\"\",\"airportName\":\"Acapulco, Mexico (ACA)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SXM\",\"countryId\":\"\",\"airportName\":\"St Maarten / Saint Martin,  (SXM)\",\"countryName\":\"St Maarten\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"ANU\",\"countryId\":\"\",\"airportName\":\"Antigua and Barbuda, Antigua (ANU)\",\"countryName\":\"Antigua\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"AUA\",\"countryId\":\"\",\"airportName\":\"Aruba (AUA)\",\"countryName\":\"Aruba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"FPO\",\"countryId\":\"\",\"airportName\":\"Freeport / Grand Bahama, Bahamas (FPO)\",\"countryName\":\"Bahamas\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZO\",\"countryId\":\"\",\"airportName\":\"Manzanillo de Cuba, Cuba (MZO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"GND\",\"countryId\":\"\",\"airportName\":\"Grenada (GND)\",\"countryName\":\"Grenada\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ACA\",\"countryId\":\"\",\"airportName\":\"Acapulco, Mexico (ACA)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"UVF\",\"countryId\":\"\",\"airportName\":\"Saint Lucia  (UVF)\",\"countryName\":\"Saint Lucia\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SXM\",\"countryId\":\"\",\"airportName\":\"St Maarten / Saint Martin,  (SXM)\",\"countryName\":\"St Maarten\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MCO\",\"countryId\":\"\",\"airportName\":\"Orlando, Florida, USA (MCO)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]}]}")

        # oneways = sunwingInfo["oneways"] ## <Serializable><OnewayFlight[]>单程
        # roundtrips = sunwingInfo["roundtrips"] ## <Serializable><RoundtripFlight[]>往返

        # text = response.text
        # flights = json.loads(text)
        # for idx in range(len(flights)):
        #     flight = flights[idx]

        #     code = flight.get("code") ## <Serializable><string>三字码
        #     countryId = flight.get("countryId") ## <Serializable><string>国家id
        #     airportName = flight.get("name") ## <Serializable><string>机场名称
        #     destinations = flight.get("destinations") ## <Serializable><string>目的地

        #     airportInfo = AirportInfo() ## <AirportInfo>机场信息
        #     airportInfo.init()
        #     airportInfo["code"] = code ## <Serializable><string>三字码
        #     airportInfo["countryId"] = countryId ## <Serializable><string>国家id
        #     airportInfo["airportName"] = airportName ## <Serializable><string>机场名称
        #     airportInfo["countryName"] = "" ## <Serializable><string>国家名称

        #     onewayFlight = OnewayFlight() ## <OnewayFlight>单程
        #     onewayFlight.init()
        #     infoClone = airportInfo.clone()
        #     onewayFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
        #     oneways.append(onewayFlight)


        #     roundtripFlight = RoundtripFlight() ## <RoundtripFlight>往返
        #     roundtripFlight.init()
        #     infoClone = airportInfo.clone()
        #     roundtripFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
        #     roundtrips.append(roundtripFlight)

        # # print("sunwingInfo", sunwingInfo)

        try:
        #     for onewayFlight in oneways:
        #         airportInfo = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
        #         code = airportInfo["code"] ## <Serializable><string>三字码
        #         url = self.oneway_url.format(code)
            
        #         yield scrapy.Request(url, callback=self.parse_oneway, meta = {'onewayFlight': onewayFlight}, dont_filter = True)

        #     for roundtripFlight in roundtrips:
        #         airportInfo = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
        #         code = airportInfo["code"] ## <Serializable><string>三字码
        #         url = self.roundtrip_url.format(code)
        #         yield scrapy.Request(url, callback=self.parse_roundtrip, meta = {'roundtripFlight': roundtripFlight}, dont_filter = True)

            # requests = self.handleExtraInfo(sunwingInfo)
            # for request in requests:
            #     yield request
            # yield sunwingInfo

            airportInfo = AirportInfo() ## <AirportInfo>机场信息
            airportInfo.init() ## <AirportInfo>机场信息
            airportInfo.jsonLoads("{\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryChineaseName\":\"加拿大\",\"countryCode\":\"CA\",\"countryId\":1,\"code\":\"YYZ\"}")

            origin_code = airportInfo["code"] ## <Serializable><string>三字码,
            origin_countryId = airportInfo["countryId"] ## <Serializable><string>国家id,
            origin_airportName = airportInfo["airportName"] ## <Serializable><string>机场名称,
            origin_countryName = airportInfo["countryName"] ## <Serializable><string>国家名称,
            origin_countryCode = airportInfo["countryCode"] ## <Serializable><string>国家Code,
            origin_countryChineaseName = airportInfo["countryChineaseName"] ## <Serializable><string>国家中文名称,

            origin = airportInfo

            airportInfo = AirportInfo() ## <AirportInfo>机场信息
            airportInfo.init() ## <AirportInfo>机场信息
            airportInfo.jsonLoads("{\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryChineaseName\":\"美国\",\"countryCode\":\"US\",\"countryId\":\"\",\"code\":\"MLB\"}")
            
            destination_code = airportInfo["code"] ## <Serializable><string>三字码,
            destination_countryId = airportInfo["countryId"] ## <Serializable><string>国家id,
            destination_airportName = airportInfo["airportName"] ## <Serializable><string>机场名称,
            destination_countryName = airportInfo["countryName"] ## <Serializable><string>国家名称,
            destination_countryCode = airportInfo["countryCode"] ## <Serializable><string>国家Code,
            destination_countryChineaseName = airportInfo["countryChineaseName"] ## <Serializable><string>国家中文名称,

            destination = airportInfo
            fromDate =self.fromDate
            returnDate =self.returnDate

            flightChooseDate = FlightChooseDate() ## <FlightChooseDate>选择飞行时间
            flightChooseDate.init() ## <FlightChooseDate>选择飞行时间
            flightChooseDate["flightType"] = FlightType.ONEWAY ## <Serializable><int>行程类型
            flightChooseDate["origin"] = origin ## <Serializable><AirportInfo>起始机场
            flightChooseDate["destination"] = destination ## <Serializable><AirportInfo>目的机场
            flightChooseDate["fromDate"] = fromDate ## <Serializable><string>开始时间
            # flightChooseDate["selectFromDate"] = selectFromDate ## <Serializable><string>开始时间
            # flightChooseDate["availableFromDates"] = availableFromDates ## <string[]>可用的开始时间
            flightChooseDate["returnDate"] = returnDate ## <Serializable><string>返回时间
            # https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?

            origin = flightChooseDate["origin"]
            origin_code = origin["code"] ## <Serializable><string>三字码

            destination = flightChooseDate["destination"]
            destination_code = destination["code"] ## <Serializable><string>三字码
            datas = {
                "engines":"S",
                "flex":"Y",
                "isMobile":"true",
                "searchtype":"OW",
                "language":"en",
                "code_ag":"rds",
                "alias":"btd",
                "date_dep": flightChooseDate["fromDate"],
                "gateway_dep": origin_code,
                "dest_dep": destination_code,
                "nb_adult":"1",
                "nb_child":"0",
            }
            url = "https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?" + parse.urlencode(datas)
            self.allowed_domains = ['sunwinggroup.ca']
            yield scrapy.Request(url=url, callback=self.parse_mobile_getReturnDate, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True)
        except Exception as e:
            print('获取页数失败', str(e))
            traceback.print_exc()

    def parseExtra(self, response):

        airportInfo = response.meta.get('airportInfo')
        code = airportInfo["code"] ## <Serializable><string>三字码

        dic = {"乍得":"TD","瓦努阿图":"VU","巴基斯坦":"PK","安圭拉":"AI","特克斯和凯科斯群岛":"TC","马耳他":"MT","哥斯达黎加":"CR","尼加拉瓜":"NI","圣基茨和尼维斯":"KN","南乔治亚岛和南桑威奇群岛":"GS","马其顿":"MK","关岛":"GU","西撒哈拉":"EH","圣巴泰勒米岛":"BL","澳大利亚":"AU","马约特":"YT","洪都拉斯":"HN","巴巴多斯":"BB","特立尼达和多巴哥":"TT","塞舌尔":"SC","摩尔多瓦":"MD","圭亚那":"GY","托克劳":"TK","文莱":"BN","不丹":"BT","斯瓦尔巴群岛和扬马延岛":"SJ","马来西亚":"MY","诺福克岛":"NF","东帝汶":"TL","新加坡":"SG","利比里亚":"LR","意大利":"IT","孟加拉":"BD","格鲁吉亚":"GE","蒙古国蒙古":"MN","西班牙":"ES","玻利维亚":"BO","纽埃":"NU","瓦利斯和富图纳":"WF","乌克兰":"UA","土耳其":"TR","开曼群岛":"KY","冰岛":"IS","黑山":"ME","肯尼亚":"KE","多哥":"TG","古巴":"CU","摩洛哥":"MA","百慕大":"BM","柬埔寨":"KH","挪威":"NO","尼日尔":"NE","尼泊尔":"NP","中非":"CF","奥兰群岛":"AX","瑙鲁":"NR","哥伦比亚":"CO","保加利亚":"BG","香港":"HK","阿联酋":"AE","芬兰":"FI","伯利兹":"BZ","叙利亚":"SY","北马里亚纳群岛":"MP","日本":"JP","马拉维":"MW","泽西岛":"JE","莱索托":"LS","基里巴斯":"KI","直布罗陀":"GI","英国":"GB","格陵兰":"GL","贝宁":"BJ","厄瓜多尔":"EC","乌拉圭":"UY","卢旺达":"RW","匈牙利":"HU","冈比亚":"GM","英属印度洋领地":"IO","瓜德罗普":"GP","斯里兰卡":"LK","印尼":"ID","危地马拉":"GT","赤道几内亚":"GQ","巴勒斯坦":"PS","几内亚":"GN","巴西":"BR","塔吉克斯坦":"TJ","朝鲜北朝鲜":"KP","澳门":"MO","比利时":"BE","沙特阿拉伯":"SA","坦桑尼亚":"TZ","阿尔及利亚":"DZ","波多黎各":"PR","留尼汪":"RE","埃及":"EG","马恩岛":"IM","白俄罗斯":"BY","新西兰":"NZ","美国":"US","希腊":"GR","圣卢西亚":"LC","科特迪瓦":"CI","圣皮埃尔和密克隆":"PM","厄立特里亚":"ER","塞内加尔":"SN","巴布亚新几内亚":"PG","伊朗":"IR","哈萨克斯坦":"KZ","菲律宾":"PH","库克群岛":"CK","图瓦卢":"TV","奥地利":"AT","乌干达":"UG","科威特":"KW","博茨瓦纳":"BW","赫德岛和麦克唐纳群岛":"HM","美属萨摩亚":"AS","加拿大":"CA","所罗门群岛":"SB","海地":"HT","英属维尔京群岛":"VG","帕劳":"PW","委内瑞拉":"VE","法国":"FR","荷兰":"NL","梵蒂冈":"VA","索马里":"SO","印度":"IN","立陶宛":"LT","阿鲁巴":"AW","拉脱维亚":"LV","布隆迪":"BI","布韦岛":"BV","波兰":"PL","阿根廷":"AR","俄罗斯":"RU","老挝":"LA","埃塞俄比亚":"ET","萨尔瓦多":"SV","吉布提":"DJ","泰国":"TH","圣文森特和格林纳丁斯":"VC","莫桑比克":"MZ","秘鲁":"PE","圣马丁(法属)":"MF","圣马丁(荷属)":"SX","南极洲":"AQ","阿富汗":"AF","皮特凯恩群岛":"PN","牙买加":"JM","汤加":"TO","以色列":"IL","土库曼斯坦":"TM","德国":"DE","苏里南":"SR","喀麦隆":"CM","列支敦士登":"LI","亚美尼亚":"AM","加蓬":"GA","圣赫勒拿":"SH","韩国南朝鲜":"KR","马尔代夫":"MV","多米尼加":"DO","突尼斯":"TN","马里":"ML","巴哈马":"BS","纳米比亚":"NA","安提瓜和巴布达":"AG","佛得角":"CV","摩纳哥":"MC","密克罗尼西亚联邦":"FM","中华民国（台湾）":"TW","美属维尔京群岛":"VI","布基纳法索":"BF","罗马尼亚":"RO","根西岛":"GG","加纳":"GH","波黑":"BA","多米尼克":"DM","智利":"CL","圣多美和普林西比":"ST","墨西哥":"MX","吉尔吉斯斯坦":"KG","科科斯群岛":"CC","苏丹":"SD","巴林":"BH","阿塞拜疆":"AZ","安哥拉":"AO","圣马力诺":"SM","美国本土外小岛屿":"UM","巴拿马":"PA","斯威士兰":"SZ","卢森堡":"LU","斯洛伐克":"SK","毛里塔尼亚":"MR","法罗群岛":"FO","伊拉克":"IQ","安道尔":"AD","塞浦路斯":"CY","马达加斯加":"MG","法属波利尼西亚":"PF","约旦":"JO","克罗地亚":"HR","捷克":"CZ","荷兰加勒比区":"BQ","黎巴嫩":"LB","中国内地":"CN","新喀里多尼亚":"NC","刚果（布）":"CG","塞拉利昂":"SL","法属圭亚那":"GF","南非":"ZA","卡塔尔":"QA","乌兹别克斯坦":"UZ","巴拉圭":"PY","丹麦":"DK","爱尔兰":"IE","马绍尔群岛":"MH","缅甸":"MM","也门":"YE","科摩罗":"KM","利比亚":"LY","马尔维纳斯群岛（福克兰）":"FK","法属南部领地":"TF","尼日利亚":"NG","瑞士":"CH","萨摩亚":"WS","葡萄牙":"PT","爱沙尼亚":"EE","阿尔巴尼亚":"AL","毛里求斯":"MU","几内亚比绍":"GW","阿曼":"OM","南苏丹":"SS","刚果（金）":"CD","马提尼克":"MQ","斐济群岛":"FJ","格林纳达":"GD","蒙塞拉特岛":"MS","越南":"VN","塞尔维亚":"RS","圣诞岛":"CX","瑞典":"SE","津巴布韦":"ZW","斯洛文尼亚":"SI","赞比亚":"ZM"}
        
        name = response.xpath('/html/body/div[2]/div/div[1]/div[1]/div/div/ul/li[4]/text()').extract_first()
        # print("name", name)
        countryCode = dic[name]  ## <Serializable><string>国家Code
        countryChineaseName = name ## <Serializable><string>国家中文名称


        airportInfo["countryCode"] = countryCode ## <Serializable><string>国家Code
        airportInfo["countryChineaseName"] = countryChineaseName ## <Serializable><string>国家中文名称

        constAirportCountryInfosCache = self.constAirportCountryInfosCache
        airportCountryInfo = AirportCountryInfo() ## <AirportCountryInfo>机场国家固定信息
        airportCountryInfo.init() ## <AirportCountryInfo>机场国家固定信息
        airportCountryInfo["code"] = code ## <Serializable><string>三字码
        airportCountryInfo["countryCode"] = countryCode ## <Serializable><string>国家Code
        airportCountryInfo["countryChineaseName"] = countryChineaseName ## <Serializable><string>国家中文名称
        constAirportCountryInfosCache.insert(airportCountryInfo)

    def handleExtraAirportInfoInfo(self, airportInfo):
        # print('handleExtraAirportInfoInfo')
        code = airportInfo["code"] ## <Serializable><string>三字码
        countryChineaseName = airportInfo["countryChineaseName"] ## <Serializable><string>国家中文名称
        ##########################################################
        constAirportCountryInfosCache = self.constAirportCountryInfosCache
        airportCountryInfo = constAirportCountryInfosCache.getAirportCountryInfoByKeyValue("code", code)

        if not airportCountryInfo:
            url = "https://jichang.gjcha.com/jichang/"+code+".html"
            request = scrapy.Request(url, callback=self.parseExtra, meta = {'airportInfo': airportInfo}, dont_filter = True)
            return request

        airportInfo["countryCode"] = airportCountryInfo["countryCode"] ## <Serializable><string>国家Code
        airportInfo["countryChineaseName"] = airportCountryInfo["countryChineaseName"] ## <Serializable><string>国家中文名称

        ##########################################################
    def handleExtraInfo(self, sunwingInfo):
        # print("handleExtraInfo")
        oneways = sunwingInfo["oneways"] ## <Serializable><OnewayFlight[]>单程
        roundtrips = sunwingInfo["roundtrips"] ## <Serializable><RoundtripFlight[]>往返

        requests = []
        try:
            for onewayFlight in oneways:
                origin = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
                destinations = onewayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

                request = self.handleExtraAirportInfoInfo(origin)
                if request: requests.append(request)
                for oneAirportInfo in destinations:
                    request = self.handleExtraAirportInfoInfo(oneAirportInfo)
                    if request: requests.append(request)

            for roundtripFlight in roundtrips:
                origin = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
                destinations = roundtripFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

                request = self.handleExtraAirportInfoInfo(origin)
                if request: requests.append(request)
                for oneAirportInfo in destinations:
                    request = self.handleExtraAirportInfoInfo(oneAirportInfo)
                    if request: requests.append(request)

            return requests
        except Exception as e:
            traceback.print_exc()

    def parse_oneway(self, response):
        try:
            # text = "[{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Coco, Cuba (CCC)\",\"destinationCode\":\"CCC\"},{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Santa Maria, Cuba (SNU)\",\"destinationCode\":\"SNU\"},{\"gateWay\":\"YFC\",\"countryName\":\"Dominican Republic\",\"destinationName\":\"Punta Cana, Dominican Republic (PUJ)\",\"destinationCode\":\"PUJ\"},{\"gateWay\":\"YFC\",\"countryName\":\"Mexico\",\"destinationName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"destinationCode\":\"CUN\"}]"
            text = response.text

            # print("..parse_oneway")
            onewayFlight = response.meta.get('onewayFlight')
            destinations = onewayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

            # print(response.text)
            dests = json.loads(text)
            for oneDest in dests:
                gateWay = oneDest.get("gateWay")
                destinationName = oneDest.get("destinationName")
                destinationCode = oneDest.get("destinationCode")
                countryName = oneDest.get("countryName")

                airportInfo = AirportInfo()
                airportInfo.init()
                airportInfo["code"] = destinationCode ## <Serializable><string>三字码
                # airportInfo["countryId"] = countryId ## <Serializable><string>国家id
                airportInfo["airportName"] = destinationName ## <Serializable><string>机场名称
                airportInfo["countryName"] = countryName ## <Serializable><string>国家名称
                destinations.append(airportInfo)

        except Exception as e:
            raise
    
    # 单程 https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi
    def parse_mobile_getReturnDate(self, response):
        # cookie = response.headers.getlist('Set-Cookie')[0].decode("utf-8")
        flightChooseDate = response.meta.get('flightChooseDate')
        availableFromDates = flightChooseDate["availableFromDates"] ## <string[]>可用的开始时间
        availableReturnDates = flightChooseDate["availableReturnDates"] ## <string[]>可用的返回时间
        formData = flightChooseDate["formData"] ## <FormData>表单数据

        available_dates_list = response.xpath('//*[@id="contenu"]/div[2]/form/label')
        sid = response.xpath('//*[@id="contenu"]/div[2]/form/input[1]/@value').extract_first()
        formData["sid"] = sid ## <string>表单sid
        print("sid", sid)
        for one in available_dates_list:
            forDate = one.xpath('./@for').extract_first()
            if "dep" in forDate:
                print("dep", forDate)
                availableFromDates.append(forDate[4:])
            # <label for="ret-20221217" class="">Melbourne - Toronto (December 17, 2022)</label>
            if "ret" in forDate:
                print("ret", forDate)
                availableReturnDates.append(forDate[4:])
                 ## <string[]>可用的开始时间

            # "Toronto to Miami (December 18, 2022)"
            # dateStr = one.extract()
            # print()

        for availableFromDate in availableFromDates:
            flightChooseDateClone = flightChooseDate.clone()
            formData = flightChooseDate["formData"] ## <FormData>表单数据
            sid = formData["sid"] ## <string>表单sid


            flightChooseDate["selectFromDate"] = availableFromDate ## <Serializable><string>选择的开始时间
            # 网页版
            # https://book.sunwing.ca/cgi-bin/results.cgi
            # 手机版
            # url = "https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi"
            datas = {
                "sid": sid,
                "searchtype":"OW",
                "flex":"Y",
                "alias":"btd",
                "date_ret": "",    
                "date_dep": availableFromDate,
                "1b_select_flight_submit":"Select",
            }
            # 航班列表
            yield scrapy.FormRequest(url=url, callback=self.parse_flightList, formdata=datas, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True)
            break
    # 航班列表
    def parse_flightList(self, response):
        flightChooseDate = response.meta.get('flightChooseDate')
        formData = flightChooseDate["formData"] ## <FormData>表单数据
        sid = formData["sid"] ## <string>表单sid
        # price = response.xpath('//*[@id="cb2974771ed4e4d169d078e2f96a354d"]/div[1]/div[3]/a')
        # print("price++", price)
        # https://shopping.sunwing.ca/cgi-bin/ajax.cgi?action=JSON_RESULTS&sid=567c0f4be8d3727209b4b5a607eacb49&group_id=523cd76252cfa445ef143aa3b8fbcc2c&searchtype_json=OW&flex=N&displayType=O&result_detail_id=&page_length=10&sorted_by=price&showTaxIn=true&grouping_type=&page=1

        DOCUMENT_HEADER_RE = re.compile("'group_id': '(\w+)',", re.S)
        result = re.search(DOCUMENT_HEADER_RE, response.text)   # 使用match方法进行匹配操作
        if result:
            print("result", result.group(1))
            group_id = result.group(1)
            datas = {
                "action":"JSON_RESULTS",
                "sid": sid,
                "group_id":group_id,
                "searchtype_json":"OW",
                "flex":"N",
                "displayType":"O",
                "result_detail_id":"",
                "page_length":"10",
                "sorted_by":"price",
                "showTaxIn":"true",
                "grouping_type":"",
                "page":"1",

            }
            url = 'https://shopping.sunwing.ca/cgi-bin/ajax.cgi?' + parse.urlencode(datas)
            cookieStr = execjs.compile(" function createCookie(name, value, days) { if (days) { var date = new Date(); date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000)); var expires = \"; expires=\" + date.toGMTString(); } else var expires = \"\"; cookie = name + \"=\" + value + expires + \"; path=/\"; return cookie; }")\
                .call('createCookie', "groupID", group_id, 1)
            
            cookies = cookieString2CookieJar(cookieStr)
            print("cookies", cookies);
            yield scrapy.Request(url=url, callback=self.parse_flightList2, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True, cookies=cookies)

# {"resultats":[{"language":"en","searchtype":"OW","engine":"S","currency":"CAD","tour_op":"SWG","tour_op_name":"SUNWING VACATIONS","type_display_type":"M","result_type":"M","novolal":"","novolre":"","key_display_type":"20ed6c2132d9c7ca065fbf76ac223deb","key_grouping_outbound":"cb2974771ed4e4d169d078e2f96a354d","key_grouping_inbound":"d41d8cd98f00b204e9800998ecf8427e","outbound_duration":"0300","total_flights_duration":"0300","fare_type":"","isflex":"N","itineraries":[{"leg_type":"O","class":"A","class_category_name":"","class_category_desc":"","branded_fare_name":"","fare_basis_code":"","ancillary_category":"","airline":"WG","airline_name":"Sunwing Airlines","flight_no":"055","airport_dep":"YYZ","date_dep":"20221210","time_dep":"0655","airport_arr":"MLB","date_arr":"20221210","time_arr":"0955","via_arp":"","num_stops":"","connections":"0","terminal":"3","equipment_type":"737","duration":"0300","layover_duration":""}],"passengers":[{"nb":"1","price":"39.00","tax":"120.00","tax_details":"","totpax":"159.00","grtot":"159.00","net":"N","base_price":"39.00"}], "promos":[], "description_plus":[{"name":"Buy one, get one 40% off","text":"","url":"https://www.sunwing.ca/en/booking/buy-one-flight-get-one-flight"}],"resultid":"0","result_detail_id":"1546834813"}],"errors":{},"status":{},"nb_results":"1","nb_results_per_grouping":""}
    def parse_flightList2(self, response):
        flightChooseDate = response.meta.get('flightChooseDate')

        obj = json.loads(response.text)
        if "resultats" in obj:
            resultats = obj["resultats"]
            for resultats_mem in resultats:
                if "passengers" in resultats_mem:
                    passengers = resultats_mem["passengers"]
                    for passengers_mem in passengers:
                        # "grtot":"159.00"
                        if "grtot" in passengers_mem:
                            grtot = passengers_mem["grtot"]
                        # "totpax":"159.00"
                        if "totpax" in passengers_mem:
                            totpax = passengers_mem["totpax"]
                        # "tax":"120.00"
                        if "tax" in passengers_mem:
                            tax = passengers_mem["tax"]
                        # "net":"N"
                        if "net" in passengers_mem:
                            net = passengers_mem["net"]
                        # "nb":"1"
                        if "nb" in passengers_mem:
                            nb = passengers_mem["nb"]
                        # "price":"39.00"
                        if "price" in passengers_mem:
                            price = passengers_mem["price"]
                        # "base_price":"39.00"
                        if "base_price" in passengers_mem:
                            base_price = passengers_mem["base_price"]
                # "key_grouping_outbound":"cb2974771ed4e4d169d078e2f96a354d"
                if "key_grouping_outbound" in resultats_mem:
                    key_grouping_outbound = resultats_mem["key_grouping_outbound"]
                # "result_type":"M"
                if "result_type" in resultats_mem:
                    result_type = resultats_mem["result_type"]
                if "novolre" in resultats_mem:
                    novolre = resultats_mem["novolre"]
                # "tour_op":"SWG"
                if "tour_op" in resultats_mem:
                    tour_op = resultats_mem["tour_op"]
                if "novolal" in resultats_mem:
                    novolal = resultats_mem["novolal"]
                # "type_display_type":"M"
                if "type_display_type" in resultats_mem:
                    type_display_type = resultats_mem["type_display_type"]
                # "currency":"CAD"
                if "currency" in resultats_mem:
                    currency = resultats_mem["currency"]
                # "isflex":"N"
                if "isflex" in resultats_mem:
                    isflex = resultats_mem["isflex"]
                # "key_grouping_inbound":"d41d8cd98f00b204e9800998ecf8427e"
                if "key_grouping_inbound" in resultats_mem:
                    key_grouping_inbound = resultats_mem["key_grouping_inbound"]
                # "result_detail_id":"1546834813"
                if "result_detail_id" in resultats_mem:
                    result_detail_id = resultats_mem["result_detail_id"]
                # "resultid":"0"
                if "resultid" in resultats_mem:
                    resultid = resultats_mem["resultid"]
                # "total_flights_duration":"0300"
                if "total_flights_duration" in resultats_mem:
                    total_flights_duration = resultats_mem["total_flights_duration"]
                # "language":"en"
                if "language" in resultats_mem:
                    language = resultats_mem["language"]
                if "itineraries" in resultats_mem:
                    itineraries = resultats_mem["itineraries"]
                    for itineraries_mem in itineraries:
                        # "connections":"0"
                        if "connections" in itineraries_mem:
                            connections = itineraries_mem["connections"]
                        if "via_arp" in itineraries_mem:
                            via_arp = itineraries_mem["via_arp"]
                        # "flight_no":"055"
                        if "flight_no" in itineraries_mem:
                            flight_no = itineraries_mem["flight_no"]
                        if "num_stops" in itineraries_mem:
                            num_stops = itineraries_mem["num_stops"]
                        # "date_dep":"20221210"
                        if "date_dep" in itineraries_mem:
                            date_dep = itineraries_mem["date_dep"]
                        # "date_arr":"20221210"
                        if "date_arr" in itineraries_mem:
                            date_arr = itineraries_mem["date_arr"]
                        # "terminal":"3"
                        if "terminal" in itineraries_mem:
                            terminal = itineraries_mem["terminal"]
                        if "class_category_desc" in itineraries_mem:
                            class_category_desc = itineraries_mem["class_category_desc"]
                        if "ancillary_category" in itineraries_mem:
                            ancillary_category = itineraries_mem["ancillary_category"]
                        if "class_category_name" in itineraries_mem:
                            class_category_name = itineraries_mem["class_category_name"]
                        # "airline":"WG"
                        if "airline" in itineraries_mem:
                            airline = itineraries_mem["airline"]
                        # "time_arr":"0955"
                        if "time_arr" in itineraries_mem:
                            time_arr = itineraries_mem["time_arr"]
                        # "time_dep":"0655"
                        if "time_dep" in itineraries_mem:
                            time_dep = itineraries_mem["time_dep"]
                        # "leg_type":"O"
                        if "leg_type" in itineraries_mem:
                            leg_type = itineraries_mem["leg_type"]
                        # "duration":"0300"
                        if "duration" in itineraries_mem:
                            duration = itineraries_mem["duration"]
                        # "equipment_type":"737"
                        if "equipment_type" in itineraries_mem:
                            equipment_type = itineraries_mem["equipment_type"]
                        if "branded_fare_name" in itineraries_mem:
                            branded_fare_name = itineraries_mem["branded_fare_name"]
                        # "airport_arr":"MLB"
                        if "airport_arr" in itineraries_mem:
                            airport_arr = itineraries_mem["airport_arr"]
                        if "layover_duration" in itineraries_mem:
                            layover_duration = itineraries_mem["layover_duration"]
                        # "airline_name":"Sunwing Airlines"
                        if "airline_name" in itineraries_mem:
                            airline_name = itineraries_mem["airline_name"]
                        # "airport_dep":"YYZ"
                        if "airport_dep" in itineraries_mem:
                            airport_dep = itineraries_mem["airport_dep"]
                        # "class":"A"
                        if "class" in itineraries_mem:
                            classes = itineraries_mem["class"]
                        if "fare_basis_code" in itineraries_mem:
                            fare_basis_code = itineraries_mem["fare_basis_code"]
        # "nb_results":"1"
        if "nb_results" in obj:
            nb_results = obj["nb_results"]

        if time_arr:
            print("time_arr", time_arr)




    def parse_roundtrip(self, response):
        # print("..parse_roundtrip", response.text)
        text = response.text
        # text = "[{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Coco, Cuba (CCC)\",\"destinationCode\":\"CCC\"},{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Santa Maria, Cuba (SNU)\",\"destinationCode\":\"SNU\"},{\"gateWay\":\"YFC\",\"countryName\":\"Dominican Republic\",\"destinationName\":\"Punta Cana, Dominican Republic (PUJ)\",\"destinationCode\":\"PUJ\"},{\"gateWay\":\"YFC\",\"countryName\":\"Mexico\",\"destinationName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"destinationCode\":\"CUN\"}]"

        roundtripFlight = response.meta.get('roundtripFlight')
        destinations = roundtripFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

        # print(response.text)
        dests = json.loads(text)
        for oneDest in dests:
            gateWay = oneDest.get("gateWay")
            destinationName = oneDest.get("destinationName")
            destinationCode = oneDest.get("destinationCode")
            countryName = oneDest.get("countryName")

            airportInfo = AirportInfo() ## <AirportInfo>机场信息
            airportInfo.init() ## <AirportInfo>机场信息
            airportInfo["code"] = destinationCode ## <Serializable><string>三字码
            # airportInfo["countryId"] = countryId ## <Serializable><string>国家id
            airportInfo["airportName"] = destinationName ## <Serializable><string>机场名称
            airportInfo["countryName"] = countryName ## <Serializable><string>国家名称
            destinations.append(airportInfo)