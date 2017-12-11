from ..baisc_entities.graph import *
from ..clustering import SpectralCluster, minimum_cut, Kmeans, Branch_and_Bound
from ..stopping_criteria.stopCriteria import *
from ..baisc_entities.dendrogram import Node,Dendrogram

###old code
"""
def is_simple(dgraph, simpletype = SizeCriteria ,threshold = 20):
      
     return simpletype(threshold).check(dgraph)

def cluster(dgraph,  clustertype = SpectralCluster, **params):
    
    return clustertype.cluster(dgraph,**params)
"""

#need to check if we want to add a stop critrea for after x runs.    
def partition(dgraph, state_subset=None, clustering_algo = SpectralCluster.SpectralCluster, stopCri = SizeCriteria(20), dendrogram = None, rootnode = 0):
    projected_graph = dgraph.project(state_subset)
    #print(projected_graph.nodes())
    #print(projected_graph.nodes())
    if dendrogram == None:  #in case no dendrogram was initiated
        dendrogram = Dendrogram(dgraph)
    else:
        if((len(projected_graph.nodes())-2)!=len(dgraph.nodes())): #in case a dendrogram WAS initiated. making sure not to add the root twice
            dendrogram.add_node(Node(rootnode,state_subset,projected_graph))
            dendrogram.add_child(rootnode,len(dendrogram.nodes())-1)
        rootnode = len(dendrogram.nodes())-1 
    #print(dendrogram.nodes()[rootnode].child())
    if stopCri.check(projected_graph):
        #print("check2")
        return dendrogram
    #print(clustering_algo.cluster)
    clusters = clustering_algo.cluster(projected_graph)
    #print("clusters: ", clusters)
    for cluster_iter in clusters:
        partition(dgraph, cluster_iter, clustering_algo, stopCri , dendrogram , rootnode )

    return dendrogram

def partition_test():

    den = None
    g = DGraph.read_dot("./dot/weighted_g2.dot")
    #den=partition(g,g.nodes()) 
    #print(len(den.node_list))  #should be 1 (root node only)
    print("testing partition on g2.dot for threshold=4:")
    den = partition(g,g.nodes(), SpectralCluster.SpectralCluster, SizeCriteria(4))
    print("the number of super-nodes in the dendogram (including the root):")
    print(len(den.node_list))  #should be 3.
    
    if(len(den.node_list)>1):
        print("the number of nodes in the 1st node (1st one after the root):")
        print(den.node_list[1].subset)
        
    print("testing partition on g2.dot for threshold=2:")
    den = partition(g,g.nodes(), SpectralCluster.SpectralCluster, SizeCriteria(2),dendrogram=None)
    print("the number of super-nodes in the dendogram (including the root):")
    print(len(den.node_list))  #should be 7.
    
    if(len(den.node_list)>1):
        print("the number of nodes in the 6th node (6th one after the root):")
        print(den.node_list[6].subset)
     

       
#spectralcluster_test()
#partition_test()
