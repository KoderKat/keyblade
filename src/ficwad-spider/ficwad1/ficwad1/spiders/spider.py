import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from ficwad1.items import Ficwad1Item
from time import gmtime, strftime
import string

#BASE_DATA_DIR is the path to the data directory for storing all output files.
# recommendation: use the data directory in ficwad-spider-v1/data/
BASE_DATA_DIR = "."

#class ficwad1Spider(scrapy.Spider) :
class ficwad1Spider(scrapy.contrib.spiders.CrawlSpider) :
  name = "ficwad1"
  #name = "ficwad1_crawl"
  allowed_domains = ["ficwad.com"]
  start_urls = ["http://ficwad.com/category/1", #Anime/Manga
                "http://ficwad.com/category/18", #Books
                "http://ficwad.com/category/30", #Cartoons
                "http://ficwad.com/category/303", #Celebrities
                "http://ficwad.com/category/21", #Comics
                "http://ficwad.com/category/4", #Games
                "http://ficwad.com/category/7", #Movies
                "http://ficwad.com/category/9", #Original
                "http://ficwad.com/category/113", #Theatre
                "http://ficwad.com/category/25", #TV
               ]

  ####################################################
  def parse(self, response) :
    it = 0
    listitems = response.xpath('//span[@class="catname"]') #//li
    #print listitems

    for cat in listitems :
      #print "*************************************************"
      #print "it = " + str(it)
      #print "cat = " + str(cat)
      #print "cat.xpath title = " + str(cat.xpath('./text()').extract()[0])
      #print "cat.xpath url = " + str(cat.xpath('../@href').extract()[0])
      #print "*************************************************"

      item = Ficwad1Item()
      fandom = cat.xpath('./text()').extract()[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      fandom = re.sub(' ', '', fandom)
      fandom = re.sub('\'', '', fandom)
      fandom = fandom.replace("|", "")
      fandom = fandom.replace("!", "")
      fandom = fandom.replace(",", "")
      fandom = fandom.replace(".", "")
      fandom = fandom.replace(":", "")
      fandom = fandom.replace("(", "")
      fandom = fandom.replace(")", "")
      fandom = fandom.replace("{", "")
      fandom = fandom.replace("}", "")
      item['fandom'] = fandom
      item['url_fandom'] = "http://ficwad.com"+str(cat.xpath('../@href').extract()[0]).encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')

      #print "fandom = " + item['fandom']
      #print "url_fandom = " + item['url_fandom']

      request = scrapy.Request(item['url_fandom'], callback=self.parseFandom)
      request.meta['item'] = item

      # collect at most 3000 stories per category
      if it > 2999 :
        break
      else :
        it = it + 1
        yield request

  ####################################################
  def parseFandom(self, response) :
    #print ".... parseFandom ...."
    #print "titles_not_blocked = " + str(response.xpath("//li/h4/a/text()").extract())
    #print "url_titles_notblocked = " + str(response.xpath("//li/h4/a/@href").extract())

    item = response.meta['item']
    url_titles_notblocked = response.xpath("//li/h4/a/@href").extract()

    it = 0
    for url in url_titles_notblocked :
      path = "http://ficwad.com"+url
      #print "In " + item['fandom'] + ": " + "path = " + path
      request = scrapy.Request(path, callback=self.parseTitle)
      request.meta['item'] = item
      yield request

  ####################################################
  def parseTitle(self, response) :
    #print ".... parseTitle .... " + str(response)
    item = response.meta['item']
    item = self.getTitleInfo(item, response)
    item = self.getAuthorInfo(item, response)
    item = self.getGenre_Rating_WC(item, response)
    if int(item['numchs']) > 0 :
      print "Multiple chapters!"
      #item = self.getText_multi(item, response)
    else :
      item = self.getText_one(item, response)

    #item['title_text'] = ''

    title = item['title']
    title = re.sub(' ', '', title)
    title = re.sub('\'', '', title)
    title = title.replace("|", "")
    title = title.replace("!", "")
    title = title.replace(",", "")
    title = title.replace(".", "")
    title = title.replace(":", "")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("{", "")
    title = title.replace("}", "")
    #print "*********** title = " + title

    r0 = item['author_rating']
    rating = ""
    if r0 == "G" or r0 == "PG" :
      rating = "e"
    elif "13" in r0 :
      rating = "t"
    else :
      rating = "m"

    fic_info_filename = BASE_DATA_DIR + title + "_info" + ".txt"
    fic_text_filename = BASE_DATA_DIR + title + "_" + rating + ".txt"

    #print "fic_info_filename = " + fic_info_filename
    #print "fic_text_filename = " + fic_text_filename

    info_file = open(fic_info_filename, 'w')
    info_file.write("###" + '\n')
    info_file.write(item['fandom'] + '\n')
    info_file.write(item['url_fandom'] + '\n')
    info_file.write(item['title'] + '\n')
    info_file.write(item['url_title'] + '\n')
    info_file.write(item['author'] + '\n')
    info_file.write(item['url_author'] + '\n')
    info_file.write(item['genre'] + '\n')
    info_file.write(item['wc'] + '\n')
    info_file.write(item['numchs'] + '\n')
    info_file.write("###")
    info_file.close()

    text_file = open(fic_text_filename, 'w')
    text_file.write("###")
    text_file.write(item['title_text'])
    text_file.write("###")
    text_file.close()

    return item

  ####################################################
  def getTitleInfo(self, item, response) :
    print ".... getTitleInfo...."

    # get title
    title_raw = response.xpath("//div/h4/a/text()").extract()
    print "title_raw = " + str(title_raw)
    title = title_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    #print "title = " + title
    title = str(title).translate( None, string.whitespace )
    title = re.sub('\'', '', title)
    title = re.sub('\n', '', title)
    title = title.replace("|", "")
    title = title.replace("!", "")
    title = title.replace(",", "")
    title = title.replace(".", "")
    title = title.replace(":", "")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("{", "")
    title = title.replace("}", "")

    # get url_title
    url_title_raw = response.xpath("//div/h4/a/@href").extract()
    #print "url_title_raw = " + str(url_title_raw)
    url_title = url_title_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    #print "url_title = " + str(url_title)

    item['title'] = title
    item['url_title'] = "http://ficwad.com"+url_title
    #item['title_text'] = ''
    return item

  ####################################################
  def getAuthorInfo(self, item, response) :
    #print ".... getAuthorInfo...."
    
    # get author
    author_raw = response.xpath("//div/span[@class='author']/a/text()").extract()
    #print "author_raw = " + str(author_raw)
    author = author_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    #print "author = " + author

    # get url_author
    url_author_raw = response.xpath("//div/span[@class='author']/a/@href").extract()
    #print "url_author_raw = " + str(url_author_raw)
    url_author = url_author_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    #print "url_author = " + str(url_author)

    item['author'] = author
    item['url_author'] = "http://ficwad.com"+url_author
    return item

  ####################################################
  def getGenre_Rating_WC(self, item, response) :
    #print ".... getGenre_Rating_WC ...."

    metaData = response.xpath("//div/p[@class='meta']/text()").extract()
    #print "metaData = " + str(metaData)

    listOfStrs = [x.encode('ascii', 'ignore').decode('ascii') for x in metaData]
    listOfStrs = [a.encode('ascii', 'ignore') for a in listOfStrs]
    #print "listOfStrs = " + str(listOfStrs)

    genre = ""
    author_rating = ""
    wc = ""
    numchs = "0"
    for elem in listOfStrs :
      elem = re.sub('-', '', elem)
      elem = re.sub(', ', ',', elem)
      elem = elem.split()

      for e in elem :
        e = e.split(":") # e is a list
        #print "e = " + str(e)

        # get genre
        if "Genres" in e :
          try: genre = e[1]
          except IndexError: genre = "none"

        # get rating
        if "Rating" in e :
          try: author_rating = e[1]
          except IndexError: author_rating = "none"

        # get word count
        try: tmp = e[0]
        except IndexError: wc = "none"
        if "words" in e[0] :
          tmp = e[0].split("w")
          wc = tmp[0]

        # get number of chapters
        if "Chapters" in e :
          try: numchs = e[1]
          except IndexError: numchs = "0"

    item['genre'] = genre.lower()
    item['author_rating'] = author_rating
    item['wc'] = wc
    item['numchs'] = numchs
    return item

  ####################################################
  def getText_multi(self, item, response) :
    print ".... getText_multi ...."

    #chlinks = response.xpath('//ul[@class="storylist"]/li/h4/a') 
    #print chlinks

    #for ch in chlinks :
    #  print "*************************************************"
    #  print "ch = " + str(ch)
    #  print "ch.xpath url = " + str(ch.xpath('./@href').extract()[0])
    #  print "*************************************************"

    #ch_url = "http://ficwad.com"+str(ch.xpath('./@href').extract()[0])

    #request = scrapy.Request(ch_url, callback=self.parseTitle)
    #yield request

  ####################################################
  def getText_one(self, item, response) :
    #print ".... getText_one ...."

    if int(item['numchs']) > 0 :
      # Collect chapter links and call parse_title
      print "Multiple chapters!"

    else :
      # get text
      text_raw = response.xpath("//div[@id='storytext']/text()").extract()

      text = []
      for t in text_raw :
        #print "t = " + str(t)
        t = t.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
        #print "t1 = " + str(t)
        t = re.sub('\n', '', t)
        #print "t2 = " + str(t)
        text.append( t )
      #print ">>>>>>>>>>> " + str(text)
      cleanText = " ".join(text)
      #print ">>>>>>>>>>> cleanText = " + cleanText

      item['title_text'] = cleanText
      return item

'''
    if int(numchs) > 0 :
      # Collect chapter links and call parse_title
      print "Multiple chapters!"
      chlinks = response.xpath('//ul[@class="storylist"]/li/h4/a') 
      print chlinks

      for ch in chlinks :
        print "*************************************************"
        print "ch = " + str(ch)
        print "ch.xpath url = " + str(ch.xpath('./@href').extract()[0])
        print "*************************************************"

      ch_url = "http://ficwad.com"+str(ch.xpath('./@href').extract()[0])

      request = scrapy.Request(ch_url, callback=self.parseTitle)
      yield request
      
    else :
      # get text
      text_raw = response.xpath("//div[@id='storytext']/text()").extract()

      text = []
      for t in text_raw :
        #print "t = " + str(t)
        t = t.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
        #print "t1 = " + str(t)
        t = re.sub('\n', '', t)
        #print "t2 = " + str(t)
        text.append( t )
      #print ">>>>>>>>>>> " + str(text)
      cleanText = " ".join(text)
      #print ">>>>>>>>>>> cleanText = " + cleanText

    item['title_text'] = cleanText

    # save info to info file
    # save text to text file
''' 
