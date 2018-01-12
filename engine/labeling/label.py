from abc import ABC, abstractmethod
from enum import Enum

>>> class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3


class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram, source, lableling_on = labeling_on_type.EDGES_AND_NODES):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source
        self.labeling_on = lableling_on


    def get_labels(self,node):
         subgraph = node.projected_graph.dgraph
         # get all inner labels (nodes and edges)
         
         labels = [attrs.get('label','') for _, attrs in get_list_of_lables()]
         # filter out empty ones
         labels = list(filter(None, labels))
         # uniqify
         labels = set(labels)
         return labels

    def get_list_of_lables():
        [attrs.get('label','') for _, attrs in 
                        itertools.chain()
        return {
            labeling_on_type.EDGES: itertools.chain(subgraph.edges.items()),
            labeling_on_type.NODES: itertools.chain(subgraph.nodes.items()),
            labeling_on_type.EDGES_AND_NODES: itertools.chain(subgraph.edges.items(), subgraph.nodes.items())
        }.get(self.lableling_on, [])    


    @abstractmethod
    def label(self):
        pass



