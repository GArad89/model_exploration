from graph import *
from cluster import BranchAndBoundCluster,SpectralCluster
from partition import SizeCriteria
from dendrogram import Node,Dendrogram

def is_simple(dgraph, simpletype = SizeCriteria ,threshold = 20):
      
     return simpletype(threshold).check(dgraph)

def cluster(dgraph,  clustertype = SpectralCluster, **params):
    
    return clustertype.cluster(dgraph,**params)


#need to check if we want to add a stop critrea for after x runs.    
def partition(dgraph, state_subset, clustertype = SpectralCluster, simpletype = SizeCriteria, threshold = 20, dendrogram = None, rootnode = 0):
    print("check")
    projected_graph = dgraph.project(state_subset)
    #print(projected_graph.nodes())
    
    if dendrogram == None:  #in case no dendrogram was initiated
        dendrogram = Dendrogram(dgraph)
    else:
        if((len(projected_graph.nodes())-2)!=len(dgraph.nodes())): #in case a dendrogram WAS initiated. making sure not to add the root twice
            dendrogram.add_node(Node(rootnode,state_subset,projected_graph))
            dendrogram.add_child(rootnode,len(dendrogram.nodes())-1)
        rootnode = len(dendrogram.nodes())-1 
        
    if is_simple(projected_graph, simpletype, threshold):
        return dendrogram

    clusters = cluster(projected_graph, clustertype)
    for cluster_iter in clusters:
        #print(cluster_iter)
        partition(dgraph, cluster_iter, clustertype, simpletype , threshold , dendrogram , rootnode )

    return dendrogram

#tests area

def spectralcluster_test():

    g = DGraph.read_dot("./dot/g2.dot")
    print("testing SpectralCluster on g2.dot:")
    print(cluster(g))
    print("\n")

def partition_test():

    den = None
    g = DGraph.read_dot("./dot/g2.dot")
    #den=partition(g,g.nodes()) 
    #print(len(den.node_list))  #should be 1 (root node only)
    print("testing partition on g2.dot:")
    den = partition(g,g.nodes(), SpectralCluster, SizeCriteria, 2)
    print("the number of super-nodes in the dendogram (including the root):")
    print(len(den.node_list))  #should be 3.
    
    if(len(den.node_list)>1):
        print("the number of nodes in the 1st node (1st one after the root):")
        print(den.node_list[1].subset)

       
#spectralcluster_test()
partition_test()
