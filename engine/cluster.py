from abc import ABC, abstractmethod
from graph import DGraph
from sklearn.cluster import SpectralClustering
import numpy as np

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
    def cluster(self, dgraph):
        """
        just the basics required for the SpectralClustering algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        
        #SpectralClustering
        sc = SpectralClustering(2, affinity='precomputed')
        sc.fit(adj_mat)
