import scrapy
import os, sys, json, traceback
import datetime, time, random
from calendar import monthrange

from properties.items import *
# https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/YYZ/OW
from urllib import parse
import logging, re
import execjs
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

class SunwingAdressSpider(scrapy.Spider):
    name = 'sunwing'
    # allowed_domains = ['sunwinggroup.ca']
    # start_urls = ['https://www.sunwing.ca/en/']
    
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com']
    
    oneway_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/OW'
    roundtrip_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/RE'
    
    def __init__(self, fromDate=None, returnDate=None, *args, **kwargs):
        super(SunwingSpider, self).__init__(*args, **kwargs)
        self.constAirportCountryInfosCache = ConstAirportCountryInfosCache()

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
        ##############################
        # chrome_cookiejar = browser_cookie3.chrome()
        # cookies = {}
        # for item in chrome_cookiejar:
        #     cookies[item.name] = item.value
        # self.cookies = None
        # self.cookies = {
        #     "SL_GWPT_Show_Hide_tmp": cookies["SL_GWPT_Show_Hide_tmp"],
        #     "SL_G_WPT_TO": cookies["SL_G_WPT_TO"],
        #     "SL_wptGlobTipTmp": cookies["SL_wptGlobTipTmp"],
        #     "SVAlias": cookies["SVAlias"],
        #     "SVDest": cookies["SVDest"],
        #     "SVLang": cookies["SVLang"],
        #     "SVsearchType": cookies["SVsearchType"],
        #     "__utmzz": cookies["__utmzz"],
        #     # "__utmzzses": cookies["__utmzzses"],
        #     "_ce.s": cookies["_ce.s"],
        #     "_clck": cookies["_clck"],
        #     "_clsk": cookies["_clsk"],
        #     "_ga": cookies["_ga"],
        #     "_gcl_au": cookies["_gcl_au"],
        #     "_gid": cookies["_gid"],
        #     "_hjAbsoluteSessionInProgress": cookies["_hjAbsoluteSessionInProgress"],
        #     "_ok": cookies["_ok"],
        #     "_okbk": cookies["_okbk"],
        #     "_okdetect": cookies["_okdetect"],
        #     "_okgid": cookies["_okgid"],
        #     "_oklv": cookies["_oklv"],
        #     "_pin_unauth": cookies["_pin_unauth"],
        #     "_scid": cookies["_scid"],
        #     "_sctr": cookies["_sctr"],
        #     "_st_bid": cookies["_st_bid"],
        #     "_tt_enable_cookie": cookies["_tt_enable_cookie"],
        #     "_ttp": cookies["_ttp"],
        #     "_uetsid": cookies["_uetsid"],
        #     "_uetvid": cookies["_uetvid"],
        #     "_up": cookies["_up"],
        #     "ajs_anonymous_id": cookies["ajs_anonymous_id"],
        #     "datadome": cookies["datadome"],
        #     "hblid": cookies["hblid"],
        #     "nf_lang": cookies["nf_lang"],
        #     "olfsk": cookies["olfsk"],
        #     "tms_VisitorID": cookies["tms_VisitorID"],
        #     "tms_wsip": cookies["tms_wsip"],
        #     "wcsid": cookies["wcsid"],
        # }
        


    # def start_requests(self):
    #     UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

    #     datas = {
    #         "jsData":"{\"ttst\":53.399999998509884,\"ifov\":false,\"log2\":false,\"wdif\":false,\"wdifrm\":false,\"log1\":false,\"br_h\":1110,\"br_w\":1557,\"br_oh\":984,\"br_ow\":1280,\"nddc\":1,\"rs_h\":1024,\"rs_w\":1280,\"rs_cd\":24,\"phe\":false,\"nm\":false,\"jsf\":false,\"ua\":\"Mozilla/10.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\",\"lg\":\"zh-CN\",\"pr\":0.800000011920929,\"hc\":8,\"ars_h\":984,\"ars_w\":1280,\"tz\":-480,\"str_ss\":true,\"str_ls\":true,\"str_idb\":true,\"str_odb\":true,\"plgod\":false,\"plg\":5,\"plgne\":true,\"plgre\":true,\"plgof\":false,\"plggt\":false,\"pltod\":false,\"hcovdr\":false,\"hcovdr2\":false,\"plovdr\":false,\"plovdr2\":false,\"ftsovdr\":false,\"ftsovdr2\":false,\"lb\":false,\"eva\":33,\"lo\":false,\"ts_mtp\":0,\"ts_tec\":false,\"ts_tsa\":false,\"vnd\":\"Google Inc.\",\"bid\":\"NA\",\"mmt\":\"application/pdf,text/pdf\",\"plu\":\"PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF\",\"hdn\":true,\"awe\":false,\"geb\":false,\"dat\":false,\"med\":\"defined\",\"aco\":\"probably\",\"acots\":false,\"acmp\":\"probably\",\"acmpts\":true,\"acw\":\"probably\",\"acwts\":false,\"acma\":\"maybe\",\"acmats\":false,\"acaa\":\"probably\",\"acaats\":true,\"ac3\":\"\",\"ac3ts\":false,\"acf\":\"probably\",\"acfts\":false,\"acmp4\":\"maybe\",\"acmp4ts\":false,\"acmp3\":\"probably\",\"acmp3ts\":false,\"acwm\":\"maybe\",\"acwmts\":false,\"ocpt\":false,\"vco\":\"probably\",\"vcots\":false,\"vch\":\"probably\",\"vchts\":true,\"vcw\":\"probably\",\"vcwts\":true,\"vc3\":\"maybe\",\"vc3ts\":false,\"vcmp\":\"\",\"vcmpts\":false,\"vcq\":\"\",\"vcqts\":false,\"vc1\":\"probably\",\"vc1ts\":true,\"dvm\":8,\"sqt\":false,\"so\":\"landscape-primary\",\"wbd\":false,\"wdw\":true,\"cokys\":\"bG9hZFRpbWVzY3NpYXBwcnVudGltZQ==L=\",\"ecpc\":false,\"lgs\":true,\"lgsod\":false,\"psn\":true,\"edp\":true,\"addt\":true,\"wsdc\":true,\"ccsr\":true,\"nuad\":true,\"bcda\":false,\"idn\":true,\"capi\":false,\"svde\":false,\"vpbq\":true,\"ucdv\":false,\"spwn\":false,\"emt\":false,\"bfr\":false,\"dbov\":false,\"npmtm\":false,\"glvd\":\"Google Inc. (NVIDIA)\",\"glrd\":\"ANGLE (NVIDIA, NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0, D3D11)\",\"tagpu\":11.600000001490116,\"prm\":true,\"tzp\":\"Asia/Shanghai\",\"cvs\":true,\"usb\":\"defined\",\"jset\":1666945129,\"cfpfe\":\"ZnVuY3Rpb24oYSl7dmFyIGI9UWEuX2dhVXNlclByZWZzO2lmKGImJmIuaW9vJiZiLmlvbygpfHxhJiYhMD09PVFhWyJnYS1kaXNhYmxlLSIrYV0pcmV0dXJuITA7dHJ5e3ZhciBjPVFhLmV4dGVybmFsO2lmKGMmJmMuX2dhVXNlclByZWZzJiYib28iPT1jLl9nYVVz\",\"stcfp\":\"bmFseXRpY3MuanM6NjI6NTgpCiAgICBhdCBaLnYgKGh0dHBzOi8vd3d3Lmdvb2dsZS1hbmFseXRpY3MuY29tL2FuYWx5dGljcy5qczo5OTozNjEpCiAgICBhdCBaLkQgKGh0dHBzOi8vd3d3Lmdvb2dsZS1hbmFseXRpY3MuY29tL2FuYWx5dGljcy5qczo5ODoxNzgp\",\"dcok\":\".sunwing.ca\",\"tbce\":0}",
    #         "events":"[{\"source\":{\"x\":307,\"y\":1107},\"message\":\"mouse move\",\"date\":1666945119004,\"id\":0},{\"source\":{\"x\":393,\"y\":818},\"message\":\"mouse move\",\"date\":1666945119114,\"id\":0},{\"source\":{\"x\":333,\"y\":743},\"message\":\"mouse move\",\"date\":1666945119387,\"id\":0},{\"source\":{\"x\":343,\"y\":767},\"message\":\"mouse move\",\"date\":1666945119497,\"id\":0},{\"source\":{\"x\":403,\"y\":727},\"message\":\"mouse move\",\"date\":1666945120774,\"id\":0}]",
    #         "eventCounters":"{\"mouse move\":13,\"mouse click\":0,\"scroll\":0,\"touch start\":0,\"touch end\":0,\"touch move\":0,\"key down\":0,\"key up\":0}",
    #         "jsType":"le",
    #         "cid":".DyGGoAIacy-NEd1E5v0LjbiVu6wFqavL2V3jwzUZZ8dexw8kjcFw6~2rHUIX61p-cXOspR0Nl_TJiLMDtBo7LmXUVwbPf6BV8F7xu0XImLLncA4VbsXfbREpu317VDp",
    #         "ddk":"E812CB49265F3F5AD3331EACED3A5C",
    #         "Referer":"https%3A%2F%2Fbook.sunwing.ca%2Fcgi-bin%2Fresults.cgi%3Fengines%3DS%26flex%3DY%26isMobile%3Dfalse%26searchtype%3DOW%26language%3Den%26code_ag%3Drds%26alias%3Dbtd%26date_dep%3D20221029%26gateway_dep%3DYYZ%26dest_dep%3DMLB%26nb_adult%3D1%26nb_child%3D0",
    #         "request":"%2Fcgi-bin%2Fresults.cgi%3Fengines%3DS%26flex%3DY%26isMobile%3Dfalse%26searchtype%3DOW%26language%3Den%26code_ag%3Drds%26alias%3Dbtd%26date_dep%3D20221029%26gateway_dep%3DYYZ%26dest_dep%3DMLB%26nb_adult%3D1%26nb_child%3D0",
    #         "responsePage":"origin",
    #         "ddv":"4.5.0",
    #     }
    #     jsData = json.loads(datas["jsData"])
    #     jsData["ua"] = UserAgent
    #     datas["jsData"] = json.dumps(jsData, ensure_ascii=False, separators=(',',':'))

    #     eventsArray = json.loads(datas["events"])
    #     for i in range(len(eventsArray)):
    #         one = eventsArray[i]
    #         one["date"] = int(time.time()) + random.randint(80 + 20*i, 120 + 20*i)
    #     datas["events"] = json.dumps(eventsArray, ensure_ascii=False, separators=(',',':'))

    #     url = "https://api-js.datadome.co/js/"
    #     yield scrapy.FormRequest(url=url, formdata=datas, callback=self.parseDatadome, cookies = self.cookies or {})

    # def parseDatadome(self, response):
    #     cookie = json.loads(response.text)["cookie"]
    #     cookie_dict =  cookieString2CookieDict(cookie)
    #     self.cookies = {
    #         "datadome": cookie_dict["datadome"]
    #     }
    #     url = self.start_urls[0]
    #     yield scrapy.Request(url=url, callback=self.parse, cookies = self.cookies or {})

    def getSearchtype(self, flightChooseDate):
        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        if flightType == FlightType.ONEWAY:
            return "OW"
        elif flightType == FlightType.ROUNDTRIP:
            return "RE"
    def parse(self, response):
        # print(".........", response.text)
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
        #     infoClone = airportInfo.cloneAll()
        #     onewayFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
        #     oneways.append(onewayFlight)


        #     roundtripFlight = RoundtripFlight() ## <RoundtripFlight>往返
        #     roundtripFlight.init()
        #     infoClone = airportInfo.cloneAll()
        #     roundtripFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
        #     roundtrips.append(roundtripFlight)

        # # print("sunwingInfo", sunwingInfo)

        try:
        #     for onewayFlight in oneways:
        #         airportInfo = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
        #         code = airportInfo["code"] ## <Serializable><string>三字码
        #         url = self.oneway_url.format(code)
            
        #         yield scrapy.Request(url, callback=self.parse_oneway, meta = {'onewayFlight': onewayFlight}, dont_filter = True, cookies = self.cookies or {})

        #     for roundtripFlight in roundtrips:
        #         airportInfo = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
        #         code = airportInfo["code"] ## <Serializable><string>三字码
        #         url = self.roundtrip_url.format(code)
        #         yield scrapy.Request(url, callback=self.parse_roundtrip, meta = {'roundtripFlight': roundtripFlight}, dont_filter = True, cookies = self.cookies or {})

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

            for i in range(1, 2):
                flightType = [FlightType.ONEWAY, FlightType.ROUNDTRIP][i]
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
            request = scrapy.Request(url, callback=self.parseExtra, meta = {'airportInfo': airportInfo}, dont_filter = True, cookies = self.cookies or {})
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
    def parse_getReturnDate(self, response):
        print("parse_chooseDate")
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
        print("parse_flightList")
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
        print("len(r0)", len(r0))
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
                print('r10:', r10)
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
                    print("time_arr", time_arr)
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
        print("request_prcie_detail")
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
        print("parse_verif1")
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
        # print('r7:', r7)
        # print('r8:', r8)
        # print('r9:', r9)
        print('r10:', r10)
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

        flightType = flightChooseDate["flightType"] ## <Serializable><int>行程类型
        allFlights = [chooseDepartingFlight, chooseReturningFlight]
        for i in range(len(r9)):            
            Fromdate = " ".join(r7[4*i:4*i+4])  ## <Serializable><string>
            Todate = " ".join(r8[4*i:4*i+4]) ## <Serializable><string>
            Nb_seats_for_ajax0 = ""
            if len(r9) > 0:
                Nb_seats_for_ajax0 = r9[i] ## <Serializable><string>
            flight = allFlights[i]
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
