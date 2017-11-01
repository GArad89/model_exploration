from abc import ABC, abstractmethod

class Cluster(ABC)

    @abstractmethod
    def cluster(self, dgraph):
        """Returns a list of set of states for dgraph
        sets can be joint
        """

class BranchAndBoundCluster (Cluster):
    def cluster(self, dgraph):
        pass #TODO: implement

class SpectralCluster (Cluster):
    def cluster(self, dgraph):
        pass #TODO: implement
