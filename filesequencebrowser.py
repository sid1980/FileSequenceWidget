#!/usr/bin/python

#
# FileSequenceWidget, FilesequenceDialog.
# charles vidal charles.vidal@gmail.com 
# 
from PySide import QtCore, QtGui
import os 
import pyseq as seq  


""""
  ListWidget to catch event Enter or arrow right , or backspace and arrow left.
"""
class ListWidget(QtGui.QListWidget):

	itemSelected = QtCore.Signal()
	gotoparent = QtCore.Signal()
	
	def keyPressEvent(self, e):
		if ( e.key() == QtCore.Qt.Key_Return or 
           e.key() == QtCore.Qt.Key_Enter  or		
           e.key() == QtCore.Qt.Key_Right) : 
			self.itemSelected.emit()
			return
				
		if ( e.key() == QtCore.Qt.Key_Backspace or 
		     e.key() == QtCore.Qt.Key_Left) :
			self.gotoparent.emit()
			return 
			
		return QtGui.QListWidget.keyPressEvent(self, e)

"""
  generic widget FileSequenceWidget
  display two list :
      one with directory 
      the orther with file or sequence file.

      you can navigate with enter on folder or arrow key.

      This widget emit a signal when you select a file or a sequence file.
"""
class FileSequenceWidget(QtGui.QWidget):
		 
    FOLDER = 0
    FILE = 1 
    SEQUENCE =2 

    fileSelected = QtCore.Signal(str)

    def getFilenameSelected( self ):
        itemSelected = self.listfile.currentIndex().data()
        return os.path.join( self.path , itemSelected )

    def selectdirectory(self):
        rows =  self.directorylist.selectionModel().selectedRows()
        itemSelected = rows[0].data()
        if  os.path.isdir(os.path.join( self.path , itemSelected)) :
			self.path = os.path.normpath( os.path.join( self.path , itemSelected) ) 
			self.pathEdit.setText( self.path )
        
	
    def selectfile(self, number):
		itemSelected = self.listfile.currentIndex().data()
		self.fileSelected.emit(os.path.join( self.path , itemSelected))

    """
      method testing if the filename is in filters
      @param filename : a filename 
      @param array of filter : .jpg, .png 
      @return boolean  
    """
    def isInFilter(self, filename, filters):
        for filter in filters:
            if filename.lower().endswith(filter.lower()):
                return True
        
        return False

    """
       @return array of filter [ .jpg , .png ]
    """
    def getFilters(self):
        strfilters = self.filtercombo.currentText()
        filters = strfilters.split(";")
        return filters

    """
      add item to the list of 
           folder list if type is FOLDER 
           file in the list view  if type is FILE or SEQUENCE
    """
    def addItem(self, fn,typefile ):
    	item = QtGui.QListWidgetItem()
        item.setText(fn)
        item.setIcon(self.icons[typefile])
        if typefile == FileSequenceWidget.FOLDER:
        	self.directorylist.addItem(item)
        else: 
            extensionfilters = self.getFilters()
            if len(extensionfilters)==0: 
                self.listfile.addItem(item)
            else:
                if self.isInFilter(fn , extensionfilters):
                    self.listfile.addItem(item)
					
	"""
    Slot to go to the directory parent.
    """
    def goToParent( self ):
        self.path = os.path.normpath( os.path.join( self.path , "..") ) 
        self.pathEdit.setText( self.path )
	
    def initInternalVar(self ):
        self._splitSequence = False
        self.iconFile = QtGui.QIcon("icons\\file.png")
        self.iconFolder = QtGui.QIcon("icons\\folder.png")
        self.iconSequence = QtGui.QIcon("icons\\sequence.png")
        self.icons = {} 
        self.icons[FileSequenceWidget.FOLDER] = self.iconFolder
        self.icons[FileSequenceWidget.FILE] = self.iconFile
        self.icons[FileSequenceWidget.SEQUENCE] = self.iconSequence
        
    def __init__(self, path, parent=None):
        super(FileSequenceWidget, self).__init__(parent)
        self.path = path
        self.initInternalVar()
        label = QtGui.QLabel("Directory")
        pathEdit = QtGui.QLineEdit()
        label.setBuddy(pathEdit)
		
        self.listfile = ListWidget()
        self.directorylist = ListWidget()

        self.pathEdit = pathEdit		

        splitter = QtGui.QSplitter()
        splitter.addWidget(self.directorylist)
        splitter.addWidget(self.listfile)
        
        self.checkboxsplitseq = QtGui.QCheckBox('Split Seq',self) 
        
        if self._splitSequence == True:
            self.checkboxsplitseq.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkboxsplitseq.setCheckState(QtCore.Qt.Unchecked)
			
	    labelfilter = QtGui.QLabel("Filter:")
        self.filtercombo = QtGui.QComboBox()
        labelfilter.setBuddy(self.filtercombo)
		
        layout = QtGui.QGridLayout()
        layout.addWidget(label, 0, 1)
        layout.addWidget(pathEdit, 0, 2)
        layout.addWidget(splitter,1,0,1,3)
        layout.addWidget(self.checkboxsplitseq, 3, 0)
        layout.addWidget(labelfilter,3,1)
        layout.addWidget(self.filtercombo,3,2)

        #
        # Connect Slot ...
        #
        self.pathEdit.textChanged.connect(self.setCurrentDirPath)
        self.listfile.doubleClicked.connect(self.selectfile)
        self.listfile.itemSelected.connect(self.selectfile)
        self.listfile.gotoparent.connect(self.goToParent)
        self.directorylist.doubleClicked.connect(self.selectdirectory)
        self.directorylist.itemSelected.connect(self.selectdirectory)
        self.directorylist.gotoparent.connect(self.goToParent)

        self.checkboxsplitseq.clicked.connect(self.splitseqchanged)
        self.filtercombo.currentIndexChanged.connect(self.filterchanged)
        self.setLayout(layout)
        self.setWindowTitle("File Sequence browser")
        pathEdit.setText(self.path)
    
    """
       Change directory callback..
    """
    def setCurrentDirPath(self , path ):
        self.directorylist.clear()
        self.listfile.clear()
        directory = QtCore.QDir(path)
        files = list(directory.entryList(QtCore.QDir.AllDirs))
        for fn in files:
       	    if fn == ".":
        	    continue
            self.addItem(fn ,FileSequenceWidget.FOLDER)

        if self._splitSequence == False: 
		    sequences, others = seq.FileSequence.find(path)
		    for s in sequences:
				self.addItem(str(s), FileSequenceWidget.SEQUENCE)
				
		    for o in others:
				self.addItem(o , FileSequenceWidget.FILE)
        else:
            files = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
            for fn in files:
				self.addItem(fn ,FileSequenceWidget.FILE)
	
    """
    slot if the checkbox split seq change.
    """
    def splitseqchanged( self ):
        self._splitSequence = self.checkboxsplitseq.isChecked()
        self.setCurrentDirPath( self.path) 
	
    """
    slot if the commbox selection change
    """
    def filterchanged(self ):
	    self.setCurrentDirPath( self.path)
	
    """
      add a filter type:
        example : 
        self.addFilter(".jpg;.png;.bmp;.gif;.pic;.exr")
    """
    def addFilter(self, filter):
	    self.filtercombo.addItem(filter)
	
