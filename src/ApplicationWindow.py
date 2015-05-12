#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from RawData import RawData
from Segmentation import Segmentation
from About import About
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class ApplicationWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self, parent= None):
        '''
        Constructor
        '''
        super(ApplicationWindow, self).__init__(parent)       
        
        # Main window setting
        self.setGeometry(0, 0, 980, 768)
        self.setWindowTitle("Customer Segmentation System")
        self.centerOnScreen()
        
        import_action = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'Impor data', self)
        import_action.setShortcut('Ctrl+i')
        import_action.setStatusTip('Impor data pelanggan')
        import_action.triggered.connect(self.show_import)
        
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        
        clean_action = QtGui.QAction('Hapus nilai kosong',self)
        #clean_action.triggered.connect(self.clean_missing_value)
        
        seg_action = QtGui.QAction('Proses', self)
        seg_action.setShortcut('F5')
        seg_action.setStatusTip('Jalankan segmentasi')
        seg_action.triggered.connect(self.segmen)
        
        save_result_data = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Simpan data hasil', self)
        save_result_data.setShortcut('Ctrl+S')
        save_result_data.setStatusTip('Simpan data hasil segmentasi')
        #save_result_data.triggered.connect(self.save_result_data_clicked)
        
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
        segmen_menu.addAction(seg_action)
        result_menu = menubar.addMenu('&Hasil Segmentasi')
        result_menu.addAction(save_result_data)
        help_menu = menubar.addMenu('&Bantuan')
        help_menu.addAction(about_action)
        # Toolbar setting
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(import_action)
        toolbar.addAction(save_result_data)
        
        
        # Show statusbar
        self.statusBar()
        
        # Setting TabWidget
        self.tabs    = QtGui.QTabWidget()
        self.tab1    = QtGui.QWidget()    
        self.tab2    = QtGui.QWidget()
        self.tab3    = QtGui.QWidget()
        
        self.tabs.addTab(self.tab1,"Pemrosesan Data")
        self.tabs.addTab(self.tab2,"Visualisasi Model")
        self.tabs.addTab(self.tab3,"Data Hasil Segmentasi")
        
        # Setting Tab 1
        self.raw_data_table = QtGui.QTableWidget(self) 
        
        self.vBoxlayout1 = QtGui.QVBoxLayout()
        self.vBoxlayout1.addWidget(self.raw_data_table)
        
        # Setting Tab 2
        self.figure = plt.figure()
        self.canvas_for_dendrogram = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas_for_dendrogram, self)
        # self.toolbar.hide() # For hide the matplotlib toolbar
        
        self.vBoxlayout2 = QtGui.QVBoxLayout()
        self.vBoxlayout2.addWidget(self.canvas_for_dendrogram)
        self.vBoxlayout2.addWidget(self.toolbar)
        
        # Setting Tab 3
        self.result_data_table = QtGui.QTableWidget(self) 
        
        self.vBoxlayout3 = QtGui.QVBoxLayout()
        self.vBoxlayout3.addWidget(self.result_data_table)
        
        #Set Layout for each tab
        self.tab1.setLayout(self.vBoxlayout1)   
        self.tab2.setLayout(self.vBoxlayout2)
        self.tab3.setLayout(self.vBoxlayout3)
        

        
        # main layout
        self.mainLayout = QtGui.QVBoxLayout()
    
        # add all main to the main vLayout
        self.mainLayout.addWidget(self.tabs)
    
        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)
    
        # set central widget
        self.setCentralWidget(self.centralWidget)
        
        
    def centerOnScreen (self):
        # Centers the window on the screen. 
        size = self.frameSize()
        desktopSize = QtGui.QDesktopWidget().screenGeometry()
        left = (desktopSize.width()/2)-(size.width()/2)
        top = (desktopSize.height()/2)-(size.height()/2)
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
                self.raw_data_table.setItem(i,j,QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
        
        # Create the columns header
        self.raw_data_table.setHorizontalHeaderLabels(list(data.columns.values))
       
    def segmen(self):
        # Clear current plot
        self.figure.clf()
        self.sgm = Segmentation(self.imp.df_selected_data)
        self.sgm
        # Draw dendrogram on canvas
        self.canvas_for_dendrogram.draw()
        # Set to Tab 2
        self.tabs.setCurrentWidget(self.tab2)
        self.sgm.get_result_data()
        self.display_result_data(self.sgm.df_result_data)
        
    def display_result_data(self, data):    
        # Specify the number of rows and columns of table
        self.result_data_table.setRowCount(len(data.index))
        self.result_data_table.setColumnCount(len(data.columns))
        
        # Set cell value of table
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.result_data_table.setItem(i,j,QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
        
        # Create the columns header
        self.result_data_table.setHorizontalHeaderLabels(list(data.columns.values))    