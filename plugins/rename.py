from PySide import QtCore, QtGui
import os 


class Plugin():
"""
    plugin to rename file(s).
"""
    def getLabel(self):
        return "Rename"

    def execute(self , filenames, widget):
        '''
            @param filenames: filename ( only  one todo make for array )
            @param widget : the FileSequenceWidget widget

        '''
        head, tail = os.path.split(filenames)
        dirname = os.path.dirname(filenames)
        # Sequence 
        if len( tail.split("[") ) > 1:
            headseq , middleseq = tail.split("[")
            number , endseq =  middleseq.split("]")
            begin , end = number.split("-")
            text, ok = QtGui.QInputDialog.getText(widget, 'Input Dialog', 'Enter your name:',QtGui.QLineEdit.Normal,headseq)
            if ok:
                for index in range( int(begin) , int (end) + 1 ):
                    src  =  os.path.join( dirname , "%s%d%s" % ( headseq, index, endseq) ) 
                    dest =  os.path.join( dirname , "%s%d%s" % ( text, index, endseq) ) 
                    os.rename( src,dest)
                    widget.refresh() 
        else:
            text, ok = QtGui.QInputDialog.getText(widget, 'Input Dialog', 'Enter your name:',QtGui.QLineEdit.Normal,tail)
            if ok:
                os.rename( filenames,os.path.join(dirname, text))
                widget.refresh() 
