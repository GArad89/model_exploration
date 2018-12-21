from .cluster_abstract import Cluster 
from sklearn.cluster import KMeans 
from networkx import spectral_layout

from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
 
class KMeansClustering (Cluster):
    """ Returns a sparset cut partition of the input dgraph.
        The number of clusters is defined by the input n.
        If len(dgraph.nodes())<n then the number of clusters would be len(dgraph.nodes())
        this clustering method uses sklearn's Kmeans method
    """

    MAX_K = 8

    def __init__(self, n = 2, find_best_k = False):
        super().__init__()
        self.n=n
        self.find_best_k = find_best_k
        
    @staticmethod
    def get_params(): 
        form = [{'key': 'n', 'type': 'text'}, {'key' : 'find_best_k', 'type' : 'select'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'find_best_k': {'type': 'boolean', 'enum': ['True', 'False'], 'title': 'Find optimal k' \
                , 'required': True},
        }
        return schema, form


    def _find_k(self, vector):

        maxK = range(1, min(len(vector), self.MAX_K, self.n))
        distortion_values = []
        vector = np.array(vector)
        for k in maxK:
            kmeanModel = KMeans(n_clusters=k).fit(vector)
            kmeanModel.fit(vector)
            distortion = sum(np.min(cdist(vector, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / vector.shape[0]
            distortion_values.append((k, distortion))
        best_k = min(distortion_values, key=lambda x: x[1])
        return best_k[0]

    def cluster(self,dgraph):
        """ the actual clustering method
            args: dgraph- (networkx' MultiDigraph) the graph being partitioned
        """
        #number of clusters can't be bigger than the number of nodes
        if(self.n>=len(dgraph.nodes())): n_clusters=len(dgraph.nodes())-1
        else: n_clusters=self.n
     
        ## graph embedding (from node to 2 dimensional vectors))
        embedding=spectral_layout(dgraph.dgraph) 
        vector_list=[]
        for node in dgraph.nodes(): 
            temp=embedding.get(str(node),None) 
            vector_list+=[temp] 
        
        ## Kmeans Clustering
        chosen_k = self.n
        if self.find_best_k:
            chosen_k = self._find_k(vector_list)
        km = KMeans(chosen_k).fit(vector_list)
        result=km.labels_

        #seperating the result list to lists for each cluster (1= the node is in the substae 0= the node is not in the state)
        dnodes=list(dgraph.nodes()) 
        output = [[] for i in range(0,max(result)+1)];
        # append each node to its cluster 
        for index, value in enumerate(result):
            output[value].append(dnodes[index])

        return output 
         
