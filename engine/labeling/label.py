from abc import ABC, abstractmethod


class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram):
        self.graph = graph
        self.dendrogram = dendrogram

    @abstractmethod
    def label(self):
        pass



