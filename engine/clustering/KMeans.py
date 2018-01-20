from .cluster_abstract import Cluster 
from sklearn.cluster import KMeans 
from networkx import spectral_layout
 
 
class KMeansClustering (Cluster):
    """ Returns a sparset cut partition of the input dgraph.
        The number of clusters is defined by the input n.
        If len(dgraph.nodes())<n then the number of clusters would be len(dgraph.nodes())
        this clustering method uses sklearn's Kmeans method
    """

    def __init__(self, n = 2):
        super().__init__()
        self.n=n
        
    @staticmethod
    def get_params(): 
        form = [{'key': 'n', 'type': 'text'}] 
        schema = { 
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True} 
            } 
        return schema, form 
 
     
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
        km = KMeans(self.n).fit(vector_list) 
        result=km.labels_

        #seperating the result list to lists for each cluster (1= the node is in the substae 0= the node is not in the state)
        dnodes=list(dgraph.nodes()) 
        output = [[] for i in range(0,max(result)+1)];
        # append each node to its cluster 
        for index, value in enumerate(result):
            output[value].append(dnodes[index])

        return output 
         
