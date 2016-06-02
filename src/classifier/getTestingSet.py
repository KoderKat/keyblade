import random
import os, sys

from os import listdir
from os.path import isfile, join

DATA_PATH = "/Users/KsComp/projects/keyblade_orig/tests/ficwad-spider-v1/data/"
TRAINING_DIR = "/Users/KsComp/projects/keyblade_orig/tests/nltk_test1/training_data/"
TESTING_DIR = "/Users/KsComp/projects/keyblade_orig/tests/nltk_test1/testing_data/"

# pick 300 random numbers between 0 and the number of documents in total set
def getIndexList( num ) :
  numTestSet = 200
  indexList = random.sample(range(0, num), numTestSet)
  
  # remove duplicates
  unique = []
  [unique.append(item) for item in indexList if item not in unique]
  indexList = unique
  
  if len(indexList) == numTestSet :
    return indexList
  else :
    getIndexList(num)

############
## DRIVER ##
############
# get file names
filenameList_e = []
filenameList_t = []
filenameList_m = []

# collect all filenames per category
for f in listdir(DATA_PATH) :
  if isfile(join(DATA_PATH, f)) :
    if ".txt" in f :
      if not "_info.txt" in f : # only _text.txt files
        filepath = TRAINING_DIR + f
        if not os.path.exists(filepath) : # no test docs appear in training set
          if "_e.txt" in f : 
            filenameList_e.append(f)
          elif "_t.txt" in f :
            filenameList_t.append(f)
          elif "_m.txt" in f :
            filenameList_m.append(f)

#print "filenameList:"
#print filenameList

# get list of random numbers
indexList_e = getIndexList( len(filenameList_e) )
indexList_t = getIndexList( len(filenameList_t) )
indexList_m = getIndexList( len(filenameList_m) )

# get list of random filenames
testing_name_list = []
for i in indexList_e :
  testing_name_list.append(filenameList_e[i])
for i in indexList_t :
  testing_name_list.append(filenameList_t[i])
for i in indexList_m :
  testing_name_list.append(filenameList_m[i])

# copy the files into the testing directory
for t in testing_name_list :
  dirname = "ficwad_" + t[:-4]
  print "Making dir : " + dirname

  fullpath = TESTING_DIR + dirname

  os.system( 'mkdir ' + fullpath )
  print "Copying file:" + t
  os.system( "cp " + DATA_PATH + t + " " + fullpath )
