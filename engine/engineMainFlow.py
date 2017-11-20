from graph import *
from dendrogram import *
from cluster import *
from partitionLoop import *
from stopCritereia import *
from jsonWorker import *

def run_algo(graph,algo_name,params,stopCriteria):
    #parsing from string to algo object
    module = __import__('cluster')
    class_ = getattr(module, algo_name)
    algo = class_() #now we have an object

    
    #parsing from string to stop criteria object
    module = __import__('stopCriteria')
    class_ = getattr(module, stopCriteria)
    stopCri = class_(20) #now we have an object #the 20 is the threshold TODO change later
    
    return partition(graph, algo,stopCri)

def get_info_list():
    return createAlgoParamsJSON();




    
