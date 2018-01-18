from .label import GraphLabeler
import networkx as nx

class STLabeling(GraphLabeler):
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)
    
    def label(self):
        for node in self.dendrogram.nodes():
            subgraph = self.graph.subgraph(node.subset)
            spanning_tree=nx.minimum_spanning_tree(subgraph)
            labels = super().get_labels(spanning_tree)
            node.label = super().shortenlabel(','.join(labels))
