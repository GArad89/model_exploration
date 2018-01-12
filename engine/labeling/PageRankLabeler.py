from .label import GraphLabeler, labeling_on_type
import networkx as nx

import logging

log = logging.getLogger(__name__)

class PageRankLabeler(GraphLabeler):
    
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)

    def label(self, label_size=3):

        ranks = nx.pagerank(self.graph.dgraph)

        def n_important_nodes(subset, n):
            nonlocal ranks
            k = min(n, len(subset))
            subset_sorted = sorted(subset, key=lambda node: ranks[node], reverse=True)
            return subset_sorted[:k]

        for super_node in self.dendrogram.nodes():
            chosen_nodes = n_important_nodes(super_node.subset, label_size)
            chosen_nodes_labels = [self.graph.node_attr(node, 'label') for node in chosen_nodes]
            super_node.label = shortenlabel(','.join(chosen_nodes_labels))



