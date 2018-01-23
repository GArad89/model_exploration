from .label import DendrogramLabeler, labeling_on_type
import networkx as nx
from .RankingLabeler import RankingLabeler


import logging

log = logging.getLogger(__name__)

class PageRankLabeler(RankingLabeler):
    
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)

    def fill_ranking_dictionary_with_nodes(self):
        self.ranks_dict = nx.pagerank_numpy(self.graph.dgraph)

    def fill_ranking_dictionary_with_edges(self):
        super().fill_ranking_dictionary_with_edges()
