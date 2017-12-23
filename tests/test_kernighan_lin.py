import sys
sys.path.append('..')

from engine.clustering.minimum_cut import MinimumCut
from engine.clustering.KernighanLinCluster import KernighanLinCluster
from engine.baisc_entities.graph import DGraph
from main.partitionLoop import partition
from networkx.classes import graph
from stopping_criteria.stopCriteria import SizeCriteria
def test():
    den = None
    g = DGraph.read_dot("../engine/dot/cvs.net.mutated.dot")
    mc = MinimumCut()
    res = mc.cluster(g)

    partition(g, clustering_algo = KernighanLinCluster, stopCri = SizeCriteria(3))


test()
