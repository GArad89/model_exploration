from abc import ABC, abstractmethod



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
        if("inNode" in dgraph.nodes()):
            return dgraph.number_of_nodes()-2 <= self.threshold
        return dgraph.number_of_nodes()-2 <= self.threshold
    
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


        

