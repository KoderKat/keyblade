starters = ["http://www.deviantart.com/browse/all/literature/fanfiction/drama/", #Drma
            "http://www.deviantart.com/browse/all/literature/fanfiction/fantasy/", #Fantasy
            "http://www.deviantart.com/browse/all/literature/fanfiction/general/", #GeneralFiction
            "http://www.deviantart.com/browse/all/literature/fanfiction/horror/", #Horror
            "http://www.deviantart.com/browse/all/literature/fanfiction/humor/", #Humor
            "http://www.deviantart.com/browse/all/literature/fanfiction/romance/", #Romance
            "http://www.deviantart.com/browse/all/literature/fanfiction/scifi/", #SciFi
           ]

outfile = open("./start_urls.txt", "w")
for url in starters :
  for i in range(0, 1500, 24) :
    newurl = '"' + url + "?offset=" + str(i) + '",'
    print newurl
    outfile.write(newurl)
outfile.close()
