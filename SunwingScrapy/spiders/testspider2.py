import scrapy
import os, sys, json, time
from properties.items import *
from middlewares import CookiesMiddleware 
from utils.utils import cookieString2CookieDict 

class TestspiderSpider(scrapy.Spider):
    name = 'test2'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        # 获取网站标题
        context = response.xpath('/html/head/title/text()')
        # 提取网站标题
        title = context.extract_first()
        print(title)
        url = self.start_urls[0]

        ###################################

        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

        datas = {
            "jsData":"{\"ttst\":53.399999998509884,\"ifov\":false,\"log2\":false,\"wdif\":false,\"wdifrm\":false,\"log1\":false,\"br_h\":1110,\"br_w\":1557,\"br_oh\":984,\"br_ow\":1280,\"nddc\":1,\"rs_h\":1024,\"rs_w\":1280,\"rs_cd\":24,\"phe\":false,\"nm\":false,\"jsf\":false,\"ua\":\"Mozilla/10.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\",\"lg\":\"zh-CN\",\"pr\":0.800000011920929,\"hc\":8,\"ars_h\":984,\"ars_w\":1280,\"tz\":-480,\"str_ss\":true,\"str_ls\":true,\"str_idb\":true,\"str_odb\":true,\"plgod\":false,\"plg\":5,\"plgne\":true,\"plgre\":true,\"plgof\":false,\"plggt\":false,\"pltod\":false,\"hcovdr\":false,\"hcovdr2\":false,\"plovdr\":false,\"plovdr2\":false,\"ftsovdr\":false,\"ftsovdr2\":false,\"lb\":false,\"eva\":33,\"lo\":false,\"ts_mtp\":0,\"ts_tec\":false,\"ts_tsa\":false,\"vnd\":\"Google Inc.\",\"bid\":\"NA\",\"mmt\":\"application/pdf,text/pdf\",\"plu\":\"PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF\",\"hdn\":true,\"awe\":false,\"geb\":false,\"dat\":false,\"med\":\"defined\",\"aco\":\"probably\",\"acots\":false,\"acmp\":\"probably\",\"acmpts\":true,\"acw\":\"probably\",\"acwts\":false,\"acma\":\"maybe\",\"acmats\":false,\"acaa\":\"probably\",\"acaats\":true,\"ac3\":\"\",\"ac3ts\":false,\"acf\":\"probably\",\"acfts\":false,\"acmp4\":\"maybe\",\"acmp4ts\":false,\"acmp3\":\"probably\",\"acmp3ts\":false,\"acwm\":\"maybe\",\"acwmts\":false,\"ocpt\":false,\"vco\":\"probably\",\"vcots\":false,\"vch\":\"probably\",\"vchts\":true,\"vcw\":\"probably\",\"vcwts\":true,\"vc3\":\"maybe\",\"vc3ts\":false,\"vcmp\":\"\",\"vcmpts\":false,\"vcq\":\"\",\"vcqts\":false,\"vc1\":\"probably\",\"vc1ts\":true,\"dvm\":8,\"sqt\":false,\"so\":\"landscape-primary\",\"wbd\":false,\"wdw\":true,\"cokys\":\"bG9hZFRpbWVzY3NpYXBwcnVudGltZQ==L=\",\"ecpc\":false,\"lgs\":true,\"lgsod\":false,\"psn\":true,\"edp\":true,\"addt\":true,\"wsdc\":true,\"ccsr\":true,\"nuad\":true,\"bcda\":false,\"idn\":true,\"capi\":false,\"svde\":false,\"vpbq\":true,\"ucdv\":false,\"spwn\":false,\"emt\":false,\"bfr\":false,\"dbov\":false,\"npmtm\":false,\"glvd\":\"Google Inc. (NVIDIA)\",\"glrd\":\"ANGLE (NVIDIA, NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0, D3D11)\",\"tagpu\":11.600000001490116,\"prm\":true,\"tzp\":\"Asia/Shanghai\",\"cvs\":true,\"usb\":\"defined\",\"jset\":1666945129,\"cfpfe\":\"ZnVuY3Rpb24oYSl7dmFyIGI9UWEuX2dhVXNlclByZWZzO2lmKGImJmIuaW9vJiZiLmlvbygpfHxhJiYhMD09PVFhWyJnYS1kaXNhYmxlLSIrYV0pcmV0dXJuITA7dHJ5e3ZhciBjPVFhLmV4dGVybmFsO2lmKGMmJmMuX2dhVXNlclByZWZzJiYib28iPT1jLl9nYVVz\",\"stcfp\":\"bmFseXRpY3MuanM6NjI6NTgpCiAgICBhdCBaLnYgKGh0dHBzOi8vd3d3Lmdvb2dsZS1hbmFseXRpY3MuY29tL2FuYWx5dGljcy5qczo5OTozNjEpCiAgICBhdCBaLkQgKGh0dHBzOi8vd3d3Lmdvb2dsZS1hbmFseXRpY3MuY29tL2FuYWx5dGljcy5qczo5ODoxNzgp\",\"dcok\":\".sunwing.ca\",\"tbce\":0}",
            "events":"[{\"source\":{\"x\":307,\"y\":1107},\"message\":\"mouse move\",\"date\":1666945119004,\"id\":0},{\"source\":{\"x\":393,\"y\":818},\"message\":\"mouse move\",\"date\":1666945119114,\"id\":0},{\"source\":{\"x\":333,\"y\":743},\"message\":\"mouse move\",\"date\":1666945119387,\"id\":0},{\"source\":{\"x\":343,\"y\":767},\"message\":\"mouse move\",\"date\":1666945119497,\"id\":0},{\"source\":{\"x\":403,\"y\":727},\"message\":\"mouse move\",\"date\":1666945120774,\"id\":0}]",
            "eventCounters":"{\"mouse move\":13,\"mouse click\":0,\"scroll\":0,\"touch start\":0,\"touch end\":0,\"touch move\":0,\"key down\":0,\"key up\":0}",
            "jsType":"le",
            "cid":".DyGGoAIacy-NEd1E5v0LjbiVu6wFqavL2V3jwzUZZ8dexw8kjcFw6~2rHUIX61p-cXOspR0Nl_TJiLMDtBo7LmXUVwbPf6BV8F7xu0XImLLncA4VbsXfbREpu317VDp",
            "ddk":"E812CB49265F3F5AD3331EACED3A5C",
            "Referer":"https%3A%2F%2Fbook.sunwing.ca%2Fcgi-bin%2Fresults.cgi%3Fengines%3DS%26flex%3DY%26isMobile%3Dfalse%26searchtype%3DOW%26language%3Den%26code_ag%3Drds%26alias%3Dbtd%26date_dep%3D20221029%26gateway_dep%3DYYZ%26dest_dep%3DMLB%26nb_adult%3D1%26nb_child%3D0",
            "request":"%2Fcgi-bin%2Fresults.cgi%3Fengines%3DS%26flex%3DY%26isMobile%3Dfalse%26searchtype%3DOW%26language%3Den%26code_ag%3Drds%26alias%3Dbtd%26date_dep%3D20221029%26gateway_dep%3DYYZ%26dest_dep%3DMLB%26nb_adult%3D1%26nb_child%3D0",
            "responsePage":"origin",
            "ddv":"4.5.0",
        }
        jsData = json.loads(datas["jsData"])
        jsData["ua"] = UserAgent
        datas["jsData"] = json.dumps(jsData, ensure_ascii=False, separators=(',',':'))

        eventsArray = json.loads(datas["events"])
        for i in range(len(eventsArray)):
            one = eventsArray[i]
            one["date"] = int(time.time()) - 5000 + random.randint(80 + 20*i, 120 + 20*i)
        datas["events"] = json.dumps(eventsArray, ensure_ascii=False, separators=(',',':'))

        url = "https://api-js.datadome.co/js/"

        yield scrapy.FormRequest(url=url, formdata=datas, callback=self.parseDatadome, cookies={"BAIDUID":"a"}, dont_filter = True)


    def parseDatadome(self, response):
        print("parseDatadome")
        cookie = json.loads(response.text)["cookie"]
        cookie_dict =  cookieString2CookieDict(cookie)
        # CookiesMiddleware.datadome = cookie_dict["datadome"]
        for i in range(3):
            url = self.start_urls[0]
            yield scrapy.Request(url=url, callback=self.parseN, cookies={"BAIDUID":"b"}, dont_filter = True)

        
    def parseN(self, response):
        for i in range(3):
            url = self.start_urls[0]
            yield scrapy.Request(url=url, cookies={"BAIDUID":"c"}, dont_filter = True)
