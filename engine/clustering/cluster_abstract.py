from abc import ABC, abstractmethod


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

