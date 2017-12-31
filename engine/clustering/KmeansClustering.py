from .cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
from sklearn.cluster import SpectralClustering, KMeans
import networkx as nx
import numpy as np


##running but not giving desired results
class KmeansClustering (Cluster):

    def getParams():
        form = [{'key': 'n', 'type': 'text'},{'key': 'affinity', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'affinity' : {'type': 'string', 'title': 'affinity'}
            }
        return schema, form

    
    def cluster(dgraph, params={'n':2}):
        """
        just the basics required for the Kmeans algorithm for now.
        need to test what kind of output it gives.
        """
        pos=nx.spectral_layout(dgraph.dgraph)
        adj_mat=[]
        for node in dgraph.nodes():
            temp=pos.get(str(node),None)
            adj_mat+=[temp]

        km = KMeans(params.get('n',2)).fit(adj_mat)

        result=km.labels_
        output=[];
        dnodes=list(dgraph.nodes())
        for i in range(0,max(result)+1):
            temp_list=[];
            for j in range(0,len(result)):
                if result[j]!=i:
                    temp_list+=[dnodes[j]]
            output.append(temp_list)
        return output
        





