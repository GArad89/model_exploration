from abc import ABC, abstractmethod
import itertools
from enum import Enum
import networkx as nx

class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3

class GraphLabeler(ABC):

    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source
        self.ordered_nodes = self.order_nodes(self.graph.dgraph)

    def order_nodes(self, dgraph):
        graph = dgraph.copy()
        init_nodes = self.find_init_nodes(graph)
        for init in init_nodes:
            cycle = self._find_cycle(graph, init)
            while cycle:
                cycle_edge = cycle[-1]
                graph.remove_edge(cycle_edge[0],cycle_edge[1])
                cycle = self._find_cycle(graph, init)
        return [n for n in nx.bfs_tree(graph, init_nodes[0])]
        # ordered_edges = nx.bfs_edges(graph, init_nodes[0])

    def _get_first_appreance_in_list(self, labels):
        seen_labels = set()
        unique_labels = []
        for l in labels:
            if l not in seen_labels:
                seen_labels.add(l)
                unique_labels.append(l)
        return unique_labels

    def get_labels(self,subgraph):
         '''
            subgraph = node.projected_graph.dgraph
            get all inner labels (nodes and edges)
            generates an order list of labels,
            ordering is by BFS traversal order over the graph
         '''
         labels = [(v, attrs.get('label','')) for v, attrs in self.get_list_of_lables(subgraph)]
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

    def get_list_of_lables(self,subgraph):
        return {
            labeling_on_type.EDGES: itertools.chain(subgraph.edges.items()),
            labeling_on_type.NODES: itertools.chain(subgraph.nodes.items()),
            labeling_on_type.EDGES_AND_NODES: itertools.chain(subgraph.edges.items(), subgraph.nodes.items())
        }.get(self.source, [])

    def shorten_label(self, lables_list, max_lables=3):
        lables_list = list(lables_list)
        l = len(lables_list)
        if l > max_lables:
            newlist = [lables_list[0]]
            print(newlist)
            for i in range(1, max_lables - 1):
                newlist += [lables_list[(l // (max_lables - 1)) * i]]
            newlist += [lables_list[-1]]
            return "\n".join(newlist)
        else:
            return "\n".join(lables_list)

    def find_init_nodes(self, graph):

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

    @abstractmethod
    def label(self):
        pass



