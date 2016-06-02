# -*- coding: utf-8 -*-

import nltk
import os
import random
import sqlite3

from nltk.corpus import names
from nltk.classify import apply_features
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.tokenize import word_tokenize
from itertools import chain
from nltk.corpus import wordnet

TESTING_DATA = "./testing_data"
SAVE_DATA = "./data"
SITE = "ficwad"

###############################################
###############################################
def document_features(document):
  document_words = set(document)
  features = {}
  for word in train_word_features :
    features['contains({})'.format(word)] = (word in document_words)
  return features

###############################################
###############################################
def getDirnames( path ) :
  dirList = []
  for f in os.listdir( path ) :
    if not os.path.isfile( path ) :
      if not f == ".DS_Store" :
        dirList.append(f)
  return dirList

###############################################
###############################################

#################
# TRAINING DATA #
#################
train_reader = CategorizedPlaintextCorpusReader('./training_data', r'.*\_.*\.txt', cat_pattern=r'.*\_(\w+)\.txt')
train_documents = [(list(train_reader.words(fileid)), category)
                   for category in train_reader.categories()
                   for fileid in train_reader.fileids(category)]
random.shuffle(train_documents)
#print train_documents

train_documents_clean = []
for i in train_documents :
  cat = i[1]
  #print cat
  newList = []
  for word in i[0] :
    #print j
    clean_word = word.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
    newList.append(clean_word)
  newTup = (newList, cat)
  train_documents_clean.append(newTup)
#print train_documents_clean 

train_word_features = nltk.FreqDist(chain(*[i for i,j in train_documents_clean]))
train_word_features = train_word_features.keys()[:]
#print train_word_features

###############################################
###############################################
# TRAININ FEATURE SET
train_featuresets = [(document_features(d), c) for (d,c) in train_documents_clean]
###############################################
###############################################

##############################################################
# TESTING DATA

# get list of story filenames
dirList = getDirnames( TESTING_DATA + '/' )
storyList = []
for d in dirList :
  story = d
  story = story.replace("ficwad_", "")
  story = story[:-2]
  storyList.append(story)

print "length of storyList = " + str(len(storyList))

dict_testing = {}
for i in range(0, len(storyList)) :
  dict_testing[ storyList[i] ] = dirList[i]

print "number of test stories = " + str(len(dict_testing))

###############################################
###############################################
# FEATURE SETS
train_featuresets = [(document_features(d), c) for (d,c) in train_documents_clean]
###############################################
###############################################
numtrain = int(len(train_documents) * 90 / 100)
# training set
#train_set = [({i:(i in tokens) for i in train_word_features}, tag) for tokens,tag in train_documents_clean[:numtrain]]
train_set = [({i:(i in tokens) for i in train_word_features}, tag) for tokens,tag in train_documents_clean[:]]
# developement test set
#dev_test_set = [({i:(i in tokens) for i in train_word_features}, tag) for tokens,tag  in train_documents_clean[numtrain:]]

##############
#   OUTPUT   #
##############
print "Training classifier..."
classifier = nltk.NaiveBayesClassifier.train(train_set)
print "... done."

#print "Classify dev_test_set:"
#print nltk.classify.accuracy(classifier, dev_test_set)
#print classifier.show_most_informative_features(50)
#print "... done."

#print "Classify test_set:"
#print nltk.classify.accuracy(classifier, test_set)
#print classifier.show_most_informative_features(10)
#print "... done."

