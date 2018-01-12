from .label import GraphLabeler
import networkx as nx
import random

class PathLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram, None)
        self.ranks = nx.pagerank(self.graph.dgraph)

    def get_strategic_nodes(self, super_node):
        """
        :return: two lists: first list is the starting nodes and the second one is the end nodes list
        """
        cluster_nodes = super_node.subset

        end_nodes = []
        for node in cluster_nodes:
            out_edges = self.graph.dgraph.out_edges(node)
            filtered = list(filter(lambda out_edge: out_edge[1] not in cluster_nodes , out_edges))
            if len(filtered) > 0:
                end_nodes.append(node)

        start_nodes = []
        for node in cluster_nodes:
            in_edges = self.graph.dgraph.in_edges(node)
            filtered = list(filter(lambda in_edge: in_edge[0] not in cluster_nodes , in_edges))
            if len(filtered) > 0:
                start_nodes.append(node)

        return start_nodes, end_nodes

    def traverse_cluster(self, start_nodes, end_nodes):
        path = []
        current_node = random.choice(start_nodes)
        path.append(current_node)
        while current_node not in end_nodes:
            out_edges = self.graph.dgraph.out_edges(current_node)
            neighbors = [edge[1] for edge in out_edges]
            current_node = random.choice(neighbors)
            path.append(current_node)

        return path

    def label(self):
        for super_node in self.dendrogram.nodes():
            start_nodes, end_nodes = self.get_strategic_nodes(super_node)
            print("start_nodes = ", start_nodes)
            print("end_nodes = ", end_nodes)

            if len(start_nodes) > 0 and len(end_nodes) > 0:
                print("path = ", self.traverse_cluster(start_nodes, end_nodes))