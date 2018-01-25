from engine.clustering.cluster_abstract import Cluster
from engine.basic_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np


class SpectralCluster(Cluster):
    """ Returns a sparset cut partition of the input dgraph.
        The number of clusters is defined by the input n.
        If len(dgraph.nodes())<n then the number of clusters would be len(dgraph.nodes())
        this clustering method uses sklearn's SpectralClustering method
    """

    def __init__(self, n = 2, affinity='precomputed', find_opt_clusters = False):
        super().__init__()
        self.n = n
        self.affinity = affinity
        self.find_opt_clusters = find_opt_clusters


    @staticmethod
    def get_params():
        form = [{'key': 'n', 'type': 'number'}, {'key' : 'find_opt_clusters', 'type' : 'select'}, {'key' : 'affinity'}]
        schema = {
            'find_opt_clusters': {'type': 'boolean', 'enum': ['True', 'False'], 'title': 'Find optimal num. clusters' \
                , 'required': True},
            'n' : {'type': 'integer', 'title': 'Number of Clusters', 'minimum' : 2, 'default': 2, 'required' : True},
            'affinity' : {
                'type' : 'string',
                'title': 'Affinity',
                'enum': ['precomputed', 'rbf', 'sigmoid', 'polynomial', 'poly', 'linear', 'cosine', 'nearest_neighbors'],
            },
        }
        return schema, form

        
    def cluster(self, dgraph):
        """ the actual clustering method
            args: dgraph- (networkx' MultiDigraph) the graph being partitioned
        """
         #number of clusters can't be bigger than the number of nodes
        if(self.n>=len(dgraph.nodes())): n_clusters=len(dgraph.nodes())-1
        else: n_clusters=self.n

        #adjacency matrix
        adj_mat = dgraph.adjacency_matrix()
        # turn to undirected graph
        adj_mat = np.maximum(adj_mat,adj_mat.transpose())

        #SpectralClustering
        if self.find_opt_clusters:
            sc = SpectralClustering(affinity=self.affinity)
            try:
                sc.fit(adj_mat)
            except:
                sc = SpectralClustering(2, affinity=self.affinity)
                sc.fit(adj_mat)
        else:
            sc = SpectralClustering(n_clusters = self.n, affinity=self.affinity)
            sc.fit(adj_mat)
        result = sc.labels_
        ordered_nodes = list(dgraph.nodes())
        # create empty clusters to gather the result
        output = [[] for i in range(0,max(result)+1)];
        # append each node to its cluster

        for index, value in enumerate(result):
            output[value].append(ordered_nodes[index])

        return output


