# FileSequenceWidget
A File Manager Widget in PySide managing the sequence file ( FILE0001.jpg FILE 0002.jpg -> FILE[0001-0002].jpg )

![Dialog](screenshot1.png "Dialog with sequense display")
![Dialog](screenshot2.png "Dialog without sequence ")
![Dialog Filter](screenshot3.png "Dialog with filter")

Thank's to aldergren for https://github.com/aldergren/pyfileseq.

I do a patch NUMBER_PATTERN = re.compile("([0-9]{1,6})").

usage : 
python filesequensebrowser.py


todo: 
  split file for each python class
  make a file explorer with the file sequence , with copy , paste , cut , rename
  do drag and drop operation. 
