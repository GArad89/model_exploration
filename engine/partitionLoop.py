from graph import *
from cluster import BranchAndBoundCluster,SpectralCluster
from stopCriteria import *
from dendrogram import Node,Dendrogram
###old code
#def is_simple(dgraph, simpletype = "Size",threshold = 20):
#    
#    if simpletype == "InOutDegree":
#        return InOutDegreeCriteria(threshold).check(dgraph)       
#    elif simpletype == "Cyclometric":
#        return CyclometricCriteria(threshold).check(dgraph)
#    else:
#       return SizeCriteria(threshold).check(dgraph)
#
#def cluster(dgraph,  clustertype = "SpectralClustering"):
#    
#    if clustertype == "BranchAndBound":
#        return BranchAndBoundCluster(dgraph,state_subset)
#    else:
#        return SpectralCluster.cluster(dgraph)
#



#need to check if we want to add a stop critrea for after x runs.    
def partition(dgraph, clustering_algo, stopCri, state_subset = None, simpletype = "Size", threshold = 20, dendrogram = None, rootnode = 0):

    projected_graph = dgraph.project(state_subset)
    #print(projected_graph.nodes())
    
    if dendrogram == None:
        dendrogram = Dendrogram(dgraph)
    else:
        projected_graph = dgraph.project(state_subset)
        dendrogram.add_node(Node(rootnode,state_subset,projected_graph))
        dendrogram.add_leaf(rootnode,len(dendrogram.nodes())-1)
        rootnode=len(dendrogram.nodes())-1 #need to make sure rootnode won't be changed by the recursion calls
        
    if stopCri.check(dgraph):
        return

    clusters = clustering_algo.cluster(projected_graph)
    for cluster_iter in clusters:
         partition(dgraph,clustering_algo, stopCri, cluster_iter)

    return dendrogram

#tests area

def spectralcluster_test():

    g = DGraph.read_dot("./dot/g2.dot")
    print("testing SpectralCluster on g2.dot:")
    print(SpectralCluster.cluster(g))
    print("\n")

def partition_test():

    den = None
    g = DGraph.read_dot("./dot/g2.dot")
    den=partition(g,g.nodes()) 
    #print(len(den.node_list))  #should be 1 (root node only)
    print("testing partition on g2.dot:")
    den=partition(g,g.nodes(),"SpectralClustering","Size",7)
    print("the number of super-nodes in the dendogram (including the root):")
    print(len(den.node_list))  #should be 4. but gives 2 currently
    print("the number of nodes in the 1st node (1st one after the root):")
    print(den.node_list[1].subset)

spectralcluster_test()
partition_test()
