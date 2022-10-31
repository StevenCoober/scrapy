# Scrapy settings for baidu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'demo'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

COOKIES_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# DOWNLOAD_FAIL_ON_DATALOSS = False  # 重试处理
# RANDOMIZE_DOWNLOAD_DELAY = True # 开启随机增加毫秒级延迟，增加访问成功率

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 5 # 想重试几次就写几
# 下面这行可要可不要
# RETRY_HTTP_CODES = [500, 502, 503, 504, 408]


# 设置超时时间
DOWNLOAD_TIMEOUT = 20
# 日志配置
# NOTSET=0
# DEBUG=10
# INFO=20
# WARN=30
# ERROR=40
# CRITICAL=50
# LOG_LEVEL = 'WARNING'
# LOG_FILE = 'demo/log/error_log.txt'

# CLOSESPIDER_TIMEOUT=15

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}



# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'middlewares.DemoSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'middlewares.DemoDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'middlewares.my_proxy': 2,
    # 'middlewares.business_proxy': 3,
    # 'middlewares.fiddle_proxy': 3,
    # 'middlewares.OneceMiddleware': 4,
    
    'toolkits.make_ua.RandomUserAgentMiddleware': 4,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 6,
    'middlewares.RandomDelayMiddleware': 999,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉

    # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':None,
    # 'middlewares.BrowserCookiesMiddleware':701
    'middlewares.MyCookiesMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'pipelines.SunwingJsonPipeline': 1,
	'pipelines.SunwingExcelPipeline': 2,
  'pipelines.TicketJsonPipeline': 3,
  'pipelines.TicketExcelPipeline': 4,
   	# 'pipelines.DemoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
