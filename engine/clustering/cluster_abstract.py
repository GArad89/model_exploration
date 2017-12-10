from abc import ABC, abstractmethod


class Cluster(ABC):

    @abstractmethod
    def cluster(self, dgraph):
        """Returns a list of set of states for dgraph
        sets can be joint
        """





