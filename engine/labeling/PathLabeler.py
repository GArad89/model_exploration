from .label import DendrogramLabeler, labeling_on_type
import networkx as nx
import random
import operator

class PathLabeler(DendrogramLabeler):

    def __init__(self, graph, dendrogram, labeling_source, max_labels=3, unify_prefix=False):
        super().__init__(graph, dendrogram, labeling_source, max_labels, unify_prefix)
        self.ranks = nx.pagerank_numpy(self.graph.dgraph)

    def is_ordered_labeler(self):
        return True

    def _is_init_or_term(self, edges, cluster_nodes, index):

        edges_filtered = list(filter(lambda edge: operator.itemgetter(index)(edge) not in cluster_nodes, edges))
        # no_self_loops = list(filter(lambda out_edge: out_edge[0] != out_edge[1], out_edges_filtered))
        return len(edges_filtered) > 0 or len(edges) == 0

    def get_init_and_terminal_nodes(self, super_node):
        """
        :return: two lists: first list is the starting nodes (in the project model)
        and the second one is the end nodes list (in the project model)
        """
        cluster_nodes = super_node.projected_graph.dgraph.nodes(data=True)
        init_nodes, end_nodes = [], []
        for node_item in cluster_nodes:
            out_edges = self.graph.dgraph.out_edges(node_item[0])
            if self._is_init_or_term(out_edges, cluster_nodes, 1):
                end_nodes.append(node_item)
            in_edges = self.graph.dgraph.in_edges(node_item[0])
            if self._is_init_or_term(in_edges, cluster_nodes, 0):
                init_nodes.append(node_item)
        return init_nodes, end_nodes

    def sort_nodes_by_ranks(self, node_items_list):
        return sorted(node_items_list, key=lambda node_item: self.ranks[node_item[0]])

    def traverse_cluster(self, start_nodes, end_nodes, super_node):
        path = []
        current_node = random.choice(start_nodes)
        if current_node in end_nodes:  #Try to avoid single node paths, TODO: improve
            end_nodes.remove(current_node)
        path.append(current_node)
        while current_node not in end_nodes:
            out_edges = self.graph.dgraph.out_edges(current_node[0])
            neighbors = [edge[1] for edge in out_edges]
            neighbors = [neighbor_item for neighbor_item in super_node.projected_graph.dgraph.nodes(data=True) if neighbor_item[0] in neighbors]
            if len(neighbors) == 0:
                return path # should not happen

            # next node is the one with the highest rank
            sorted_neighbors_by_rank = self.sort_nodes_by_ranks(neighbors)
            current_node = sorted_neighbors_by_rank.pop()

            # look for a neighbors that we haven't seen before to prevent getting into a cycle
            while (current_node in path) and len(sorted_neighbors_by_rank) > 0:
                current_node = sorted_neighbors_by_rank.pop()

            if current_node in path:
                return path # there's no such node

            path.append(current_node)

        return path

    def select_important_nodes_and_edges(self, super_node):
        start_nodes, end_nodes = self.get_init_and_terminal_nodes(super_node)
        path = self.traverse_cluster(start_nodes, end_nodes, super_node)
        if self.source == labeling_on_type.NODES:
            return path
        else:
            edges_items_in_path = []
            for idx in range(len(path) - 1):
                edge = (path[idx][0], path[idx + 1][0])
                edge_item = (edge, super_node.projected_graph.dgraph.edges[edge])
                edges_items_in_path.append(edge_item)
            if self.source == labeling_on_type.EDGES:
                return edges_items_in_path
            else:
                return path + edges_items_in_path