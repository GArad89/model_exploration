from abc import ABC, abstractmethod
from enum import Enum
import networkx as nx
import os

class labeling_on_type(Enum):
    EDGES = 1
    NODES = 2
    EDGES_AND_NODES = 3

class DendrogramLabeler(ABC):

    def __init__(self, graph, dendrogram, source=labeling_on_type.EDGES_AND_NODES, max_labels=3, unify_prefix=False):
        self.graph = graph
        self.dendrogram = dendrogram
        self.source = source
        self.max_labels = max_labels # max labels for each superstate
        self.ordered_nodes = self._order_nodes(self.graph.dgraph)
        self.unify_prefix = unify_prefix

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
        node2rank = {}
        for init in init_nodes:
            sorted_nodes_from_init = [n for n in nx.bfs_tree(graph, init)]
            for current_ind, n in enumerate(sorted_nodes_from_init):
                ind = min(node2rank.get(n, current_ind), current_ind)
                node2rank[n] = ind
        sorted_nodes = sorted(node2rank, key=node2rank.get)
        return sorted_nodes
        # ordered_edges = nx.bfs_edges(graph, init_nodes[0])

    @abstractmethod
    def is_ordered_labeler(self):
        pass

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
         if not self.is_ordered_labeler():
             labels = sorted(labels,
                    key=lambda x: self.ordered_nodes.index(x[0]) if len(x[0]) == 1 else self.ordered_nodes.index(x[0][0]))
         # only keep labels
         labels = [x[1] for x in labels]
         # uniqify labels
         if not self.is_ordered_labeler(): #TODO change is_unique_labeler
            labels = list(set(labels))
         return labels

    #returns a shorten version of labels_list with maximum of self.max_labels labels
    def _shorten_label(self, lables_list):
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


    ## since edges that connect the same source and target are unified by
    ## ";\n" in when the model is read, we need to split them before making the labeling!
    def _split_multiple_label_labels(self, labels):
        sub_labels = [x.split(";\n") for x in labels]
        labels = []
        for x in sub_labels:
            labels.extend(x)
        return list(labels)

    def _unify_labels_with_common_prefix(self, labels):

        if len(list(labels)) <= 1:
            return self._shorten_label(labels)

        labels = self._shorten_label(labels).split(",\n")
        # shortest common prefix
        import re

        prefix_map = {}
        for l in labels:
            words = re.split("\W+", l.replace("_", " "))
            pref_labels = prefix_map.get(words[0],[])
            pref_labels.append(l)
            prefix_map[words[0]] = pref_labels

        label = ""
        for pref in prefix_map:
            pref_labels = prefix_map[pref]
            if len(pref_labels) == 1:
                label += pref_labels[0] + "\n"
                continue
            prefix = os.path.commonprefix(pref_labels)

            adj_labels = set([l[len(prefix):] for l in pref_labels])
            label += prefix + ': (' + ";".join(list(filter(lambda x: x, adj_labels))) + ')\n'
        return label

    def label(self):
        # label the dendrogram's nodes
        for super_node in self.dendrogram.nodes()[1:]:

            labels = self.get_labels(super_node)
            print(len(super_node.vertices()))
            labels = self._split_multiple_label_labels(labels)
            if self.unify_prefix:
                super_node.label = self._unify_labels_with_common_prefix(labels)
            else:
                super_node.label = self._shorten_label(labels)

            if not super_node.label: #TODO:roee(hack)
                cluster_nodes = super_node.projected_graph.dgraph.nodes(data=True)
                init_nodes = self.graph.get_initial_nodes()
                sink_nodes = self.graph.get_sink_nodes()
                has_init_nodes = len(list(filter(lambda x: x in init_nodes, cluster_nodes))) > 0
                has_sink_nodes = len(list(filter(lambda x: x in sink_nodes, cluster_nodes))) > 0
                super_node.label = ""
                if len(cluster_nodes) == 1:
                    super_node.label = "Concrete state:"
                if has_init_nodes:
                    super_node.label += "Init"
                elif has_sink_nodes:
                    if has_init_nodes:
                        super_node.label += "Init & Terminal"
                    else:
                        super_node.label += "Terminal"
                # else:
                    # super_node.label += "Unlabeled"

    @abstractmethod
    def select_important_nodes_and_edges(self, super_node):
        pass


