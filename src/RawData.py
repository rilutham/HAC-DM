#!/usr/bin/python
# -*- coding: utf-8 -*-

"""a"""

from PyQt4 import QtGui, QtCore
from QtGui import QDialogButtonBox
import pandas as pd

class RawData(QtGui.QDialog):
    '''
    Showing dialog for select data attribute
    '''
    
    def __init__(self):
        '''
        Display QDialog with QListWidget and QDialogbutton_box
        '''
        super(RawData, self).__init__()
        self.setWindowTitle('Impor data pelanggan')
        # Qdialog's size and center it on screen.
        self.resize(300, 400)
        size = self.frameSize()
        desktop_size = QtGui.QDesktopWidget().screenGeometry()
        left = (desktop_size.width()/2)-(size.width()/2)
        top = (desktop_size.height()/2)-(size.height()/2)
        self.move(left, top)
        # Qlabel for instruction.
        txt_select = QtGui.QLabel('Silahkan pilih atribut yang akan digunakan!', self)
        # ListWidget for display data column
        self.v_list = QtGui.QListWidget()
        self.v_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.v_list.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        # button_box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.get_selected_column)
        button_box.rejected.connect(self.close_dialog)
        # Displaying the widget
        self.layout_vertical = QtGui.QVBoxLayout(self)
        self.layout_vertical.addWidget(txt_select)
        self.layout_vertical.addWidget(self.v_list)
        self.layout_vertical.addWidget(button_box)
        # list of selected column
        self.selected_col = []
        self.selected_data = None
        self.df_selected_data = None
        self.display_table = None
        # Call initial method.
        self.get_file()
        self.add_attribute_to_list()
    
    def get_file(self):
        '''
        Provides a dialog that allow users to select only *.csv file.
        '''
        self.file = QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.csv)")
        # Read the *csv file
        self.raw_data = pd.read_csv(str(self.file), header=0, index_col=False, nrows=1)
    
    def add_attribute_to_list(self):
        '''
        Add all data attribute to QListWidget
        '''
        self.cols = []
        for i in list(self.raw_data.columns):
            self.cols.append(i)
        # Add checkbox to each of attribute
        for col in self.cols:
            self.item = QtGui.QListWidgetItem(col)
            self.v_list.addItem(self.item)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.item.setCheckState(QtCore.Qt.Unchecked)
    
    def get_selected_column(self):
        '''
        a
        '''
        # list of selected column
        #self.selected_col = []
        # add checked item to selected columns list
        for index in xrange(self.v_list.count()):
            check_box = self.v_list.item(index)
            state = check_box.checkState()
            # state = 2 (Checked)
            if state == 2:
                self.selected_col.append(str(self.v_list.item(index).text()))
        self.import_selected_data()
    
    def import_selected_data(self):
        '''
        Import data with the selected column
        '''
        self.selected_data = pd.read_csv(str(self.file), header=0, index_col=False, \
                                          usecols=self.selected_col)
        # Insert data to DataFrame
        self.df_selected_data = pd.DataFrame(self.selected_data)
        # State of displaying data on ApplicationWindow
        self.display_table = True
        # Signal
        self.accept()
    
    def close_dialog(self):
        '''
        d
        '''
        # State of displaying data on ApplicationWindow
        self.display_table = False
        # Signal
        self.reject()
        