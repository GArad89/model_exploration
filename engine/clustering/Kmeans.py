from .cluster_abstract import Cluster
from sklearn.cluster import KMeans


##running but not giving desired results
class KmeansClustering (Cluster):

    def __init__(self, n=2):
        self.n = n

    def get_params():
        form = [{'key': 'n', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            }
        return schema, form

    
    def cluster(self, dgraph):
        """
        just the basics required for the Kmeans algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()

        adj_mat=adj_mat.max() - adj_mat
        #print(adj_mat)
       # adj_mat=np.add( adj_mat, adj_mat.transpose() )
        
        #KMeans clustering
        ##eigen_values, eigen_vectors = np.linalg.eigh(adj_mat)
        #adj_mat=np.exp(- adj_mat ** 2 / (2.* 0.3 ** 2))
        #np.fill_diagonal(adj_mat,0)
        #print(adj_mat)
        km = KMeans(self.n).fit(adj_mat)
        #km.fit(adj_mat)
        result=km.labels_
        #print(km.cluster_centers_)
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
        





