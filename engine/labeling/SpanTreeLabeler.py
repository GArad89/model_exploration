from ..baisc_entities.graph import *
from .label import GraphLabeler

class STLabeling(SuperstateGraphLabeler):
    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)
    
    def label(self):
        for node in self.dendrogram.nodes():
            node.label = get_label_for_subset(node.subset)

def get_label_for_subset(self, subset):
    subgraph = self.graph.subgraph(subset)
        spanning_tree=nx.minimum_spanning_tree(subgraph)
    
    
    def label_spanning_tree(self, spanningtree):
        label = "";
        for edge in spanningtree.edges():
            edge_data = spanningtree.get_edge_data(edge)
                if 'label' in edge_data:
                    label += edge_data['label']
