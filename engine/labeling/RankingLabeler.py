from abc import ABC, abstractmethod
from .label import DendrogramLabeler, labeling_on_type


class RankingLabeler(DendrogramLabeler):
    def __init__(self, graph, dendrogram, source=labeling_on_type.EDGES_AND_NODES, max_labels=3):
        super().__init__(graph, dendrogram, source, max_labels)
        self.ranks_dict = {}
        if(source == labeling_on_type.NODES):
            self.fill_ranking_dictionary_with_nodes()
        elif(source == labeling_on_type.EDGES):
            self.fill_ranking_dictionary_with_edges()
        else:
            self.fill_ranking_dictionary_with_nodes()
            self.fill_ranking_dictionary_with_edges()

    # returns an items list of top self.max_labels most important nodes
    def get_important_nodes_list(self, items_subset):
        k = min(self.max_labels, len(items_subset))
        items_subset_sorted = sorted(items_subset, key=lambda node_item : self.ranks_dict[node_item[0]], reverse=True)
        return items_subset_sorted[:k]

    # returns an items list of top self.max_labels most important edges
    def get_important_edges_list(self, items_subset):
        k = min(self.max_labels, len(items_subset))
        items_subset = [((item[0], item[1]), item[2]) for item in items_subset]
        items_subset_sorted = sorted(items_subset, key=lambda edge_item : self.ranks_dict[edge_item[0]], reverse=True)
        return items_subset_sorted[:k]


    # selecting most importand nodes and edges according to source, using self.ranks_dict
    def select_important_nodes_and_edges(self, super_node):
        sub_graph = super_node.projected_graph.dgraph
        if self.source == labeling_on_type.NODES:
            chosen_nodes = self.get_important_nodes_list(sub_graph.nodes(data=True))
            return chosen_nodes
        elif self.source == labeling_on_type.EDGES:
            chosen_edges = self.get_important_edges_list(sub_graph.edges(data=True))
            return chosen_edges
        else:
            chosen_items = self.get_important_nodes_list(sub_graph.nodes(data=True))
            chosen_items.extend(self.get_important_edges_list(sub_graph.edges(data=True)))
            chosen_items = sorted(chosen_items, key = lambda x : self.ranks_dict[x[0]], reverse=True)
            k = min(self.max_labels, len(chosen_items))
            return chosen_items[: k]

    # Fill the ranking dictionary self.ranks_dict with nodes from the entire graph as keys and ranks as values.
    @abstractmethod
    def fill_ranking_dictionary_with_nodes(self):
        # Fill the ranking dictionary self.ranks_dict with nodes from the entire graph as keys and ranks as values.
        pass


    # Fill the ranking dictionary self.ranks_dict with edges from the entire graph as keys and ranks as values.
    # Default ranks of edges is calculated using nodes ranks if the dictionary is not empty:
    @abstractmethod
    def fill_ranking_dictionary_with_edges(self):
        if not self.ranks_dict:
            self.fill_ranking_dictionary_with_nodes()
        for edge_item in self.graph.dgraph.edges(data=True):
            edge = (edge_item[0], edge_item[1])
            out_node = edge[0]
            in_node = edge[1]

            out_node_rank = self.ranks_dict[out_node] / len(self.graph.dgraph.out_edges(out_node))
            in_node_rank = self.ranks_dict[in_node] / len(self.graph.dgraph.in_edges(in_node))
            self.ranks_dict[(edge[0], edge[1])] = (in_node_rank + out_node_rank) / 2.0

            # out_node_rank = self.ranks_dict[out_node]
            # in_node_rank = self.ranks_dict[edge[1]]
            # self.ranks_dict[(edge[0], edge[1])] = (in_node_rank + out_node_rank) / (2 * len(self.graph.dgraph.out_edges(out_node)))