from .graph import *
from .cluster import BranchAndBoundCluster,SpectralCluster, KmeansClustering
from .stopCriteria import *
from .dendrogram import Cluster,Dendrogram

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
def partition(dgraph, state_subset=None, clustering_algo = SpectralCluster, stopCri = SizeCriteria(20), dendrogram = None, parent_cluster = None):
    projected_graph = dgraph.project(state_subset)
    #print(projected_graph.nodes())
    #print(projected_graph.nodes())
    if dendrogram == None:  #in case no dendrogram was initiated
        dendrogram = Dendrogram(dgraph)
        parent_cluster = dendrogram.root_cluster
        new_cluster = parent_cluster
    else:
        if((len(projected_graph.nodes())-2)!=len(dgraph.nodes())): #in case a dendrogram WAS initiated. making sure not to add the root twice
            new_cluster = Cluster(parent_cluster,state_subset,projected_graph)
            dendrogram.add_cluster(new_cluster, parent_cluster)

    #print(dendrogram.nodes()[rootnode].child())
    if stopCri.check(projected_graph):
        #print("check2")
        return dendrogram
    #print(clustering_algo.cluster)
    clusters = clustering_algo.cluster(projected_graph)
    parent_cluster = new_cluster
    #print("clusters: ", clusters)
    for cluster_iter in clusters:
        partition(dgraph, cluster_iter, clustering_algo, stopCri , dendrogram , parent_cluster)

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
