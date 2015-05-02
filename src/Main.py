""" 
Customer Segmentation using Hierarchical Agglomerative Clustering

Riky Lutfi Hamzah
Informatics Engineering 
Indonesia Computer University
"""

import sip
sip.setapi('QString', 3)
sip.setapi('QVariant', 3)
import pandas as pd

from PyQt4 import QtGui

class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.dataTable = QtGui.QTableWidget(self)
        
        self.btnImport = QtGui.QPushButton('Import', self)
        self.btnImport.clicked.connect(self.importcsv)
    
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.dataTable)
        self.layoutVertical.addWidget(self.btnImport)
                    
    def importcsv(self):
        # Provides a dialog that allow users to select only *.csv file.
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.csv)")
        
        # Read the *csv file and store it into DataFrame
        df  = pd.DataFrame.from_csv(self.fileName,header=0, index_col=False)
        
        # Specify the number of rows and columns of table
        self.dataTable.setRowCount(len(df.index))
        self.dataTable.setColumnCount(len(df.columns))
        
        # Set cell value of table
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.dataTable.setItem(i,j,QtGui.QTableWidgetItem(str(df.iget_value(i, j))))
        
        # Create the columns header
        self.dataTable.setHorizontalHeaderLabels(list(df.columns.values))

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())