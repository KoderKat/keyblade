import os, sys
import sqlite3
from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#####################
#    DATA MACROS    #
#####################
DATA_DIR = '/Users/KsComp/projects/keyblade/data/'
NAME_DB = 'keyblade_fanfics.db'

#################################################################### 
def main(): 
  app = QtGui.QApplication(sys.argv) 
  w = Window() 
  w.show() 
  sys.exit(app.exec_()) 

#################################################################### 
class Window(QtGui.QWidget): 
  def __init__(self): 
    super(Window, self).__init__()
    self.setGeometry(0,0,1000,600)
    self.setWindowTitle("KeyBlade: A Fanfiction Knowledge Base")
    self.setWindowIcon(QtGui.QIcon(os.getcwd() + '/keyblade_logo_small.png'))

    # set background color
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background,QtCore.Qt.white)
    self.setPalette(palette)

    self.logo = self.getLogo()          # get logo
    self.txtBuff = self.getMessageBox("        ", 40)  # text buffer for formatting header
    self.mbox0 = self.getMessageBox("<b>Welcome to KeyBlade!</b>", 40)  # get msg box 0
    self.mbox1 = self.getMessageBox("<b>Use the form below to query information from the knowledge base:</b>", 15)  # get msg box 1
    self.mbox2 = self.getMessageBox("<b>Or, input a custom SQL query:</b>", 15)  # get msg box 2
    self.mbox3 = self.getMessageBox('*Get schema: SELECT sql FROM sqlite_master WHERE name="keyblade_fanfics_complete" <br> *Get list of tables: SELECT name FROM sqlite_master WHERE type="table"', 12)  # get msg box 3

    # make text selectable
    self.mbox3.setTextInteractionFlags(Qt.TextSelectableByMouse)

    # ------------------------------- #
    #          FORM LAYOUT            #
    # ------------------------------- #
    # Create the form layout that manages the labeled controls
    self.form_layout = QtGui.QFormLayout()
    self.siteBox = self.getFormBox(self.getOptions("site")) # define site box
    self.genreBox = self.getFormBox(self.getOptions("genre")) # define site box
    self.fandomBox = self.getFormBox(self.getOptions("fandom")) # define site box

    self.form_layout.addRow('site: ', self.siteBox)
    self.form_layout.addRow('genre: ', self.genreBox)
    self.form_layout.addRow('fandom: ', self.fandomBox)

    # get form boxes
    dictFormBoxes = {}
    # initialize form boxes
    dictFormBoxes['siteBox']   = ""
    dictFormBoxes['genreBox']  = ""
    dictFormBoxes['fandomBox'] = ""
    # populate form boxes
    dictFormBoxes['siteBox']   = self.siteBox
    dictFormBoxes['genreBox']  = self.genreBox
    dictFormBoxes['fandomBox'] = self.fandomBox

    self.sbtn1 = self.getSearchButton(dictFormBoxes) # get search button
    # ------------------------------- #
    # ------------------------------- #

    # ------------------------------- #
    #       CUSTOM QUERY LAYOUT       #
    # ------------------------------- #
    self.cq = QtGui.QFormLayout()
    self.f1 = QtGui.QLineEdit(self)
    self.f1.returnPressed.connect( lambda: self.searchAction_custom() )
    self.f1.move(0,0)
    self.f1.setFixedWidth(400)
    self.cq.addRow("QUERY: ", self.f1)
    self.sbtn2 = self.getCustomSearchButton() # get search button
    self.qbtn2 = self.getQuitButton()         # get quit button
    # ------------------------------- #
    # ------------------------------- #

    # create table
    list_data = self.getData()
    self.lm = MyListModel(list_data, self)
    self.lv = QListView()
    self.lv.setModel(self.lm)

    # data display list
    self.queryResults = QListView()

    #self.mylistView = QtGui.QListView()
    #self.model = QtGui.QStandardItemModel(self.mylistView)
    #for l in list_data :
    #  # create an item with a caption
    #  item = QtGui.QStandardItem(l)
    #  # Add the item to the model
    #  self.model.appendRow(item)
    # Apply the model to the list view
    #self.mylistView.setModel(self.model)

    # output message for query execution status
    self.outmsg = QtGui.QLabel()
    self.outmsg.setTextInteractionFlags(Qt.TextSelectableByMouse)

    # ------------------------------- #
    #             LAYOUT              #
    # ------------------------------- #
    layout = QtGui.QVBoxLayout()
    top = QtGui.QHBoxLayout()
    top.addWidget(self.logo)                       # logo
    top.addWidget(self.txtBuff)
    top.addWidget(self.mbox0, 100, Qt.AlignLeft)
    layout.addLayout(top)
    layout.addWidget(self.mbox1)
    splitPane = QtGui.QHBoxLayout()
    self.lhs = QtGui.QVBoxLayout()
    self.rhs = QtGui.QVBoxLayout()
    # LHS form layout:
    self.lhs.addLayout(self.form_layout)                   # form
    self.lhs.addWidget(self.sbtn1, 0, Qt.AlignHCenter)     # search button
    # LHS custom query layout
    self.lhs.addWidget(self.mbox2)
    self.lhs.addLayout(self.cq)                            # form
    self.lhs.addWidget(self.sbtn2, 0, Qt.AlignHCenter)     # search button
    self.lhs.addWidget(self.qbtn2, 0, Qt.AlignHCenter)     # quit button
    self.lhs.addWidget(self.mbox3)
    # RHS display results
    #self.rhs.addWidget(self.lv)                                 # results view
    self.rhs.addWidget(self.queryResults)
    # combine layouts
    splitPane.addLayout(self.lhs)
    splitPane.addLayout(self.rhs)
    layout.addLayout(splitPane)
    self.setLayout(layout)

  # ------------------------------- #
  #            METHODS              #
  # ------------------------------- #
  ##################
  ##    getData   ##
  ##################
  def getData(self) :
    data_list = []
    for i in range(0, 1000) :
      data_list.append(i)
    return data_list

  #####################
  ##    getOptions   ##
  #####################
  def getOptions( self, fieldType ) :
    optionsList = []
    if fieldType == "site" :
      optionsList = ['ALL','ao3', 'deviantart', 'ficwad']
    elif fieldType == "genre" :
      optionsList = self.getGenres()
      #optionsList = ['ALL', 'scifi', 'action', 'horror']
    elif fieldType == "fandom" :
      optionsList = self.getFandoms()
      #optionsList = ['ALL', 'Avatar', 'StarTrek', 'StarWars']
    return optionsList

  ####################
  ##    getGenres   ##
  ####################
  def getGenres(self) :
    genreList = []
    #self.connection = sqlite3.connect( './keyblade_fanfics.db' )
    self.connection = sqlite3.connect( DATA_DIR + NAME_DB )
    self.cursor = self.connection.cursor()

    # ao3 genres
    self.cursor.execute( 'SELECT genre from ao3 ;' )
    ao3_genres = self.cursor.fetchall()

    # deviantart genres
    self.cursor.execute( 'SELECT genre from deviantart ;' )
    deviantart_genres = self.cursor.fetchall()

    # ficwad genres
    self.cursor.execute( 'SELECT genre from ficwad ;' )
    ficwad_genres = self.cursor.fetchall()

    genreList.extend(ao3_genres)
    genreList.extend(deviantart_genres)
    genreList.extend(ficwad_genres)

    cleanGenreList = []
    cleanGenreList.append('ALL') # include the default ALL option
    # genreList is of the form [(u'action',), (u'adventure',)]
    # clean genreList
    for tup in genreList :
      g = tup[0]
      g = g.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      cleanGenreList.append(g) 

    # remove duplicates
    unique = []
    [unique.append(item) for item in cleanGenreList if item not in unique]
    cleanGenreList = unique

    #print "genreList = " + str(genreList)
    #print "cleanGenreList = " + str(cleanGenreList)
    return cleanGenreList

  #####################
  ##    getFandoms   ##
  #####################
  def getFandoms(self) :
    fandomList = []
    #self.connection = sqlite3.connect( './keyblade_fanfics.db' )
    self.connection = sqlite3.connect( DATA_DIR + NAME_DB )
    self.cursor = self.connection.cursor()

    # ao3 fandoms
    self.cursor.execute( 'SELECT fandom from ao3 ;' )
    ao3_fandoms = self.cursor.fetchall()

    # deviantart fandoms
    self.cursor.execute( 'SELECT fandom from deviantart ;' )
    deviantart_fandoms = self.cursor.fetchall()

    # ficwad fandoms
    self.cursor.execute( 'SELECT fandom from ficwad ;' )
    ficwad_fandoms = self.cursor.fetchall()

    fandomList.extend(ao3_fandoms)
    fandomList.extend(deviantart_fandoms)
    fandomList.extend(ficwad_fandoms)

    cleanFandomList = []
    cleanFandomList.append('ALL') # include the default ALL option
    # genreList is of the form [(u'action',), (u'adventure',)]
    # clean genreList
    for tup in fandomList :
      g = tup[0]
      g = g.encode('ascii', 'ignore').decode('ascii').encode('ascii', 'ignore')
      cleanFandomList.append(g) 

    # remove duplicates
    unique = []
    [unique.append(item) for item in cleanFandomList if item not in unique]
    cleanFandomList = unique

    #print "fandomList = " + str(fandomList)
    #print "cleanFandomList = " + str(cleanFandomList)
    return cleanFandomList

  #####################
  ##    getFormBox   ##
  #####################
  def getFormBox(self, listOfOptions) :
    # Create and fill the combo box to choose the salutation
    siteBox = QtGui.QComboBox(self)
    siteBox.addItems(listOfOptions)
    siteBox.setFixedWidth(310)
    return siteBox

  ##################
  ##    getLogo   ##
  ##################
  def getLogo(self) :
    logo = QtGui.QLabel(self)
    logo.setPixmap(QPixmap(os.getcwd() + "/keyblade_logo_small.png"))
    return logo

  ########################
  ##    getMessageBox   ##
  ########################
  def getMessageBox(self, msg, fontsize) :
    box = QtGui.QLabel(self)
    box.setText(msg)
    box.setStyleSheet("font-size: " + str(fontsize) + "px; font-family: Arial;")
    return box

  ##########################
  ##    getSearchButton   ##
  ##########################
  def getSearchButton(self, dictFormBoxes) :
    sbtn = QtGui.QPushButton("Search!", self)
    sbtn.clicked.connect( lambda: self.searchAction(dictFormBoxes) )
    sbtn.setFixedHeight(50)
    sbtn.setFixedWidth(210)
    return sbtn

  ################################
  ##    getCustomSearchButton   ##
  ################################
  def getCustomSearchButton(self) :
    sbtn = QtGui.QPushButton("Custom Search!", self)
    sbtn.setAutoDefault(True)
    sbtn.clicked.connect( lambda: self.searchAction_custom() )
    sbtn.setFixedHeight(50)
    sbtn.setFixedWidth(210)
    return sbtn

  #######################
  ##    searchAction   ##
  #######################
  def searchAction(self, dictFormBoxes) :
    # get current options in form boxes
    dictCurrOpts = {}
    for k in dictFormBoxes :
      dictCurrOpts[k] = str( dictFormBoxes[k].currentText() )
    #print "dictCurrOpts = " + str( dictCurrOpts )
    query = self.getQuery( dictCurrOpts )
    #print "query = " + query

    results = []
    results = self.getResults( query )
    self.cleanresults = []
    if not results == [] :
      for i in range(0,len(results)) :
        row = ''
        for j in range(0, len(results[i])) :  # results[i] is a tuple
          t = results[i]
          elem = t[j]
          row += str(elem) + ","
        row = row[:-1]
        #print "row = " + row
        self.cleanresults.append(row)

    #print "results = " + str(results)
    #print "clean results = " + str(self.cleanresults)

    # display results
    self.rhs.removeWidget(self.queryResults) # clears previous results display
    self.queryResultsModel = MyListModel(self.cleanresults, self)
    self.queryResults.setModel(self.queryResultsModel)
    self.rhs.addWidget(self.queryResults)

  #####################
  ##    getResults   ##
  #####################
  def getResults( self, query ) : # string input
    #print "In getResults ..."
    query = str(query)
    query = query.replace("\'", "\"")
    query = query.replace(";", "")
    query = str(query)
    print "query = " + query
    results = []
    self.connection = sqlite3.connect(DATA_DIR + NAME_DB)
    self.cursor = self.connection.cursor()
    try :
      #self.cursor.execute( 'SELECT name FROM sqlite_master WHERE type="table" ;' )
      #self.cursor.execute( 'SELECT sql FROM sqlite_master WHERE name="ao3" ;' )
      self.cursor.execute( query )
      #self.cursor.execute( 'SELECT * from keyblade_fanfics_complete ;' )
      results = self.cursor.fetchall()
      self.outmsg.setText( query )
    except :
      self.outmsg.setText( "ERROR: Invalid query -- see terminal error.")      
    # post message
    self.lhs.addWidget( self.outmsg )
    #print "results = " + str(results)
    return results

  ###################
  ##    getQuery   ##
  ###################
  def getQuery(self, dictCurrOpts) :
    query = ''
    SELECT = 'SELECT *'
    FROM = 'FROM keyblade_fanfics_complete'
    WHERE = ''

    site   = dictCurrOpts['siteBox']
    genre  = dictCurrOpts['genreBox']
    fandom = dictCurrOpts['fandomBox']

    # site
    if not (site== "") :
      if not (site == "ALL") :
        if WHERE == "" :
          WHERE += "WHERE "
        else :
          WHERE += " and "
        WHERE += 'site = "' + site + '"'
      else :
        WHERE += ''

    # genre
    if not (genre == "") :
      if not (genre == "ALL") :
        if WHERE == "" :
          WHERE += "WHERE "
        else :
          WHERE += " and "
        WHERE += 'genre = "' + genre + '"'

    # fandom
    if not (fandom == "") :
      if not (fandom == "ALL") :
        if WHERE == "" :
          WHERE += "WHERE "
        else :
          WHERE += " and "
        WHERE += 'fandom = "' + fandom + '"'

    # generate query
    if WHERE == "" :
      query = SELECT + ' ' + FROM
    else :
      query = SELECT + ' ' + FROM + ' ' + WHERE

    return query + ";"

  ##############################
  ##    searchAction_custom   ##
  ##############################
  def searchAction_custom(self) :
    results = []
    cleanresults = []
    inputQuery = self.f1.text() + ";" # assume user forgot the semicolon
    print "inputQuery = " + inputQuery
    results = self.getResults( inputQuery )
    if not results == [] :
      for i in range(0,len(results)) :
        row = ''
        for j in range(0, len(results[i])) :  # results[i] is a tuple
          t = results[i]
          elem = t[j]
          row += str(elem) + ","
        row = row[:-1]
        #print "row = " + row
        cleanresults.append(row)

    self.queryResultsModel = MyListModel(cleanresults, self)
    self.queryResults.setModel(self.queryResultsModel)
    self.rhs.addWidget(self.queryResults)

  ########################
  ##    getQuitButton   ##
  ########################
  def getQuitButton(self) :
    qbtn = QtGui.QPushButton("Quit", self)
    qbtn.clicked.connect( self.close_application )
    qbtn.setFixedHeight(40)
    qbtn.setFixedWidth(210)
    return qbtn

  ############################
  ##    close_application   ##
  ############################
  def close_application(self) :
    print("Custom message")
    choice = QtGui.QMessageBox.question(self, "KeyBlade", "Quit KeyBlade?",
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    if choice == QtGui.QMessageBox.Yes :
      print("Exiting Now")
      sys.exit()
    else :
      pass

#################################################################### 
# from http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
class MyListModel(QAbstractListModel):
  def __init__(self, datain, parent=None, *args):
    """ datain: a list where each item is a row
    """
    QAbstractListModel.__init__(self, parent, *args)
    self.listdata = datain

  def rowCount(self, parent=QModelIndex()):
    return len(self.listdata)

  def data(self, index, role):
    if index.isValid() and role == Qt.DisplayRole:
      return QVariant(self.listdata[index.row()])
    else:
      return QVariant()

####################################################################
if __name__ == "__main__": 
  main()
