# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DeviantItem(scrapy.Item):
  # define the fields for your item here like:
  fandom = Field()
  url_fandom = Field()
  title = Field()
  url_title = Field()

  author = Field()
  url_author = Field()
  genre = Field()
  author_rating = Field()
  title_text = Field()

  wc = Field()
  numchs = Field()
