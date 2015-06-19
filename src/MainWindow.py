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
        
        self.seg_action = QtGui.QAction(QtGui.QIcon('icons/run.png'),'Proses', self)
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
        toolbar.addAction(self.seg_action)
        toolbar.addAction(self.save_result_action)
        
        # Show statusbar
        self.statusBar()
        
        # Setting TabWidget
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()  
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tab4 = QtGui.QWidget()  

        ### Setting Tab 1 ###
        self.tabs.addTab(self.tab1, "Pengolahan Data")
        ## Left side
        # Frame "data detail"
        self.stat_frame = QtGui.QFrame()
        self.stat_frame.setMaximumHeight(200)
        self.txt_data_detail = QtGui.QLabel("Rincian Data:")
        self.txt_data_detail.setStyleSheet("font: bold; ")
        self.txt_stats = QtGui.QLabel('', self)
        self.txt_note = QtGui.QLabel("Keterangan Tabel: ", self)
        self.txt_note.setStyleSheet("font: bold")
        txt_label_1 = QtGui.QLabel("  Label/ Meta atribut", self)
        txt_label_1.setStyleSheet("background-color:#19B5FE; color:black")
        # VLayout for frame "data detail"
        self.stat_layout = QtGui.QVBoxLayout()
        self.stat_frame.setLayout(self.stat_layout)
        self.stat_layout.insertWidget(0, self.txt_data_detail)
        self.stat_layout.insertWidget(1, self.txt_stats)
        self.stat_layout.insertWidget(2, self.txt_note)
        self.stat_layout.insertWidget(3, txt_label_1)
        # Empty frame
        self.empty_frame_1 = QtGui.QFrame()
        # Left side frame in Tab 1
        self.left_frame = QtGui.QFrame()
        self.left_frame.setMaximumWidth(275)
        self.left_frame.setMinimumWidth(275)
        self.left_frame.setStyleSheet("background-color:#dadfe1; color:black")
        self.left_side_layout = QtGui.QVBoxLayout()
        self.left_frame.setLayout(self.left_side_layout)
        self.left_side_layout.addWidget(self.stat_frame)
        self.left_side_layout.addWidget(self.empty_frame_1)

        ## Tab 1 layout
        self.txt_table_exist = QtGui.QLabel("""Tidak ada data yang ditampilkan.\n
Pilih menu Data > Impor data (Ctrl+i) untuk mengimpor data""", self)
        self.txt_table_exist.setStyleSheet("color: gray; font: italic;")
        self.raw_data_table = QtGui.QTableWidget(self)
        self.v_box_layout_1 = QtGui.QHBoxLayout()
        self.v_box_layout_1.addWidget(self.txt_table_exist)
        self.v_box_layout_1.addWidget(self.left_frame)
        self.v_box_layout_1.addWidget(self.raw_data_table)
        self.left_frame.hide()
        self.raw_data_table.hide()
        
        ### Setting Tab 2 ###
        self.tabs.addTab(self.tab2, "Visualisasi Model")
        self.txt_visual_exist = QtGui.QLabel("""Tidak ada visualisasi model yang ditampilkan.\n
Impor data pelanggan, kemudian lakukan proses segmentasi dengan menekan F5 atau pilih menu Segmentasi > Proses""", self)
        self.txt_visual_exist.setStyleSheet("color: gray; font: italic;")
        self.txt_set_distance = QtGui.QLabel('Masukkan jarak potong dendrogram: ', self)
        self.treshold_edit = QtGui.QLineEdit()
        self.btn_treshold = QtGui.QPushButton("Submit", self)
        self.btn_treshold.clicked.connect(self.set_treshold)
        self.figure = plt.figure(facecolor='#dadfe1')
        self.canvas_for_dendrogram = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas_for_dendrogram, self)
        self.treshold_frame = QtGui.QFrame()
        self.treshold_layout = QtGui.QHBoxLayout()
        self.treshold_frame.setLayout(self.treshold_layout)
        self.treshold_layout.addWidget(self.txt_set_distance)
        self.treshold_layout.addWidget(self.treshold_edit)
        self.treshold_layout.addWidget(self.btn_treshold)
        #self.treshold_layout.addWidget(self.txt_n_cluster)
        self.v_box_layout_2 = QtGui.QVBoxLayout()
        self.v_box_layout_2.addWidget(self.txt_visual_exist)
        self.v_box_layout_2.addWidget(self.treshold_frame)
        self.v_box_layout_2.addWidget(self.canvas_for_dendrogram)
        self.v_box_layout_2.addWidget(self.toolbar)
        self.treshold_frame.hide()
        self.canvas_for_dendrogram.hide()
        self.toolbar.hide()
        
        ### Setting Tab 3 ###
        self.tabs.addTab(self.tab3, "Informasi Hasil Segmentasi")
        self.txt_information_exist = QtGui.QLabel("""Tidak ada informasi yang ditampilkan.\n
Impor data pelanggan, kemudian lakukan proses segmentasi dengan menekan F5 atau pilih menu Segmentasi > Proses.""", self)
        self.txt_information_exist.setStyleSheet("color: gray; font: italic;")

        self.txt_summary = QtGui.QLabel("Hasil Segmentasi Pelanggan: ", self)
        self.txt_summary.setStyleSheet("font: bold;")
        self.txt_n_cluster = QtGui.QLabel('',self)
        self.cluster_list = QtGui.QListWidget()
        self.cluster_list.setMaximumHeight(225)
        txt_note_3 = QtGui.QLabel("Keterangan Tabel: ", self)
        txt_note_3.setStyleSheet("font: bold")
        txt_label_3 = QtGui.QLabel("  ID_Segmen", self)
        txt_label_3.setStyleSheet("background-color:#3FC380; color:black")
        
        self.summary_frame = QtGui.QFrame()
        self.summary_frame.setMaximumHeight(300)
        self.summary_layout = QtGui.QVBoxLayout()
        self.summary_frame.setLayout(self.summary_layout)
        self.summary_layout.insertWidget(0, self.txt_summary)
        self.summary_layout.insertWidget(1, self.txt_n_cluster)
        self.summary_layout.insertWidget(2, self.cluster_list)
        self.summary_layout.insertWidget(3, txt_note_3)
        self.summary_layout.insertWidget(4, txt_label_3)
        # Empty frame
        self.empty_frame_3 = QtGui.QFrame()
        # Left side frame in Tab 3
        self.left_frame_3 = QtGui.QFrame()
        self.left_frame_3.setMaximumWidth(275)
        self.left_frame_3.setMinimumWidth(275)
        self.left_frame_3.setStyleSheet("background-color:#dadfe1; color:black")
        self.left_side_3_layout = QtGui.QVBoxLayout()
        self.left_frame_3.setLayout(self.left_side_3_layout)
        self.left_side_3_layout.addWidget(self.summary_frame)
        self.left_side_3_layout.addWidget(self.empty_frame_3)
        # Right side
        self.txt_summary_stat = QtGui.QLabel("Statistik: ", self)
        self.txt_summary_stat.setStyleSheet("font: bold;")
        self.knowledge_table = QtGui.QTableWidget(self)
        self.txt_summary_exp = QtGui.QLabel("Keterangan: ", self)
        self.txt_summary_exp.setStyleSheet("font: bold;")
        self.knowledge_text = QtGui.QTextBrowser(self)
        self.right_frame_3 = QtGui.QFrame()
        self.right_side_3_layout = QtGui.QVBoxLayout()
        self.right_frame_3.setLayout(self.right_side_3_layout)
        self.right_side_3_layout.addWidget(self.txt_summary_stat)
        self.right_side_3_layout.addWidget(self.knowledge_table)
        self.right_side_3_layout.addWidget(self.txt_summary_exp)
        self.right_side_3_layout.addWidget(self.knowledge_text)
        
        self.v_box_layout_3 = QtGui.QHBoxLayout()
        self.v_box_layout_3.addWidget(self.txt_information_exist)
        self.v_box_layout_3.addWidget(self.left_frame_3)
        self.v_box_layout_3.addWidget(self.right_frame_3)
        self.left_frame_3.hide()
        self.knowledge_table.hide()
        self.knowledge_text.hide()
        self.txt_summary_exp.hide()
        self.txt_summary_stat.hide()
        
        ### Setting Tab 4 ###
        self.tabs.addTab(self.tab4, "Data Hasil Segmentasi")
        self.txt_result_exist = QtGui.QLabel("""Tidak ada data hasil yang ditampilkan.\n
Impor data pelanggan, kemudian lakukan proses segmentasi dengan menekan F5 atau pilih menu Segmentasi > Proses.""", self)
        self.txt_result_exist.setStyleSheet("color: gray; font: italic;")
        self.result_data_table = QtGui.QTableWidget(self) 
        self.v_box_layout_4 = QtGui.QHBoxLayout()
        self.v_box_layout_4.insertWidget(0, self.txt_result_exist)
        self.v_box_layout_4.insertWidget(1, self.result_data_table)
        self.result_data_table.hide()
        
        #Set Layout for each tab
        self.tab1.setLayout(self.v_box_layout_1)
        self.tab2.setLayout(self.v_box_layout_2)
        self.tab3.setLayout(self.v_box_layout_3)
        self.tab4.setLayout(self.v_box_layout_4)
        
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
                self.left_frame.show()
                self.raw_data_table.show() 
                self.txt_visual_exist.show()
                self.txt_information_exist.show()
                self.txt_result_exist.show()
                
                # Close widget
                self.txt_table_exist.hide()
                self.treshold_frame.hide()
                self.canvas_for_dendrogram.hide()
                self.toolbar.hide()
                self.figure.clf()
                self.left_frame_3.hide()
                self.result_data_table.hide()
                self.knowledge_table.hide()
                self.knowledge_text.hide()
                self.txt_summary_exp.hide()
                self.txt_summary_stat.hide()
                    
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
                self.raw_data_table.item(i,0).setBackground(QtGui.QColor(25,181,254))
                
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
                msgBox = QtGui.QMessageBox(self)
                msgBox.setText("Tidak ada atribut yang dipilih!")
                msgBox.setInformativeText("Silahkan pilih atribut")
                msgBox.setIcon(2)
                msgBox.exec_()
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
            self.left_frame_3.show()
            self.txt_n_cluster.setText(self.sgm.n_cluster)
            self.txt_visual_exist.hide()
            self.treshold_frame.show()
            plt.ylabel("Jarak antar pelanggan")
            plt.xlabel("Pelanggan")
            self.canvas_for_dendrogram.show()
            self.toolbar.show()
            self.txt_result_exist.hide()
            self.result_data_table.show()
            self.txt_information_exist.hide()
            self.knowledge_table.show()
            self.knowledge_text.show()
            self.txt_summary_exp.show()
            self.txt_summary_stat.show()
            self.show_result_summary()
            
            # Draw dendrogram on canvas
            self.canvas_for_dendrogram.draw()
            # Set to Tab 2
            self.tabs.setCurrentWidget(self.tab2)
            # Display result data in QTableWidget
            self.display_result_data(self.sgm.df_result_data)
            # Enable some menu item
            self.save_result_action.setEnabled(True)
            
            self.show_knowledge(self.sgm.df_result_data)

    def show_result_summary(self):
        self.cluster_list.clear()
        # Segment result summary
        for x in self.sgm.summary_list:
            self.item = QtGui.QListWidgetItem(x)
            self.cluster_list.addItem(self.item)

    def set_treshold(self):
        self.figure.clf()
        self.treshold_text = str(self.treshold_edit.text())
        self.treshold_value = float(self.treshold_text)
        self.sgm.refresh_result_data(self.treshold_value)

        self.txt_n_cluster.setText(self.sgm.n_cluster)

        self.show_result_summary()

        # Draw dendrogram on canvas
        plt.ylabel("Jarak antar pelanggan")
        plt.xlabel("Pelanggan")
        self.canvas_for_dendrogram.draw()
        # Set to Tab 2
        self.tabs.setCurrentWidget(self.tab2)
        # Display result data in QTableWidget
        self.display_result_data(self.sgm.df_result_data)
        
        self.show_knowledge(self.sgm.df_result_data)
        
    def display_result_data(self, data):    
        # Specify the number of rows and columns of table
        self.result_data_table.setRowCount(len(data.index))
        self.result_data_table.setColumnCount(len(data.columns))
        
        # Set cell value of table
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.result_data_table.setItem\
                (i, j, QtGui.QTableWidgetItem(str(data.iget_value(i, j))))
                if (self.sgm.cluster_index[i] % 10 == 1):
                    # Green
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(177, 245, 67))
                elif (self.sgm.cluster_index[i] % 10 == 2):
                    # Blue
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(0, 214, 221))
                elif (self.sgm.cluster_index[i] % 10 == 3):
                    # Pink
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(255, 53, 139))
                elif (self.sgm.cluster_index[i] % 10 == 4):
                    # Yellow
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(242, 255, 46))
                elif (self.sgm.cluster_index[i] % 10 == 5):
                    # Fresh Orange
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(255, 94, 0))
                elif (self.sgm.cluster_index[i] % 10 == 6):
                    # Gray
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(151, 104, 209))
                elif (self.sgm.cluster_index[i] % 10 == 7):
                    # Cream
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(252, 125, 73))
                elif (self.sgm.cluster_index[i] % 10 == 8):
                    # Dark gray
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(126, 138, 162))
                elif (self.sgm.cluster_index[i] % 10 == 9):
                    # Dark Green
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(2, 166, 118))
                elif (self.sgm.cluster_index[i] % 10 == 0):
                    # Blue
                    self.result_data_table.item(i,j).setBackground(QtGui.QColor(102, 12, 232))
                
        # Create the columns header
        self.result_data_table.setHorizontalHeaderLabels(list(data.columns.values))

    def show_knowledge(self, data):
        # Show knowledge result
        grouped_data = data.groupby('ID_Segmen')
        summed_data =  grouped_data.sum()
        # Add new column (cluster_ID) to knowledge data
        #summed_data['ID_Segmen'] =
        #self.cluster_index 
        # Specify the number of rows and columns of table
        self.knowledge_table.setRowCount(grouped_data.ngroups)
        self.knowledge_table.setColumnCount(len(grouped_data.sum().columns) + 1)
        # Set cell value of table
        for i in range(grouped_data.ngroups):
            self.knowledge_table.setItem(i,0,QtGui.QTableWidgetItem(str(i+1)))
            for j in range(len(grouped_data.sum().columns)):
                self.knowledge_table.setItem\
                (i, j+1, QtGui.QTableWidgetItem(str(summed_data.get_values()[i][j])))
            
        # Create the columns header
        knowledge_column_name = list(grouped_data.sum().columns.values)
        knowledge_column_name.insert(0,"Segmen ke-")
        self.knowledge_table.setHorizontalHeaderLabels(knowledge_column_name)
        
        # Color first column
        for i in range(grouped_data.ngroups):
            for j in range(len(grouped_data.sum().columns) + 1):
                self.knowledge_table.item(i,0).setBackground(QtGui.QColor(63,195,128))
                
        self.knowledge_text.clear()
        
        for i in range(grouped_data.ngroups):
            size_of_each_group = list(grouped_data.size())[i]
            item1 = int(summed_data['jumlah_item_1'].get_values()[i])
            item2 = int(summed_data['jumlah_item_2'].get_values()[i])
            item3 = int(summed_data['jumlah_item_lbs3'].get_values()[i])
            transaksi1 = int(summed_data['jumlah_transaksi_1'].get_values()[i])
            transaksi2 = int(summed_data['jumlah_transaksi_lbs2'].get_values()[i])
            custom_name = int(summed_data['custom_name'].get_values()[i])
            segmen_title = "Segmen ke-{0}".format(i+1)
            self.knowledge_text.append(segmen_title)
            ket1 = "> Pelanggan pada segmen ke-{0} membeli: ".format(i+1)
            self.knowledge_text.append(ket1)
            if item1 > 0:
                item1_note = "    1 jersey: {0} pelanggan ({1:.2f}%)".format(item1, float(item1) / size_of_each_group * 100)
                self.knowledge_text.append(item1_note)
            if item2 > 0:
                item2_note = "    2 jersey: {0} pelanggan ({1:.2f}%)".format(item2, float(item2) / size_of_each_group * 100)
                self.knowledge_text.append(item2_note)
            if item3 > 0:
                item3_note = "    lebih dari 2 jersey: {0} pelanggan ({1:.2f}%)".format(item3, float(item3) / size_of_each_group * 100)
                self.knowledge_text.append(item3_note)
            self.knowledge_text.append("dalam:")
            if transaksi1 > 0:
                transaksi1_note = "    1x transaksi: {0} pelanggan ({1:.2f}%)".format(transaksi1, float(transaksi1) / size_of_each_group * 100)
                self.knowledge_text.append(transaksi1_note)
            if transaksi2 > 0:
                transaksi2_note = "    lebih dari 1x transaksi: {0} pelanggan ({1:.2f}%)".format(transaksi2, float(transaksi2) / size_of_each_group * 100)
                self.knowledge_text.append(transaksi2_note)
            if custom_name > 0:
                custom_name_note = "> Pelanggan yang membeli custom name sebanyak {0} pelanggan ({1:.2f}%)".format(custom_name, float(custom_name) / size_of_each_group * 100)
                self.knowledge_text.append(custom_name_note)
            new_line = "\n"
            self.knowledge_text.append(new_line)
                 
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
