import scrapy
import os, sys, json, traceback
import datetime, time, random
from calendar import monthrange
# print(client.get(code='MOW'))
# print(client.get(country_code='RU'))
# print(client.get(name='Moscow'))
from properties.items import *
# https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/YYZ/OW
from urllib import parse
import logging, re
import execjs
# https://api-js.datadome.co/js/
# https://services.sunwinggroup.ca/beta/api//SV/search/getGatewayforBrand/en/SWG
# {"status":200,"cookie":"datadome=_QKhGLZpS2Cuwzl9v75n_NjgXv~iwJrgvUMfCuJACquQZ.zVewajLK-2nB2__eBjnDe_wWSU7iAs6ONVuD.gKU63DlcFEyEAKYLY0rgEeb-phsH.XmSnFZ-n9mleygD; Max-Age=31536000; Domain=.captcha-delivery.com; Path=/; Secure; SameSite=Lax"}
# https://login.sunwing.ca/api/v1/sessions/me
# https://bsb.widgets.sunwingtravelgroup.com/session
# https://book.sunwing.ca/cgi-bin/results.cgi?engines=S&flex=Y&isMobile=false&searchtype=RE&language=en&code_ag=rds&alias=btd&date_dep=20221028&gateway_dep=YYZ&dest_dep=MLB&nb_adult=2&nb_child=0&date_ret=20221104
import browser_cookie3

