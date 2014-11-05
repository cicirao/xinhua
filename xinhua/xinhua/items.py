# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinhuaItem(scrapy.Item):
  # define the fields for your item here like:
  link = scrapy.Field()
  published_at = scrapy.Field()

  content = scrapy.Field()
  title = scrapy.Field()
  word_frequency = scrapy.Field()


  # title XPath: /html//div[@id='extresult']//div[@align='left'][0]//a/text()
  # link XPath: /html//div[@id='extresult']//div[@align='left'][0]//a/href()
  # published_at:  /html//div[@id='extresult']//div[@align='left'][0]/span[@class='style2a'][0]/text() match regex