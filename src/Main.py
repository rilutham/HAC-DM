#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Customer Segmentation System
--- Undergraduate Thesis Project ---

Riky Lutfi Hamzah
Informatics Engineering
Indonesia Computer University
"""

import sys
from PyQt4 import QtGui
from MainWindow import MainWindow
from StartupDialog import StartupDialog

def main():
    '''
    Call StartupDialog object
    '''
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    strdialog = StartupDialog()
    strdialog.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

