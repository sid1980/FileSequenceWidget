from PySide import QtCore, QtGui
import os 


class dialogSequence(QtGui.QDialog):
    
    def __init__(self, head, tail,padding):
        super(dialogSequence, self).__init__()
        self.initUI(head, tail, padding)
        
    def initUI(self, head, tail, padding):      
 
        self.le = QtGui.QLineEdit(self)
        self.le.setText(head)
        self.padding = QtGui.QSpinBox()
        self.padding.setValue(padding)
        self.extension = QtGui.QLineEdit(self)
        self.extension.setText(tail) 
        #self.usepadding = QtGui.QCheckBox(self)

        formLayout = QtGui.QFormLayout()
        formLayout.addRow(self.tr(" Enter the new head name:"), self.le)
        #formLayout.addRow(self.tr("Use Padding :"), self.usepadding)
        formLayout.addRow(self.tr("Padding:"), self.padding)
        formLayout.addRow(self.tr("Extension:"), self.extension)
        
        self._buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel )

        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)
        
        formLayout.addWidget(self._buttonBox)

        # Set dialog layout
        self.setLayout(formLayout)

        self.setWindowTitle('Rename sequence')
    
    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getRenameSequence(head, tail,padding):
        dialog = dialogSequence(head, tail, padding)
        result = dialog.exec_()
        head = dialog.le.text()
        extension = dialog.extension.text()
        padding = dialog.padding.value()
        #usepadding = dialog.usepadding.checkState()

        return (head,extension,padding, result == QtGui.QDialog.Accepted) 



class Plugin():
    """
    plugin to rename file(s).
    """
    def getLabel(self):
        return "Rename"

    def acceptSequence(self):
        return True

    def acceptOnlySequence(self):
        pass

    def execute(self , filenames, widget):
        '''
            @param filenames: filename ( only  one todo make for array )
            @param widget : the FileSequenceWidget widget

        '''
        head, tail = os.path.split(filenames)
        dirname = os.path.dirname(filenames)
        # Sequence
        if widget.isSequence(tail):
            seq= widget.getSequenseObj(tail)
            headseq = seq.head
            endseq = seq.tail
            begin = seq.first
            end = seq.last
            oldpadding = seq.padding 
            text,extension,padding,  ok =  dialogSequence.getRenameSequence(headseq,endseq, oldpadding) 
            if ok:
                for index in range( int(begin) , int (end) + 1 ):
                    indexstrsrc = str(index).rjust(oldpadding,'0')
                    indexstrdest = str(index).rjust(padding,'0')

                    src  =  os.path.join( dirname , "%s%s%s" % ( headseq, indexstrsrc, endseq) ) 
                    dest =  os.path.join( dirname , "%s%s%s" %  ( text, indexstrdest, extension) ) 
                    os.rename( src,dest)
                    widget.refresh() 
        else:
            text, ok = QtGui.QInputDialog.getText(widget, 'Input Dialog', 'Enter your name:',QtGui.QLineEdit.Normal,tail)
            if ok:
                os.rename( filenames,os.path.join(dirname, text))
                widget.refresh() 
