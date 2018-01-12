from abc import ABC, abstractmethod
import itertools
from enum import Enum
import re

class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3

class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES, max_lables_per_node = 5):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source
        self.max_lables_per_node = max_lables_per_node
 


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

    def shortenlabel(label):
        lables_list = re.split(' |,|_|-',label)
        l = len(lables_list)
        if  l > max_lables_per_node:
            newlist = []
            newlist += lables_list[0]
            for i in range(1,max_lables_per_node-1):
                newlist += lables_list[(l/(max_lables_per_node-1))*i]
            newlist += lables_lisst[-1]
            return ','.join(newlist)
        else:
            return label
            


    @abstractmethod
    def label(self):
        pass



