from engine.clustering.cluster_abstract import Cluster
from engine.basic_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np
import logging
log = logging.getLogger(__name__)

class SpectralCluster(Cluster):
    """ Returns a sparset cut partition of the input dgraph.
        The number of clusters is defined by the input n.
        If len(dgraph.nodes())<n then the number of clusters would be len(dgraph.nodes())
        this clustering method uses sklearn's SpectralClustering method
    """

    MAX_K = 8

    def __init__(self, n = 2, affinity='precomputed', find_opt_clusters = False):
        super().__init__()
        self.n = n
        self.affinity = affinity
        self.find_opt_clusters = find_opt_clusters


    @staticmethod
    def get_params():
        form = [{'key': 'n', 'type': 'number'}, {'key' : 'affinity'}] ## {'key' : 'find_opt_clusters', 'type' : 'select'},
        schema = {
            # 'find_opt_clusters': {'type': 'boolean', 'enum': ['True', 'False'], 'title': 'Find optimal num. clusters' \
            #     , 'required': True},
            'n' : {'type': 'integer', 'title': 'Number of Clusters', 'minimum' : 2, 'default': 2, 'required' : True},
            'affinity' : {
                'type' : 'string',
                'title': 'Affinity',
                'enum': ['precomputed', 'rbf', 'sigmoid', 'polynomial', 'poly', 'linear', 'cosine', 'nearest_neighbors'],
            },
        }
        return schema, form


    def _find_k(self, adj, k): ## TODO: add support
          return k
    #     from scipy.spatial.distance import cdist
    #     upper_bound = min(k, self.MAX_K)
    #     k_values = range(2, min(adj_mat.shape[0], self.MAX_K, self.n))
    #     distortion_values = []
    #     for k in k_values:
    #         sc = SpectralClustering(k, affinity=self.affinity)
    #         sc.fit(adj_mat)
    #         distortion = sum(np.min(cdist(adj_mat, sc.labels_, 'euclidean'), axis=1)) / adj_mat.shape[0]
    #         distortion_values.append((k, distortion))
    #     best_k = min(distortion_values, key=lambda x:x[1])
    #     return best_k[0]


    def call_spectral(self, adj_mat, k=2):

        sc = None
        if self.affinity == "nearest_neighbors":
            neighbors = min(10, int(adj_mat.shape[0] / 2))
            neighbors = max(1, neighbors)
            sc = SpectralClustering(k, affinity=self.affinity, n_neighbors= neighbors)
        else:
            neighbors = -1
            sc = SpectralClustering(k, affinity=self.affinity)
        log.debug("Spectral clustering parameters:", k, "-", neighbors, "-",adj_mat.shape[0])
        sc.fit(adj_mat)
        return sc

    def cluster(self, dgraph):
        """ the actual clustering method
            args: dgraph- (networkx' MultiDigraph) the graph being partitioned
        """
        #adjacency matrix
        adj_mat = dgraph.adjacency_matrix()
        # turn to undirected graph
        adj_mat = np.maximum(adj_mat,adj_mat.transpose())

        #SpectralClustering
        # if self.find_opt_clusters: TODO add support in optimal K
        #     try:
        #         k = self._find_k(adj_mat)
        #         log.debug("optimal k found:", k)
        #         sc = self.call_spectral(adj_mat, k)
        #     except Exception as e:
        #         sc = self.call_spectral(adj_mat, 2)
        # else:
        k = min(self.n, adj_mat.shape[0] - 1)
        sc = self.call_spectral(adj_mat, k)
        result = sc.labels_
        ordered_nodes = list(dgraph.nodes())
        # create empty clusters to gather the result
        output = [[] for i in range(0,max(result)+1)];
        # append each node to its cluster

        for index, value in enumerate(result):
            output[value].append(ordered_nodes[index])

        return output


