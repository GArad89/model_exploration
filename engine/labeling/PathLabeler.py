from .label import DendrogramLabeler, labeling_on_type
import networkx as nx
import random


class PathLabeler(DendrogramLabeler):

    def __init__(self, graph, dendrogram, labeling_source):
        super().__init__(graph, dendrogram, labeling_source)
        self.ranks = nx.pagerank_numpy(self.graph.dgraph)

    def get_sink_nodes(self):
        sink_nodes = []
        for node_item in self.graph.dgraph.nodes(data=True):
            if len(self.graph.dgraph.out_edges(node_item[0])) == 0:
                sink_nodes.append(node_item)
        return sink_nodes

    def get_initial_nodes(self):
        inital_nodes = []
        for node_item in self.graph.dgraph.nodes(data=True):
            if len(self.graph.dgraph.in_edges(node_item[0])) == 0:
                inital_nodes.append(node_item)
        return inital_nodes

    def get_strategic_nodes(self, super_node):
        """
        :return: two lists: first list is the starting nodes and the second one is the end nodes list
        """
        cluster_nodes = super_node.projected_graph.dgraph.nodes(data=True)

        end_nodes = []
        for node_item in cluster_nodes:
            out_edges = self.graph.dgraph.out_edges(node_item[0])
            out_edges_filtered = list(filter(lambda out_edge: out_edge[1] not in cluster_nodes , out_edges))
            if len(out_edges_filtered) > 0:
                end_nodes.append(node_item)

        start_nodes = []
        for node_item in cluster_nodes:
            in_edges = self.graph.dgraph.in_edges(node_item[0])
            in_edges_filtered = list(filter(lambda in_edge: in_edge[0] not in cluster_nodes , in_edges))
            if len(in_edges_filtered) > 0:
                start_nodes.append(node_item)

        # cluster contains the 'initial' node, choose it as a starting node
        if len(start_nodes) == 0:
            start_nodes = [node_item1 for node_item1,node_item2 in zip(self.get_initial_nodes(),cluster_nodes) if node_item1[0] == node_item2[0]]

        # no out edges from this cluster to another - choose the sink nodes
        if len(end_nodes) == 0:
            end_nodes = [node_item1 for node_item1, node_item2 in zip(self.get_sink_nodes(), cluster_nodes) if node_item1[0] == node_item2[0]]

        return start_nodes, end_nodes

    def sort_nodes_by_ranks(self, node_items_list):
        return sorted(node_items_list, key=lambda node_item: self.ranks[node_item[0]])

    def traverse_cluster(self, start_nodes, end_nodes, super_node):
        path = []
        current_node = random.choice(start_nodes)
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
        start_nodes, end_nodes = self.get_strategic_nodes(super_node)
        path = self.traverse_cluster(start_nodes, end_nodes, super_node)
        if (self.source == labeling_on_type.NODES):
            return path
        else:
            edges_items_in_path = []

            for idx in range(len(path) - 1):
                edge = (path[idx][0], path[idx + 1][0])
                edge_item = (edge, super_node.projected_graph.dgraph.edges[edge])
                edges_items_in_path.append(edge_item)
            if(self.source == labeling_on_type.EDGES):
                return edges_items_in_path
            else:
                return path + edges_items_in_path