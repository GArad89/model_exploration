from .cluster_abstract import Cluster 
from engine.baisc_entities.graph import DGraph 
from sklearn.cluster import KMeans 
from networkx import spectral_layout
 
 
class KmeansClustering (Cluster):

    def __init__(self, n = 2):
        super().__init__()
        self.n=n
        
    @staticmethod
    def getParams(): 
        form = [{'key': 'n', 'type': 'text'}] 
        schema = { 
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True} 
            } 
        return schema, form 
 
     
    def cluster(self,dgraph):

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
        output=[]; 
        dnodes=list(dgraph.nodes()) 
        for i in range(0,max(result)+1): 
            temp_list=[]; 
            for j in range(0,len(result)): 
                if result[j]!=i: 
                    temp_list+=[dnodes[j]] 
            output.append(temp_list) 
        return output 
         
