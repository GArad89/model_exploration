from ..baisc_entities.graph import *
from .label import GraphLabeler, labeling_on_type

class STLabeling(GraphLabeler):
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)
    
    def label(self):
        for node in self.dendrogram.nodes():
            subgraph = self.graph.subgraph(node.subset)
            spanning_tree=nx.minimum_spanning_tree(subgraph)
            labels = super().get_labels(spanning_tree)
            node.label = '_'.join(labels)
