# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from properties.items import *
import xlwt
import xlrd
import logging
from utils.utils import saveTickets 
class SunwingJsonPipeline:
    sunwingInfo = None
    json_path = os.getcwd() + "/datas/Sunwing.json"
    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.sunwingInfo = None

    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        if self.sunwingInfo:
            jsonStr = self.sunwingInfo.jsonDumps()
            with open(self.json_path, "w", encoding='utf-8') as fp:
                fp.write(jsonStr)

    def process_item(self, item, spider):
        if not isinstance(item, SunwingInfo):
            return item
        self.sunwingInfo = item
        print("SunwingJsonPipeline process_item")
        # jsonStr = self.sunwingInfo.jsonDumps()
        # print("jsonStr", jsonStr)
        return item
class TicketJsonPipeline:
    chooses = None
    json_path = os.getcwd() + "/datas/Ticket.json"
    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        chooses = Chooses() ## <Chooses>
        chooses.init() ## <Chooses>
        self.chooses = chooses


    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        if self.chooses:
            print('TicketJsonPipeline 共有%d个数据'%(len(self.chooses)))
            jsonStr = self.chooses.jsonDumps()
            with open(self.json_path, "w", encoding='utf-8') as fp:
                fp.write(jsonStr)
    def process_item(self, item, spider):
        if not isinstance(item, FlightChooseDate):
            return item
        chooses = self.chooses ## <Chooses>
        flightChooseDates = chooses["flightChooseDates"] ## <Serializable><FlightChooseDate>所有选择飞行时间
        flightChooseDates.append(item)
        print("TicketJsonPipeline process_item")
        return item

class TicketExcelPipeline:
    chooses = None
    def open_spider(self, spider):
        print('TicketExcelPipeline开始爬虫，链接数据库')
        chooses = Chooses() ## <Chooses>
        chooses.init() ## <Chooses>
        self.chooses = chooses

    def close_spider(self, spider):
        print('TicketExcelPipeline 爬虫结束, 关闭通道')
        if self.chooses:
            saveTickets(self.chooses, os.getcwd() + "/datas/Tickets.xls")

    def process_item(self, item, spider):
        print('TicketExcelPipeline 爬虫结束, 关闭通道')
        if not isinstance(item, FlightChooseDate):
            return item
        chooses = self.chooses ## <Chooses>
        flightChooseDates = chooses["flightChooseDates"] ## <Serializable><FlightChooseDate>所有选择飞行时间
        flightChooseDates.append(item)
        print("TicketExcelPipeline process_item")
        return item

# # -*- coding: utf-8 -*-
# import xlwt
# import xlrd


# class ExcelPrintPipeline(object):
#     def __init__(self):
#         self.f = xlwt.Workbook()  # 创建工作薄
#         self.sheet1 = self.f.add_sheet(u'种子资源', cell_overwrite_ok=True)
#         self.rowsTitle = [u'标题', u'影片名称', u'导演', u'影片演员', u'语言', u'影片类型', u'影片地区', u'更新时间', u'影片状态', u'上映日期', u'剧情介绍', u'影片地址']  # 创建标题
#         for i in range(0, len(self.rowsTitle)):
#             # 最后一个参数设置样式
#             self.sheet1.write(0, i, self.rowsTitle[i], self.set_style('Times new Roman', 220, True))
#         # Excel保存位置
#         self.f.save('C:/torrent_movie.xls')

#     def open_spider(self, spider):
#         print("开始输出xlsx文件")

#     def process_item(self, item, spider):
#         data = xlrd.open_workbook('C:/torrent_movie.xls')  # 打开Excel文件
#         table = data.sheets()[0]  # 通过索引顺序获取table，因为初始化时只创建了一个table，因此索引值为0
#         rowCount = table.nrows  # 获取行数   ，下次从这一行开始
#         data = []
#         # 拼装成一个列表
#         # data.append(rowCount + m)  # 为每条添加序号
#         data.append(item['torrent_title'])
#         data.append(item["torrent_name"])
#         data.append(item["torrent_director"])
#         data.append(item["torrent_actor"])
#         data.append(item['torrent_language'])
#         data.append(item["torrent_type"])
#         data.append(item["torrent_region"])
#         data.append(item["torrent_update_time"])
#         data.append(item['torrent_status'])
#         data.append(item["torrent_show_time"])
#         data.append(item["torrent_introduction"])
#         data.append(item["torrent_url"])

