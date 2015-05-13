#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Segmentation.py
@author: rilutham
"""

from PyQt4 import QtGui
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

class Segmentation(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        super(Segmentation, self).__init__()
        # Data which is use for distance measure
        self.data = data
        self.n_cols = len(self.data.columns)
        n_rows = len(self.data.index)
        self.dist_data = self.data.ix[:, 1:self.n_cols]
        self.dendro_label = self.data.ix[0:n_rows, 0:1]
        self.df_result_data = None
        
        # Call initial methods
        self.count_distance()
        self.do_segmentation()
    
    def count_distance(self):   
        # Count the distance with jaccard distance
        self.row_dist = pd.DataFrame(squareform(pdist(self.dist_data, metric='jaccard')))
        self.row_dist = self.row_dist.fillna(0)
        
    def do_segmentation(self):  
        # Cluster using complete linkage
        self.row_clusters = linkage(self.row_dist, method='complete')
        
        # Generate dendrogram and labels
        dendrogram(self.row_clusters,labels = self.dendro_label.values)
        
        self.df_result_data = self.data
        # Generate cluster index
        cluster_index = fcluster(self.row_clusters, t=2, criterion='maxclust')
        # Add new column (cluster_index) to result data
        self.df_result_data['ID_Segmen'] = cluster_index
        
           
    def refresh_result_data(self, treshold):
        # Generate dendrogram and labels
        dendrogram(self.row_clusters, color_threshold=treshold ,labels = self.dendro_label.values)
        
        self.df_result_data = self.data
        # Generate cluster index
        cluster_index = fcluster(self.row_clusters, t=treshold, criterion='distance')
        # Add new column (cluster_index) to result data
        self.df_result_data['ID_Segmen'] = cluster_index
        