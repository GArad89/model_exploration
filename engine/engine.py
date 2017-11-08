from graph import *
from cluster import BranchAndBoundCluster,SpectralCluster
from partition import *
from dendrogram import Node,Dendrogram

def is_simple(dgraph, simpletype = "Size",threshold = 20):
    
    if simpletype == "InOutDegree":
        return InOutDegreeCriteria(threshold).check(dgraph)       
    elif simpletype == "Cyclometric":
        return CyclometricCriteria(threshold).check(dgraph)
    else:
       return SizeCriteria(threshold).check(dgraph)

def cluster(dgraph,  clustertype = "SpectralClustering"):
    
    if clustertype == "BranchAndBound":
        return BranchAndBoundCluster(dgraph,state_subset)
    else:
        return SpectralCluster.cluster(dgraph)

def partition(dgraph, state_subset, clustertype = "SpectralClustering", simpletype = "Size", threshold = 20, dendrogram = None, rootnode = 0):

    print(state_subset)
    projected_graph = dgraph.project(state_subset)
    
    if dendrogram == None:
        dendrogram = Dendrogram(dgraph)
    else:   
        dendrogram.add_node(Node(rootnode,state_subset,projected_graph))
        dandrogram.add_leaf(rootnode,len(dendrogram.nodes())-1)
        rootnode=len(dendrogram.nodes())-1 #need to make sure rootnode won't be changed by the recursion calls
        
    if is_simple(projected_graph, simpletype, threshold):
        return

    clusters = cluster(projected_graph, clustertype)
    for clutser in clusters:
         partition(dgraph, cluster, clustertype, simpletype , threshold , dendrogram , rootnode )

    return dendrogram

#tests area

def spectralcluster_test():

    g = DGraph.read_dot("./dot/g2.dot")
    print(cluster(g))

def partition_test():

    den = None
    g = DGraph.read_dot("./dot/g2.dot")
    den=partition(g,g.nodes()) 
    #print(len(den.node_list))  #should be 1 (root node only)
    den=partition(g,g.nodes(),"SpectralClustering","Size",2) 
    print(len(den.node_list))  #should be 3. but gives 2 currently
    print(den.node_list[1].subset)

#spectralcluster_test()
partition_test()