it = 0
for key in dict_testing :
  print "it = " + str(it)
  it = it + 1
  print "key = " + str(key)
  title = key
  dirname = dict_testing[key]
  story_dir = TESTING_DATA + '/' + dirname 
  ################
  # TESTING DATA #
  ################
  # documents in the test set must adhere to the "_<rating>.txt" convention
  test_reader = CategorizedPlaintextCorpusReader(story_dir, r'.*\_.*\.txt', cat_pattern=r'.*\_(\w+)\.txt')
  test_documents = [(list(test_reader.words(fileid)), category)
                     for category in test_reader.categories()
                     for fileid in test_reader.fileids(category)]
  random.shuffle(test_documents)
  #print test_documents

  test_documents_clean = []
  for i in test_documents :
    cat = i[1]
    #print cat
    newList = []
    for word in i[0] :
      #print j
      clean_word = word.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      newList.append(clean_word)
    newTup = (newList, cat)
    test_documents_clean.append(newTup)
  #print test_documents_clean 

  print "number of test docs = " + str( len(test_documents_clean) )

  test_word_features = nltk.FreqDist(chain(*[i for i,j in test_documents_clean]))
  test_word_features = test_word_features.keys()[:]
  #print test_word_features


  ###############################################
  ###############################################
  # FEATURE SETS
  test_featuresets = [(document_features(d), c) for (d,c) in test_documents_clean]
  ###############################################
  ###############################################
  # actual test set
  test_set = [({i:(i in tokens) for i in test_word_features}, tag) for tokens,tag  in test_documents_clean[:]]

  ##############
  #   OUTPUT   #
  ##############
  print "Training classifier..."
  #classifier = nltk.NaiveBayesClassifier.train(train_set)
  print "... done."

  #print "Classify dev_test_set:"
  #print nltk.classify.accuracy(classifier, dev_test_set)
  #print classifier.show_most_informative_features(50)
  #print "... done."

  #print "Classify test_set:"
  #print nltk.classify.accuracy(classifier, test_set)
  #print classifier.show_most_informative_features(10)
  #print "... done."

  # GET DIRTY WORDS
  dirtywords = []
  if os.path.isfile("./dirtywords.txt") :
    infile = open("./dirtywords.txt", "r")
    for line in infile :
      #print line
      dirtywords.append(line.replace("\n", ""))
    infile.close()
  #print dirtywords

  # classify a set of documents
  for j in range(0, len(test_documents_clean)) :
    #print "j = " + str(j)
    print "Classify single document:"
    currDocumentKeys = test_featuresets[j][0].keys()
    #print currDocumentKeys

    # a story is automatically rated m if it contains any of the specified dirty words
    flag = False
    for i in dirtywords :
      #print i
      if ("contains("+i+")" in currDocumentKeys) and (test_featuresets[j][0]["contains("+i+")"]==True) :
        print "automatically m"
        #auto_rating = "m"
        flag = True

    auto_rating = ""
    auto_rating_dirtywords = ""
    accuracy = ""
    if flag == True :
      auto_rating_dirtywords = "m"
      auto_rating = classifier.classify(test_featuresets[j][0])
      accuracy = nltk.classify.accuracy(classifier, test_featuresets)
      print nltk.classify.accuracy(classifier, test_featuresets)
    else :
      auto_rating = classifier.classify(test_featuresets[j][0])
      accuracy = nltk.classify.accuracy(classifier, test_featuresets)
      print nltk.classify.accuracy(classifier, test_featuresets)

    print title
    print auto_rating
    print auto_rating_dirtywords

    #save data to dir
    connection = sqlite3.connect(SAVE_DATA + '/' + 'ratings.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS ratings (id INTEGER PRIMARY KEY, title VARCHAR(100), auto_rating VARCHAR(100), auto_rating_dirtywords VARCHAR(100), accuracy VARCHAR(100), site VARCHAR(100))')
    cursor.execute("SELECT * FROM ratings WHERE title='" + title + "'" )
    result = cursor.fetchone()
    if result:
      print ("MESSAGE: Item already in database: ", title, auto_rating, SITE)
    else:
      cursor.execute("""INSERT INTO ratings (title, auto_rating, auto_rating_dirtywords, accuracy, site) values (?, ?, ?, ?, ?)""", (title, auto_rating, auto_rating_dirtywords, accuracy, SITE))
      connection.commit()

    print "... done."
