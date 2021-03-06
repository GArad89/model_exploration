from .label import DendrogramLabeler, labeling_on_type
import itertools


class SimpleLabeler(DendrogramLabeler):

    def __init__(self, graph, dendrogram, source, max_labels=3, unify_prefix=False):
        super().__init__(graph, dendrogram, source, max_labels, unify_prefix)

    def is_ordered_labeler(self):
        return False

    def select_important_nodes_and_edges(self, super_node):
        sub_dgraph = super_node.projected_graph.dgraph
        return {
            labeling_on_type.EDGES: itertools.chain(sub_dgraph.edges.items()),
            labeling_on_type.NODES: itertools.chain(sub_dgraph.nodes.items()),
            labeling_on_type.EDGES_AND_NODES: itertools.chain(sub_dgraph.edges.items(), sub_dgraph.nodes.items())
        }.get(self.source, [])
