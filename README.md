# KeyBlade: A Fanfiction Knowledge Base

## Installation

The backend software for the KeyBlade knowledge base is written in Python. The scrapers depend on [scrapy](http://scrapy.org); the classifier (Auto-Rating Classifier) depends in [NLTK](http://www.nltk.org); and the GUI depends on [PyQT](https://riverbankcomputing.com/software/pyqt/intro).

To install KeyBlade, clone the repository and run setup.py from the top directory.

## Running scrapers

To run a particular scraper, cd into the top directory of the chosen scraper and run the command "scrapy crawl name_of_spider".
<br/> <br/>
Example:<br/>
  $ cd src/ao3-spider/ao3-spider/ao3/<br/>
  $ scrapy crawl ao3<br/>

## Running the Auto-Rating Classifier

Running the Auto-Rating Classifier requires populating the data directory for the Ficwad spider. After populating the directory, run the getTestingSet.py and getTrainingSet.py scripts to populate the testing_data and training_data directories, respectively.  Optionally, populate the dirtywords.txt file with a list of dirty words capable of throwing a work into the M rating category. Run the classifier.py script to create a ratings.db file in the src/classifier/data/ directory.
 

## Running the GUI

To run the GUI, cd into src/gui and run the command "python keyblade_gui.py". The interface should appear behind all currently opened applications (on a Mac).

