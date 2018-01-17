from engine.stopping_criteria.stopCriteria import SizeCriteria
from engine.baisc_entities.dendrogram import Node,Dendrogram

import logging
log = logging.getLogger(__name__)


def add_dendrogram_node(dendrogram, rootnode, state_subset, projected_graph):
    dendrogram.add_node(Node(rootnode, state_subset, projected_graph))
    dendrogram.add_child(rootnode, len(dendrogram.nodes()) - 1)


def _partition(dgraph, state_subset, clustering_algo, stop_criterion, dendrogram, rootnode):
    projected_graph = dgraph.project(state_subset)
    #log.debug(state_subset)
    # if not first iteration
    if len(projected_graph.nodes()) != len(dgraph.nodes()): #in case a dendrogram WAS initiated. making sure not to add the root twice

        add_dendrogram_node(dendrogram, rootnode, state_subset, projected_graph)
        rootnode = len(dendrogram.nodes())-1
        # check if the iteration reached the stop criterion
        if stop_criterion.check(projected_graph):
            if len(projected_graph.nodes()) == 1:
                return dendrogram
            for n in projected_graph.nodes():
                add_dendrogram_node(dendrogram, rootnode, [n], dgraph.project(n))
            return dendrogram

    #run clustering algorithm and run parition on each cluster
    clusters = clustering_algo.cluster(projected_graph)
    log.debug(clusters)
    for cluster_iter in clusters:
        _partition(dgraph, cluster_iter, clustering_algo, stop_criterion , dendrogram , rootnode)

    return dendrogram


def partition(dgraph, clustering_algo, stop_criterion=SizeCriteria(20)):
    dendrogram = Dendrogram(dgraph)
    return _partition(dgraph, state_subset=dgraph.nodes(), clustering_algo=clustering_algo, stop_criterion=stop_criterion, dendrogram=dendrogram, rootnode = 0)