#         for i in range(len(data)):
#             self.sheet1.write(rowCount, i, data[i])  # 写入数据到execl中
#         self.f.save('C:/torrent_movie.xls')
#         return item

#     def close_spider(self, spider):
#         self.f.save('C:/torrent_movie.xls')
#         print("结束输出xlsx文件")

#     #该函数设置字体样式
#     def set_style(self,name, height, bold=False):
#         style = xlwt.XFStyle()  # 初始化样式
#         font = xlwt.Font()  # 为样式创建字体
#         font.name = name
#         font.bold = bold
#         font.colour_index = 2
#         font.height = height
#         style.font = font
#         return style
class SunwingExcelPipeline:
    sunwingInfo = None
    file_path = "Sunwing.xls"
    #该函数设置字体样式
    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.colour_index = 0
        font.height = height
        style.font = font
        return style

    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.sunwingInfo = None

    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        # print('self.sunwingInfo', self.sunwingInfo)
        f = xlwt.Workbook()  # 创建工作薄
        sheet1 = f.add_sheet(u'种子资源', cell_overwrite_ok=True)
        # "from_code": from_code, ## <Serializable><string>三字码
        # "from_countryId": from_countryId, ## <Serializable><string>国家id
        # "from_airportName": from_airportName, ## <Serializable><string>机场名称
        # "from_countryName": from_countryName, ## <Serializable><string>国家名称
        # "from_countryCode": from_countryCode, ## <Serializable><string>国家Code
        # "from_countryChineaseName": from_countryChineaseName, ## <Serializable><string>国家中文名称
        # "dest_code": dest_code, ## <Serializable><string>三字码
        # "dest_countryId": dest_countryId, ## <Serializable><string>国家id
        # "dest_airportName": dest_airportName, ## <Serializable><string>机场名称
        # "dest_countryName": dest_countryName, ## <Serializable><string>国家名称
        # "dest_countryCode": dest_countryCode, ## <Serializable><string>国家Code
        # "dest_countryChineaseName": dest_countryChineaseName, ## <Serializable><string>国家中文名称
        rowsTitle = {
            '类型': ["单程", "返程"], 
            '出发城市': "from_code", 
            '到达城市': "dest_code", 
            '出发国家': "from_countryCode",
            '出发国家(中文)': "from_countryChineaseName", 
            '到达国家': "dest_countryCode", 
            # '到达国家(中文)': "dest_countryChineaseName", 
            '国内/国际': ["DOM", "INT"],
        }  # 创建标题
        rowNum = 0
        keys = list(rowsTitle.keys())
        values = list(rowsTitle.values())
        for i in range(0, len(values)):
            # 最后一个参数设置样式
            sheet1.write(0, i, keys[i], self.set_style('Times new Roman', 220, True))

        rowNum = rowNum + 1

        sunwingInfo = self.sunwingInfo
        if not sunwingInfo:
            logging.debug('SunwingExcelPipeline 没有数据')
            return
        # print("sunwingInfo", sunwingInfo.jsonDumps())

        oneways = sunwingInfo["oneways"] ## <Serializable><OnewayFlight[]>单程
        roundtrips = sunwingInfo["roundtrips"] ## <Serializable><RoundtripFlight[]>往返
        for onewayFlight in oneways:
            origin = onewayFlight["origin"] ## <Serializable><AirportInfo>起始地
            destinations = onewayFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

            from_code = origin["code"] ## <Serializable><string>三字码
            from_countryId = origin["countryId"] ## <Serializable><string>国家id
            from_airportName = origin["airportName"] ## <Serializable><string>机场名称
            from_countryName = origin["countryName"] ## <Serializable><string>国家名称
            from_countryCode = origin["countryCode"] ## <Serializable><string>国家Code
            from_countryChineaseName = origin["countryChineaseName"] ## <Serializable><string>国家中文名称

            for destination in destinations:

                dest_code = destination["code"] ## <Serializable><string>三字码
                dest_countryId = destination["countryId"] ## <Serializable><string>国家id
                dest_airportName = destination["airportName"] ## <Serializable><string>机场名称
                dest_countryName = destination["countryName"] ## <Serializable><string>国家名称
                dest_countryCode = destination["countryCode"] ## <Serializable><string>国家Code
                dest_countryChineaseName = destination["countryChineaseName"] ## <Serializable><string>国家中文名称

                sheet1.write(rowNum, 0, values[0][0], self.set_style('Times new Roman', 220, False))
                ID = 0 if from_countryCode == dest_countryCode else 1
                sheet1.write(rowNum, len(keys) - 1, values[len(keys) - 1][ID], self.set_style('Times new Roman', 220, False))

                columns = {
                    "from_code": from_code, ## <Serializable><string>三字码
                    "from_countryId": from_countryId, ## <Serializable><string>国家id
                    "from_airportName": from_airportName, ## <Serializable><string>机场名称
                    "from_countryName": from_countryName, ## <Serializable><string>国家名称
                    "from_countryCode": from_countryCode, ## <Serializable><string>国家Code
                    "from_countryChineaseName": from_countryChineaseName, ## <Serializable><string>国家中文名称
                    "dest_code": dest_code, ## <Serializable><string>三字码
                    "dest_countryId": dest_countryId, ## <Serializable><string>国家id
                    "dest_airportName": dest_airportName, ## <Serializable><string>机场名称
                    "dest_countryName": dest_countryName, ## <Serializable><string>国家名称
                    "dest_countryCode": dest_countryCode, ## <Serializable><string>国家Code
                    "dest_countryChineaseName": dest_countryChineaseName, ## <Serializable><string>国家中文名称
                }
                for i in range(1, len(keys) - 1):
                   sheet1.write(rowNum, i, columns[values[i]], self.set_style('Times new Roman', 220, False))
                rowNum = rowNum + 1

        for roundtripFlight in roundtrips:
            origin = roundtripFlight["origin"] ## <Serializable><AirportInfo>起始地
            destinations = roundtripFlight["destinations"] ## <Serializable><AirportInfo[]>目的地

            from_code = origin["code"] ## <Serializable><string>三字码
            from_countryId = origin["countryId"] ## <Serializable><string>国家id
            from_airportName = origin["airportName"] ## <Serializable><string>机场名称
            from_countryName = origin["countryName"] ## <Serializable><string>国家名称
            from_countryCode = origin["countryCode"] ## <Serializable><string>国家中文名称
            from_countryChineaseName = origin["countryChineaseName"] ## <Serializable><string>国家中文名称

            for destination in destinations:

                dest_code = destination["code"] ## <Serializable><string>三字码
                dest_countryId = destination["countryId"] ## <Serializable><string>国家id
                dest_airportName = destination["airportName"] ## <Serializable><string>机场名称
                dest_countryName = destination["countryName"] ## <Serializable><string>国家名称
                dest_countryCode = destination["countryCode"] ## <Serializable><string>国家中文名称
                dest_countryChineaseName = destination["countryChineaseName"] ## <Serializable><string>国家中文名称

                sheet1.write(rowNum, 0, values[0][1], self.set_style('Times new Roman', 220, False))
                ID = 0 if from_countryCode == dest_countryCode else 1
                sheet1.write(rowNum, len(keys) - 1, values[len(keys) - 1][ID], self.set_style('Times new Roman', 220, False))

                columns = {
                    "from_code": from_code, ## <Serializable><string>三字码
                    "from_countryId": from_countryId, ## <Serializable><string>国家id
                    "from_airportName": from_airportName, ## <Serializable><string>机场名称
                    "from_countryName": from_countryName, ## <Serializable><string>国家名称
                    "from_countryCode": from_countryCode, ## <Serializable><string>国家Code
                    "from_countryChineaseName": from_countryChineaseName, ## <Serializable><string>国家中文名称
                    "dest_code": dest_code, ## <Serializable><string>三字码
                    "dest_countryId": dest_countryId, ## <Serializable><string>国家id
                    "dest_airportName": dest_airportName, ## <Serializable><string>机场名称
                    "dest_countryName": dest_countryName, ## <Serializable><string>国家名称
                    "dest_countryCode": dest_countryCode, ## <Serializable><string>国家Code
                    "dest_countryChineaseName": dest_countryChineaseName, ## <Serializable><string>国家中文名称
                }
                for i in range(1, len(keys) - 1):
                   sheet1.write(rowNum, i, columns[values[i]], self.set_style('Times new Roman', 220, False))
                rowNum = rowNum + 1

        # Excel保存位置
        f.save(os.getcwd() + '/datas/cities.xls')


    def process_item(self, item, spider):
        print("SunwingExcelPipeline process_item")
        
        # if True:
        #     jsonStr = "{\"doubleFlights\":[{\"fromFlight\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\"},\"destFlights\":[]},{\"fromFlight\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"},{\"code\":\"CCC\",\"countryId\":\"\",\"airportName\":\"Cayo Coco, Cuba (CCC)\",\"countryName\":\"Cuba\"},{\"code\":\"SNU\",\"countryId\":\"\",\"airportName\":\"Cayo Santa Maria, Cuba (SNU)\",\"countryName\":\"Cuba\"},{\"code\":\"PUJ\",\"countryId\":\"\",\"airportName\":\"Punta Cana, Dominican Republic (PUJ)\",\"countryName\":\"Dominican Republic\"},{\"code\":\"CUN\",\"countryId\":\"\",\"airportName\":\"Cancun / Riviera Maya, Mexico (CUN)\",\"countryName\":\"Mexico\"}]}],\"oneFlights\":[{\"fromFlight\":{\"code\":\"YBG\",\"countryId\":1,\"airportName\":\"Bagotville\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YYC\",\"countryId\":1,\"airportName\":\"Calgary\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YDF\",\"countryId\":1,\"airportName\":\"Deer Lake\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YEG\",\"countryId\":1,\"airportName\":\"Edmonton\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YFC\",\"countryId\":1,\"airportName\":\"Fredericton\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQX\",\"countryId\":1,\"airportName\":\"Gander\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YHZ\",\"countryId\":1,\"airportName\":\"Halifax\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YHM\",\"countryId\":1,\"airportName\":\"Hamilton\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YLW\",\"countryId\":1,\"airportName\":\"Kelowna\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YKF\",\"countryId\":1,\"airportName\":\"Kitchener\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YXU\",\"countryId\":1,\"airportName\":\"London\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQM\",\"countryId\":1,\"airportName\":\"Moncton\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YUL\",\"countryId\":1,\"airportName\":\"Montreal\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YYB\",\"countryId\":1,\"airportName\":\"North Bay\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YOW\",\"countryId\":1,\"airportName\":\"Ottawa\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQB\",\"countryId\":1,\"airportName\":\"Québec\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQR\",\"countryId\":1,\"airportName\":\"Regina\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YXE\",\"countryId\":1,\"airportName\":\"Saskatoon\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YAM\",\"countryId\":2,\"airportName\":\"Sault Ste. Marie\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YYT\",\"countryId\":1,\"airportName\":\"St. John's\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YSB\",\"countryId\":1,\"airportName\":\"Sudbury\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQT\",\"countryId\":1,\"airportName\":\"Thunder Bay\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YYZ\",\"countryId\":1,\"airportName\":\"Toronto\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YVR\",\"countryId\":1,\"airportName\":\"Vancouver\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YQG\",\"countryId\":1,\"airportName\":\"Windsor\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]},{\"fromFlight\":{\"code\":\"YWG\",\"countryId\":1,\"airportName\":\"Winnipeg\",\"countryName\":\"\"},\"destFlights\":[{\"code\":\"MLB\",\"countryId\":\"\",\"airportName\":\"Melbourne, USA (MLB)\",\"countryName\":\"USA\"}]}]}"
        #     sunwingInfo = SunwingInfo() ## <SunwingInfo>所有信息
        #     sunwingInfo.init() ## <SunwingInfo>所有信息
        #     sunwingInfo.jsonLoads(jsonStr)
        if isinstance(item, SunwingInfo):
            self.sunwingInfo = item
        # jsonStr = sunwingInfo.jsonDumps()
        # print("jsonStr", jsonStr)
        return item 


