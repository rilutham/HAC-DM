""" 
Customer Segmentation using Hierarchical Agglomerative Clustering
--- Undergraduate Thesis Project ---

Riky Lutfi Hamzah
Informatics Engineering 
Indonesia Computer University
"""

import sys
import sip
sip.setapi('QString', 3)
sip.setapi('QVariant', 3)
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from PyQt4 import QtGui

class ApplicationWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Customer Segmentation App")
        
        # QPushButton for import data
        self.btn_import = QtGui.QPushButton('Import', self)
        self.btn_import.clicked.connect(self.import_csv)
        
        # TableWidget for imported data
        self.raw_data_table = QtGui.QTableWidget(self)
        
        # QPushButton for clustering the customer data
        btn_segmen = QtGui.QPushButton('Process', self)
        btn_segmen.clicked.connect(self.segmen)
        
        # Canvas for Dendrogram
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.toolbar.hide() # For hide the matplotlib toolbar
        
        # TableWidget for result data
        self.result_data_table = QtGui.QTableWidget(self)
        
        # QPushButton for save result data
        self.btn_save = QtGui.QPushButton('Save', self)
        self.btn_save.clicked.connect(self.save_csv)
        
        # Displaying the widget
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.btn_import)
        self.layoutVertical.addWidget(self.raw_data_table)
        self.layoutVertical.addWidget(btn_segmen)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.toolbar)
        self.layoutVertical.addWidget(self.result_data_table)
        self.layoutVertical.addWidget(self.btn_save)
        
                    
    def import_csv(self):
        # Provides a dialog that allow users to select only *.csv file.
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.csv)")
        
        # Read the *csv file and store it into DataFrame
        global df_raw_data
        df_raw_data  = pd.DataFrame.from_csv(file_name,header=0, index_col=False)
        
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
    
    def save_csv(self):
        # Provides a dialog that allow users to give file name and location on disk.
        file_name_save = QtGui.QFileDialog.getOpenFileName(self, 'Save File',".","(*.csv)")
        
        # Write DataFrame into *.csv file.
        df_raw_data.to_csv(file_name_save, sep=',', index=False)
        
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
        df_result_data.insert(loc=n_cols, column="ID_Segmen", value=cluster_index)        
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
          
if __name__ == '__main__':  
    app = QtGui.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())