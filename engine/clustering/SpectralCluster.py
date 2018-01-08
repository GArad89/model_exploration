from engine.clustering.cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np


class SpectralCluster(Cluster):
    """ Returns a sparset cut partition of the input dgraph.
        The number of clusters is defined by the input n.
        If len(dgraph.nodes())<n then the number of clusters would be len(dgraph.nodes())
        this clustering method uses sklearn's SpectralClustering method

    """


    def __init__(self, n = 2):
        super().__init__()
        self.n = n


    @staticmethod
    def get_params():
        form = [{'key': 'n', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True}  }
        return schema, form


        
    def cluster(self, dgraph):
        
        #number of clusters can't be bigger than the number of nodes
        if(self.n>=len(dgraph.nodes())): n_clusters=len(dgraph.nodes())-1
        else: n_clusters=self.n
        print(dgraph.nodes())

        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        adj_mat=np.maximum(adj_mat,adj_mat.transpose())

        #SpectralClustering
        sc = SpectralClustering(n_clusters,affinity='precomputed')
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


