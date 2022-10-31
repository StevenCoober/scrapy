import os, sys, glob, random, traceback, json
import xlwt
import xlrd
import scrapy
from functools import cmp_to_key
from properties.items import *
def cookieString2CookieDict(cookie: str = "") -> dict:
    """
    将字符串形式的cookie转成RequestsCookieJar
    :param cookie: 待转换的cookie字符串
    :return: RequestsCookieJar 对象
    """
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

# cookieString2CookieDict("jsData\=%7B%22ttst%22%3A67.59999999403954%2C%22ifov%22%3Afalse%2C%22log2%22%3Afalse%2C%22wdif%22%3Afalse%2C%22wdifrm%22%3Afalse%2C%22log1%22%3Afalse%2C%22br_h%22%3A697%2C%22br_w%22%3A1706%2C%22br_oh%22%3A984%2C%22br_ow%22%3A1280%2C%22nddc%22%3A1%2C%22rs_h%22%3A1024%2C%22rs_w%22%3A1280%2C%22rs_cd%22%3A24%2C%22phe%22%3Afalse%2C%22nm%22%3Afalse%2C%22jsf%22%3Afalse%2C%22ua%22%3A%22Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F106.0.0.0%20Safari%2F537.36%22%2C%22lg%22%3A%22zh-CN%22%2C%22pr%22%3A0.75%2C%22hc%22%3A8%2C%22ars_h%22%3A984%2C%22ars_w%22%3A1280%2C%22tz%22%3A-480%2C%22str_ss%22%3Atrue%2C%22str_ls%22%3Atrue%2C%22str_idb%22%3Atrue%2C%22str_odb%22%3Atrue%2C%22plgod%22%3Afalse%2C%22plg%22%3A5%2C%22plgne%22%3Atrue%2C%22plgre%22%3Atrue%2C%22plgof%22%3Afalse%2C%22plggt%22%3Afalse%2C%22pltod%22%3Afalse%2C%22hcovdr%22%3Afalse%2C%22hcovdr2%22%3Afalse%2C%22plovdr%22%3Afalse%2C%22plovdr2%22%3Afalse%2C%22ftsovdr%22%3Afalse%2C%22ftsovdr2%22%3Afalse%2C%22lb%22%3Afalse%2C%22eva%22%3A33%2C%22lo%22%3Afalse%2C%22ts_mtp%22%3A0%2C%22ts_tec%22%3Afalse%2C%22ts_tsa%22%3Afalse%2C%22vnd%22%3A%22Google%20Inc.%22%2C%22bid%22%3A%22NA%22%2C%22mmt%22%3A%22application%2Fpdf%2Ctext%2Fpdf%22%2C%22plu%22%3A%22PDF%20Viewer%2CChrome%20PDF%20Viewer%2CChromium%20PDF%20Viewer%2CMicrosoft%20Edge%20PDF%20Viewer%2CWebKit%20built-in%20PDF%22%2C%22hdn%22%3Afalse%2C%22awe%22%3Afalse%2C%22geb%22%3Afalse%2C%22dat%22%3Afalse%2C%22med%22%3A%22defined%22%2C%22aco%22%3A%22probably%22%2C%22acots%22%3Afalse%2C%22acmp%22%3A%22probably%22%2C%22acmpts%22%3Atrue%2C%22acw%22%3A%22probably%22%2C%22acwts%22%3Afalse%2C%22acma%22%3A%22maybe%22%2C%22acmats%22%3Afalse%2C%22acaa%22%3A%22probably%22%2C%22acaats%22%3Atrue%2C%22ac3%22%3A%22%22%2C%22ac3ts%22%3Afalse%2C%22acf%22%3A%22probably%22%2C%22acfts%22%3Afalse%2C%22acmp4%22%3A%22maybe%22%2C%22acmp4ts%22%3Afalse%2C%22acmp3%22%3A%22probably%22%2C%22acmp3ts%22%3Afalse%2C%22acwm%22%3A%22maybe%22%2C%22acwmts%22%3Afalse%2C%22ocpt%22%3Afalse%2C%22vco%22%3A%22probably%22%2C%22vcots%22%3Afalse%2C%22vch%22%3A%22probably%22%2C%22vchts%22%3Atrue%2C%22vcw%22%3A%22probably%22%2C%22vcwts%22%3Atrue%2C%22vc3%22%3A%22maybe%22%2C%22vc3ts%22%3Afalse%2C%22vcmp%22%3A%22%22%2C%22vcmpts%22%3Afalse%2C%22vcq%22%3A%22%22%2C%22vcqts%22%3Afalse%2C%22vc1%22%3A%22probably%22%2C%22vc1ts%22%3Atrue%2C%22dvm%22%3A8%2C%22sqt%22%3Afalse%2C%22so%22%3A%22landscape-primary%22%2C%22wbd%22%3Afalse%2C%22wdw%22%3Atrue%2C%22cokys%22%3A%22bG9hZFRpbWVzY3NpYXBwL%3D%22%2C%22ecpc%22%3Afalse%2C%22lgs%22%3Atrue%2C%22lgsod%22%3Afalse%2C%22psn%22%3Atrue%2C%22edp%22%3Atrue%2C%22addt%22%3Atrue%2C%22wsdc%22%3Atrue%2C%22ccsr%22%3Atrue%2C%22nuad%22%3Atrue%2C%22bcda%22%3Afalse%2C%22idn%22%3Atrue%2C%22capi%22%3Afalse%2C%22svde%22%3Afalse%2C%22vpbq%22%3Atrue%2C%22ucdv%22%3Afalse%2C%22spwn%22%3Afalse%2C%22emt%22%3Afalse%2C%22bfr%22%3Afalse%2C%22dbov%22%3Afalse%2C%22npmtm%22%3Afalse%2C%22glvd%22%3A%22Google%20Inc.%20(NVIDIA)%22%2C%22glrd%22%3A%22ANGLE%20(NVIDIA%2C%20NVIDIA%20GeForce%20GTX%20960%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)%22%2C%22tagpu%22%3A42%2C%22prm%22%3Atrue%2C%22tzp%22%3A%22Asia%2FShanghai%22%2C%22cvs%22%3Atrue%2C%22usb%22%3A%22defined%22%2C%22jset%22%3A1667143019%7D&events\=%5B%5D&eventCounters\=%5B%5D&jsType\=ch&cid\=.A_9iJl9CW~2XKtn7m7FhiHg~e1NJ2zRUakgcAeOS2Stro24VOo7xkDM~GhXgIrtGQtXXyiCHdm.gkGUNbGc6RjHhLO~UtY8rfifdru6i1b.Dy6fOz1e-hN13MP_R3UU&ddk\=E812CB49265F3F5AD3331EACED3A5C&Referer\=https%253A%252F%252Fbook.sunwing.ca%252Fcgi-bin%252Fresults.cgi%253Fengines%253DS%2526flex%253DY%2526isMobile%253Dfalse%2526searchtype%253DOW%2526language%253Den%2526code_ag%253Drds%2526alias%253Dbtd%2526date_dep%253D20221031%2526gateway_dep%253DYYZ%2526dest_dep%253DMLB%2526nb_adult%253D1%2526nb_child%253D0&request\=%252Fcgi-bin%252Fresults.cgi%253Fengines%253DS%2526flex%253DY%2526isMobile%253Dfalse%2526searchtype%253DOW%2526language%253Den%2526code_ag%253Drds%2526alias%253Dbtd%2526date_dep%253D20221031%2526gateway_dep%253DYYZ%2526dest_dep%253DMLB%2526nb_adult%253D1%2526nb_child%253D0&responsePage\=origin&ddv\=4.5.0")

