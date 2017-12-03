from .graph import *
from .dendrogram import *
from .cluster import *
from .partitionLoop import *
from .stopCriteria import *
from .jsonWorker import *


def run_algo(graph,algo_name,params,stopCriteria):
    #parsing from string to algo object
    module = __import__('engine.cluster')
    module=getattr(module, 'cluster')
    algo_class = getattr(module, algo_name) #we want the algorithm class and not an initialized algorithm
    #algo = class_() #now we have an object
    
    #parsing from string to stop criteria object
    module = __import__('engine.stopCriteria')
    module=getattr(module, 'stopCriteria')
    class_ = getattr(module, stopCriteria) 
    stopCri = class_(2) #now we have an object #the 20 is the threshold TODO change later
    dendro=partition(graph,graph.nodes(), algo_class, stopCri)
    
    return dendrogramToJSON(dendro)

def get_info_list():
    return createAlgoParamsJSON();

###tests###


#print(run_algo(DGraph.read_dot("./dot/g2.dot"),"SpectralCluster",None,stopCriteria="SizeCriteria"))
#print(get_info_list())

    
