from .label import GraphLabeler
import networkx as nx
import numpy as np

np.set_printoptions(precision=5)

class RandomWalkLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)
        self.laplacian_mat = np.array(nx.directed_laplacian_matrix(self.graph.dgraph))

    def label(self, iterations=1000):

        print(self.laplacian_mat) # Y.S: not sure why some values are negative.

        n = len(self.laplacian_mat)
        x = np.zeros(n)
        x[0] = 1

        m_t = self.laplacian_mat
        for i in range(iterations):
            m_t = np.matmul(m_t, self.laplacian_mat)

        x = x @ m_t

