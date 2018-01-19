from abc import ABC, abstractmethod
import itertools
from enum import Enum
import re

class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3

class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source


    def get_labels(self,subgraph):
         # subgraph = node.projected_graph.dgraph
         # get all inner labels (nodes and edges)
         
         labels = [attrs.get('label','') for _, attrs in self.get_list_of_lables(subgraph)]
         # filter out empty ones
         labels = list(filter(None, labels))
         # uniqify
         labels = set(labels)
         return labels

    def get_list_of_lables(self,subgraph):
        return {
            labeling_on_type.EDGES: itertools.chain(subgraph.edges.items()),
            labeling_on_type.NODES: itertools.chain(subgraph.nodes.items()),
            labeling_on_type.EDGES_AND_NODES: itertools.chain(subgraph.edges.items(), subgraph.nodes.items())
        }.get(self.source, [])

    def shorten_label(self, lables_list, max_lables=3):
        lables_list = list(lables_list)
        l = len(lables_list)
        if l > max_lables:
            newlist = [lables_list[0]]
            print(newlist)
            for i in range(1, max_lables - 1):
                newlist += [lables_list[(l // (max_lables - 1)) * i]]
            newlist += [lables_list[-1]]
            return "\n".join(newlist)
        else:
            return "\n".join(lables_list)

    @abstractmethod
    def label(self):
        pass



