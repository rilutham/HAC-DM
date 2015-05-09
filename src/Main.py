#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Customer Segmentation using Hierarchical Agglomerative Clustering
--- Undergraduate Thesis Project ---

Riky Lutfi Hamzah
Informatics Engineering 
Indonesia Computer University
"""

import sys
from PyQt4 import QtGui
from ApplicationWindow import ApplicationWindow


def main():
    app = QtGui.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()