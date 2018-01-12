from .label import GraphLabeler
import networkx as nx
import random

class PathLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram, None)
        self.ranks = nx.pagerank(self.graph.dgraph)


    def get_sink_nodes(self):
        sink_nodes = []
        for node in self.graph.dgraph.nodes():
            if len(self.graph.dgraph.out_edges(node)) == 0:
                sink_nodes.append(node)
        return sink_nodes

    def get_initial_nodes(self):
        inital_nodes = []
        for node in self.graph.dgraph.nodes():
            if len(self.graph.dgraph.in_edges(node)) == 0:
                inital_nodes.append(node)
        return inital_nodes

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

        # cluster contains the 'initial' node, choose it as a starting node
        if len(start_nodes) == 0:
            start_nodes = list(set(self.get_initial_nodes()) & set(cluster_nodes))

        # no out edges from this cluster to another - choose the sink nodes
        if len(end_nodes) == 0:
            end_nodes = list(set(self.get_sink_nodes()) & set(cluster_nodes))

        return start_nodes, end_nodes

    def rank_nodes(self, nodes):
        return sorted(nodes, key=lambda node: self.ranks[node])

    def traverse_cluster(self, start_nodes, end_nodes):
        path = []
        current_node = random.choice(start_nodes)
        path.append(current_node)
        while current_node not in end_nodes:
            out_edges = self.graph.dgraph.out_edges(current_node)
            neighbors = [edge[1] for edge in out_edges]

            if len(neighbors) == 0:
                return path # should not happen

            # next node is the one with the highest rank
            ranked_neighbors = self.rank_nodes(neighbors)
            current_node = ranked_neighbors.pop()

            # look for a neighbors that we haven't seen before to prevent getting into a cycle
            while (current_node in path) and len(ranked_neighbors) > 0:
                current_node = ranked_neighbors.pop()

            if current_node in path:
                return path # there's no such node

            path.append(current_node)

        return path

    def label(self):
        for super_node in self.dendrogram.nodes():
            start_nodes, end_nodes = self.get_strategic_nodes(super_node)
            return self.traverse_cluster(start_nodes, end_nodes)
