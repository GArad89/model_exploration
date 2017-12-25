from abc import ABC, abstractmethod


class SuperstateGraphLabeler(ABC):

    def __init__(self, graph, superstates):
        self.graph = graph
        self.superstates = superstates

    @abstractmethod
    def label(self):
        pass



