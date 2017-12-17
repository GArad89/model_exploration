from engine.clustering.cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np


class SpectralCluster (Cluster):

    def getParams():
        form = [{'key': 'n', 'type': 'text'},{'key': 'affinity', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'affinity' : {'type': 'string', 'title': 'affinity'}
            }
        return schema, form
        




        
    def cluster(dgraph, n = 2, affinity='precomputed'):
        """
        just the basics required for the SpectralClustering algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        #print(adj_mat)
        if("inNode" in dgraph.nodes()):
            adj_mat=np.delete(adj_mat, np.s_[-2::], 1)
            adj_mat=np.delete(adj_mat, np.s_[-2::], 0)
        #print(adj_mat)

        
        #SpectralClustering
        sc = SpectralClustering(2,affinity=affinity)
        sc.fit(adj_mat)
        result=sc.labels_
        #seperating the result list to lists for each cluster (1= the node is in the substae 0= the node is not in the state)
        output=[];
        dnodes=list(dgraph.nodes())
        for i in range(0,max(result)+1):
            temp_list=[];
            for j in range(0,len(result)):
                if result[j]!=i:
                    temp_list+=[dnodes[j]]
            output.append(temp_list)
        return output


