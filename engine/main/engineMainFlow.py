from engine.clustering import get_cluster_algorithm
from engine.stopping_criteria import get_stopping_criterion
from engine.labeling import get_labeling_method
from engine.utils.jsonWorker import serialize_dendrogram
from .partitionLoop import partition
import logging

log = logging.getLogger(__name__)

import importlib

def run_algorithm(graph, algo_name, params, stopping_criterion, stopping_parameter, labeling_method, labeling_source):
    #parsing from string + paramsto algo object
    algo_class = get_cluster_algorithm(algo_name) #we want the algorithm class
    algo = algo_class(**params) #now we have an object
    
    stopping_criterion_class = get_stopping_criterion(stopping_criterion)
    stopping_criterion = stopping_criterion_class(stopping_parameter) # now we have an object
    dendrogram = partition(graph, algo, stopping_criterion)

    labeler_class = get_labeling_method(labeling_method)
    labeler = labeler_class(graph, dendrogram, labeling_source)
    labeler.label()

    log.info(len(dendrogram.nodes()))

    for super_node in dendrogram.nodes():
        log.info(super_node.label)

    return serialize_dendrogram(dendrogram)

