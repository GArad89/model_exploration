from .label import DendrogramLabeler,labeling_on_type
from .RankingLabeler import RankingLabeler
import networkx as nx
import numpy as np

import logging

log = logging.getLogger(__name__)

np.set_printoptions(precision=5)

class RandomWalkLabeler(RankingLabeler):
        
    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES, max_labels = 3):
        self.google_mat = nx.google_matrix(graph.dgraph)
        self.google_mat = np.array(self.google_mat)
        super().__init__(graph, dendrogram, source, max_labels)

    def fill_ranking_dictionary_with_nodes(self):
        ## X(G^t)=X   X=[1/n,1/n,...,1/n]
        n = len(self.graph.nodes())
        X = np.zeros(n)
        nodes = self.graph.dgraph.nodes()
        for i in range(n):
            X[i] = 1 / n
        chk = False
        while (chk == False):
            temp = np.matmul(X, self.google_mat)
            chk = True
            for i in range(n):
                if (abs(X[i] - temp[i]) > 0.001):
                    chk = False
            if (chk == False):
                X = temp

        X = temp
        self.ranks_dict = dict(zip(nodes, X))

    def fill_ranking_dictionary_with_edges(self):
        super().fill_ranking_dictionary_with_edges()


            
            

              
