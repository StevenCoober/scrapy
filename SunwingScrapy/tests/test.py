import os, sys, glob, random, traceback, json
import xlwt
import xlrd
import scrapy
from functools import cmp_to_key
sys.path.append(os.path.abspath("D:/Projects/demo/SunwingScrapy/properties"))
from items import *

json_path = os.getcwd() + r"/../datas/Ticket.json"
chooses = None
if os.path.isfile(json_path):
    with open(json_path, "r", encoding='utf-8') as fp:
        data=fp.read()
        chooses = Chooses() ## <HouseScrapy>所有信息
        chooses.init() ## <Chooses>
        chooses.jsonLoads(data)


# a = {
#     "a"+"b":1
# }
# print([1] + [2])
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
        print("columnCount", columnCount, data)
        sheet.write(row, columnCount, data, style)
        columnCount = columnCount + 1

    sheet1 = f.add_sheet(u'种子资源', cell_overwrite_ok=True)
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

    def formatFee(flightChooseDates, vnames):
        t = ["费用(%s):%s"%(fee["feeName"], fee["feePrice"]) for i, fee in enumerate(fees)]
        return "\n".join(t)

    FlightChooseDate.formatcb
    def formatcb(flights, vnames):
        str = ""
        for flight in flights:
            flightName = flight["flightName"] ## <Serializable><string>航班名字
            planeName = flight["planeName"] ## <Serializable><string>飞机名字
            # allTickets = flight["allTickets"] ## <Ticket[]>所有可选的票
            chooseTicket = flight["chooseTicket"] ## <Serializable><Ticket>选择票据
            Itinerary = flight["Itinerary"] ## <string>旅行日程
            time_dep = flight["time_dep"] ## <Serializable><string>出发时间
            time_arr = flight["time_arr"] ## <Serializable><string>到达时间
            duration = flight["duration"] ## <Serializable><string>时间跨度
            Fromdate = flight["Fromdate"] ## <Serializable><string>
            Todate = flight["Todate"] ## <Serializable><string>
            Nb_seats_for_ajax0 = flight["Nb_seats_for_ajax0"] ## <Serializable><string>
            str = str + "flightName:%s\n"%flightName
            str = str + "%s\n"%Fromdate
            str = str + "%s\n"%Todate
            str = str + "%s\n"%Nb_seats_for_ajax0
            str = str + "选择票价:%s\n"%(chooseTicket["price"])
        return str
    Flight.formatcb = formatcb
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

saveTickets(chooses, os.getcwd() + '/../datas/Tickets.xls')