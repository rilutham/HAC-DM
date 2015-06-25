#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Segmentation.py
@author: rilutham
"""

from PyQt4 import QtGui
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.stats import itemfreq
#from sklearn.metrics import silhouette_score


class Segmentation(QtGui.QWidget):
    '''
    Apply Hierarchical Agglomerative Clustering
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
        self.label = self.data.ix[0:n_rows, 0:1]

        # Label for dendrogram
        self.dendro_label = []
        for i in range(n_rows):
            self.dendro_label.append(self.label.values[i][0])

        self.df_result_data = None

        # Call initial methods
        self.count_distance()
        self.do_segmentation()

    def count_distance(self):
        '''
        Count distance beetwen object using jaccard distance
        '''
        self.row_dist = pd.DataFrame(squareform(pdist(self.dist_data, metric='jaccard')))
        self.row_dist = self.row_dist.fillna(0)

    def do_segmentation(self):
        '''
        Apply Complete Linkage method and generate dendrogram
        '''
        # Cluster using complete linkage
        self.row_clusters = linkage(self.row_dist, method='complete')

        self.df_result_data = self.data
        # Generate cluster index
        self.cluster_index = fcluster(self.row_clusters, t=2, criterion='maxclust')

        # Generate dendrogram and labels
        dendrogram(self.row_clusters, labels=self.dendro_label, \
                leaf_font_size=9, leaf_rotation=90)

        # Add new column (cluster_index) to result data
        self.df_result_data['ID_Segmen'] = self.cluster_index

        self.n_cluster = "Jumlah segmen yang terbentuk: {0}".format(max(self.cluster_index))

        freq_of_cluster = dict(itemfreq(self.cluster_index))
        self.summary_list = []
        for key, val in freq_of_cluster.items():
            isi = "Segmen ke-{0}: {1} pelanggan".format(key, val)
            self.summary_list.append(isi)
        # Silhouette
        #a = silhouette_score(self.row_dist, self.df_result_data['ID_Segmen'], metric="precomputed")

    def refresh_result_data(self, treshold):
        '''
        Generate dendrogram with new treshold
        '''
        # Generate dendrogram and labels
        dendrogram(self.row_clusters, color_threshold=treshold, labels=self.dendro_label, \
                   leaf_font_size=9, leaf_rotation=90)

        self.df_result_data = self.data
        # Generate cluster index
        self.cluster_index = fcluster(self.row_clusters, t=treshold, criterion='distance')
        # Add new column (cluster_index) to result data
        self.df_result_data['ID_Segmen'] = self.cluster_index

        freq_of_cluster = dict(itemfreq(self.cluster_index))
        self.summary_list = []
        for key, val in freq_of_cluster.items():
            isi = "Segmen ke-{0}: {1} pelanggan".format(key, val)
            self.summary_list.append(isi)
        self.n_cluster = "Jumlah segmen yang terbentuk: {0}".format(max(self.cluster_index))

        # Silhouette
        #a = silhouette_score(self.row_dist, self.df_result_data['ID_Segmen'], metric="precomputed")

