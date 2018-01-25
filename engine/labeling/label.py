from abc import ABC, abstractmethod
from enum import Enum
import networkx as nx
import os

class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3

class DendrogramLabeler(ABC):

    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES, max_labels = 3):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source
        self.max_labels = max_labels # max labels for each superstate
        self.ordered_nodes = self._order_nodes(self.graph.dgraph)

    #return bfs ordered list of nodes of dgraph
    def _order_nodes(self, dgraph):
        graph = dgraph.copy()
        init_nodes = self._find_init_nodes(graph)
        for init in init_nodes:
            cycle = self._find_cycle(graph, init)
            while cycle:
                cycle_edge = cycle[-1]
                graph.remove_edge(cycle_edge[0],cycle_edge[1])
                cycle = self._find_cycle(graph, init)
        return [n for n in nx.bfs_tree(graph, init_nodes[0])]
        # ordered_edges = nx.bfs_edges(graph, init_nodes[0])

    #returns a list of unique labels of list of labels
    def _get_first_appreance_in_list(self, labels):
        seen_labels = set()
        unique_labels = []
        for l in labels:
            if l not in seen_labels:
                seen_labels.add(l)
                unique_labels.append(l)
        return unique_labels

    def get_labels(self, super_node):
         '''
            subgraph = node.projected_graph.dgraph
            get all inner labels (nodes and edges)
            generates an order list of labels,
            ordering is by BFS traversal order over the graph
         '''
         labels = [(v, attrs.get('label','')) for v, attrs in self.select_important_nodes_and_edges(super_node)]
         # filter out empty ones
         labels = list(filter(lambda x: x[1], labels))
         # sort labels according to bfs order
         labels = sorted(labels,
                key=lambda x: self.ordered_nodes.index(x[0]) if len(x[0]) == 1 else self.ordered_nodes.index(x[0][0]))
         # only keep labels
         labels = [x[1] for x in labels]
         # uniqify labels
         labels = self._get_first_appreance_in_list(labels)
         return labels

    #returns a shorten version of labels_list with maximum of self.max_labels labels
    def shorten_label(self, lables_list):
        lables_list = list(lables_list)
        l = len(lables_list)
        if l > self.max_labels:
            newlist = [lables_list[0]]
            for i in range(1, self.max_labels - 1):
                newlist += [lables_list[(l // (self.max_labels - 1)) * i]]
            newlist += [lables_list[-1]]
            return ",\n".join(newlist)
        else:
            return ",\n".join(lables_list)

    def _find_init_nodes(self, graph):

        init_nodes = []
        for n in graph.nodes():
            if not graph.in_edges(n):
                init_nodes.append(n)
        return init_nodes

    def _find_cycle(self, graph, init):
        cycle = None
        try:
            cycle = nx.find_cycle(graph, init)
        except:
            pass
        return cycle

    def label(self):
        unnamed_cluster = 1
        # label the dendrogram's nodes
        for super_node in self.dendrogram.nodes()[1:]:
            labels = self.get_labels(super_node)
            # shortest common prefix
            prefix = os.path.commonprefix(list(labels))
            if not prefix or len(list(labels)) <= 1:
                # NOTE ESCAPED \n for graphviz happiness
                # node.label = super().shorten_label("\n".join(labels))
                super_node.label = self.shorten_label(labels)
            else:
                #TODO: deal with empty suffix and repeated labels
                adj_labels = [ l[len(prefix):] for l in labels]
                super_node.label = prefix + ': (' + self.shorten_label(adj_labels) + ')'
                # node.label = super().shorten_label("{prefix}{{\n{suffixes}}}".format(
                #     prefix=prefix,
                #     suffixes=",\n".join(l[len(prefix):] for l in labels)
                #     ))

            if not super_node.label:
                #TODO:roee(hack)
                super_node.label = "Unnamed {}".format(unnamed_cluster)
                unnamed_cluster += 1

    @abstractmethod
    def select_important_nodes_and_edges(self, super_node):
        pass


