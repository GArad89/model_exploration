from .label import DendrogramLabeler, labeling_on_type
import networkx as nx

class STLabeling(DendrogramLabeler):
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)

    def select_important_nodes_and_edges(self, super_node):
        subgraph = super_node.projected_graph.dgraph
        spanning_tree=nx.minimum_spanning_tree(subgraph)
        if (self.source == labeling_on_type.NODES):
            return spanning_tree.nodes(data=True)
        else:
            edges = spanning_tree.edges(data=True)
            if(self.source == labeling_on_type.EDGES):
                return edges
            else:
                return spanning_tree.nodes(data=True) + edges