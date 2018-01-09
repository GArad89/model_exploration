from engine.baisc_entities.graph import *
from engine.baisc_entities.dendrogram import *
from engine.clustering import get_cluster_algorithm
from engine.stopping_criteria import get_stopping_criterion
from engine.labeling import get_labeling_method
from engine.utils.jsonWorker import *
from .partitionLoop import partition

import importlib

def run_algo(graph, algo_name, params, stopping_criterion, labeling_method):
    #parsing from string + paramsto algo object
    algo_class = get_cluster_algorithm(algo_name) #we want the algorithm class
    algo = algo_class(**params) #now we have an object
    
    #parsing from string to stop criteria object
    class_ = get_stopping_criterion(stopping_criterion)
    # TODO: get parameter from the form
    stopCri = class_(2) #now we have an object #the 20 is the threshold TODO change later
    dendro=partition(graph, algo, stopCri)

    labeler = get_labeling_method(labeling_method)(graph, dendro)
    labeler.label()
    
    return dendrogramToJSON(dendro)

def get_info_list():
    return createAlgoParamsJSON();



    
