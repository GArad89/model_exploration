from engine.baisc_entities.graph import *
from engine.baisc_entities.dendrogram import *
from engine.clustering import *
from engine.stopping_criteria.stopCriteria import *
from engine.labeling import TfIdfLabeler
from engine.utils.jsonWorker import *
from .partitionLoop import partition

import importlib

def run_algo(graph,algo_name,params,stopCriteria):
    #parsing from string to algo object
    module = importlib.import_module('engine.clustering.'+algo_name)
    algo_class = getattr(module, algo_name) #we want the algorithm class and not an initialized algorithm
    #algo = class_() #now we have an object
    
    #parsing from string to stop criteria object
    module = importlib.import_module('engine.stopping_criteria.stopCriteria')
    class_ = getattr(module, stopCriteria) 
    stopCri = class_(2) #now we have an object #the 20 is the threshold TODO change later
    dendro=partition(graph, algo_class(), stopCri)

    labeler = TfIdfLabeler.TfIdfLabeler(graph, dendro)
    labeler.label()
    
    return dendrogramToJSON(dendro)

def get_info_list():
    return createAlgoParamsJSON();

###tests###


#print(run_algo(DGraph.read_dot("./dot/g2.dot"),"SpectralCluster",None,stopCriteria="SizeCriteria"))
#print(get_info_list())

    
