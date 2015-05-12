#!/usr/bin/python
# -*- coding: utf-8 -*-

"""MainWindow.py
@author: rilutham
"""

from PyQt4 import QtGui
from RawData import RawData
from Segmentation import Segmentation
from About import About
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__(parent)
        # Main window setting
        self.setGeometry(0, 0, 980, 768)
        self.setWindowTitle("Sistem Segmentasi Pelanggan")
        self.center_on_screen()
        # Menu action
        import_action = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'Impor data', self)
        import_action.setShortcut('Ctrl+i')
        import_action.setStatusTip('Impor data pelanggan')
        import_action.triggered.connect(self.show_import)
        
        exit_action = QtGui.QAction('Keluar', self)
        exit_action.setShortcut('Ctrl+q')
        exit_action.setStatusTip('Keluar dari aplikasi')
        exit_action.triggered.connect(self.close)
        
        clean_action = QtGui.QAction('Hapus nilai kosong', self)
        #clean_action.triggered.connect(self.clean_missing_value)
        
        self.seg_action = QtGui.QAction('Proses', self)
        self.seg_action.setShortcut('F5')
        self.seg_action.setStatusTip('Jalankan proses segmentasi')
        self.seg_action.setEnabled(False)
        self.seg_action.triggered.connect(self.segmen)
        
        self.save_result_action = QtGui.QAction(QtGui.QIcon('icons/save.png'),\
                                                'Simpan data hasil', self)
        self.save_result_action.setShortcut('Ctrl+Shift+S')
        self.save_result_action.setStatusTip('Simpan data hasil segmentasi')
        self.save_result_action.setEnabled(False)
        self.save_result_action.triggered.connect(self.save_result_data)
        
        about_action = QtGui.QAction('Tentang Aplikasi', self)
        about_action.triggered.connect(self.show_about)
        
        # Menubar setting
        menubar = self.menuBar()
        data_menu = menubar.addMenu('&Data')
        data_menu.addAction(import_action)
        data_menu.addAction(exit_action)
        preprocess_menu = menubar.addMenu('&Preprocessing')
        preprocess_menu.addAction(clean_action)
        segmen_menu = menubar.addMenu('&Segmentasi')
        segmen_menu.addAction(self.seg_action)
        result_menu = menubar.addMenu('&Hasil Segmentasi')
        result_menu.addAction(self.save_result_action)
        help_menu = menubar.addMenu('&Bantuan')
        help_menu.addAction(about_action)
        
        # Toolbar setting
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(import_action)
        toolbar.addAction(self.save_result_action)
        
        # Show statusbar
        self.statusBar()
        
        # Setting TabWidget
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()  
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()

        self.tabs.addTab(self.tab1, "Pengolahan Data")
        # Setting Tab 1
        self.raw_data_table = QtGui.QTableWidget(self) 
        self.v_box_layout_1 = QtGui.QVBoxLayout()
        self.v_box_layout_1.addWidget(self.raw_data_table)
        
        # Setting Tab 2
        self.figure = plt.figure()
        self.canvas_for_dendrogram = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas_for_dendrogram, self)
        # self.toolbar.hide() # For hide the matplotlib toolbar
        self.v_box_layout_2 = QtGui.QVBoxLayout()
        self.v_box_layout_2.addWidget(self.canvas_for_dendrogram)
        self.v_box_layout_2.addWidget(self.toolbar)
        
        # Setting Tab 3
        self.result_data_table = QtGui.QTableWidget(self) 
        self.v_box_layout_3 = QtGui.QVBoxLayout()
        self.v_box_layout_3.addWidget(self.result_data_table)
        
        #Set Layout for each tab
        self.tab1.setLayout(self.v_box_layout_1)   
        self.tab2.setLayout(self.v_box_layout_2)
        self.tab3.setLayout(self.v_box_layout_3)
        
        # main layout
        self.main_layout = QtGui.QVBoxLayout()
        # add all main to the main vLayout
        self.main_layout.addWidget(self.tabs)
        # central widget
        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(self.main_layout)
        # set central widget
        self.setCentralWidget(self.central_widget)
        
    def center_on_screen(self):
        # Centers the window on the screen. 
        size = self.frameSize()
        desktop_size = QtGui.QDesktopWidget().screenGeometry()
        left = (desktop_size.width()/2)-(size.width()/2)
        top = (desktop_size.height()/2)-(size.height()/2)
        self.move(left, top)
    
    def show_import(self):
        self.imp = RawData()
        self.imp.exec_()
        if self.imp.display_table:
            if not self.imp.selected_col:
                self.imp.get_selected_column()
                print("Tidak ada kolom dipilih!") #Seharusnya tampilkan dalam dialog
            else:
                self.imp.import_selected_data()
                self.display_raw_data(self.imp.df_selected_data)
                
                # Set to Tab 1
                self.tabs.setCurrentWidget(self.tab1)
                
                # Close widget in another tab
                self.canvas_for_dendrogram.hide()
                self.toolbar.hide()
                self.result_data_table.hide()
                
                # Enable/ disable some menu
                self.seg_action.setEnabled(True)
                self.save_result_action.setEnabled(False)
        
    def show_about(self):
        abt = About(self)
        abt.show()         
    
    def display_raw_data(self, data):    
        # Specify the number of rows and columns of table
        self.raw_data_table.setRowCount(len(data.index))
        self.raw_data_table.setColumnCount(len(data.columns))
        
        # Set cell value of table
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.raw_data_table.setItem(i, j, QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
        
        # Create the columns header
        self.raw_data_table.setHorizontalHeaderLabels(list(data.columns.values))
       
    def segmen(self):
        self.sgm = Segmentation(self.imp.df_selected_data)
        self.sgm
        
        # Set Tab 2 and Tab 3
        self.tabs.addTab(self.tab2, "Visualisasi Model")
        self.canvas_for_dendrogram.show()
        self.toolbar.show()
        self.tabs.addTab(self.tab3, "Data Hasil Segmentasi")
        self.result_data_table.show()
        
        # Draw dendrogram on canvas
        self.canvas_for_dendrogram.draw()
        # Set to Tab 2
        self.tabs.setCurrentWidget(self.tab2)
        # Display result data in QTableWidget
        self.sgm.get_result_data()
        self.display_result_data(self.sgm.df_result_data)
        # Enable some menu item
        self.save_result_action.setEnabled(True)
        
    def display_result_data(self, data):    
        # Specify the number of rows and columns of table
        self.result_data_table.setRowCount(len(data.index))
        self.result_data_table.setColumnCount(len(data.columns))
        
        # Set cell value of table
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.result_data_table.setItem\
                (i, j, QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
        
        # Create the columns header
        self.result_data_table.setHorizontalHeaderLabels(list(data.columns.values))
    
    def save_result_data(self):
        # Provides a dialog that allow users to give file name and location on disk.
        self.file_name_save = QtGui.QFileDialog.getSaveFileName\
        (self, "Save File", ".", "(Comma Separated Value *.csv)")
        # Write DataFrame into *.csv file.
        self.sgm.df_result_data.to_csv(self.file_name_save, sep=',', index=False)
        