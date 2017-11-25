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
    def getParams():
        return {},[] #TODO

    
    def cluster(self, dgraph):
        pass #TODO: implement

class SpectralCluster (Cluster):

    def getParams():
        form = [{'key': 'n', 'type': 'text'},{'key': 'affinity', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'affinity' : {'type': 'string', 'title': 'affinity'}
            }
        return schema, form
        




        
    def cluster(dgraph, n = 2, affinity='amg'):
        """
        just the basics required for the SpectralClustering algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        
        #SpectralClustering
        sc = SpectralClustering(n)
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


