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

    def getAirportCountryInfoByKeyValue(self, key, code):
        constAirportCountryInfo = self.constAirportCountryInfo ## <ConstAirportCountryInfo>所有机场国家固定信息

        airportCountryInfos = constAirportCountryInfo["airportCountryInfos"] ## <Serializable><AirportCountryInfo[]>机场国家固定信息
        airportCountryInfoN = (e for i, e in enumerate(airportCountryInfos) if e[key] == code)
        findAirportCountryInfo = next(airportCountryInfoN, None)
        return findAirportCountryInfo


class SunwingAdressSpider(scrapy.Spider):
    name = 'sunwingAdressSpider'
    allowed_domains = ['sunwinggroup.ca']
    start_urls = ['https://services.sunwinggroup.ca/beta/api/search/getGatewayforBrand/en/SWG/RE']
    
    
    oneway_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/OW'
    roundtrip_url = 'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{}/RE'
    
    def __init__(self, fromDate=None, returnDate=None, *args, **kwargs):
        super(SunwingAdressSpider, self).__init__(*args, **kwargs)
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


    def parse(self, response):
        # print(".........", response.text)
        sunwingInfo = SunwingInfo() ## <SunwingInfo>所有信息
        sunwingInfo.init()

        oneways = sunwingInfo["oneways"] ## <Serializable><OnewayFlight[]>单程
        roundtrips = sunwingInfo["roundtrips"] ## <Serializable><RoundtripFlight[]>往返

        text = response.text
        flights = json.loads(text)
        for idx in range(len(flights)):
            flight = flights[idx]

            code = flight.get("code") ## <Serializable><string>三字码
            countryId = flight.get("countryId") ## <Serializable><string>国家id
            airportName = flight.get("name") ## <Serializable><string>机场名称
            destinations = flight.get("destinations") ## <Serializable><string>目的地

            airportInfo = AirportInfo() ## <AirportInfo>机场信息
            airportInfo.init()
            airportInfo["code"] = code ## <Serializable><string>三字码
            airportInfo["countryId"] = countryId ## <Serializable><string>国家id
            airportInfo["airportName"] = airportName ## <Serializable><string>机场名称
            airportInfo["countryName"] = "" ## <Serializable><string>国家名称

            onewayFlight = OnewayFlight() ## <OnewayFlight>单程
            onewayFlight.init()
            infoClone = airportInfo.cloneAll()
            onewayFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
            oneways.append(onewayFlight)


            roundtripFlight = RoundtripFlight() ## <RoundtripFlight>往返
            roundtripFlight.init()
            infoClone = airportInfo.cloneAll()
            roundtripFlight["origin"] = infoClone ## <Serializable><AirportInfo>起始地
            roundtrips.append(roundtripFlight)


        try:
            for onewayFlight in oneways:
                airportInfo = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
                code = airportInfo["code"] ## <Serializable><string>三字码
                url = self.oneway_url.format(code)
            
                yield scrapy.Request(url, callback=self.parse_oneway, meta = {'onewayFlight': onewayFlight}, dont_filter = True, cookies = self.cookies or {})

            for roundtripFlight in roundtrips:
                airportInfo = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
                code = airportInfo["code"] ## <Serializable><string>三字码
                url = self.roundtrip_url.format(code)
                yield scrapy.Request(url, callback=self.parse_roundtrip, meta = {'roundtripFlight': roundtripFlight}, dont_filter = True, cookies = self.cookies or {})
            yield sunwingInfo
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


        ##########################################################
    def parse_oneway(self, response):
        try:
            # text = "[{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Coco, Cuba (CCC)\",\"destinationCode\":\"CCC\"},{\"gateWay\":\"YFC\",\"countryName\":\"Cuba\",\"destinationName\":\"Cayo Santa Maria, Cuba (SNU)\",\"destinationCode\":\"SNU\"},{\"gateWay\":\"YFC\",\"countryName\":\"Dominican Republic\",\"destinationName\":\"Punta Cana, Dominican Republic (PUJ)\",\"destinationCode\":\"PUJ\"},{\"gateWay\":\"YFC\",\"countryName\":\"Mexico\",\"destinationName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"destinationCode\":\"CUN\"}]"
            text = response.text

            onewayFlight = response.meta.get('onewayFlight')
            destinations = onewayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

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

            origin = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
            
            destinations = onewayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地
            airportInfos = [origin] + destinations
            for airportInfo in airportInfos:
                # print('handleExtraAirportInfoInfo')
                code = airportInfo["code"] ## <Serializable><string>三字码
                ##########################################################
                constAirportCountryInfosCache = self.constAirportCountryInfosCache
                airportCountryInfo = constAirportCountryInfosCache.getAirportCountryInfoByKeyValue("code", code)

                if not airportCountryInfo:
                    url = "https://jichang.gjcha.com/jichang/"+code+".html"
                    yield scrapy.Request(url, callback=self.parseExtra, meta = {'airportInfo': airportInfo}, dont_filter = True, cookies = self.cookies or {})

                airportInfo["countryCode"] = airportCountryInfo["countryCode"] ## <Serializable><string>国家Code
                airportInfo["countryChineaseName"] = airportCountryInfo["countryChineaseName"] ## <Serializable><string>国家中文名称


        except Exception as e:
            raise
    
    def parse_roundtrip(self, response):
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

        origin = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
        destinations = roundtripFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

        airportInfos = [origin] + destinations
        for airportInfo in airportInfos:
            # print('handleExtraAirportInfoInfo')
            code = airportInfo["code"] ## <Serializable><string>三字码
            ##########################################################
            constAirportCountryInfosCache = self.constAirportCountryInfosCache
            airportCountryInfo = constAirportCountryInfosCache.getAirportCountryInfoByKeyValue("code", code)

            if not airportCountryInfo:
                url = "https://jichang.gjcha.com/jichang/"+code+".html"
                yield scrapy.Request(url, callback=self.parseExtra, meta = {'airportInfo': airportInfo}, dont_filter = True, cookies = self.cookies or {})

            airportInfo["countryCode"] = airportCountryInfo["countryCode"] ## <Serializable><string>国家Code
            airportInfo["countryChineaseName"] = airportCountryInfo["countryChineaseName"] ## <Serializable><string>国家中文名称
