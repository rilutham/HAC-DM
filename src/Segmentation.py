'''
Created on May 12, 2015

@author: rilutham
'''
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

class Segmentation():
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        # Data which is use for distance measure
        self.data = data
        self.n_cols = len(self.data.columns)
        n_rows = len(self.data.index)
        self.dist_data = self.data.ix[:,1:self.n_cols]
        self.dendro_label = self.data.ix[0:n_rows,0:1]
        
        self.count_distance()
        self.do_segmentation()
    
    def count_distance(self):   
        # Count the distance with jaccard distance
        self.row_dist = pd.DataFrame(squareform(pdist(self.dist_data, metric='jaccard')))
        self.row_dist = self.row_dist.fillna(0)
        
    def do_segmentation(self):  
        # Cluster using complete linkage
        self.row_clusters = linkage(self.row_dist, method='complete')
        
        # Generate dendrogram and place it into canvas
        dendrogram(self.row_clusters, labels=self.dendro_label.values)
           
    def get_result_data(self):
        
        self.df_result_data = self.data
        # Generate cluster index
        cluster_index = fcluster(self.row_clusters, t=5, criterion='maxclust')
        # Add new column (cluster_index) to result data
        self.df_result_data['ID_Segmen'] = cluster_index        
        