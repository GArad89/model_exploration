from .label import GraphLabeler
import networkx as nx
import numpy as np

np.set_printoptions(precision=5)

class RandomWalkLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)
        self.laplacian_mat = np.array(nx.directed_laplacian_matrix(self.graph.dgraph, alpha=0.1, walk_type='pagerank'))

    def label(self, iterations=1000):

        n = len(self.laplacian_mat)
        x = np.zeros(n)
        x[0] = 1

        m_t = np.matrix(self.laplacian_mat)
        for i in range(iterations):
            m_t = np.matmul(m_t, self.laplacian_mat)

        x = np.matmul(x, m_t)
        print(x)

