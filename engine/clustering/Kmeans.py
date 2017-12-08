from .cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np


##running but not giving desired results
class KmeansClustering (Cluster):

    def getParams():
        form = [{'key': 'n', 'type': 'text'},{'key': 'affinity', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'affinity' : {'type': 'string', 'title': 'affinity'}
            }
        return schema, form

    
    def cluster(dgraph, n = 2):
        """
        just the basics required for the Kmeans algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        if("inNode" in dgraph.nodes()):
            adj_mat=np.delete(adj_mat, np.s_[-2::], 1)
            adj_mat=np.delete(adj_mat, np.s_[-2::], 0)
        adj_mat=adj_mat.max()-adj_mat
        print(adj_mat)
       # adj_mat=np.add( adj_mat, adj_mat.transpose() )
        
        #KMeans clustering
        ##eigen_values, eigen_vectors = np.linalg.eigh(adj_mat)
        #adj_mat=np.exp(- adj_mat ** 2 / (2.* 0.3 ** 2))
        #np.fill_diagonal(adj_mat,0)
        #print(adj_mat)
        km = KMeans(n).fit(adj_mat)
        #km.fit(adj_mat)
        result=km.labels_
        print(km.cluster_centers_)
        #seperating the result list to lists for each cluster (1= the node is in the substae 0= the node is not in the state)
        output=[];
        for i in range(0,max(result)+1):
            temp_list=[];
            for j in range(0,len(result)):
                if result[j]!=i:
                    temp_list+=[0]
                else:
                    temp_list+=[1]
            output.append(temp_list)
        return output
        





