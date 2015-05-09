'''
Created on May 9, 2015

@author: rilutham
'''

from PyQt4 import QtGui

class About(QtGui.QDialog):
    
    def __init__(self, parent):
        super(About, self).__init__(parent)
        self.setWindowTitle('Tentang Aplikasi')
        self.resize(350, 350)
        self.txt_about = QtGui.QLabel("""Customer Segmentation System
Version: 0.1
Build id: 2015-05-9

(c) Copyleft Riky Lutfi Hamzah.  All rights reserved.
Visit http://github.com/rilutham/HAC-DM

Developed by Riky Lutfi Hamzah 
http://rikylutfihamzah.com/""",self)
        self.scroll_reg = QtGui.QScrollArea()
 
        self.scroll_reg.setWidget(self.txt_about)
        
        # Displaying the widget
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.scroll_reg)