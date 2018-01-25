from .label import DendrogramLabeler,labeling_on_type
from .RankingLabeler import RankingLabeler
import networkx as nx
import numpy as np

import logging

log = logging.getLogger(__name__)

np.set_printoptions(precision=5)

class RandomWalkLabeler(RankingLabeler):

    MIN_DELTA = 0.001
        
    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES, max_labels = 3):
        self.google_mat = nx.google_matrix(graph.dgraph)
        self.google_mat = np.array(self.google_mat)
        super().__init__(graph, dendrogram, source, max_labels)

    def fill_ranking_dictionary_with_nodes(self):
        ## X(G^t)=X   X=[1/n,1/n,...,1/n] TODO: imporve this, only choose root nodes
        n = len(self.graph.nodes())
        X = np.ones(n) * (1.0 / n)
        diff = 1
        while diff > self.MIN_DELTA:
            temp = np.matmul(X, self.google_mat)
            diff = max([abs(X[i] - temp[i]) for i in range(n)])
            X = temp

        nodes = self.graph.dgraph.nodes()
        self.ranks_dict = dict(zip(nodes, X))

    def fill_ranking_dictionary_with_edges(self):
        super().fill_ranking_dictionary_with_edges()


            
            

              
