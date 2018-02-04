from abc import ABC, abstractmethod
import networkx as nx

class Cluster(ABC):

    @staticmethod
    def get_params():
        """
        Return json-schema and form describing the parameters this clustering algorithm accepts
        Json schema is standard, see documentation for jsonForm javascript library at for description of form
        Example at SpectralCluster
        """
        form = []
        schema = {}
        return schema, form

    @abstractmethod
    def cluster(self, dgraph):
        """
        graph => [[node a, node b, node c], [node d, node e, ...], ...]
        Accepts a dgraph, returns a list of lists of nodes, each sublist being a cluster
        ( nodes are node keys in the graph, e.g. list(dgraph.nodes())) )
        """
        raise NotImplementedError

    def unify_bi_dir_edges(self, directed_edge_dic):
        unified_keys_dic = {}
        for key in directed_edge_dic:
            nk = tuple(sorted(key))
            values = unified_keys_dic.get(nk, [])
            values.append(directed_edge_dic[key])
            unified_keys_dic[nk] = values
        return unified_keys_dic

    def to_undirected(self, graph):

        cop = graph.copy()
        cop = cop.to_undirected()

        labels_dic = nx.get_edge_attributes(graph, 'label')
        weights_dic = nx.get_edge_attributes(graph, 'weight')
        nlabels_dic = self.unify_bi_dir_edges(labels_dic)
        nweights_dic = self.unify_bi_dir_edges(weights_dic)
        nlabels_dic = dict([(k, "\n;".join(v))  for k, v in nlabels_dic.items()])
        nweights_dic = dict([(k, sum(v)) for k, v in nweights_dic.items()])
        nx.set_edge_attributes(cop, nlabels_dic, 'label')
        nx.set_edge_attributes(cop, nweights_dic, 'weight')
        return cop