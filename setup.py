# setup.py
import fileinput
import os
import sys

# from http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
def replaceAll(file,searchExp,replaceExp):
  for line in fileinput.input(file, inplace=1):
    if searchExp in line:
      line = line.replace(searchExp,replaceExp)
    sys.stdout.write(line)

# get current working directory
currdir = os.getcwd()

# get data directory paths
AO3_DATA = currdir + "/src/ao3-spider/data/"
DEVIANTART_DATA = currdir + "/src/deviantart-spider/data/"
FICWAD_DATA = currdir + "/src/ficwad-spider-v1/data/"

print currdir
print AO3_DATA
print DEVIANTART_DATA
print FICWAD_DATA

# get filelist
filelist = []
AO3_PIPE = currdir + "/src/ao3-spider/ao3-spider/ao3/ao3/pipelines.py"
DEVIANTART_PIPE = currdir + "/src/deviantart-spider/deviant/deviant/pipelines.py"
FICWAD_PIPE = currdir + "/src/ficwad-spider/ficwad1/ficwad1/pipelines.py"

AO3_SPIDER = currdir + "/src/ao3-spider/ao3-spider/ao3/ao3/spiders/spider.py"
DEVIANTART_SPIDER = currdir + "/src/deviantart-spider/deviant/deviant/spiders/spider.py"
FICWAD_SPIDER = currdir + "/src/ficwad-spider/ficwad1/ficwad1/spidersi/spider.py"

filelist.append(AO3_PIPE)
filelist.append(DEVIANTART_PIPE)
filelist.append(FICWAD_PIPE)
filelist.append(AO3_PIPE)
filelist.append(DEVIANTART_PIPE)
filelist.append(FICWAD_PIPE)

# replace BASE_DIR and BASE_DATA_DIR strings
print filelist
for f in filelist :

  if "ao3" in f and ("BASE_DIR" or "BASE_DATA_DIR" in line) :
    replaceAll(f, 'BASE_DIR = "."', 'BASE_DIR = "' + AO3_DATA + '"')
    replaceAll(f, 'BASE_DATA_DIR = "."', 'BASE_DAT_DIR = "' + AO3_DATA + '"')
  elif "deviant" in f and ("BASE_DIR" or "BASE_DATA_DIR" in line) :
    replaceAll(f, 'BASE_DIR = "."', 'BASE_DIR = "' + DEVIANTART_DATA + '"')
    replaceAll(f, 'BASE_DATA_DIR = "."', 'BASE_DATA_DIR = "' + DEVIANTART_DATA + '"')
  elif "ficwad" in f and ("BASE_DIR" or "BASE_DATA_DIR" in line) :
    replaceAll(f, 'BASE_DIR = "."', 'BASE_DIR = "' + FICWAD_DATA + '"')
    replaceAll(f, 'BASE_DATA_DIR = "."', 'BASE_DATA_DIR = "' + FICWAD_DATA + '"')

#EOF
