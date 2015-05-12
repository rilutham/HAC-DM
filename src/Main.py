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


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()