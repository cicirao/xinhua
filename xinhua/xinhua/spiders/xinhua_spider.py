import scrapy
from scrapy.http import Request, HtmlResponse
from xinhua.items import XinhuaItem

import requests
import json
from scrapy.selector import Selector

import urllib
from HTMLParser import HTMLParser

class XinhuaSpider(scrapy.Spider):
  name = "xinhua"
  download_delay = 1 
  allowed_domains = ["info.search.news.cn"]
  start_urls = ["http://info.search.news.cn/result.jspa?pno=23&rp=40&t1=0&btn=%CB%D1+%CB%F7&t=1&n1=%D7%D4%C8%BB%D6%AE%D3%D1&np=1&ct=%D7%D4%C8%BB%D6%AE%D3%D1&ss=2"]
  # def start_requests(self):
  #   for i in xrange(31, 41):
  #     yield self.make_requests_from_url("http://info.search.news.cn/result.jspa?pno=%d&rp=40&t1=0&btn=%%CB%%D1+%%CB%%F7&t=1&n1=%%D7%%D4%%C8%%BB%%D6%%AE%%D3%%D1&np=1&ct=%%25%%3F%%25%%3F%%25%%3F%%25%%3F%%25%%3F%%25%%3F%%25%%3F%%25%%3F&ss=2" % i)

  def parse(self, response):
    for page in response.xpath('//div[@align="left"]')[:-1]:
      # if article.xpath('span[@class="style1d"]/a/text()') == True:
      item = XinhuaItem()

      title = page.xpath('span[@class="style1d"]/a/text()').extract()[0]
      link = page.xpath('span[@class="style1d"]/a/@href').extract()[0]
      published_at = page.xpath('span[@class="style2a"]/text()').re(r'\d{4}-\d{2}-\d{2}')[0]

      item['title'] = title.encode('utf-8')
      item['link'] = link
      item['published_at'] = published_at

      try: # filter available websites
        d = urllib.urlopen(link)
        if d.getcode() == 200: # check if valid
          data = d.read()  
          r = requests.get(link)
          if r.encoding.lower() != 'utf-8' and r.encoding.lower() != 'gbk': # convert charset
            data = data.decode('gb2312').encoding('utf-8')
          elif r.encoding.lower() == 'gbk':
            data = data.decode('gbk').encoding('utf-8')

          hxs = Selector(text=data)
          
          if hxs.xpath('//p').extract(): # get p node text
            content = ''.join(hxs.xpath('//p//text()').extract()).strip()

          elif link.startswith('http://www.p5w.net/'): # special website with no p tag
            content = ''.join(hxs.xpath('//div[@class="new_content_p BSHARE_POP"]//text()').extract()).strip()
          elif link.startswith('http://hy.stock.cnfol.com/') or link.startswith('http://news.cnfol.com/'):
            content = ''.join(hxs.xpath('//div[@id="__content"]//text()').extract()).strip()
          elif link.startswith('http://mzl.wenming.cn/'):
            content = ''.join(hxs.xpath('//div[@class="Custom_UnionStyle"]//text()').extract()).strip()  

          else: # just in case
            content = ["no p tag"]
          
          item['content'] = content # pass value to the instance
        else:
          item['content'] = "can not load page"

      except Exception,e:
        item['content'] = "This webpage is not available"
      yield item

    # for url in urls:
    url = "http://info.search.news.cn/" + response.xpath('//div[@align="left"]/u/a/@href').extract()[-1]
    # print url
    # url = "http://info.search.news.cn/" + url
    print url
    yield Request(url, callback=self.parse)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
