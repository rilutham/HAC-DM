'''
Created on May 14, 2015

@author: rilutham
'''
import pandas as pd
from PyQt4 import QtGui

class Bining(QtGui.QDialog):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Bining, self).__init__()
        self.setWindowTitle('Bining atribut')
        # Qdialog's size and center it on screen.
        self.resize(300, 300)
        size = self.frameSize()
        desktop_size = QtGui.QDesktopWidget().screenGeometry()
        left = (desktop_size.width()/2)-(size.width()/2)
        top = (desktop_size.height()/2)-(size.height()/2)
        self.move(left, top)
        
        # Qlabel for instruction.
        txt_select = QtGui.QLabel('Silahkan pilih atribut!', self)
        # ListWidget for display data column
        self.v_list = QtGui.QListWidget()
        txt_n_bin = QtGui.QLabel('Jumlah bin: ', self)
        self.n_bin_edit = QtGui.QLineEdit()
        self.bin_frame = QtGui.QFrame()
        self.bin_layout = QtGui.QHBoxLayout()
        self.bin_frame.setLayout(self.bin_layout)
        self.bin_layout.addWidget(txt_n_bin)
        self.bin_layout.addWidget(self.n_bin_edit)
        # button_box
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.get_selected_column)
        button_box.rejected.connect(self.close_dialog)
        # Displaying the widget
        self.layout_vertical = QtGui.QVBoxLayout(self)
        self.layout_vertical.addWidget(txt_select)
        self.layout_vertical.addWidget(self.v_list)
        self.layout_vertical.addWidget(self.bin_frame)
        self.layout_vertical.addWidget(button_box)
    
    def add_attribute_to_list(self, data):
        '''
        Add all data attribute to QListWidget
        '''
        self.data = data
        self.cols = [] 
        for i in list(self.data.columns):
            self.cols.append(i)
            
        # Add checkbox to each of attribute
        for col in self.cols:
            self.item = QtGui.QListWidgetItem(col)
            self.v_list.addItem(self.item)
    
    def get_selected_column(self):
        '''
        get selected column
        '''
        # selected column
        for i in self.v_list.selectedItems():
            self.selected_col = str(i.text())
        
        self.n_bin = str(self.n_bin_edit.text())
        if self.n_bin == '2':
            bins = [0, min(self.data[self.selected_col]), max(self.data[self.selected_col])]
            group_names = ['1','>=2']
        elif self.n_bin == '3':
            bins = [0, min(self.data[self.selected_col]), 2, max(self.data[self.selected_col])]
            group_names = ['1','2','>=3']
        self.data[self.selected_col] = pd.cut(self.data[self.selected_col], bins, labels=group_names)
        
        # State of displaying data on MainWindow
        self.display_table = True
        # Signal
        self.accept()
        
    def close_dialog(self):
        '''
        Close dialog
        '''
        # State of displaying data on MainWindow
        self.display_table = False
        # Signal
        self.reject()