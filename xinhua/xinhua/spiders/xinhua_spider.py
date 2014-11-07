import scrapy
from scrapy.http import Request, HtmlResponse
from xinhua.items import XinhuaItem

import requests
import json
from scrapy.selector import Selector

import urllib

class XinhuaSpider(scrapy.Spider):
  name = "xinhua"
  download_delay = 1 
  allowed_domains = ["info.search.news.cn"]
  start_urls = ["http://info.search.news.cn/result.jspa?pno=21&rp=40&t1=0&btn=%CB%D1+%CB%F7&t=1&n1=%D7%D4%C8%BB%D6%AE%D3%D1&np=1&ct=%25%3F%25%3F%25%3F%25%3F%25%3F%25%3F%25%3F%25%3F&ss=2"]
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

      try:
        d = urllib.urlopen(link)
        if d.getcode() == 200: # check if valid
          data = d.read()  
          r = requests.get(link)
          if r.encoding == 'gb2312':
            data = unicode(data, "gb2312").encode("utf8")
          elif r.encoding == 'gbk':
            data = unicode(data, "gbk").encode("utf8")
          hxs = Selector(text=data)
          if hxs.xpath('//p').extract():
            # if hxs.select('//p/span/text()').extract():
            #   content = hxs.select('//p').extract()
            # else: 
            content = hxs.xpath('//p/text()').extract()
            for i in content:
              i = i.encode('utf-8')
            item['content'] = content
          else:
            item['content'] = "no p tag"
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

  
#   def parse_detail(self, response):
#     if url.startswith("http://news.xinhuanet.com/"):
#       # item['title'] = response.xpath('//h1[@id="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="content"]/text()').extract()

#     else if url.startswith("http://www.cq.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@class="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="article"]').extract()

#     else if url.startswith("http://www.qh.xinhuanet.com/"):
#       # item['title'] = response.xpath('//td[@class="xilantop"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="Content"]/text()').extract()

#     else if url.startswith("http://www.sc.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="s6"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="xhw"]/text()').extract()  

#     else if url.startswith("http://www.he.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="newstit"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="zhenwen"]/text()').extract()

#     else if url.startswith("http://www.sn.xinhuanet.com/"):
#       # item['title'] = response.xpath('//td[@class="text_t"]/text()').extract()[0]
#       item['content'] = response.xpath('//td[@class="text"]/text()').extract()

#     else if url.startswith("http://www.js.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="Title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="Content"]/text()').extract()

#     else if url.startswith("http://www.bj.xinhuanet.com/"):
#       # item['title'] = response.xpath('//h1[@id="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="contentblock"]/text()').extract()

#     else if url.startswith("http://www.hq.xinhuanet.com/"):
#       # item['title'] = response.xpath('//h1/text()').extract()[0]
#       item['content'] = response.xpath('//td[@class="content"]/text()').extract()

#     else if url.startswith("http://www.qstheory.cn/"):
#       # item['title'] = response.xpath('//div[@class="main"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="Text_area"]/text()').extract()
# # qs text_area may need more specific
#     else if url.startswith("http://www.zj.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="news_content_container"]/h2/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="news_content"]/text()').extract()

#     else if url.startswith("http://sh.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="Title"]/text()').extract()[0]
#       item['content'] = response.xpath('//td[@class="p1"]/text()').extract()

#     else if url.startswith("http://www.jx.xinhuanet.com/"):
#       # item['title'] = response.xpath('//span[@class="xilanwz"]/text()').extract()[0]
#       item['content'] = response.xpath('//td[@class="text2"]/text()').extract()
# ##
#     else if url.startswith("http://sg.xinhuanet.com/"):
#       # item['title'] = response.xpath('//span[@class="txt18_xilan"]/text()').extract()[0]
#       item['content'] = response.xpath('//span[@id="content"]/text()').extract()

#     else if url.startswith("http://www.fj.xinhuanet.com/"):
#       # item['title'] = response.xpath('//h1/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="Content"]/p/text()').extract()

#     else if url.startswith("http://www.hb.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@class="wz_bt"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="wz_nr"]/p/text()').extract()

#     else if url.startswith("http://www.sd.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@class="title"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="content"]/p/text()').extract()

#     else if url.startswith("http://www.ln.xinhuanet.com/"):
#       # item['title'] = response.xpath('//strong/text()').extract()[1]
#       item['content'] = response.xpath('//td[@class="hei"]/span/p/text()').extract()

#     else if url.startswith("http://www.xinhuatrip.org/"):
#       # item['title'] = response.xpath('//h1[@class="detail_title"]/text()').extract()[0]
#       item['content'] = response.xpath('//ul[@class="detail_content"]/p/text()').extract()

#     else if url.startswith("http://www.sanya.news.cn/"):
#       # item['title'] = response.xpath('//td[@class="show_title"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//td[@class="content1"]/p/text()').extract()

#     else if url.startswith("http://www.gd.xinhuanet.com/"):
#       # item['title'] = response.xpath('//div[@id="ArticleTit"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="ArticleCnt"]/p/text()').extract()

#     else if url.startswith("http://www.sx.xinhuanet.com/"):
#       # item['title'] = response.xpath('//span[@id="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="Content"]/p/text()').extract()

#     else if url.startswith("http://www.gz.xinhuanet.com/"):
#       # item['title'] = response.xpath('//td[@class="bt"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="zw"]/p/text()').extract()

#     else if url.startswith("http://nb.wenming.cn/"):
#       # item['title'] = response.xpath('//div[@class="hd"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()

#     else if url.startswith("http://zz.wenming.cn/"):
#       # item['title'] = response.xpath('//div[@class="hd"]/h1/text()').extract()[0]
#       item['content'] = response.xpath('//span[@class="fontSize14 lineHight23"]/p/text()').extract()

#     else if url.startswith("http://www.ha.xinhuanet.com/"):
#       # item['title'] = response.xpath('//span[@id="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="Content"]/p/text()').extract()

#     else if url.startswith("http://bj.wenming.cn/"):
#       # item['title'] = response.xpath('//div[@id="title_tex"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="tex"]/p/text()').extract()

#     else if url.startswith("http://www.xj.xinhuanet.com/") or url.startswith("http://bt.xinhuanet.com/"):
#       # item['title'] = response.xpath('//h2/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="ArticleContent"]/p/text()').extract()

#     else if url.startswith("http://www.tj.xinhuanet.com/"):
#       # item['title'] = response.xpath('//span[@id="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@id="Content"]/p/text()').extract()

#     else if url.startswith("http://mzl.wenming.cn/"):
#       # item['title'] = response.xpath('//span[@id="title_tex"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="Custom_UnionStyle"]/text()').extract()

#     else if url.startswith("http://hncd.wenming.cn/"):
#       # item['title'] = response.xpath('//td[@class="title"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()

#     else if url.startswith("http://www.zgpaw.com.cn/"):
#       # item['title'] = response.xpath('//div[@id="Title"]/text()').extract()[0]
#       item['content'] = response.xpath('//font[@id="Zoom"]/p/text()').extract()

#     else if url.startswith("http://sxbj.wenming.cn/"):
#       # item['title'] = response.xpath('//td[@class="title_txt"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()

#     else if url.startswith("http://sxbj.wenming.cn/"):
#       # item['title'] = response.xpath('//td[@class="title_txt"]/text()').extract()[0]
#       item['content'] = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
    

#     yield item
