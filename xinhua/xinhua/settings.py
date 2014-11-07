# -*- coding: utf-8 -*-

# Scrapy settings for xinhua project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xinhua'

SPIDER_MODULES = ['xinhua.spiders']
NEWSPIDER_MODULE = 'xinhua.spiders'

DNSCACHE_ENABLED = False
DOWNLOAD_TIMEOUT = 60
LOG_LEVEL = 'INFO'
CONCURRENT_REQUESTS = 100
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xinhua (+http://www.yourdomain.com)'
