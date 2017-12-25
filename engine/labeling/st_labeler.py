from ..baisc_entities.graph import *
from .label import GraphLabeler

class STLabeling(SuperstateGraphLabeler):
    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)

    def label(self):
        for node in self.dendrogram.nodes():
            node.label = get_label_for_subset(node.subset)

    def get_label_for_subset(self,subset):
        pass
