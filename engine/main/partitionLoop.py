from ..baisc_entities.graph import *
from ..clustering import SpectralCluster, minimum_cut, Kmeans, Branch_and_Bound
from ..stopping_criteria.stopCriteria import *
from ..baisc_entities.dendrogram import Node,Dendrogram


def _partition(dgraph, state_subset, clustering_algo, stop_criterion, dendrogram, rootnode):
    projected_graph = dgraph.project(state_subset)

    # if not first iteration
    if len(projected_graph.nodes()) != len(dgraph.nodes()): #in case a dendrogram WAS initiated. making sure not to add the root twice
        dendrogram.add_node(Node(rootnode,state_subset,projected_graph))
        dendrogram.add_child(rootnode,len(dendrogram.nodes())-1)
        rootnode = len(dendrogram.nodes())-1
    #print(dendrogram.nodes()[rootnode].child())
    if stop_criterion.check(projected_graph):
        #print("check2")
        return dendrogram
    #print(clustering_algo.cluster)
    clusters = clustering_algo.cluster(projected_graph)
    #print("clusters: ", clusters)
    for cluster_iter in clusters:
        _partition(dgraph, cluster_iter, clustering_algo, stop_criterion , dendrogram , rootnode )

    return dendrogram


def partition(dgraph, clustering_algo, stop_criterion = SizeCriteria(20)):
    dendrogram = Dendrogram(dgraph)
    return _partition(dgraph, state_subset=dgraph.nodes(), clustering_algo=clustering_algo, stop_criterion=stop_criterion, dendrogram=dendrogram, rootnode = 0)
