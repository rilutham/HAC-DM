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
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | \
                QtGui.QDialogButtonBox.Cancel)
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
        self.selected_col = None
        for i in self.v_list.selectedItems():
            self.selected_col = str(i.text())
        # Check missing value
        if self.data[self.selected_col].isnull().values.ravel().sum() > 0:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Masih terdapat data kosong pada atribut!")
            msgBox.setInformativeText("Silahkan hapus data kosong!")
            msgBox.setIcon(2)
            msgBox.exec_()
        # Number of bin from user input
        self.n_bin = int(self.n_bin_edit.text())
        # Do binning
        bins = []
        if self.n_bin == 2:
            bins = [0, min(self.data[self.selected_col]), max(self.data[self.selected_col])]
            group_names = ['1', '2']
        elif self.n_bin == 3:
            bins = [0, min(self.data[self.selected_col]), 2, max(self.data[self.selected_col])]
            group_names = ['1', '2', '3']
        elif self.n_bin < 2 or self.n_bin > 3:
            msg_box = QtGui.QMessageBox(self)
            msg_box.setText("Jumlah bin tidak diizinkan.")
            msg_box.setInformativeText("Silahkan masukkan jumlah bin yang sesuai!")
            msg_box.setIcon(2)
            msg_box.exec_()

        # Add new value to attribute
        if bins:
            self.data[self.selected_col] = pd.cut(self.data[self.selected_col], \
                    bins, labels=group_names)
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

class DeriveAttribute(QtGui.QDialog):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(DeriveAttribute, self).__init__()
        self.setWindowTitle('Menurunkan atribut')
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
        # button_box
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | \
                QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.get_selected_column)
        button_box.rejected.connect(self.close_dialog)
        # Displaying the widget
        self.layout_vertical = QtGui.QVBoxLayout(self)
        self.layout_vertical.addWidget(txt_select)
        self.layout_vertical.addWidget(self.v_list)
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
        # Check missing value
        if self.data[self.selected_col].isnull().values.ravel().sum() > 0:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Masih terdapat data kosong pada atribut!")
            msgBox.setInformativeText("Silahkan hapus data kosong!")
            msgBox.setIcon(2)
            msgBox.exec_()
        # Count number of possible value for each column
        unique_value = self.data.groupby(self.selected_col).count()
        unique_value_len = len(unique_value.index)

        # Create list for new atribut
        val_list = []
        for x in range(0, unique_value_len):
            for y in range(0, len(self.data[self.selected_col].index)):
                if x == 0:
                    if self.data[self.selected_col][y] == '1':
                        val_list.append(1)
                    else:
                        val_list.append(0)
                elif x == 1:
                    if self.data[self.selected_col][y] == '2':
                        val_list.append(1)
                    else:
                        val_list.append(0)
                elif x == 2:
                    if self.data[self.selected_col][y] == '3':
                        val_list.append(1)
                    else:
                        val_list.append(0)
            name = "{0}_{1}".format(self.selected_col, x+1)
            self.data[name] = val_list
            val_list = []
        # Delete "super-column"
        self.data = self.data.drop(self.selected_col, 1)
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

