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
       return (dgraph.max_in_out_degree() <= self.threshold) | (dgraph.number_of_nodes() <= 1)


class CyclometricCriteria(StopCriteria):  #Todo: extension print values to learn on how to suggest the users what values to use

    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, dgraph, **params):
        cyclomertic_complexity = dgraph.number_of_edges() - dgraph.number_of_nodes() + 2 * dgraph.number_of_components()
        return (cyclomertic_complexity < self.threshold) | (dgraph.number_of_nodes() <= 1)


        

