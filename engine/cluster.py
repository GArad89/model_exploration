from abc import ABC, abstractmethod
from graph import DGraph
from sklearn.cluster import SpectralClustering
import numpy as np
import networkx as nx

class Cluster(ABC):

    @abstractmethod
    def cluster(self, dgraph):
        """Returns a list of set of states for dgraph
        sets can be joint
        """

class BranchAndBoundCluster (Cluster):
    def cluster(self, dgraph):
        pass #TODO: implement

class SpectralCluster (Cluster):
    def cluster(dgraph, n = 2):
        """
        just the basics required for the SpectralClustering algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        if("inNode" in dgraph.nodes()):
            adj_mat=np.delete(adj_mat, np.s_[-2::], 1)
            adj_mat=np.delete(adj_mat, np.s_[-2::], 0)
        
        #SpectralClustering
        sc = SpectralClustering(n, affinity='precomputed')
        sc.fit(adj_mat)
        result=sc.labels_

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


