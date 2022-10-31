from scrapy.cmdline import execute
import random, os, sys, requests, json, time, logging

# 本程序为爬虫起始入口，直接运行本程序即可运行爬虫
# execute(['scrapy', 'crawl', 'sunwing', '--nolog'])

# execute(['scrapy', 'crawl', 'sunwingAdressSpider'])
execute(['scrapy', 'crawl', 'sunwingTicketSpider'])
# execute(['scrapy', 'crawl', 'test'])
# execute(['scrapy', 'crawl', 'ticket', '-s LOG_LEVEL=DEBUG'])

# execute("scrapy crawl testspider".split())  #followall is the spider's name/
# execute(['scrapy', 'crawl', 'testspider'])

