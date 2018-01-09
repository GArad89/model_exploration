from abc import ABC, abstractmethod


class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram, source):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source

    @abstractmethod
    def label(self):
        pass



