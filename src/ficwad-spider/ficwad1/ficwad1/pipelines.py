# -*- coding: utf-8 -*-
#
# This code is based on the pipeline code written by Alex Black for the IMDB-spider project available at: https://github.com/alexwhb/IMDB-spider
# IMDB-spider is copyrighted by Alex Black: The MIT License (MIT) Copyright (c) 2014 Alex Black

from scrapy import log
import sqlite3 as sqlite

#BASE_DIR is the path to the data directory for storing all output files.
# recommendation: use the data directory in ficwad-spider-v1/data/
#BASE_DIR = PREPEND + "/ficwad-spider-v1/data/"
BASE_DIR = "."

class Ficwad1Pipeline(object):
  def __init__(self):
    # Possible we should be doing this in spider_open instead, but okay
    self.connection = sqlite.connect(BASE_DIR + 'ficwad.db')
    self.cursor = self.connection.cursor()
    self.cursor.execute('CREATE TABLE IF NOT EXISTS ficwad (id INTEGER PRIMARY KEY, fandom VARCHAR(100), ' \
                                                            'url_fandom VARCHAR(200), ' \
                                                            'title VARCHAR(100), ' \
                                                            'url_title VARCHAR(200), ' \
                                                            'author VARCHAR(80), ' \
                                                            'url_author VARCHAR(200), ' \
                                                            'genre VARCHAR(100), ' \
                                                            'author_rating VARCHAR(80), ' \
                                                            'auto_rating VARCHAR(80), ' \
                                                            'wordcount VARCHAR(80), ' \
                                                            'numchapters VARCHAR(80))'
                       )

  # Take the item and put it in database - do not allow duplicates
  def process_item(self, item, spider):
    self.cursor.execute("SELECT * FROM ficwad WHERE url_title=? AND url_author=?", (item['url_title'], item['url_author']))
    result = self.cursor.fetchone()
    if result:
      #log.msg("Item already in database: %s" % item, level=log.DEBUG)
      print ("MESSAGE: Item already in database: %s" % item)
    else:
      self.cursor.execute("""INSERT INTO ficwad (fandom, url_fandom, title, url_title, author, url_author, genre, author_rating, wordcount, numchapters) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (
                           item['fandom'],
                           item['url_fandom'],
                           item['title'],
                           item['url_title'],
                           item['author'],
                           item['url_author'],
                           item['genre'],
                           item['author_rating'],
                           item['wc'],
                           item['numchs']
                         ))
      self.connection.commit()

      #log.msg("Item stored : " % item, level=log.DEBUG)
      print ("Item stored : " % item)
    return item

  def handle_error(self, e):
    log.err(e)
