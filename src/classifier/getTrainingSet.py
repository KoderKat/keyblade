import random
import os, sys

from os import listdir
from os.path import isfile, join

# Grab data collected from ficwad as a training set for the classifier.
# 32 training documents per rating category: e, t, m
# make sure training_data is empty before running. The script will not remove existing files.
# run as: $ python getTrainingSet.py

# Replace the following macros with absolute paths to ficwad-spider-v1/data/ and nltk_test1/training_data/, respectively:
DATA_PATH = "."
TRAINING_DIR = "."

def getIndexList( num ) :
  # because 32 is statistically significant
  indexList = random.sample(range(0, num), 32)
  
  # remove duplicates
  unique = []
  [unique.append(item) for item in indexList if item not in unique]
  indexList = unique
  
  if len(indexList) == 32 :
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
for f in listdir(DATA_PATH) :
  if isfile(join(DATA_PATH, f)) :
    if ".txt" in f :
      if not "_info.txt" in f :
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
training_name_list = []
for i in indexList_e :
  training_name_list.append(filenameList_e[i])
for i in indexList_t :
  training_name_list.append(filenameList_t[i])
for i in indexList_m :
  training_name_list.append(filenameList_m[i])

# copy the files into the training directory
for t in training_name_list :
  print "Copying file:" + t
  os.system( "cp " + DATA_PATH + t + " " + TRAINING_DIR )