"""
Modal Dialog to select seauence file..
By default the path in the home users
Example
fsd = FileSequenceDialog(["",".jpg;.png;.bmp;.gif;.pic;.exr",".jpg",".png",".mov;.avi;.mp4;.mpg"]) # for windows
    if fsd.exec_() == QtGui.QDialog.Accepted:
        print fsd.getFilename()

""" 
class FileSequenceDialog(QtGui.QDialog):

    """
       constructor
       @param filters array of extension 
       @param the begin path for the dialog. by default QtCore.QDir.homePath() 
    """
    def __init__(self, filters, path = QtCore.QDir.homePath()):
        super(FileSequenceDialog, self).__init__()
        self.setWindowTitle('Select File Sequence...')
        self.widget = FileSequenceWidget(path)
        
        for f in filters:
             self.widget.addFilter(f)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.widget)
        self._buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)

        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)
		
        self.widget.fileSelected.connect(self.fileSelected)
        layout.addWidget(self._buttonBox)
        # Set dialog layout
        self.setLayout(layout)
        
    def fileSelected(self, fullpathname):
		self.accept()
	
    def getFilename(self):
		return self.widget.getFilenameSelected()
        
class MainWindow(QtGui.QMainWindow):
   
    def __init__(self):
    	super(MainWindow, self).__init__()
        

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
	
    fsd = FileSequenceDialog(["",".jpg;.png;.bmp;.gif;.pic;.exr",".jpg",".png",".mov;.avi;.mp4;.mpg"])
    if fsd.exec_() == QtGui.QDialog.Accepted:
        print fsd.getFilename()
	
    sys.exit(app.exec_())