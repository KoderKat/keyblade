import scrapy
import re
import string
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from ao3.items import Ao3Item
from time import gmtime, strftime


BASE_DATA_DIR = "."

class ao3Spider(scrapy.contrib.spiders.CrawlSpider) :
  name = "ao3"
  allowed_domains = ["archiveofourown.org"]
  start_urls = [#"https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms", #Anime/Manga
                #"https://archiveofourown.org/media/Books%20*a*%20Literature/fandoms", #Books/Literature
                #"https://archiveofourown.org/media/Cartoons%20*a*%20Comics%20*a*%20Graphic%20Novels/fandoms", #Cartoons/Comics/GraphicNovels
                #"https://archiveofourown.org/media/Celebrities%20*a*%20Real%20People/fandoms", #Celebrities/RealPeople
                #"https://archiveofourown.org/media/Movies/fandoms", #Movies
                #"https://archiveofourown.org/media/Music%20*a*%20Bands/fandoms", #Music/Bands
                #"https://archiveofourown.org/media/Other%20Media/fandoms", #OtherMedia
                #"https://archiveofourown.org/media/Theater/fandoms", #Theater
                "https://archiveofourown.org/media/TV%20Shows/fandoms", #TVShows
                "https://archiveofourown.org/media/Video%20Games/fandoms", #VideoGames
                "https://archiveofourown.org/media/Uncategorized%20Fandoms/fandoms", #UncategorizedFandom
               ]

  ####################################################
  def parse(self, response) :
    it = 0
    listitems = response.xpath('//div/div/div/ol/li/ul/li/a')
    #print "listitems = " + str(listitems)

    for cat in listitems :
      item = Ao3Item()
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
      item['url_fandom'] = cat.xpath('./@href').extract()[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')

      #print "fandom = " + item['fandom']
      #print "url_fandom = " + item['url_fandom']

      request = scrapy.Request(item['url_fandom'], callback=self.parseFandom)
      request.meta['item'] = item

      yield request
      # collect at most 30000 stories per category
      #if it >= 30000 :
      #  break
      #else :
      #  it = it + 1
      #  yield request

  ####################################################
  def parseFandom(self, response) :
    item = response.meta['item']

    story_urls_list = response.xpath('//div/div/div/ol/li/div/h4[@class="heading"]/a[1]/@href').extract()
    #author_urls_list = response.xpath('//div/div/div/ol/li/div/h4[@class="heading"]/a/@href').extract()

    #print story_urls_list
    for url in story_urls_list :
      url = url.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      #print url
      path = "http://archiveofourown.org"+url
  
      item['url_title'] = path

      #print "In " + item['fandom'] + ": " + "path = " + path

      if not "chapter" in url :
        request = scrapy.Request(path, callback=self.parseTitle)
        request.meta['item'] = item
      else :
        print "Multiple chapters!"
      yield request

  ####################################################
  def parseTitle(self, response) :
    #print ".... parseTitle .... " + str(response)
    item = response.meta['item']
    item = self.getTitleInfo(item, response)
    item = self.getAuthorInfo(item, response)
    item = self.get_Rating_WC(item, response)
    item = self.getText_one(item, response)

    title = item['title']
    rating = item['author_rating']

    fic_info_filename = BASE_DATA_DIR + title + "_info" + ".txt"
    #fic_text_filename = BASE_DATA_DIR + title + "_" + rating + ".txt"

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

    return item
    '''
    text_file = open(fic_text_filename, 'w')
    text_file.write("###")
    text_file.write(item['title_text'])
    text_file.write("###")
    text_file.close()
    item['title_text'] = '' # do not store title text in db

    return item
    '''
  ####################################################
  def getTitleInfo(self, item, response) :
    #print ".... getTitleInfo...."

    # get title
    title_raw = response.xpath("//h2[@class='title heading']/text()").extract()
    #print "title_raw = " + str(title_raw)

    if len(title_raw) != 0 :
      title = title_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      title = title.translate(None, string.whitespace)
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
      #print "*********** title = " + title
      item['title'] = title
    else :
      print "Blocked or empty"
      item['title'] = ''
    return item

  ####################################################
  def getAuthorInfo(self, item, response) :
    #print ".... getAuthorInfo...."
    
    # get url_author
    url_author = ""
    url_author_raw = response.xpath("//h3[@class='byline heading']/a[@rel='author']/@href").extract()
    #print "url_author_raw = " + str(url_author_raw)

    if len(url_author_raw) != 0 :
      url_author = url_author_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      #print "url_author = " + url_author

      # get author
      author = ""
      author_raw = response.xpath("//h3[@class='byline heading']/a[@rel='author']/text()").extract()
      #print "author_raw = " + str(author_raw)
      author = author_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      #print "author = " + str(author)

      item['url_author'] = url_author
      item['author'] = author

    else :
      print "Blocked or empty" 
      item['url_author'] = ''
      item['author'] = ''
    return item

  ####################################################
  def get_Rating_WC(self, item, response) :
    #print ".... get_Rating_WC ...."

    # get rating
    author_rating = ""
    author_rating_raw = response.xpath("//dd[@class='rating tags']/ul/li/a[@class='tag']/text()").extract()#[0]
    #print "author_rating_raw = " + str(author_rating_raw)

    if len(author_rating_raw) != 0 :
      author_rating = author_rating_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      author_rating = re.sub(' ', '', author_rating)
      author_rating = re.sub('\'', '', author_rating)
      author_rating = author_rating.replace("|", "")
      author_rating = author_rating.replace("!", "")
      author_rating = author_rating.replace(",", "")
      author_rating = author_rating.replace(".", "")
      author_rating = author_rating.replace(":", "")
      author_rating = author_rating.replace("(", "")
      author_rating = author_rating.replace(")", "")
      author_rating = author_rating.replace("{", "")
      author_rating = author_rating.replace("}", "")
    else :
      author_rating = ""

    #print "author_rating = " + author_rating

    # get word count
    wc = ""
    wc_raw = response.xpath("//dd[@class='stats']/dl[@class='stats']/dd[@class='words']/text()").extract()
    if len(wc_raw) != 0 :
      #print "wc_raw = " + str(wc_raw)
      wc = wc_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    else :
      wc = ""

    # get number of chapters
    numchs = "0"
    numchs_raw = response.xpath("//dd[@class='stats']/dl[@class='stats']/dd[@class='chapters']/text()").extract()
    if (len(numchs_raw) != 0) and (numchs != '?') :
      numchs = numchs_raw[0].encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      numchs = numchs.split("/")
      numchs = numchs[1]
    else :
      numchs = "0"

    item['genre'] = ''
    item['author_rating'] = author_rating
    item['wc'] = wc
    item['numchs'] = numchs
    return item

  ####################################################
  def getText_one(self, item, response) :
    #print ".... getText_one ...."

    item['title_text'] = ''
    return item
    '''
    if int(item['numchs']) > 1 :
      # Collect chapter links and call parse_title
      #print "Multiple chapters!"
      item['title_text'] = ''
    else :
      # get text
      text_raw = response.xpath("//div[@class='userstuff']/p/text()").extract()
      #print "text_raw = " + str(text_raw)

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
