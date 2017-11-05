from abc import ABC, abstractmethod
from scipy.stats.mstats_basic import threshold



class StopCriteria(ABC):

    @abstractmethod
    def check(self, dgraph, **params):
        """Returns a boolean indicating if the partitioning
        procedure needs to be stopped
        """

class SizeCriteria(StopCriteria):

    threshold = 5
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        return dgraph.number_of_nodes() <= self.threshold
    
class InOutDegreeCriteria(StopCriteria):

    threshold = 3
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        return dgraph.maxInOutDegree() <= threshold


class CyclometricCriteria(StopCriteria):

    threshold = 1
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        return ( dgraph.number_of_nodes() - dgraph.number_of_edges() + 2*dgraph.numberOfComponenets()) < threshold


        