def saveTickets(chooses, savePath):
    f = xlwt.Workbook()  # 创建工作薄

    flightChooseDates = chooses["flightChooseDates"] ## <Serializable><FlightChooseDate[]>所有选择飞行时间
    columnCount = 0
    def columnBegin():
        nonlocal columnCount
        columnCount = 0
    def writeColumn(sheet, row, data):
        nonlocal columnCount
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = 'Times new Roman'
        font.bold = True
        font.colour_index = 0
        font.height = 220
        style.font = font
        # print("columnCount", columnCount, data)
        sheet.write(row, columnCount, data, style)
        columnCount = columnCount + 1

    sheet1 = f.add_sheet(u'种子资源', cell_overwrite_ok=True)
    if len(flightChooseDates) == 0: return
    flightChooseDate = flightChooseDates[0]

    def comps(a, b):
        numa = 0
        numb = 0
        numa = ((numa + 1) << 1) if int(a["selectFromDate"]) > int(b["selectFromDate"]) else numa
        numb = ((numb + 1) << 1) if int(a["selectFromDate"]) < int(b["selectFromDate"]) else numb

        # print("...", a["selectReturnDate"], b["selectReturnDate"])
        # numa = ((numa + 1) << 1) if int(a["selectReturnDate"]) > int(b["selectReturnDate"]) else numa
        # numb = ((numb + 1) << 1) if int(a["selectReturnDate"]) < int(b["selectReturnDate"]) else numb
        return numa - numb

    flightChooseDates = sorted(flightChooseDates, key=cmp_to_key(comps))

    def formatFee(fees, vnames):
        t = ["费用(%s):%s"%(fee["feeName"], fee["feePrice"]) for i, fee in enumerate(fees)]
        return "\n".join(t)
    Fee.formatcb = formatFee

    def formatFlight(flights, vnames):
        t = ""
        for flight in flights:
            flightName = flight["flightName"] ## <Serializable><string>航班名字
            planeName = flight["planeName"] ## <Serializable><string>飞机名字
            originCityName = flight["originCityName"] ## <string>出发城市
            destinationCityName = flight["destinationCityName"] ## <string>到达城市
            # allTickets = flight["allTickets"] ## <Ticket[]>所有可选的票
            chooseTicket = flight["chooseTicket"] ## <Serializable><Ticket>选择票据
            Itinerary = flight["Itinerary"] ## <string>旅行日程
            time_dep = flight["time_dep"] ## <Serializable><string>出发时间
            time_arr = flight["time_arr"] ## <Serializable><string>到达时间
            duration = flight["duration"] ## <Serializable><string>时间跨度
            Fromdate = flight["Fromdate"] ## <Serializable><string>
            Todate = flight["Todate"] ## <Serializable><string>
            Nb_seats_for_ajax0 = flight["Nb_seats_for_ajax0"] ## <Serializable><string>
            t = t + "Flight:%s\n"%flightName
            t = t + "From:%s\n"%originCityName
            t = t + "To:%s\n"%destinationCityName
            t = t + "选择票价:%s\n"%(chooseTicket["price"])
            t = t + "%s\n"%Fromdate
            t = t + "%s\n"%Todate
            t = t + "Duration:%s\n"%duration
            t = t + "%s\n"%Nb_seats_for_ajax0
        return t
    Flight.formatcb = formatFlight

    datasMap = flightChooseDate.serializeFormat()

    substitude = {
        "_flightType": "乘坐类型(0单程1往返)",
        # "_selectFromDate": ,
        # "_selectReturnDate": ,

        # "_Air_Transportation_Charges": "Air Transportation Charges",
        # "_Surcharges": "Surcharges",
        # "_Taxes_Fees_And_Charges": "Taxes Fees And Charges",
        # "_Td_Pricetotal": "Td Pricetotal",

        "_origin_code": "出发城市",
        # "_origin_countryId": ,
        # "_origin_airportName": "出发城市",
        # "_origin_countryName": "出发城市",
        "_origin_countryCode": "出发国家",
        "_origin_countryChineaseName": "出发国家(中文)",
        "_destination_code": "到达城市",
        # "_destination_countryId": ,
        # "_destination_airportName": ,
        # "_destination_countryName": "到达城市",
        "_destination_countryCode": "到达国家",
        "_destination_countryChineaseName": "到达国家(中文)",
        "chooseDepartingFlight": "出发航班",
        "chooseReturningFlight": "抵达航班",
        "Details Price": "价格明细",
        "Upgrade_Your_Experience": "Upgrade Your Experience",
        "Protect_Your_Vacation": "Protect Your Vacation",
        "Airport_Lounge": "Airport Lounge",
        "Excursions": "Excursions",
    }


    for data in list(substitude.values()):
        writeColumn(sheet1, 0, data)
        
    for i in range(0, len(flightChooseDates)):
        flightChooseDate = flightChooseDates[i]
        columnBegin()
        datasMap = flightChooseDate.serializeFormat()

        newDatasMap = {}
        for k, v in substitude.items():
            if k in datasMap:
                newDatasMap[substitude[k]] = datasMap[k]
            if k == "Details Price":
                newDatasMap["Details Price"] = "%s\n%s\n%s\n%s\n"%(datasMap["_Air_Transportation_Charges"],
                datasMap["_Surcharges"],
                datasMap["_Taxes_Fees_And_Charges"],
                datasMap["_Td_Pricetotal"])


        for k, v in newDatasMap.items():
            writeColumn(sheet1, i+1, v)

    f.save(savePath)