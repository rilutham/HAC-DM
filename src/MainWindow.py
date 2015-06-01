#!/usr/bin/python
# -*- coding: utf-8 -*-

"""MainWindow.py
@author: rilutham
"""

from PyQt4 import QtGui
from RawData import RawData
from Preprocessing import Bining, DeriveAttribute
from Segmentation import Segmentation
from About import About
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__()
        self.init_ui()
    
    def init_ui(self):
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
        
        fill_zero_act = QtGui.QAction('Isi dengan nilai 0', self)
        fill_zero_act.triggered.connect(self.fill_with_zero)
        
        delete_row_act = QtGui.QAction('Hapus baris', self)
        delete_row_act.triggered.connect(self.delete_missing_row)
        
        miss_value_action = QtGui.QMenu('Tangani nilai kosong', self)
        miss_value_action.addAction(fill_zero_act)
        miss_value_action.addAction(delete_row_act)
        
        bining_act = QtGui.QAction('Bining atribut', self)
        bining_act.triggered.connect(self.show_bining)
        
        derive_act = QtGui.QAction('Penurunan atribut', self)
        derive_act.triggered.connect(self.derive_attribute)
        
        self.seg_action = QtGui.QAction('Proses', self)
        self.seg_action.setShortcut('F5')
        self.seg_action.setStatusTip('Jalankan proses segmentasi')
        self.seg_action.setEnabled(False)
        self.seg_action.triggered.connect(self.segmen_customer)
        
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
        preprocess_menu.addMenu(miss_value_action)
        preprocess_menu.addAction(bining_act)
        preprocess_menu.addAction(derive_act)
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
        self.stat_frame = QtGui.QFrame()
        self.frame_layout = QtGui.QHBoxLayout()
        self.stat_frame.setLayout(self.frame_layout)
        self.txt_table_exist = QtGui.QLabel("""Tidak ada data yang ditampilkan.\n
Pilih menu Data > Impor data (Ctrl+i) untuk mengimpor data""", self)
        self.txt_table_exist.setStyleSheet("color: gray; font: italic;")
        self.txt_stats = QtGui.QLabel('', self)
        self.txt_stats.setStyleSheet("font-size: 10pt; font: bold; ")
        self.frame_layout.addWidget(self.txt_stats)
        
        self.raw_data_table = QtGui.QTableWidget(self)
        self.v_box_layout_1 = QtGui.QVBoxLayout()
        self.v_box_layout_1.addWidget(self.txt_table_exist)
        self.v_box_layout_1.addWidget(self.stat_frame)
        self.v_box_layout_1.addWidget(self.raw_data_table)
        self.stat_frame.hide()
        self.raw_data_table.hide()
        
        # Setting Tab 2
        self.tabs.addTab(self.tab2, "Visualisasi Model")
        self.txt_visual_exist = QtGui.QLabel("""Tidak ada visualisasi model yang ditampilkan.\n
Impor data pelanggan, kemudian lakukan proses segmentasi dengan menekan F5 atau pilih menu Segmentasi > Proses""", self)
        self.txt_visual_exist.setStyleSheet("color: gray; font: italic;")
        self.txt_set_distance = QtGui.QLabel('Masukkan jarak potong dendrogram: ', self)
        self.treshold_edit = QtGui.QLineEdit()
        self.btn_treshold = QtGui.QPushButton("Submit", self)
        self.btn_treshold.clicked.connect(self.set_treshold)
        self.figure = plt.figure()
        self.canvas_for_dendrogram = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas_for_dendrogram, self)
        self.treshold_frame = QtGui.QFrame()
        self.treshold_layout = QtGui.QHBoxLayout()
        self.treshold_frame.setLayout(self.treshold_layout)
        self.treshold_layout.addWidget(self.txt_set_distance)
        self.treshold_layout.addWidget(self.treshold_edit)
        self.treshold_layout.addWidget(self.btn_treshold)
        self.v_box_layout_2 = QtGui.QVBoxLayout()
        self.v_box_layout_2.addWidget(self.txt_visual_exist)
        self.v_box_layout_2.addWidget(self.treshold_frame)
        self.v_box_layout_2.addWidget(self.canvas_for_dendrogram)
        self.v_box_layout_2.addWidget(self.toolbar)
        self.treshold_frame.hide()
        self.canvas_for_dendrogram.hide()
        self.toolbar.hide()
        
        # Setting Tab 3
        self.tabs.addTab(self.tab3, "Data Hasil Segmentasi")
        self.txt_result_exist = QtGui.QLabel("""Tidak ada data hasil yang ditampilkan.\n
Impor data pelanggan, kemudian lakukan proses segmentasi dengan menekan F5 atau pilih menu Segmentasi > Proses.""", self)
        self.txt_result_exist.setStyleSheet("color: gray; font: italic;")
        self.result_data_table = QtGui.QTableWidget(self) 
        self.v_box_layout_3 = QtGui.QVBoxLayout()
        self.v_box_layout_3.addWidget(self.txt_result_exist)
        self.v_box_layout_3.addWidget(self.result_data_table)
        self.result_data_table.hide()
        
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
    
    
        
    def show_import(self):
        self.imp = RawData()
        self.imp.exec_()
        if self.imp.display_table == True:
            if len(self.imp.selected_col) == 0:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setText("Tidak ada atribut yang dipilih!")
                msgBox.setInformativeText("Silahkan pilih minimal 2 atribut")
                msgBox.setIcon(2)
                msgBox.exec_()
            elif len(self.imp.selected_col) == 1:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setText("Hanya satu atribut yang dipilih!")
                msgBox.setInformativeText("Silahkan pilih minimal 2 atribut")
                msgBox.setIcon(2)
                msgBox.exec_()
            else:
                self.display_raw_data(self.imp.df_selected_data)
                
                # Count data statistics
                self.imp.count_stats(self.imp.df_selected_data)
                self.txt_stats.setText(self.imp.stats)
                
                # Set to Tab 1
                self.tabs.setCurrentWidget(self.tab1)
                self.stat_frame.show()
                self.raw_data_table.show() 
                self.txt_visual_exist.show()
                self.txt_result_exist.show()
                
                # Close widget
                self.txt_table_exist.hide()
                self.treshold_frame.hide()
                self.canvas_for_dendrogram.hide()
                self.toolbar.hide()
                self.figure.clf() 
                self.result_data_table.hide()
                    
                # Enable/ disable some menu
                self.seg_action.setEnabled(True)
                self.save_result_action.setEnabled(False)

    def display_raw_data(self, data):
        self.ready_data = data   
        # Specify the number of rows and columns of table
        self.raw_data_table.setRowCount(len(self.ready_data.index))
        self.raw_data_table.setColumnCount(len(self.ready_data.columns))
        
        # Set cell value of table
        for i in range(len(self.ready_data.index)):
            for j in range(len(self.ready_data.columns)):
                self.raw_data_table.setItem(i, j, QtGui.QTableWidgetItem(str(self.ready_data.iget_value(i, j))))
        
        # Color first column
        for i in range(len(self.ready_data.index)):
            for j in range(len(self.ready_data.columns)):
                self.raw_data_table.item(i,0).setBackground(QtGui.QColor(229,229,229))
                
        # Create the columns header
        self.raw_data_table.setHorizontalHeaderLabels(list(self.ready_data.columns.values))

        return self.ready_data
    
    def fill_with_zero(self):
        self.tabs.setCurrentWidget(self.tab1)
        if self.imp.missing_row_num == 0:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Tidak terdapat data kosong!")
            msgBox.setIcon(2)
            msgBox.exec_()
        elif self.imp.missing_row_num > 0:
            self.df_clean_data = self.imp.df_selected_data.fillna(0)
            # Count data statistics
            self.imp.count_stats(self.df_clean_data)
            self.txt_stats.setText(self.imp.stats)
            self.display_raw_data(self.df_clean_data)
    
    def delete_missing_row(self):
        self.tabs.setCurrentWidget(self.tab1)
        msgBox = QtGui.QMessageBox(self)
        msgBox.setInformativeText("Apakah Anda yakin untuk menghapus data kosong?")
        msgBox.setIcon(4)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        ret = msgBox.exec_()
        if ret == QtGui.QMessageBox.Ok:
            #Save was clicked
            if self.imp.missing_row_num == 0:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setText("Tidak terdapat data kosong!")
                msgBox.setIcon(2)
                msgBox.exec_()
            elif self.imp.missing_row_num > 0:  
                self.df_clean_data = self.imp.df_selected_data.dropna(axis=0)
                # Count data statistics
                self.imp.count_stats(self.df_clean_data)
                self.txt_stats.setText(self.imp.stats)
                self.display_raw_data(self.df_clean_data)
        
    def show_bining(self):
        self.tabs.setCurrentWidget(self.tab1)
        self.bin = Bining()
        self.bin.add_attribute_to_list(self.ready_data)
        self.bin.exec_()
        if self.bin.display_table:
            if not self.bin.selected_col:
                print("Tidak ada atribut dipilih!") #Seharusnya tampilkan dalam dialog
            else:
                self.display_raw_data(self.bin.data)
    
    def derive_attribute(self):
        self.tabs.setCurrentWidget(self.tab1)
        self.derv = DeriveAttribute()
        self.derv.add_attribute_to_list(self.ready_data)
        self.derv.exec_()
        if self.derv.display_table:
            if not self.derv.selected_col:
                print("Tidak ada atribut dipilih!") #Seharusnya tampilkan dalam dialog
            else:
                self.display_raw_data(self.derv.data)
        
    def segmen_customer(self):
        if self.imp.missing_num > 0:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Masih terdapat data kosong!")
            msgBox.setIcon(3)
            msgBox.exec_()
        elif self.imp.missing_num == 0:
            self.sgm = Segmentation(self.ready_data)
            self.sgm
            
            # Set Tab 2 and Tab 3
            self.txt_visual_exist.hide()
            self.treshold_frame.show()
            self.canvas_for_dendrogram.show()
            self.toolbar.show()
            self.txt_result_exist.hide()
            self.result_data_table.show()
            
            # Draw dendrogram on canvas
            self.canvas_for_dendrogram.draw()
            # Set to Tab 2
            self.tabs.setCurrentWidget(self.tab2)
            # Display result data in QTableWidget
            self.display_result_data(self.sgm.df_result_data)
            # Enable some menu item
            self.save_result_action.setEnabled(True)
        
    def set_treshold(self):
        self.figure.clf()
        self.treshold_text = str(self.treshold_edit.text())
        self.treshold_value = float(self.treshold_text)
        self.sgm.refresh_result_data(self.treshold_value)
        
        # Draw dendrogram on canvas
        self.canvas_for_dendrogram.draw()
        # Set to Tab 2
        self.tabs.setCurrentWidget(self.tab2)
        # Display result data in QTableWidget
        self.display_result_data(self.sgm.df_result_data)
        
    def display_result_data(self, data):    
        # Specify the number of rows and columns of table
        self.result_data_table.setRowCount(len(data.index))
        self.result_data_table.setColumnCount(len(data.columns))
        
        # Set cell value of table
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.result_data_table.setItem\
                (i, j, QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
        
        # Color first column
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.result_data_table.item(i,0).setBackground(QtGui.QColor(229,229,229))
                self.result_data_table.item(i,len(data.columns)-1).setBackground(QtGui.QColor(0,255,0))
        
        
                
        # Create the columns header
        self.result_data_table.setHorizontalHeaderLabels(list(data.columns.values))
    
    def save_result_data(self):
        # Provides a dialog that allow users to give file name and location on disk.
        self.file_name_save = QtGui.QFileDialog.getSaveFileName\
        (self, "Save File", ".", "(Comma Separated Value *.csv)")
        # Write DataFrame into *.csv file.
        self.sgm.df_result_data.to_csv(self.file_name_save, sep=',', index=False)
    
    def show_about(self):
        abt = About()
        abt.exec_()

    def center_on_screen(self):
        # Centers the window on the screen. 
        size = self.frameSize()
        desktop_size = QtGui.QDesktopWidget().screenGeometry()
        left = (desktop_size.width()/2)-(size.width()/2)
        top = (desktop_size.height()/2)-(size.height()/2)
        self.move(left, top)
