from abc import ABC, abstractmethod
from cluster import BranchAndBoundCluster,SpectralCluster


class StopCriteria(ABC):

    @abstractmethod
    def check(self, dgraph, **params):
        """Returns a boolean indicating if the partitioning
        procedure needs to be stopped
        """

class SizeCriteria(StopCriteria):

    threshold = 1
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        return dgraph.number_of_nodes() <= self.threshold
    
class InOutDegreeCriteria(StopCriteria):

    threshold = 1
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        pass #TODO: implement

class CyclometricCriteria(StopCriteria):

    threshold = 1
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        pass #TODO: implement

def project(dgraph,state_subset):
    """input: a graph and a set of states
        output: a "model" (just the graph implementation for the dendogram i assume?)
        ***project should be a method instead of a function accrdoig to
        the requirements***
    """    
        
def graph_partition(dgraph, state_subset, clustertype = "SpectralClustering",simpletype = "Size",threshold = 20):

    model = project(dgraph,state_subset)
    
    #is_simple(m)
    if simpletype == "InOutDegree":
        if InOutDegreeCriteria(threshold).check(model) == True:
            return
    elif simpletype=="Cyclometric":
        if CyclometricCriteria(threshold).check(model) == True:
            return
    else:
       if SizeCriteria(threshold).check(model) == True:
           return
    
    #cluster(S) **should either be cluster(M,S) or should be cluster(model) with a way to recognize the "dummy" states
    if clustertype == "BranchAndBound":
        groups = BranchAndBoundCluster(dgraph,state_subset)
    else:
        groups = SpectralCluster(dgraph,state_subset)

        #placeholder until i figure out the exact output for the cluster methods

    """for g in groups:
        graph_partition(dgraph,groups[g])"""
