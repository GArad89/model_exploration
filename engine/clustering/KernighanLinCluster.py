from .cluster_abstract import Cluster
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection


class KernighanLinCluster(Cluster):

    @staticmethod
    def get_params():
        form = []
        schema = {}
        return schema, form

    def cluster(self, dgraph, weight=None):
        udgraph = super().to_undirected(dgraph.dgraph)
        A, B = kernighan_lin_bisection(udgraph, weight=weight)
        return [A, B]



