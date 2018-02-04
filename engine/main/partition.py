from engine.stopping_criteria.stop_criteria import SizeCriteria
from engine.basic_entities.dendrogram import Node,Dendrogram

import random
import logging
log = logging.getLogger(__name__)


def _add_dendrogram_node(dendrogram, rootnode, state_subset, projected_graph):
    dendrogram.add_node(Node(rootnode, state_subset, projected_graph))
    dendrogram.add_child(rootnode, len(dendrogram.nodes()) - 1)


def _fix_single_label_partition(clusters):

    if len(clusters) > 1:  # i.e. all nodes got the same label due to symmetry, choose arbitrarily and remove
        return clusters
    nodes = clusters[0]
    special_index = random.randint(0, len(nodes) - 1)
    clusters.append([clusters[0].pop(special_index)])
    return clusters


def _partition(dgraph, state_subset, clustering_algo, stop_criterion, dendrogram, rootnode):
    projected_graph = dgraph.project(state_subset)
    #log.debug(state_subset)
    # if not first iteration
    if len(projected_graph.nodes()) != len(dgraph.nodes()): #in case a dendrogram WAS initiated. making sure not to add the root twice
        if ((len(projected_graph.nodes()) == 1) and ("initial" in projected_graph.nodes())):
            return
        _add_dendrogram_node(dendrogram, rootnode, state_subset, projected_graph)
        rootnode = len(dendrogram.nodes())-1
        # check if the iteration reached the stop criterion
        if stop_criterion.check(projected_graph):
            if len(projected_graph.nodes()) == 1:
                return dendrogram
            for n in projected_graph.nodes():
                _add_dendrogram_node(dendrogram, rootnode, [n], dgraph.project(n))
            return dendrogram

    #run clustering algorithm and run parition on each cluster
    clusters = clustering_algo.cluster(projected_graph)
    clusters = _fix_single_label_partition(clusters)
    log.debug(clusters)
    for cluster_iter in clusters:
        _partition(dgraph, cluster_iter, clustering_algo, stop_criterion , dendrogram , rootnode)

    return dendrogram


def partition(dgraph, clustering_algo, stop_criterion=SizeCriteria(20)):
    """recursivly partition the inputted graph, using the clustering algorithm.
       the partition iteration stops when stop_criterion is reached.
       args:
           dgraph-(DGraph) a directed graph implementation
           clustering_algo-(a class inheriting from Cluster located in engine.clustering.cluster_abstract) the clustering algorithm to be used.
           stop_criterion-(a class inheriting from StopCriteria located in engine.stopping_criteria.stop_criteria) the stop critrea for the iteration.
    """
    dendrogram = Dendrogram(dgraph)
    return _partition(dgraph, state_subset=dgraph.nodes(), clustering_algo=clustering_algo, stop_criterion=stop_criterion, dendrogram=dendrogram, rootnode = 0)
