from abc import ABC, abstractmethod


class StopCriteria(ABC):

    @abstractmethod
    def check(self, dgraph, **params):
        """Returns a boolean indicating if the partitioning
        procedure needs to be stopped
        """
        raise NotImplementedError


class SizeCriteria(StopCriteria):

    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):

        #print("the dgraph number of nodes is: ",dgraph.number_of_nodes())
        return dgraph.number_of_nodes() <= self.threshold


class InOutDegreeCriteria(StopCriteria):

    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
       return (dgraph.maxInOutDegree() <= self.threshold) | (dgraph.number_of_nodes() <= 1)


class CyclometricCriteria(StopCriteria):

    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        return (( dgraph.number_of_nodes() - dgraph.number_of_edges() + 2*dgraph.numberOfComponenets()) < self.threshold) | (dgraph.number_of_nodes() <= 1)


        

