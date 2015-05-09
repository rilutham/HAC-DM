#!/usr/bin/python
# -*- coding: utf-8 -*-

from About import About
from PyQt4 import QtGui
import  pandas as pd
#from ImportData import ImportData
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class ApplicationWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(ApplicationWindow, self).__init__(parent)
        self.init_ui()
                
    def init_ui(self):               
        
        # Main window setting
        self.setGeometry(0, 0, 980, 768)
        self.setWindowTitle("Customer Segmentation System")
        self.centerOnScreen()
        
        import_action = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'Impor data', self)
        import_action.setShortcut('Ctrl+i')
        import_action.setStatusTip('Impor data pelanggan')
        import_action.triggered.connect(self.import_csv)
        
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        
        seg_action = QtGui.QAction('Proses', self)
        seg_action.setShortcut('F5')
        seg_action.setStatusTip('Jalankan segmentasi')
        seg_action.triggered.connect(self.segmen)
        
        save_result_data = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Simpan data hasil', self)
        save_result_data.setShortcut('Ctrl+S')
        save_result_data.setStatusTip('Simpan data hasil segmentasi')
        save_result_data.triggered.connect(self.save_result)
        
        about_action = QtGui.QAction('Tentang Aplikasi', self)
        about_action.triggered.connect(self.show_about)
        
        # Menubar setting
        menubar = self.menuBar()
        data_menu = menubar.addMenu('&Data')
        data_menu.addAction(import_action)
        data_menu.addAction(exit_action)
        preprocess_menu = menubar.addMenu('&Preprocessing')
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
        
        self.tabs.addTab(self.tab1,"Data Processing Tab")
        self.tabs.addTab(self.tab2,"Dendrogram")
        self.tabs.addTab(self.tab3,"Result Data")
        
        # Setting Tab 1
        self.raw_data_table = QtGui.QTableWidget(self) 
        
        self.vBoxlayout1 = QtGui.QVBoxLayout()
        self.vBoxlayout1.addWidget(self.raw_data_table)
        
        # Setting Tab 2
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.toolbar.hide() # For hide the matplotlib toolbar
        
        self.vBoxlayout2 = QtGui.QVBoxLayout()
        self.vBoxlayout2.addWidget(self.canvas)
        self.vBoxlayout2.addWidget(self.toolbar)
        
        # Setting Tab 1
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
        '''centerOnScreen()
        Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))   
    
    def show_about(self):
        abt = About(self)
        abt.show()
           
    def import_csv(self):
        # Provides a dialog that allow users to select only *.csv file.
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.csv)")
        
        # Read the *csv file and store it into DataFrame
        global df_raw_data
        df_raw_data  = pd.DataFrame.from_csv(str(file_name),header=0, index_col=False)
        
        # Specify the number of rows and columns of table
        self.raw_data_table.setRowCount(len(df_raw_data.index))
        self.raw_data_table.setColumnCount(len(df_raw_data.columns))
        
        # Set cell value of table
        for i in range(len(df_raw_data.index)):
            for j in range(len(df_raw_data.columns)):
                self.raw_data_table.setItem(i,j,QtGui.QTableWidgetItem(str(df_raw_data.iget_value(i, j))))
        
        # Create the columns header
        self.raw_data_table.setHorizontalHeaderLabels(list(df_raw_data.columns.values))
        
        return df_raw_data   
    
    def segmen(self):      
        # Data which is use for distance measure
        n_cols = len(df_raw_data.columns)
        n_rows = len(df_raw_data.index)
        dist_data = df_raw_data.ix[:,1:n_cols]
        dendro_label = df_raw_data.ix[0:n_rows,0:1]
        
        # Count the distance with jaccard distance
        row_dist = pd.DataFrame(squareform(pdist(dist_data, metric='jaccard')))
        
        # Cluster using complete linkage
        row_clusters = linkage(row_dist, method='complete')
        
        # Generate dendrogram and place it into canvas
        dendrogram(row_clusters, labels=dendro_label.values)
        self.canvas.draw()
        
        # Generate cluster index
        cluster_index = fcluster(row_clusters, t=5, criterion='maxclust')
        
        ### Display data result
        # Add new column (cluster_index) to result data
        df_result_data = df_raw_data
        df_result_data['ID_Segmen'] = cluster_index        
        new_result_data_column = n_cols + 1
        
        # Specify the number of rows and columns of result table
        self.result_data_table.setRowCount(len(df_result_data.index))
        self.result_data_table.setColumnCount(new_result_data_column)
        
        # Set cell value of result table
        for i in range(len(df_result_data.index)):
            for j in range(new_result_data_column):
                self.result_data_table.setItem(i,j,QtGui.QTableWidgetItem(str(df_result_data.iget_value(i, j))))
        
        # Create the columns header
        self.result_data_table.setHorizontalHeaderLabels(list(df_result_data.columns.values))
    
    def save_result(self):
        # Provides a dialog that allow users to give file name and location on disk.
        file_name_save = QtGui.QFileDialog.getOpenFileName(self, 'Save File',".","(*.csv)")
        
        # Write DataFrame into *.csv file.
        df_raw_data.to_csv(file_name_save, sep=',', index=False)  