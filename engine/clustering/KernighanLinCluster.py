from .cluster_abstract import Cluster
from ..baisc_entities.graph import DGraph
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

class KernighanLinCluster(Cluster):

    def cluster(self, dgraph, weight=None):
        udgraph = dgraph.dgraph.to_undirected()
        A, B = kernighan_lin_bisection(udgraph, weight=weight)
        return [A, B]



