from .label import GraphLabeler, labeling_on_type
import networkx as nx

import logging

log = logging.getLogger(__name__)

class PageRankLabeler(GraphLabeler):
    
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)

    def label(self, label_size=3):
        ranks = nx.pagerank_numpy(self.graph.dgraph)
        def n_important_nodes(subset, n):
            nonlocal ranks
            k = min(n, len(subset))
            subset_sorted = sorted(subset, key=lambda node: ranks[node], reverse=True)
            return subset_sorted[:k]

        def n_important_edges(subset_edges, n):
            nonlocal ranks
            edges_ranks = {}
            for edge in subset_edges:
                out_node = edge[0]
                out_node_rank = ranks[out_node]
                edges_ranks[(edge[0], edge[1])] = out_node_rank / len(self.graph.dgraph.out_edges())

            log.debug(edges_ranks)

            k = min(n, len(subset_edges))
            subset_sorted = sorted(subset_edges, key=lambda edge: edges_ranks[(edge[0], edge[1])], reverse=True)
            return subset_sorted[:k]
        chosen_labels=[]
        for super_node in self.dendrogram.nodes()[1:]:
            if self.source == labeling_on_type.NODES:
                chosen_nodes = n_important_nodes(super_node.subset, label_size)
                chosen_labels = [self.graph.node_attr(node, 'label') for node in chosen_nodes]
            elif self.source == labeling_on_type.EDGES:
                chosen_edges = n_important_edges(super_node.projected_graph.edges(), label_size)
                chosen_labels = [self.graph.dgraph.edges[(edge[0], edge[1])].get('label','') for edge in chosen_edges]
            else:  #both edges and nodes
                chosen_nodes = n_important_nodes(super_node.subset, label_size)
                chosen_labels_nodes = [self.graph.node_attr(node, 'label') for node in chosen_nodes]
                chosen_edges = n_important_edges(super_node.projected_graph.edges(), label_size)
                chosen_labels_edges = [self.graph.dgraph.edges[(edge[0], edge[1])].get('label','') for edge in chosen_edges]
                for i in range(int(len(chosen_labels_nodes)/2)): #since the edge and node ranks arent normalized, they can't be compared. we "mix" the labels as such: node,edge,node...
                    chosen_labels+=[chosen_labels_nodes[i]]
                    chosen_labels+=[chosen_labels_edges[i]]
            chosen_labels = [l for l in chosen_labels if l]
            log.debug(chosen_labels)
            # super_node.label = super().shorten_label(','.join(chosen_labels))
            super_node.label = super().shorten_label(chosen_labels)
