#!/usr/bin/python
# -*- coding: utf-8 -*-
"""About.py 
@author: rilutham
"""

import os
from PyQt4 import QtGui
from About import About

class StartupDialog(QtGui.QDialog):
    """
    Display application information
    """
    def __init__(self):
        super(StartupDialog, self).__init__()
        self.setWindowTitle('Selamat Datang di Sistem Segmentasi Pelanggan')
        self.resize(375, 375)
        
        # Logo
        pic = QtGui.QLabel(self)
        pic.setGeometry(0, 0, 363, 140)
        pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/icons/logo2.jpg"))
        
        # Button
        self.btn_help = QtGui.QPushButton("Halaman Bantuan", self)
        self.btn_help.clicked.connect(self.show_help)
        self.btn_pass_to_app = QtGui.QPushButton("Ke Aplikasi >>", self)
        self.btn_pass_to_app.clicked.connect(self.pass_to_app)
        
        # Display Button
        self.btn_frame = QtGui.QFrame()
        self.horiz_layout = QtGui.QHBoxLayout(self)
        self.btn_frame.setLayout(self.horiz_layout)
        self.horiz_layout.addWidget(self.btn_help)
        self.horiz_layout.addWidget(self.btn_pass_to_app)
        # Displaying the widget
        self.layout_vertical = QtGui.QVBoxLayout(self)
        self.layout_vertical.addWidget(pic)
        self.layout_vertical.addWidget(self.btn_frame)
    
    def show_help(self):
        self.reject()
        abt = About()
        abt.exec_()
        
    def pass_to_app(self):
        self.reject()
    