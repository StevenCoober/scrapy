import os, sys, glob, random, traceback, json
import xlwt
import xlrd
import scrapy
from functools import cmp_to_key
sys.path.append(os.path.abspath("D:/Projects/demo/SunwingScrapy"))
from properties.items import *
from utils.utils import saveTickets

json_path = os.getcwd() + r"/../datas/Ticket.json"
chooses = None
if os.path.isfile(json_path):
    with open(json_path, "r", encoding='utf-8') as fp:
        data=fp.read()
        chooses = Chooses() ## <HouseScrapy>所有信息
        chooses.init() ## <Chooses>
        chooses.jsonLoads(data)

saveTickets(chooses, os.getcwd() + '/../datas/Tickets.xls')