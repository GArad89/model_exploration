from .label import GraphLabeler
import networkx as nx


class PageRankLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)


    def label(self):

        ranks = nx.pagerank(self.graph.dgraph)

        for super_node in self.dendrogram.nodes():
            max_rank = -1
            max_ranked_node = None
            for node in super_node.subset:
                if ranks[node] > max_rank:
                    max_rank = ranks[node]
                    max_ranked_node = self.graph.node_attr(node, 'label')

            super_node.label = max_ranked_node