class SunwingTicketSpider(scrapy.Spider):
    name = 'sunwingTicketSpider'
    allowed_domains = ['sunwinggroup.ca']
    start_urls = ['https://www.sunwing.ca/en/']
 
    def __init__(self, fromDate=None, returnDate=None, *args, **kwargs):
        super(SunwingTicketSpider, self).__init__(*args, **kwargs)

        nowDate = datetime.datetime.now().strftime('%Y%m%d')
        tomorrowDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
        if fromDate == None:
            fromDate = tomorrowDate

        self.fromDate = fromDate
        
        if returnDate == None:
            allDays = monthrange(datetime.datetime.now().year, datetime.datetime.now().month )[1]
            returnDate = "%02d%02d%02d"%(datetime.datetime.now().year, datetime.datetime.now().month, allDays)
            theDayAfterTomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")

            if returnDate == nowDate:
                returnDate = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")
        self.returnDate = returnDate
        self.cookies = {}
        json_path = os.getcwd() + "/datas/Sunwing.json"
        sunwingInfo = SunwingInfo() ## <SunwingInfo>所有信息
        with open(json_path, "r", encoding='utf-8') as fp:
            jsonStr = fp.read()
            sunwingInfo.jsonLoads(jsonStr)
        self.sunwingInfo = sunwingInfo
        ##############################
 
    def getSearchtype(self, flightChooseDate):
        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        if flightType == FlightType.ONEWAY:
            return "OW"
        elif flightType == FlightType.ROUNDTRIP:
            return "RE"
    def parse(self, response):
        print("<<<<<<<<<<<<<<<<<<<<<<<<<")

        sunwingInfo = self.sunwingInfo ## <SunwingInfo>所有信息
        # sunwingInfo.init()
        # sunwingInfo.jsonLoads("{\"oneways\":[{\"origin\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MCO\",\"countryId\":\"\",\"airportName\":\"Orlando, Florida, USA (MCO)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[]},{\"origin\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]}],\"roundtrips\":[{\"origin\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"FPO\",\"countryId\":\"\",\"airportName\":\"Freeport / Grand Bahama, Bahamas (FPO)\",\"countryName\":\"Bahamas\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ADZ\",\"countryId\":\"\",\"airportName\":\"San Andres, Colombia (ADZ)\",\"countryName\":\"Colombia\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZO\",\"countryId\":\"\",\"airportName\":\"Manzanillo de Cuba, Cuba (MZO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ACA\",\"countryId\":\"\",\"airportName\":\"Acapulco, Mexico (ACA)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SXM\",\"countryId\":\"\",\"airportName\":\"St Maarten / Saint Martin,  (SXM)\",\"countryName\":\"St Maarten\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"ANU\",\"countryId\":\"\",\"airportName\":\"Antigua and Barbuda, Antigua (ANU)\",\"countryName\":\"Antigua\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"AUA\",\"countryId\":\"\",\"airportName\":\"Aruba (AUA)\",\"countryName\":\"Aruba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"FPO\",\"countryId\":\"\",\"airportName\":\"Freeport / Grand Bahama, Bahamas (FPO)\",\"countryName\":\"Bahamas\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"LIR\",\"countryId\":\"\",\"airportName\":\"Liberia / Guanacaste, Costa Rica (LIR)\",\"countryName\":\"Costa Rica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CYO\",\"countryId\":\"\",\"airportName\":\"Cayo Largo, Cuba (CYO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"HOG\",\"countryId\":\"\",\"airportName\":\"Holguin, Cuba (HOG)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZO\",\"countryId\":\"\",\"airportName\":\"Manzanillo de Cuba, Cuba (MZO)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"GND\",\"countryId\":\"\",\"airportName\":\"Grenada (GND)\",\"countryName\":\"Grenada\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RTB\",\"countryId\":\"\",\"airportName\":\"Roatan, Honduras (RTB)\",\"countryName\":\"Honduras\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MBJ\",\"countryId\":\"\",\"airportName\":\"Montego Bay, Jamaica (MBJ)\",\"countryName\":\"Jamaica\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"ACA\",\"countryId\":\"\",\"airportName\":\"Acapulco, Mexico (ACA)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"RIH\",\"countryId\":\"\",\"airportName\":\"Playa Blanca, Panama (RIH)\",\"countryName\":\"Panama\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"UVF\",\"countryId\":\"\",\"airportName\":\"Saint Lucia  (UVF)\",\"countryName\":\"Saint Lucia\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SXM\",\"countryId\":\"\",\"airportName\":\"St Maarten / Saint Martin,  (SXM)\",\"countryName\":\"St Maarten\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MIA\",\"countryId\":\"\",\"airportName\":\"Miami/Fort Lauderdale, Florida, USA (MIA)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MCO\",\"countryId\":\"\",\"airportName\":\"Orlando, Florida, USA (MCO)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]},{\"origin\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},\"destinations\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"VRA\",\"countryId\":\"\",\"airportName\":\"Varadero, Cuba (VRA)\",\"countryName\":\"Cuba\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"POP\",\"countryId\":\"\",\"airportName\":\"Puerto Plata, Dominican Republic (POP)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"SJD\",\"countryId\":\"\",\"airportName\":\"Los Cabos, Mexico (SJD)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MZT\",\"countryId\":\"\",\"airportName\":\"Mazatlan, Mexico (MZT)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"PVR\",\"countryId\":\"\",\"airportName\":\"Puerto Vallarta, Mexico (PVR)\",\"countryName\":\"Mexico\",\"countryCode\":\"\",\"countryChineaseName\":\"\"},{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryCode\":\"\",\"countryChineaseName\":\"\"}]}]}")

        try:
            oneways = sunwingInfo["oneways"] ## <Serializable><OnewayFlight[]>单程
            roundtrips = sunwingInfo["roundtrips"] ## <Serializable><RoundtripFlight[]>往返

            for wayFlight in (oneways+roundtrips):
                flightType = wayFlight["flightType"] ## <int>
            # airportInfo = AirportInfo() ## <AirportInfo>机场信息
            # airportInfo.init() ## <AirportInfo>机场信息
            # airportInfo.jsonLoads("{\"airportName\":\"Toronto\",\"countryName\":\"\",\"countryChineaseName\":\"加拿大\",\"countryCode\":\"CA\",\"countryId\":1,\"code\":\"YYZ\"}")
            # origin = airportInfo

            # airportInfo = AirportInfo() ## <AirportInfo>机场信息
            # airportInfo.init() ## <AirportInfo>机场信息
            # airportInfo.jsonLoads("{\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\",\"countryChineaseName\":\"美国\",\"countryCode\":\"US\",\"countryId\":\"\",\"code\":\"MLB\"}")
            # destination = airportInfo
                origin = wayFlight["origin"] ## <Serializable><AirportInfo>起始地
                destinations = wayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

                for destination in destinations:
                    fromDate =self.fromDate
                    returnDate =self.returnDate

                    # flightType = [FlightType.ONEWAY, FlightType.ROUNDTRIP][i]
                    flightChooseDate = FlightChooseDate() ## <FlightChooseDate>选择飞行时间
                    flightChooseDate.init() ## <FlightChooseDate>选择飞行时间
                    flightChooseDate["flightType"] = flightType ## <Serializable><int>行程类型
                    flightChooseDate["origin"] = origin ## <Serializable><AirportInfo>起始机场
                    flightChooseDate["destination"] = destination ## <Serializable><AirportInfo>目的机场
                    flightChooseDate["fromDate"] = fromDate ## <Serializable><string>开始时间
                    flightChooseDate["returnDate"] = returnDate ## <Serializable><string>返回时间
                    # https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi?

                    flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
                    origin = flightChooseDate["origin"]
                    fromDate = flightChooseDate["fromDate"]
                    origin_code = origin["code"] ## <Serializable><string>三字码

                    destination = flightChooseDate["destination"]
                    destination_code = destination["code"] ## <Serializable><string>三字码

                    datas = {
                        "alias":"btd",
                        "code_ag":"rds",
                        "date_dep": fromDate,
                        "dest_dep": destination_code,
                        "engines":"S",
                        "flex":"Y",
                        "gateway_dep": origin_code,
                        "isMobile":"false",
                        "language":"en",
                        "nb_adult":"1",
                        "nb_child":"0",
                        "searchtype": self.getSearchtype(flightChooseDate),
                    }
                    if flightType == FlightType.ROUNDTRIP:
                        datas["date_ret"] = returnDate
                        # datas = {
                        #     "alias":"btd",
                        #     "code_ag":"rds",
                        #     "date_dep":"20221028",
                        #     "date_ret":"20221104",
                        #     "dest_dep":"MLB",
                        #     "engines":"S",
                        #     "flex":"Y",
                        #     "gateway_dep":"YYZ",
                        #     "isMobile":"false",
                        #     "language":"en",
                        #     "nb_adult":"1",
                        #     "nb_child":"0",
                        #     "searchtype":"RE",
                        # }

                    url = "https://book.sunwing.ca/cgi-bin/results.cgi?" + parse.urlencode(datas)
                    yield scrapy.Request(url=url, callback=self.parse_getReturnDate, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True, headers={'Referer':'https://www.sunwing.ca/'}, cookies = self.cookies or {})

                # if len(destinations) > 0:
                #     break
        except Exception as e:
            print('获取页数失败', str(e))
            traceback.print_exc()

    # 单程 https://shopping.sunwing.ca/cgi-bin/mobile/results.cgi
    def parse_getReturnDate(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> parse choose date")
        flightChooseDate = response.meta.get('flightChooseDate')
        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型

        availableFromDates = flightChooseDate["availableFromDates"] ## <string[]>可用的开始时间
        availableReturnDates = flightChooseDate["availableReturnDates"] ## <string[]>可用的返回时间
        formData = flightChooseDate["formData"] ## <FormData>表单数据

        available_dates_list = response.xpath('//*[@id="content"]/form/div/div[1]/div[2]/label')
        sid = response.xpath('//*[@id="content"]/form/input[1]/@value').extract_first()
        formData["sid"] = sid ## <string>表单sid

        for one in available_dates_list:
            forDate = one.xpath('./@for').extract_first()
            if "dep" in forDate:
                availableFromDates.append(forDate[8:])
            if "ret" in forDate:
                availableReturnDates.append(forDate[8:])

        flightChooseDateArray = []
        if flightType == FlightType.ONEWAY:
            for availableFromDate in availableFromDates:
                flightChooseDateClone = flightChooseDate.cloneAll()
                flightChooseDateClone["selectFromDate"] = availableFromDate ## <Serializable><string>选择的开始时间
                flightChooseDateArray.append(flightChooseDateClone)
        elif flightType == FlightType.ROUNDTRIP:
            for availableFromDate in availableFromDates:
                for availableReturnDate in availableReturnDates:
                    flightChooseDateClone = flightChooseDate.cloneAll()
                    flightChooseDateClone["selectFromDate"] = availableFromDate ## <Serializable><string>选择的开始时间
                    flightChooseDateClone["selectReturnDate"] = availableReturnDate ## <Serializable><string>选择的返回时间
                    flightChooseDateArray.append(flightChooseDateClone)
        for one_flightChooseDate in flightChooseDateArray:
            one_flightType = one_flightChooseDate["flightType"] ## <Serializable><int>行程类型
            one_selectFromDate = one_flightChooseDate["selectFromDate"] ## <Serializable><string>选择的开始时间
            one_selectReturnDate = one_flightChooseDate["selectReturnDate"] ## <Serializable><string>选择的返回时间
            # 网页版
            # https://book.sunwing.ca/cgi-bin/results.cgi
            datas = {
                "sid": sid,
                "searchtype": self.getSearchtype(one_flightChooseDate),
                "flex":"Y",
                "date_dep": one_selectFromDate,
                # "date_ret": "",
                "alias":"btd",
                "1b_select_flight_submit":"Select",
            }

            if flightType == FlightType.ROUNDTRIP:
                datas["date_ret"] = one_selectReturnDate
            # "sid":"4fb57acd9e09aa91fee34158b1d65310",
            # "searchtype":"OW",
            # "flex":"Y",
            # "alias":"btd",
            # "date_dep":"20221210",
            #  date_ret    
            # "1b_select_flight_submit":"Select",

            # "sid":"7c0f165f7e4154f410253009e70ec6e1",
            # "searchtype":"RE",
            # "flex":"Y",
            # "alias":"btd",
            # "date_dep":"20221217",
            # "date_ret":"20221221",
            # "1b_select_flight_submit":"Select",

            
            headers = response.headers
            headers["sid"] = sid

            if one_flightType == FlightType.ROUNDTRIP:
                datas["date_ret"] = one_selectReturnDate
            # print("datas", datas);
            url = "https://book.sunwing.ca/cgi-bin/results.cgi"
            # 航班列表
            yield scrapy.FormRequest(url=url, headers=headers, callback=self.parse_flightList, formdata=datas, meta = {'flightChooseDate': one_flightChooseDate}, dont_filter = True, cookies = self.cookies or {})

    # 航班列表
    def parse_flightList(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> parse flight info")
        flightChooseDate = response.meta.get('flightChooseDate')
        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        departingFlights = flightChooseDate["departingFlights"] ## <Flight>出发航班
        returningFlights = flightChooseDate["returningFlights"] ## <Flight>返程航班

        selectFromDate = flightChooseDate["selectFromDate"] ## <Serializable><string>选择的开始时间
        selectReturnDate = flightChooseDate["selectReturnDate"] ## <Serializable><string>选择的返回时间
        # print("flightChooseDate", flightChooseDate["formData"])
        # //*[@id="content"]/div[2]/section/form/div[1]/div/table/tbody/tr/td[1]/div/a
        root = response
        # r0 = root.xpath('/html/body/div[2]/div/div[2]/section/form')
        r0 = root.xpath('//*[@id="content"]/div[2]/section/form/div')
        r1 = root.xpath('//*[@id="content"]/div[2]/section[2]/div')
        
        forms = [r0, r1]
        flights = [departingFlights, returningFlights]
        
        for i in range(2):
            drForm = forms[i]

            oneFilght = flights[i]
            for form in drForm:
                r10 = form.xpath('./div/table/tbody/tr/td[1]/div/a/text()').getall()
                r11 = form.xpath('./div/table/tbody/tr/td[1]/div//li/text()').getall()
                r2 = form.xpath('./div/table/tbody/tr/td[2]/table/tbody/tr/td[1]/div//span//text()').getall()
                r3 = form.xpath('./div/table/tbody/tr/td[2]/table/tbody/tr/td[2]//text()').getall()
                r4 = form.xpath('./div/table/tbody/tr/td[2]/table/tbody/tr/td[3]//text()').getall()
                r5 = form.xpath('./div/table/tbody/tr/td[3]//text()').getall()
                r6 = root.xpath('./div/table/tbody/tr/td[4]/div[2]/a/text()').getall()
                r7 = form.xpath('./div/table/tbody/tr/td[5]/table/tbody/tr[1]/td/div/input/@value').getall()
                r8 = form.xpath('./div/table/tbody/tr/td[5]/table/tbody/tr[1]/td/div/label/span/text()').getall()
                r9 = form.xpath('./div/table/tbody/tr/td[5]/table/tbody/tr[1]/td/div/label/@class').getall()

                # r10: ['WG055']
                # r11: ['Operated by Sunwing Airlines', 'Class: A', '737']
                # r2: ['Sat', 'Dec 17', '2022']
                # r3: ['\n                                                        ', 'Departing', '6:55 am\n                                                    ']
                # r4: ['\n                                                        ', 'Arriving', '9:55 am', 'Sat\n                                                    ']
                # r5: ['03h 00m']
                # r6: []
                # r7: ['eJwBUAKv_VNhbHRlZF9ficMNI4q68oNHgZzhIl77yhPEU1CUJPxxcvWGZTCeUf9KQuc2YqvefbKvwe_V6gYgzHCBwyVzRhMaFhVAS7d8YomvBVKhhu_X_m1jXBV4_Si7Hqmr7nk3juX2a1jQB0OEGxWOLwU322-ZZYqrdxeRqmUbran8admd-ISkRroxwvRHjmYlVAfsFmj0Iq21Ljo9qJOTmyERYaY1ZUMDpCW3t0B-BSjbC3LNQxIP0PK4zCQA1UIlcTys5lqI8CrrS9iCYOGA1AlwoHGDdaKZEpouSlcMkDxj6_xI62CGbmzg--mln_LasbFEOa87Srast_FC9VOG-vSzlaLMNSKfYY8xYuPkddowF8JneovtLOxZxQeNuExf9AC8SyHQgePNWk2rlF2ve_30dIqNldrugYhk2PrCMXnCv321sNIgHV2aIBjCfTj4lYYN8zj7gfYPsLmsu_uvCUVF7BxNTlanw1x3L06OrBxtKEA_NDSDtD1GEoN6-4BLC5ridbXikkRFIJK6qKNenqrN16G8s7idyaEoR7nQqKp1VIf7JQTkpnxEA2YQiGqBS1NBqx-v5TFo2SmzNd7I-UWeDtF9LKuw8kwQAapuzR_mzO3hJpk6LnUash0uqZKWWnGsJJ5QnucNb125smTYR8GJaluhYOAxfJfqtdeHmw1_PFXgjk0ME2WMjRh_vCtoV2020W521s1BNBxnTBqXvRwc1x-Mf8_FKhXcTqROiI029ZotrnIrCFAyCzWmBwAJ83D35mAkuWRQmuDptKsKw86ylX4UeyW9', 'eJwBUAKv_VNhbHRlZF9ficMNI4q68oNHgZzhIl77yhPEU1CUJPxxcvWGZTCeUf9KQuc2YqvefbKvwe_V6gYgzHCBwyVzRhMaFhVAS7d8YomvBVKhhu_X_m1jXBV4_Si7Hqmr7nk3juX2a1jQB0OEGxWOLwU322-ZZYqrdxeRqmUbran8admd-ISkRroxwvRHjmYlVAfsFmj0Iq21Ljo9qJOTmyERYaY1ZUMDpCW3t0B-BSjbC3LNQxIP0PK4zCQA1UIlcTys5lqI8CrrS9iCYOGA1AlwoHGDdaKZEpouSlcMkDxj6_xI62CGbmzg--mln_LasbFEOa87Srast_FC9VOG-vSzlaLMNSKfYY8xYuPkddowF8JneovtLOxZxQeNuExf9AC8SyHQgePNWk2rlF2ve_30dIqNldrugYhk2PrCMXnCv321sNIgHV2aIBjCfTj4lYYN8zj7gfYPsLmsu_uvCUVF7BxNTlanw1x3L06OrBxtKEA_NDSDtD1GEoN6-4BLC5ridbXikkRFIJK6qKNenqrN16G8s7idyaEoR7nQqKp1VIf7JQTkpnxEA2YQiGqBS1NBqx-v5TFo2SmzNd7I-UWeDtF9LKuw8kwQAapuzR_mzO3hJpk6LnUash0uqZKWWnGsJJ5QnucNb125smTYR8GJaluhYOAxfJfqtdeHmw1_PFXgjk0ME2WMjRh_vCtoV2020W521s1BNBxnTBqXvRwc1x-Mf8_FKhXcTqROiI029ZotrnIrCFAyCzWmBwAJ83D35mAkuWRQmuDptKsKw86ylX4UeyW9']
                # r8: ['$199', '$249']
                # r8: ['position_static', 'has_hoverover position_static']
                
                for i in range(len(r10)):
                    # print('r10:', r10)
                    # print('r11:', r11)
                    # print('r2:', r2)
                    # print('r3:', r3)
                    # print('r4:', r4)
                    # print('r5:', r5)
                    # print('r6:', r6)
                    # # print('r7:', r7)
                    # print('r8:', r8)
                    # print('r9:', r9)

                    flightName = r10[i]
                    planeName = r11[-1] ## <Serializable><string>飞机名字
                    Itinerary = " ".join(r2) ## <string>旅行日程

                    allTickets = []
                    for i in range(len(r7)):

                        resultatsAller = r7[i]## <Serializable><string>key
                        price = r8[i] ## <Serializable><string>价格
                        has_hoverover = 'has_hoverover' in r9[i]

                        ticket = Ticket() ## <Ticket>票据
                        ticket.init() ## <Ticket>票据
                        ticket["ticketType"] = i ## <int>票据类型
                        ticket["resultatsAller"] = resultatsAller ## <Serializable><string>key
                        ticket["price"] = price ## <Serializable><string>价格
                        ticket["has_hoverover"] = has_hoverover ## <Serializable><bool>已经卖完了
                        allTickets.append(ticket)

                    time_dep = r3[-1] ## <Serializable><string>出发时间
                    time_arr = " ".join(r4[1:4]).strip() ## <Serializable><string>到达时间
                    
                    # choosePriceclassType = ## <Serializable><int>航班选择时选择费用类型
                    duration = r5[0] ## <Serializable><string>时间跨度

                    flight = Flight() ## <Flight>来回航班
                    flight.init() ## <Flight>来回航班
                    flight["flightName"] = flightName ## <Serializable><string>航班名字
                    flight["planeName"] = planeName ## <Serializable><string>飞机名字
                    flight["allTickets"] = allTickets ## <Ticket[]>所有可选的票
                    # flight["chooseTicket"] = chooseTicket ## <Serializable><Ticket>航班选择时选择费用类型
                    flight["Itinerary"] = Itinerary ## <string>旅行日程
                    flight["time_dep"] = time_dep ## <Serializable><string>出发时间
                    flight["time_arr"] = time_arr ## <Serializable><string>到达时间
                    flight["duration"] = duration ## <Serializable><string>时间跨度

                    oneFilght.append(flight)

        flightChooseDateArray = []
        if flightType == FlightType.ONEWAY:
            for one_departingFlight in departingFlights:
                flightChooseDateClone = flightChooseDate.cloneAll()
                flightChooseDateClone["chooseDepartingFlight"] = one_departingFlight.cloneAll() ## <Serializable><Flight>选择出发航班


                chooseDepartingFlight = flightChooseDateClone["chooseDepartingFlight"]
                allTickets = chooseDepartingFlight["allTickets"] ## <Ticket[]>所有可选的票
                for oneTicket in allTickets:
                    _flightChooseDateClone = flightChooseDateClone.cloneAll()
                    has_hoverover = oneTicket["has_hoverover"] ## <Serializable><bool>已经卖完了
                    if not has_hoverover:
                        chooseDepartingFlight = _flightChooseDateClone["chooseDepartingFlight"] ## <Serializable><Flight>选择出发航班
                        chooseDepartingFlight["chooseTicket"] = oneTicket ## <Serializable><Ticket>选择票据
                        flightChooseDateArray.append(_flightChooseDateClone)
        elif flightType == FlightType.ROUNDTRIP:
            for one_departingFlight in departingFlights:
                for one_returningFlight in returningFlights:
                    flightChooseDateClone = flightChooseDate.cloneAll()
                    flightChooseDateClone["chooseDepartingFlight"] = one_departingFlight.cloneAll() ## <Serializable><Flight>选择出发航班
                    flightChooseDateClone["chooseReturningFlight"] = one_returningFlight.cloneAll() ## <Serializable><Flight>选择返程航班

                    chooseDepartingFlight = flightChooseDateClone["chooseDepartingFlight"]
                    chooseDepartingFlight_allTickets = chooseDepartingFlight["allTickets"] ## <Ticket[]>所有可选的票
                    chooseReturningFlight = flightChooseDateClone["chooseReturningFlight"]
                    chooseReturningFlight_allTickets = chooseReturningFlight["allTickets"] ## <Ticket[]>所有可选的票
                    for idx in range(len(chooseDepartingFlight_allTickets)):

                        oneChooseDepartingFlight_allTicket = chooseDepartingFlight_allTickets[idx]

                        if idx < len(chooseReturningFlight_allTickets):
                            oneChooseReturningFlight_allTicket = chooseReturningFlight_allTickets[idx]
                            has_hoverover = oneChooseDepartingFlight_allTicket["has_hoverover"] ## <Serializable><bool>已经卖完了
                            if not has_hoverover:
                                _flightChooseDateClone = flightChooseDateClone.cloneAll()

                                _chooseDepartingFlight = _flightChooseDateClone["chooseDepartingFlight"]
                                _chooseDepartingFlight["chooseTicket"] = oneChooseDepartingFlight_allTicket ## <Serializable><Ticket>选择票据

                                _chooseReturningFlight = _flightChooseDateClone["chooseReturningFlight"]
                                _chooseReturningFlight["chooseTicket"] = oneChooseReturningFlight_allTicket ## <Serializable><Ticket>选择票据
                                flightChooseDateArray.append(_flightChooseDateClone)

        for flightChooseDate in flightChooseDateArray:
            yield self.request_prcie_detail(flightChooseDate)


    def request_prcie_detail(self, flightChooseDate):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> request prcie detail")
        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        chooseDepartingFlight = flightChooseDate["chooseDepartingFlight"] ## <Serializable><Flight>选择出发航班
        chooseReturningFlight = flightChooseDate["chooseReturningFlight"] ## <Serializable><Flight>选择返程航班
        formData = flightChooseDate["formData"] ## <FormData>表单数据
        if flightType == FlightType.ONEWAY:
            chooseTicket = chooseDepartingFlight["chooseTicket"] ## <Serializable><Ticket>选择票据
            ticketType = chooseTicket["ticketType"] ## <int>票据类型
            resultatsAller = chooseTicket["resultatsAller"] ## <Serializable><string>key

            priceclass = None
            if ticketType == TicketType.Regular:
                priceclass = "regular"
            elif ticketType == TicketType.Flexible:
                priceclass = "flexible"
            else:
                priceclass = "full"

            datas = {
                "sid":formData["sid"], 
                "resultatsAller": resultatsAller,
                "priceclass": priceclass,
                "package1_submit":"Continue", 
                "language":"en",
                "is_domestic":"1",
            }

            url = "https://book.sunwing.ca/cgi-bin/verif.cgi"
            
            return scrapy.FormRequest(url=url, callback=self.parse_verif, formdata=datas, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True, cookies = self.cookies or {})
        elif flightType == FlightType.ROUNDTRIP:

            departing_chooseTicket = chooseDepartingFlight["chooseTicket"] ## <Serializable><Ticket>选择票据
            departing_ticketType = departing_chooseTicket["ticketType"] ## <int>票据类型
            departing_resultatsAller = departing_chooseTicket["resultatsAller"] ## <Serializable><string>key

            returning_chooseTicket = chooseReturningFlight["chooseTicket"] ## <Serializable><Ticket>选择票据
            returning_ticketType = returning_chooseTicket["ticketType"] ## <int>票据类型
            returning_resultatsAller = returning_chooseTicket["resultatsAller"] ## <Serializable><string>key

            if departing_ticketType == TicketType.Regular:
                priceclass = "regular"
            elif departing_ticketType == TicketType.Flexible:
                priceclass = "flexible"
            else:
                priceclass = "full"

            datas = {
                "is_domestic":"1",
                "language":"en",
                "package3_submit":"Continue", 
                "priceclass": priceclass,
                "resultatsAller": departing_resultatsAller,
                "resultatsRetour": returning_resultatsAller,
                "sid": formData["sid"],
            }

            url = "https://book.sunwing.ca/cgi-bin/verif.cgi"
            return scrapy.FormRequest(url=url, callback=self.parse_verif, formdata=datas, meta = {'flightChooseDate': flightChooseDate}, dont_filter = True, cookies = self.cookies or {})

    def parse_verif(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> parse verif")
        flightChooseDate = response.meta.get('flightChooseDate')
        chooseDepartingFlight = flightChooseDate["chooseDepartingFlight"] ## <Serializable><Flight>选择出发航班
        chooseReturningFlight = flightChooseDate["chooseReturningFlight"] ## <Serializable><Flight>选择返程航班


        Upgrade_Your_Experience = flightChooseDate["Upgrade_Your_Experience"] ## <Serializable><Fee[]>
        Protect_Your_Vacation = flightChooseDate["Protect_Your_Vacation"] ## <Serializable><Fee[]>
        Airport_Lounge = flightChooseDate["Airport_Lounge"] ## <Serializable><Fee[]>
        Excursions = flightChooseDate["Excursions"] ## <Serializable><Fee[]>

        feeArray = [Upgrade_Your_Experience, Protect_Your_Vacation, Airport_Lounge]

        root = response
        r0 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section/section')
        r1 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section/div')
        
        for i in range(len(r0)):
            r00 = r0[i].xpath('./div')
            for j in range(len(r00)):

                # r0000: ['Pre Purchase 1st Bag For Departing Flight']
                # r0001: ['+$50', '.00', 'per person', '\n\t\t      \t\t\t\t']
                r0000 = r00[j].xpath('./div[1]/h4//text()').getall()
                r0001 = r00[j].xpath('./div[2]/div/p//text()').getall()
                if len(r0001) > 0 and len(r0000) > 0:
                    fee = Fee()
                    fee.init() ## <Fee>
                    feeName = r0000[0] ## <Serializable><string>费用名字
                    feePrice = " ".join(r0001[0:3]) ## <Serializable><string>费用价格

                    
                    fee["feeName"] = feeName ## <Serializable><string>费用名字
                    fee["feePrice"] = feePrice ## <Serializable>
                    feeArray[i].append(fee)

        for i in range(len(r1)):
            # r10: ['Brevard Zoo 1 Day Admission']
            # r11: ['\n\t      \t\t\t\t\t', '+$40', '.00', 'per person', '\n\t\t      \t\t\t\t', '\t      \t\t\t\t\t\t\t\n\t      \t\t\t\t']
            r10 = r1[i].xpath('./div/div[2]/div[2]/h5//text()').getall()
            r11 = r1[i].xpath('./div/div[2]/div[3]//text()').getall()
            fee = Fee()
            fee.init() ## <Fee>
            if r10 and r11:
                feeName = r10[0] ## <Serializable><string>费用名字
                feePrice = " ".join(r11[1:4]) ## <Serializable><string>费用价格

                fee["feeName"] = feeName ## <Serializable><string>费用名字
                fee["feePrice"] = feePrice ## <Serializable>
                Excursions.append(fee)
        
        r7 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section[2]/div[1]/ul/li/ul/li[4]/span//text()').getall()
        r8 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section[2]/div[1]/ul/li/ul/li[5]/span/nobr//text()').getall()
        r9 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section[2]/div[1]/ul/li/ul/li[6]//text()').getall()
        r10 = root.xpath('//*[@id="flightpricetable"]/tr[2]//text()').getall()
        r11 = root.xpath('//*[@id="flightpricetable"]/tr[3]//text()').getall()
        r12 = root.xpath('//*[@id="flightpricetable"]/tr[4]/td[2]//text()').getall()
        r13 = root.xpath('//*[@id="flightpricetable"]/tr[5]/td[2]//text()').getall()
        r14 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section[2]/div[1]/ul/li/ul/li[2]/span[1]//text()').getall()
        r15 = root.xpath('/html/body/div[2]/div[1]/div[2]/form/section[2]/div[1]/ul/li/ul/li[2]/span[2]//text()').getall()
        # print('r7:', r7)
        # print('r8:', r8)
        # print('r9:', r9)
        # print('r10:', r10)
        # print('r11:', r11)
        # print('r12:', r12)
        # print('r13:', r13)


        # r7: ['Departing: ', 'Sat Dec 10 2022', ' ', '6:55 AM', 'Departing: ', 'Sat Dec 10 2022', ' ', '12:25 PM']
        # r8: ['Arriving: ', 'Sat Dec 10 2022', ' ', '9:55 AM', 'Arriving: ', 'Sat Dec 10 2022', ' ', '3:10 PM']
        # r9: ['1 ticket: 1 adults ', '1 ticket: 1 adults ']
        # r10: ['\n            ', 'Air\xa0Transportation Charges', '\n            ', '1 X ', '$119.00', '\n          ']
        # r11: ['\n            ', 'Surcharges', '\n            ', '1 X ', '$38.88', '\n          ']
        # r12: ['1 X ', '$144.57']
        # r13: ['$302.45 ', 'CAD']
        # r14: ['Toronto (YYZ)', 'Melbourne (MLB )']
        # r15: ['Melbourne (MLB)', 'Toronto (YYZ )']


        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        allFlights = [chooseDepartingFlight, chooseReturningFlight]
        for i in range(len(r9)):            
            Fromdate = " ".join(r7[4*i:4*i+4])  ## <Serializable><string>
            Todate = " ".join(r8[4*i:4*i+4]) ## <Serializable><string>
            Nb_seats_for_ajax0 = ""
            if len(r9) > 0:
                Nb_seats_for_ajax0 = r9[i] ## <Serializable><string>
            flight = allFlights[i]
            flight["originCityName"] = r14[i] ## <string>出发城市
            flight["destinationCityName"] = r15[i] ## <string>到达城市
            flight["Fromdate"] = Fromdate ## <Serializable><string>
            flight["Todate"] = Todate ## <Serializable><string>
            flight["Nb_seats_for_ajax0"] = Nb_seats_for_ajax0 ## <Serializable><string>

        Air_Transportation_Charges = " ".join(r10[3:5])## <Serializable><string>
        Surcharges = ""
        if len(r11) > 5:
            Surcharges = " ".join([r11[1],r11[3],r11[4]])## <Serializable><string>
        Taxes_Fees_And_Charges = " ".join(r12)## <Serializable><string>
        Td_Pricetotal = " ".join(r13)## <Serializable><string>

        flightChooseDate["Excursions"] = Excursions ## <Serializable><Fee[]> flightChooseDate["Air_Transportation_Charges"] = Air_Transportation_Charges ## <Serializable><string>
        flightChooseDate["Air_Transportation_Charges"] = Air_Transportation_Charges ## <Serializable><string>
        flightChooseDate["Surcharges"] = Surcharges ## <Serializable><string>
        flightChooseDate["Taxes_Fees_And_Charges"] = Taxes_Fees_And_Charges ## <Serializable><string>
        flightChooseDate["Td_Pricetotal"] = Td_Pricetotal ## <Serializable><string>
        yield flightChooseDate
